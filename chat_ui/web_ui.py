import streamlit as st
from crew.main_crew import AssistantCrew

# Initialize Streamlit app
st.title("R&D Assistant Chat")
st.write("Ask me anything to help with your research and development tasks!")

# Initialize the Crew
crew = AssistantCrew()

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
                result = crew.run(prompt)
                st.markdown(result)
            except Exception as e:
                st.markdown(f"Error: {str(e)}")
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": result})
