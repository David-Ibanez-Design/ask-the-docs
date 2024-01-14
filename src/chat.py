import streamlit as st
from codeinterpreterapi import CodeInterpreterSession, File

def displayResponse(message, prompt=None):
        st.write(message["content"])
        if len(message["files"])>0:
            for _file in message["files"]:
                st.image(_file.get_image(), caption=prompt, use_column_width=True)

def handleChat(uploaded_file_name, col_names, uploaded_files_list):
        
        # Check and initialize session state variables if not present
        # Initialize the chat messages history
        if "messages" not in st.session_state.keys(): 
            # Initial greetings by the LLM 
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hello ! Ask me anything about " + uploaded_file_name, 
                    "files": []
                }
            ]
        
        # Display user prompt in chat history and store it in message{}
        if prompt := st.chat_input(placeholder="Query " + uploaded_file_name, key='input'):
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt, 
                "files": []
            })

        # Display the prior chat messages
        for message in st.session_state.messages:  
            with st.chat_message(message["role"]):
                displayResponse(message)
        
        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    with CodeInterpreterSession(modal="gpt-4") as session:

                            final_prompt =  prompt+" .If relevant, please use the following column names to answer the query: " +', '.join(col_names)
                            response = session.generate_response(final_prompt, files=uploaded_files_list)
                            message = {
                                "role": "assistant", 
                                "content": response.content,
                                "files": response.files
                            }
                st.session_state.messages.append(message) 
                displayResponse(message, prompt)