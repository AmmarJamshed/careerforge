import base64
import json
import requests
import streamlit as st

GITHUB_REPO = "YOUR_USERNAME/careerforge-data"  # Change this
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

def github_get(path):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"

    r = requests.get(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}"
    })

    data = r.json()
    content = base64.b64decode(data["content"]).decode()
    return json.loads(content), data["sha"]


def github_update(path, new_data, sha):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"

    encoded = base64.b64encode(
        json.dumps(new_data, indent=4).encode()
    ).decode()

    r = requests.put(url, json={
        "message": f"update {path}",
        "content": encoded,
        "sha": sha
    }, headers={
        "Authorization": f"token {GITHUB_TOKEN}"
    })

    return r.status_code in [200, 201]
