from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def get_context_from_vectorstore(query):
    db = Chroma(persist_directory="data/chroma", embedding_function=OpenAIEmbeddings())
    docs = db.similarity_search(query)
    return docs