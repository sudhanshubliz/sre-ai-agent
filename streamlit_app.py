import streamlit as st
from rag.rag_engine import query_logs

st.set_page_config(page_title="CI/CD Log Assistant", page_icon="🧪")

# Chat UI setup
st.title("🔍 CI/CD Log Assistant Chatbot")

# Initialize the chat history (st.session_state keeps the chat history across messages)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to display chat
def display_messages():
    for msg in st.session_state.messages:
        if msg['role'] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")

# Input box for the user
user_input = st.text_input("Your question:")

# If the user submits a message
if user_input:
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Query the logs using LlamaIndex
    with st.spinner("Thinking..."):
        response = query_logs(user_input)

    # Add AI's response to chat history
    st.session_state.messages.append({"role": "ai", "content": response})

    # Display the updated chat
    display_messages()

else:
    display_messages()
