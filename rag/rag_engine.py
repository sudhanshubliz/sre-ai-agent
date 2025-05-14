from llama_index import VectorStoreIndex, ServiceContext
from llama_index.storage.storage_context import StorageContext

def query_logs(query: str) -> str:
    """
    Query the RAG index and get an answer from the logs.
    :param query: The user’s question to the logs.
    :return: Answer string from the RAG query.
    """
    # Load the vector index
    storage_context = StorageContext.from_defaults(persist_dir="rag/index")
    index = VectorStoreIndex.load_from_storage(storage_context)

    # Build a query engine
    query_engine = index.as_query_engine()

    # Get the response from the query engine
    response = query_engine.query(query)

    return response
