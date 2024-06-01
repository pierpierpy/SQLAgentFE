import streamlit as st
import chat
import login
import styles
import random
from dotenv import load_dotenv

load_dotenv()


def main():
    st.title("SQL agent")
    st.session_state.conversations = []
    try:
        if "token" in st.session_state and st.session_state.token:
            st.query_params["page"] = "chat"
            display_conversations_sidebar()
            show_chat()
        else:
            login_form()
    except Exception as e:
        st.error(f"An error occurred: {e}")


def login_form():
    st.title("Login")
    st.query_params["user"] = ""
    st.query_params["conversation_id"] = ""
    st.query_params["page"] = "login"
    try:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            token = login.authenticate(username, password)
            if token:
                st.session_state.messages = []
                st.query_params["user"] = username
                if (
                    "conversation_id" in st.query_params
                    and st.query_params["conversation_id"]
                ):
                    st.session_state.token = token
                    messages = st.session_state.messages = (
                        chat.get_conversation_by_user_id(
                            conversation_id=st.query_params["conversation_id"],
                            user_id=st.query_params["user"],
                            token=token,
                        )
                    )
                    if messages:
                        st.success("Login successful!")
                        st.rerun()
                st.session_state.token = token
                st.query_params["conversation_id"] = chat.get_conversation(
                    token, user_id=username
                )
                st.query_params["user"] = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Authentication failed. Please check your credentials.")
    except Exception as e:
        st.error(f"Login error: {e}")


def display_conversations_sidebar():
    st.session_state.conversations = chat.get_conversations_by_user_id(
        token=st.session_state.token, user_id=st.query_params["user"]
    )
    with st.sidebar:
        if st.button("🗑️", key="sidebar_trash"):
            try:

                chat.clear_history(
                    st.query_params["conversation_id"],
                    st.query_params["user"],
                    st.session_state.token,
                )
                if len(st.session_state.conversations) == 1:
                    st.query_params["conversation_id"] = chat.get_conversation(
                        st.session_state.token, user_id=st.query_params["user"]
                    )
                else:
                    st.session_state.conversations = chat.get_conversations_by_user_id(
                        token=st.session_state.token, user_id=st.query_params["user"]
                    )
                    st.query_params["conversation_id"] = st.session_state.conversations[
                        0
                    ]
                st.session_state.messages = []
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing history: {e}")

        if st.button("➕", key="sidebar_add"):
            try:

                st.query_params["conversation_id"] = chat.get_conversation(
                    st.session_state.token, user_id=st.query_params["user"]
                )
                st.session_state.conversations = chat.get_conversations_by_user_id(
                    token=st.session_state.token, user_id=st.query_params["user"]
                )
                st.session_state.messages = []
                st.rerun()
            except Exception as e:
                st.error(f"Error starting a new conversation: {e}")
        st.header("Conversations")
        for conversation in st.session_state.conversations:
            if st.button(conversation, key=conversation):
                st.query_params["conversation_id"] = conversation
                st.session_state.messages = chat.get_conversation_by_user_id(
                    conversation_id=st.query_params["conversation_id"],
                    user_id=st.query_params["user"],
                    token=st.session_state.token,
                )
                st.rerun()


def show_chat():
    st.markdown(styles.chat_styles, unsafe_allow_html=True)

    try:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.markdown(styles.clear_button_style, unsafe_allow_html=True)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("ask me a question about the database"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                spinner_message = [
                    "looking for an answer!",
                    "working for your answer",
                ]
                with st.spinner(random.choice(spinner_message)):
                    answer = chat.chat(
                        st.session_state.messages,
                        st.query_params["conversation_id"],
                        st.session_state.token,
                    )
                    if answer:
                        response = st.write_stream(answer)

                    else:
                        if "token" in st.session_state:
                            del st.session_state["token"]
                        st.rerun()
                st.session_state.conversations = chat.get_conversations_by_user_id(
                    token=st.session_state.token, user_id=st.query_params["user"]
                )
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Chat error: {e}")


if __name__ == "__main__":
    main()
