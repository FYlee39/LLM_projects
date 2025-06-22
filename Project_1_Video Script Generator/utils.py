from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

# get api key from the environment
import os

def generate_script(subject, video_length,
                    creativity, api_Key):
    """
    Generating a script for a given subject.
    :param subject: subject of the video
    :param video_length: length of the video
    :param creativity: creativity of the AI
    :param api_Key:
    :return:
    """

    # template for Title
    title_template = ChatPromptTemplate.from_messages(
        [("human", "Please come up with a attractive title for the subject of {subject}."),]
    )

    # template for script
    script_template = ChatPromptTemplate.from_messages(
        [("human",
            """You are a blogger of a short video channel. Based on the following title and related information, 
            write a video script for the short video channel. Video title: {title}, video duration: {duration} minutes,
             the length of the generated script should follow the video duration requirements as much as possible.
            It is required to catch the ball at the beginning, provide dry goods in the middle, and have a surprise at the end.
             The script format should also be separated according to [beginning, middle, end].
            The overall content should be expressed in a relaxed and interesting way to attract young people.
             The script content can be combined with the following Wikipedia search information, but it is only for reference.
              Only relevant information can be combined, and irrelevant information can be ignored:
               ```{wikipedia_search}```""")]
    )

    # Define model
    model = ChatOpenAI(openai_api_key=api_Key, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    # search in wikipedia
    search = WikipediaAPIWrapper()
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return search_result, title, script



if __name__ == '__main__':
    pass
    # print(generate_script("sora model", 1, 0.7, os.getenv("OPENAI_API_KEY")))
