import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from crew.main_crew import AssistantCrew
from tools.git_manager import init_git_repo, commit_changes, push_to_github

# Initialize Streamlit app
st.title("R&D Assistant Chat")
st.write("Ask me anything to help with your research and development tasks!")

# Initialize the Crew
if "crew" not in st.session_state:
    st.session_state.crew = AssistantCrew()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What do you want to build or research?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.crew.run(prompt)
                st.markdown(result)
            except Exception as e:
                st.markdown(f"Error: {str(e)}")
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": result})

# GitHub Integration Section
st.sidebar.header("GitHub Integration")

# Initialize Git repo (only once)
if "repo" not in st.session_state:
    repo_path = os.getcwd()
    st.session_state.repo = init_git_repo(repo_path)
    st.sidebar.success("Git repository initialized!")

# Commit and Push
commit_message = st.sidebar.text_input("Commit Message", value="Update from R&D Assistant")
remote_url = st.sidebar.text_input("GitHub Repo URL (HTTPS)", placeholder="https://github.com/username/repo.git")

if st.sidebar.button("Commit and Push to GitHub"):
    if not remote_url:
        st.sidebar.error("Please provide a GitHub repository URL.")
    else:
        with st.sidebar:
            with st.spinner("Committing and pushing..."):
                try:
                    commit_result = commit_changes(st.session_state.repo, commit_message)
                    st.success(commit_result)
                    push_result = push_to_github(st.session_state.repo, remote_url)
                    st.success(push_result)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Clear History Button
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.crew = AssistantCrew()  # Reset the crew to clear its history
    st.success("Chat history cleared!")