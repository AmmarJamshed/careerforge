import streamlit as st

def ai_chatbot():
    st.title("🤖 AI Chatbot")

    query = st.text_area("Ask anything about admissions, scholarships or careers:")

    if st.button("Ask"):
        st.write("AI Response: (placeholder)")  # Replace with Groq or OpenAI API
