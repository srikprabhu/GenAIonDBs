# LLM connection
import json
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")
api_version = os.getenv("api_version")
azure_endpoint = os.getenv("azure_endpoint")
model_deployment_name = os.getenv("model_deployment_name")

def get_me_llm_response(message_prompt):
    from openai import AzureOpenAI
    import json

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )

    response = client.chat.completions.create(
        model=model_deployment_name,  
        messages=message_prompt
    )

    j = response.model_dump_json()
    j = json.loads(j)
    # print(j)

    return j["choices"][0]["message"]["content"]

# Selection of kind of SQL
dialect="SQLite" # (MySQL/PostgreSQL/SQLite)

# Schema of Tables for LLM context
schema_context="""
CREATE TABLE Employee (
    EmployeeId INTEGER PRIMARY KEY,
    LastName NVARCHAR(20),
    FirstName NVARCHAR(20),
    Title NVARCHAR(30),
    ReportsTo INTEGER,
    FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId))
"""

# System prompt for LLM
def get_system_prompt(dialect, schema_context):
    system_prompt="""
    You are a SQL expert specializing in <dialect> databases. Generate precise SQL queries using these rules:

    1. Use schema context: 
    
    <schema_context>
    
    2. Prefer CTEs over nested subqueries
    3. Include explicit column aliases
    4. Use standard ANSI SQL unless specified
    5. Add brief comments explaining complex logic

    Based on user's query, generate SQL query.
    Output formate: {"sql_query":"generated query result"}
    """.replace("<dialect>",dialect).replace("<schema_context>",schema_context)
    return system_prompt


if __name__ == "__main__":
    # User query :
    user_queries = [
            "Count of employees by job title",
            "List all employees with their managers' names",
            "Count of employees by job title",
            "Find employees without direct reports (leaf nodes)",
            "Show employees with 'Manager' in their title",
        ]

    query_response = []
    query_response.append({"schema":schema_context})
    system_prompt = get_system_prompt(dialect,schema_context)
    for user_query in user_queries:
        message_prompt = [
                {"role": "system","content": system_prompt},
                {"role":"user", "content":user_query}
            ]

        response = get_me_llm_response(message_prompt)
        # print("-"*20,"\n",response,"\n","-"*20)
        import json
        response = json.loads(response)
        # print("+"*20,"\n",response,"\n","+"*20)
        print("User query: ",user_query,"\n")
        print("LLM response :\n",response["sql_query"])

        query_response.append({"user_query":user_query,"sql_query":response["sql_query"]})

    with open("sql_results_v1.json", "w") as json_file:
        json.dump(query_response, json_file, indent=4)

    print("JSON file saved successfully!")