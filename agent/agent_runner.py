from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def run_risk_agent(pr_summary):
    # Initialize the ChatOpenAI model with temperature and API key
    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    # Your logic here
    result = llm.predict(pr_summary)
    print(os.getenv("OPENAI_API_KEY"))
    # Return the result
    return result