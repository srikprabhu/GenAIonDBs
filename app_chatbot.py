import streamlit as st
from Gen_AI_DB_2 import final_response

st.set_page_config(
    page_title="Query Response",
    page_icon="deloitte_logo.ico",
    layout="wide"
)

st.image('Deloitte-Logo.png', width = 120)

# Streamlit app structure
st.title("Query Response")

# Create a chat history container
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.write(message)  # Use st.write to display the chat history

# Display a text area where the user can type multiple lines of text
query = st.text_area("Enter your query:")

# Check if the user has entered any text
if query:
    # Process the text (for example, split into sentences or perform other operations)
    st.session_state.messages.append(f"You: {query}")
    response = final_response(query,str(st.session_state.messages))  # Example: Convert to lowercase
    st.session_state.messages.append(f"Bot: {response}")