import streamlit as st

from utils import qa_agent
from langchain.memory import ConversationBufferMemory


if __name__ == '__main__':
    # title
    st.title("AI PDF agent")

    # side bar
    with st.sidebar:
        # text
        openai_api_key = st.text_input("Please enter your OpenAI API key here:", type="password")

        # using markdown to create a hyperlink
        st.markdown("[Obtain OpenAI API key here](https://platform.openai.com/account/api-keys)")

    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True,
                                                              memory_key="chat_history",
                                                              output_key="answer")

    uploaded_file = st.file_uploader("Upload a PDF: ", type="pdf")

    question = st.text_input("Question about the PDF:", disabled=not uploaded_file)

    if uploaded_file and question and not openai_api_key:
        st.info("Please enter your OpenAI API key")
        st.stop()

    if uploaded_file and question and openai_api_key:
        with st.spinner("AI is thinking, please wait..."):
            response = qa_agent(openai_api_key,
                                st.session_state["memory"],
                                uploaded_file, question)
        st.write("### Answer")
        st.write(response["answer"])
        st.session_state["chat_history"] = response["chat_history"]


    if "chat_history" in st.session_state:
        with st.expander("Chat history"):
            for i in range(0, len(st.session_state["chat_history"]), 2):
                human_message = st.session_state["chat_history"][i]
                ai_message = st.session_state["chat_history"][i + 1]
                st.write(human_message.content)
                st.write(ai_message.content)
                if i < len(st.session_state["chat_history"]) - 2:
                    st.divider()