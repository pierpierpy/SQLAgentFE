import requests
import json
import os
from dotenv import load_dotenv
import time
import ast

load_dotenv()

base = os.environ.get("base")


def chat(query: str, conversation_id: str, token: str):
    url = f"{base}/chat/qa/{conversation_id}"

    payload = json.dumps({"query": query[-1]["content"]})
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    for word in response.iter_lines(decode_unicode=True):
        if "meta" in ast.literal_eval(word):
            # yield ast.literal_eval(word)["meta"]
            continue
        else:
            if "ans" in ast.literal_eval(word):
                yield ast.literal_eval(word)["ans"]
            else:
                yield False
        time.sleep(float(os.environ.get("STREAMING_BUFFER")))


def clear_history(conversation_id: str, user_id: str, token: str):
    url = f"{base}/memory/removechatmemory/{conversation_id}?user_id={user_id}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("DELETE", url, headers=headers)
    return response


def get_conversation(token: str, user_id: str):
    url = f"{base}/chat/conversation?user_id={user_id}"

    payload = {}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["conversation_id"]


def get_conversation_by_user_id(conversation_id: str, user_id: str, token: str) -> list:
    url = f"{base}/memory/userchat/{conversation_id}?user_id={user_id}"

    payload = {}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    output = response.json()["conversation"]
    return map_data(output)


def map_data(data):
    mapped_data = []
    for item in data:
        role = "assistant" if item["type"] == "ai" else "user"
        content = item["data"]["content"]
        mapped_data.append({"role": role, "content": content})
    return mapped_data


def get_conversations_by_user_id(user_id: str, token: str) -> list:
    url = f"{base}/memory/userconversations/?user_id={user_id}"

    payload = {}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["conversation_ids"]
