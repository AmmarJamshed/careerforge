import streamlit as st
from groq import Groq

# Load Groq key from Streamlit Secrets
GROQ_KEY = st.secrets["GROQ_API_KEY"]

def ai_chatbot():
    st.title("🤖 CareerForge AI Chatbot (Groq Powered)")

    st.write("Ask anything about careers, skills, universities, scholarships, or admissions.")

    user_input = st.text_area("Your question:")

    if st.button("Ask AI"):
        if not user_input.strip():
            st.warning("Please enter a question.")
            return

        try:
            client = Groq(api_key=GROQ_KEY)

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are CareerForge AI — an expert advisor for careers, universities, scholarships, and skill development."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.4,
                max_tokens=600
            )

            ai_reply = response.choices[0].message.content
            st.success("AI Response:")
            st.write(ai_reply)

        except Exception as e:
            st.error(f"Groq API error: {e}")
