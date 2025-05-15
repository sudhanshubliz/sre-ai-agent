from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from groq import Groq
import os

def run_risk_agent(pr_summary):
    # Load environment variables from the .env file
    load_dotenv()
    # Ensure the API key is correctly loaded

   # api_key = os.getenv("OPENAI_API_KEY")

    # Load API key securely
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")


    if not api_key:
        raise RuntimeError("Environment variable OPENAI_API_KEY is not set.")

    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

    # Run the agent with the provided summary
    result = llm.predict(pr_summary)
    return result