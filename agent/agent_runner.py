from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from agent.retrieve_context import get_context_from_vectorstore

def run_risk_agent(pr_summary):
    llm = ChatOpenAI(temperature=0)
    docs = get_context_from_vectorstore(pr_summary)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=docs)
    result = chain.run(pr_summary)
    return result
