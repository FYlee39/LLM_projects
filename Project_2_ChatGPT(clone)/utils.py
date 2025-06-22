from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

def generate_chat_response(prompt, memory, api_key):

    model = ChatOpenAI(openai_api_key=api_key)
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})

    return response["response"]

if __name__ == '__main__':

    memory = ConversationBufferMemory(return_messages=True)

    print(generate_chat_response(prompt="Who is Newton?", memory=memory, api_key=os.getenv("OPENAI_API_KEY")))
    print(generate_chat_response(prompt="What's my last question?", memory=memory, api_key=os.getenv("OPENAI_API_KEY")))

