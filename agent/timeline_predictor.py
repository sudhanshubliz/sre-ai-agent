from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def predict_timeline(pr_summary, context):
    llm = ChatOpenAI()
    prompt = PromptTemplate.from_template("""
    Based on this change request and past incidents, estimate:
    - Risk Window (when issues might appear)
    - Stability Time (how long to monitor)
    - Suggested Rollout Strategy

    PR Summary: {summary}
    Context: {context}
    """)

    return llm.predict(prompt.format(summary=pr_summary, context=context))
