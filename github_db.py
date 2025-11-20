import base64
import json
import requests
import streamlit as st

# Correct GitHub repo
GITHUB_REPO = "AmmarJamshed/careerforge"
GITHUB_DATA_FOLDER = "data"

# Load GitHub Token
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

def github_get(filename):
    """
    Reads a JSON file from GitHub inside /data folder.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DATA_FOLDER}/{filename}"

    response = requests.get(
        url,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )

    data = response.json()

    # If GitHub returns error (e.g. Not Found), handle it gracefully
    if "content" not in data:
        raise ValueError(
            f"GitHub GET failed for {filename}. Response was: {data}"
        )

    content = base64.b64decode(data["content"]).decode()
    return json.loads(content), data["sha"]


def github_update(filename, new_data, sha):
    """
    Writes JSON back to GitHub inside /data folder.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_DATA_FOLDER}/{filename}"

    encoded = base64.b64encode(
        json.dumps(new_data, indent=4).encode()
    ).decode()

    response = requests.put(
        url,
        json={
            "message": f"Updated {filename}",
            "content": encoded,
            "sha": sha
        },
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )

    if response.status_code not in [200, 201]:
        raise ValueError(
            f"GitHub UPDATE failed for {filename}. Response was: {response.json()}"
        )

    return True
