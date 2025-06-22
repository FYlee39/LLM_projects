import streamlit as st
from utils import generate_script

if __name__ == '__main__':
    # title
    st.title("Video Script Generator")

    # sidebar
    with st.sidebar:
        # text
        openai_api_key = st.text_input("Please enter your OpenAI API key here:", type="password")

        # using markdown to create a hyperlink
        st.markdown("[Obtain OpenAI API key here](https://platform.openai.com/account/api-keys)")

    subject = st.text_input("Please input the subject of the video")

    video_length = st.number_input("Please input the number of minutes of the video",
                                   min_value=0.1, step=0.1)

    creativity = st.slider("Please input the creativity of the script (smaller value means more rigorous, vise versa)",
                           min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    submit = st.button("Generate Script")

    if submit and not openai_api_key:
        st.info("Please enter your OpenAI API key")
        st.stop()

    if submit and not subject:
        st.info("Please enter your subject")
        st.stop()

    if submit and not video_length >= 0.1:
        st.info("The length of the video must be greater than 0.1.")
        st.stop()

    if submit:
        # add loading effect
        with st.spinner("Generating script..."):
            search_result, title, script = generate_script(subject, video_length,
                                                           creativity, openai_api_key)

        st.success("Script generated")
        st.subheader("Title:")
        st.write(title)
        st.subheader("Script:")
        st.write(script)

        # Collapse and expand components
        with st.expander("Search result"):
            st.info(search_result)
