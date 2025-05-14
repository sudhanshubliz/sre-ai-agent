from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def score_risk(pr_summary, context):
    llm = ChatOpenAI(temperature=0)
    prompt = PromptTemplate.from_template("""
    Given the following PR summary and context, assign a RISK SCORE (0 to 10) and explain your reasoning.

    PR Summary: {summary}
    Context: {context}

    Respond in this format:
    Risk Score: <number>
    Reason: <explanation>
    """)

    full_prompt = prompt.format(summary=pr_summary, context=context)
    response = llm.predict(full_prompt)
    return response
