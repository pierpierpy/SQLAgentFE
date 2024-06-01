import requests
import json
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

base = os.environ.get("base")


def authenticate(username, password):
    url = f"{base}/user/login"
    payload = json.dumps({"email": username, "password": password})
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None
