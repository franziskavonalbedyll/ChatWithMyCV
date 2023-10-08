"""
A Streamlit application to interactively chat about the content of a CV.

Usage:
- Run the Streamlit application using the command: `streamlit run chat.py`

Example:
    >>> CV_EXPLANATIONS_PATH = "../data/cv_explanations.txt"
    >>> DB_DIR = "../embeddings_database"
    >>> embeddings = create_embeddings(CV_EXPLANATIONS_PATH, DB_DIR)
"""

import streamlit as st
from ask import ask_question
from build_index import create_embeddings
from download_data import download

DB_DIR = "../embeddings_database"

cv_explanation_data = download()
embeddings = create_embeddings(cv_explanation_data, DB_DIR)

st.set_page_config(
    page_title=f"{st.secrets['FULL_NAME']} - Chat with my CV",
    page_icon=":speech_balloon:",
)
st.subheader(f"{st.secrets['FULL_NAME']} - Chat with my CV")
prompt_box = st.empty()
st.write("")
answer_box = st.empty()

# Store LLM generated responsens
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I'm here to answer "
            f"your questions regarding {st.secrets['FIRST_NAME']}'s CV. "
            "Ask me anything!",
        }
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("generating..."):
            answer = ask_question(prompt, embeddings)
            st.write(answer)
    message = {"role": "assistant", "content": answer}
    st.session_state.messages.append(message)
