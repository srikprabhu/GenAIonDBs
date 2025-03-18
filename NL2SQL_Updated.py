import os
import json
import pymysql
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# LLM connection settings
api_key = os.getenv("api_key")
api_version = os.getenv("api_version")
azure_endpoint = os.getenv("azure_endpoint")
model_deployment_name = os.getenv("model_deployment_name")

# MySQL connection settings
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")

# Function to get LLM response from Azure OpenAI
def get_llm_response(message_prompt):
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )

    response = client.chat.completions.create(
        model=model_deployment_name,
        messages=message_prompt
    )
    
    # Parse response and return generated SQL
    j = response.model_dump_json()
    j = json.loads(j)
    return j["choices"][0]["message"]["content"]

# Function to get a connection to the MySQL database
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        return connection
    except pymysql.MySQLError as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Function to retrieve schema information from MySQL database
def get_schema_info(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    schema_info = {}
    
    # Get columns of each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()
        schema_info[table_name] = [column[0] for column in columns]
    
    cursor.close()
    return schema_info

# Function to generate SQL query using the LLM based on schema and user query
def generate_sql_query(schema_info, user_query, conversation_history):
    prompt = f"""
    You are a SQL expert. Based on the following database schema, generate a valid SQL query to answer the user's question. 
    Please ensure the query includes all aspects of the user's question, and return only the SQL query.

    Database Schema:
    """
    
    # Dynamically add schema info (tables and columns)
    for table, columns in schema_info.items():
        prompt += f"\n{table} (" + ", ".join(columns) + ")"
    
    prompt += f"\n\nConversation History: {conversation_history}\n\nUser Query: {user_query}\n\nSQL Query:"

    # Send prompt to LLM
    message_prompt = [{"role": "system", "content": "You are a SQL expert."},
                      {"role": "user", "content": prompt}]
    
    sql_query = get_llm_response(message_prompt)
    return sql_query.strip()

# Function to sanitize the SQL query
def sanitize_sql_query(query):
    # Remove unwanted markdown formatting or backticks
    sanitized_query = query.replace("```sql", "").replace("```", "").strip()
    
    # If the response contains extra explanation text, discard it
    if "To better assist you" in sanitized_query or "Could you please specify" in sanitized_query:
        return ""
    
    return sanitized_query

# Function to run the SQL query on the database and get results
def run_sql_query(db_connection, query):
    try:
        # Sanitize the SQL query before execution
        query = sanitize_sql_query(query)
        
        if not query:
            return "Error: The generated SQL query is invalid or unclear."

        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pymysql.MySQLError as e:
        st.error(f"Error executing query: {e}")
        return None

# Function to format the result for better readability
def format_result(result):
    formatted_result = ""
    columns = [
        "Default ID", "Loan ID", "Default Date", "Default Reason", "Remarks", 
        "Employee Name", "Address", "Phone Number", "Email", "Date Of Birth", 
        "Loan Amount", "Credit Score", "Income", "Employment Type", "Loan Term", 
        "Past Defaults", "Loan Status"
    ]
    
    for idx, value in enumerate(result[0]):
        formatted_result += f"**{columns[idx]}:** {value}\n"
    
    return formatted_result

# Function to process the user's query, generate SQL query, execute it, and return results
def process_user_query(user_query, conversation_history):
    # Connect to the database
    db_connection = get_db_connection()
    if not db_connection:
        return f"Error: Unable to connect to the MySQL database."
    
    # Retrieve schema information from MySQL
    schema_info = get_schema_info(db_connection)

    # Generate SQL query using the LLM with conversation history
    sql_query = generate_sql_query(schema_info, user_query, conversation_history)

    # Execute the generated SQL query
    result = run_sql_query(db_connection, sql_query)

    # Format the result
    if result is None or len(result) == 0:
        return f"""
**Question:** {user_query}

**SQL Query:** {sql_query}

**Result:** No results found.
        """

    # Format result to be self-explanatory
    formatted_result = format_result(result)

    # Add this new question and result to conversation history
    conversation_history.append(f"User: {user_query}")
    conversation_history.append(f"SQL Query: {sql_query}")
    conversation_history.append(f"Result: {formatted_result}")

    return f"""
**Question:** {user_query}

**SQL Query:** {sql_query}

**Result:**\n{formatted_result}
    """

# Streamlit User Interface
def main():
    st.title("SQL Query Generator & Executor")
    
    # Store conversation history across multiple queries
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    # Display previous conversation history
    if st.session_state.conversation_history:
        st.subheader("Conversation History:")
        for idx, entry in enumerate(st.session_state.conversation_history):
            st.markdown(f"**Entry {idx+1}:** {entry}")

    # User input for the query
    user_query = st.text_input("Enter your SQL question:", "")
    
    if user_query:
        result = process_user_query(user_query, st.session_state.conversation_history)
        st.markdown(result)

if __name__ == "__main__":
    main()
