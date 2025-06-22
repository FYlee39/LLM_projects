import streamlit as st
from utils import generate_chat_response
from langchain.memory import ConversationBufferMemory

if __name__ == '__main__':
    # title
    st.title("ChatGPT(clone)")

    # sidebar
    with st.sidebar:
        # text
        openai_api_key = st.text_input("Please enter your OpenAI API key here:", type="password")

        # using markdown to create a hyperlink
        st.markdown("[Obtain OpenAI API key here](https://platform.openai.com/account/api-keys)")

    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["message"] = [{"role": "ai",
                                        "content": "Hello, I am your AI assistant, how can I help you today?"}]

    for message in st.session_state["message"]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input()

    if prompt:
        if not openai_api_key:
            st.info("Please enter your OpenAI API key")
            st.stop()

        st.session_state["message"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)

        with st.spinner("Please wait..."):
            response = generate_chat_response(prompt, st.session_state["memory"],
                                          openai_api_key)

        msg = {"role": "ai", "content": response}
        st.session_state["message"].append(msg)
        st.chat_message("ai").write(response)