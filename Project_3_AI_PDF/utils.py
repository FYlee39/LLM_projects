from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import os

def qa_agent(openai_api_key, memory, uploaded_file, question):
    model = ChatOpenAI(openai_api_key=openai_api_key)

    file_contents = uploaded_file.read()
    temp_file = "temp.pdf"
    with open(temp_file, "wb") as f:
        f.write(file_contents)

    loader = PyPDFLoader(temp_file)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # max length for each chunk
        chunk_overlap=50,  # the length of overlap of different parts
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]  # order matters
    )

    texts = text_splitter.split_documents(docs)

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openai_api_key)  # need key

    db = FAISS.from_documents(texts, embeddings_model)

    retriever = db.as_retriever()

    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )

    response = qa.invoke({"chat_history": memory, "question": question})
    return response