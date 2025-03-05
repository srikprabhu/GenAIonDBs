#importing necessary libraries
import re
import ast
import time
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from config import openai_api_key
from config import azure_endpoint
from config import deployment_id
from config import api_version
from config import db_link

#llm model authorization
llm = AzureChatOpenAI(
    azure_deployment=deployment_id,  # or your deployment
    api_version=api_version,  # or your api version
    api_key=openai_api_key,  
    azure_endpoint = azure_endpoint
)

# Connect to the database (e.g., SQLite)
db = SQLDatabase.from_uri(db_link)

#Table & It's Column Descriptions
table_column_descriptions={"Customers":{"customer_id":"Each Customer has different ids",
                                        "first_name":"First name of the customer",
                                        "last_name":"Last Name of the customer",
                                        "email":"email address of the customer",
                                        "phone_number":"phone number of the customer"},
                           "Accounts":{"account_id":"Account id of different accounts. Each customer can has multiple accounts",
                                       "customer_id":"Customer Id of the customer which has the account.",
                                       "account_type":"The type of the account Savings, credit etc",
                                       "balance":"balance amount in the account"},
                           "Transactions":{"transaction_id":"Each transaction has different transaction ids. Each account can do multiple transactions",
                                           "account_id":"Account ID of the account which made the transaction.",
                                           "transaction_type": "The type of the transaction like payment, withdrawal, deposit etc",
                                           "amount":"amount money of the transaction",
                                           "transaction_date":"The date in which the transaction occured.It's in YYYY-MM-DD format.",
                                           "description":"The description of the transaction on how or for which the transaction's being done"
                                          },
                            "PaymentsDue":{"payment_id":"Every due payment has a payment id",
                                           "account_id":"The account id of the customer which has the payment due",
                                           "payment_amount":"The money amount that is due for payment",
                                           "due_date":"The due date before which the customer has to make the payment. It's in YYYY-MM-DD format",
                                           "payment_status":"The status of the payment like due, paid, late etc"
                                          }
                          }


#Schema information
# Query to get all table names
query = "SELECT name FROM sqlite_master WHERE type='table';"

# Execute the query and fetch results
table_names = db.run(query)

print(table_names)#debugging
#Changing the string output to it's literal form.
table_names=ast.literal_eval(table_names)

#list of table names.
table_names=[item[0] for item in table_names]

#table, column & type pair
all_tab_col=""
for table_name in table_names:
    query = f"PRAGMA table_info({table_name});"
    result = db.run(query)
    result=ast.literal_eval(result)
    
    if isinstance(result, list) and len(result) > 0:
        # Extract the second element (column name) from each tuple if it's valid
        cols= [str({row[1]:row[2]}) for row in result]
    tab_col=f"{table_name} ({','.join(cols)}) "
    all_tab_col=all_tab_col+'\n'+tab_col


    #the template will give a sqllite sql query & the tables used in the sql query as an output.
template="""
You are a SQL expert. Based on the following database schema, generate a SQL query to answer the user's question. You can use multiple tables. Also give the relevant tables that's being used in the SQL query.

Database Schema:
{all_tab_col}

table column details:
{table_column_descriptions}

User Question: {query}

Please give the output in the following JSON format:
SQL Query: ONLY give the sql query generated as an output. I want to directly feed it into the sql query.,
Relevant Tables: The column used in the SQL Query. Just the Table Names in comma separated format.

"""

#prompttemplate takes table,column group, query, column descriptions of all tables.
query_generation_prompt = PromptTemplate(
    input_variables=["query", "all_tab_col","table_column_descriptions"],
    template=template
)

query_generation_chain = LLMChain(prompt=query_generation_prompt, llm=llm)

#query generation tool & it's function
def query_generation(query, all_tab_col, table_column_descriptions):
    return query_generation_chain.run(query=query, all_tab_col=all_tab_col, table_column_descriptions=table_column_descriptions)

query_generation_tool=Tool(
        name="Query Generation",
        func=query_generation,
        description="Query Generation"
    )


#the prompt template will give the final response of the query in natural language
template="""I will give you a query & it's answer which is extracted through a sql query along with the table's info from which it's extracted from & the descriptions of each column of the table. You will have to answer the query in English.

Tips:
**Please take into account all the informations of all the tables. Also each column of each table has different functions.**
Think thrice before giving an answer.
Summarize the answer in 150 tokens. Make the answer clear & concise with exact numbers & do not create numbers by yourself.

Steps:
1.Understand the query.
2.Understand the SQL query: columns, tables used & how it's being used. 
3.Check the table information of each table: which columns being used in the sql query & what's the sql query asking for.
4.Understand the response of the sql query which each value represent.

Query:{query},

Answer:{result},

SQL Query:{sql_query},

Table Column Descriptions: {table_column_details}
"""

NL_response_prompt=PromptTemplate(
    input_variables=["query","result","sql_query","table_column_details"],
    template=template
)

NL_response_chain=LLMChain(prompt=NL_response_prompt,llm=llm)

def NL_response(query,result,sql_query,table_column_details):
    return NL_response_chain.run(query=query,result=result,sql_query=sql_query,table_column_details=table_column_details)

NL_response_tool=Tool(
    name="NL_response",
    func=NL_response,
    description="Natural Language Response"
)

def final_response(query):
    
    #it will give sql query & relevant table details
    sql_query_table=query_generation_tool.func(query, all_tab_col, table_column_descriptions)
    print(sql_query_table)#debugging
    
    sql_query_table=ast.literal_eval(sql_query_table)
    sql_query=sql_query_table["SQL Query"]
    
    print(sql_query)
    
    #sql query result
    result=db.run(sql_query)
    
#     print(result)#debugging
    
    selected_tables=sql_query_table["Relevant Tables"].split(',')
    selected_tables=[selected_table.strip() for selected_table in selected_tables]
    table_column_details=""
    for selected_table in selected_tables:
        table_column_detail=table_column_descriptions[f"{selected_table}"]
        table_column_details=table_column_details+f"\n{selected_table} : {str(table_column_detail)}"
    
#     print(table_column_details)#debugging
    
    response=NL_response_tool.func(query,result,sql_query,table_column_details)
    
    return response


# ##############TestScript############
if __name__ == "__main__":
    query="Give me customer id 1 customer's all transaction details."
    response=final_response(query)
    print(response)