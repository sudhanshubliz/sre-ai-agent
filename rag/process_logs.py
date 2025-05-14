import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load GitHub token from .env file

# GitHub API constants
GITHUB_API_URL = "https://github.com"
REPO_OWNER = "sudhanshubliz"
REPO_NAME = "sre-ai-agent"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_logs(run_id):
    """
    Fetch logs from GitHub Actions for a specific run.
    :param run_id: GitHub Actions run ID
    :return: Log text content
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    logs_url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/logs"
    response = requests.get(logs_url, headers=headers)

    if response.status_code == 200:
        log_url = response.json()['url']  # Fetch the log file URL
        log_data = requests.get(log_url).text
        return log_data
    else:
        raise Exception(f"Failed to fetch logs: {response.status_code}, {response.text}")

def process_and_index_logs(log_data):
    """
    Process logs and create vector index for querying.
    :param log_data: Raw log data text
    """
    from llama_index import ServiceContext, VectorStoreIndex, SimpleDirectoryReader

    # Example process: Turn the logs into documents
    documents = SimpleDirectoryReader.from_string(log_data).load_data()

    # Build a vector index for RAG querying
    index = VectorStoreIndex.from_documents(documents)

    # Save the index for later use
    index.save_to_disk("rag/index")

    print("Logs successfully indexed!")

if __name__ == "__main__":
    run_id = "15032328954"  # Replace with your actual run ID
    log_data = get_github_logs(run_id)
    process_and_index_logs(log_data)
