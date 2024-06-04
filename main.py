import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from prompts import new_prompt, instruction_str, context, translation_prompt
from note_engine import note_engine
from text_query_engine import TextQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from httpx import ReadTimeout, ConnectTimeout

# Load environment variables
load_dotenv()

# Define the path to the CSV file
dictionary_path = os.path.join("data", "combined_dictionary.csv")

# Load the CSV data into a Pandas DataFrame
dictionary_df = pd.read_csv(dictionary_path)

# Create an SQLite database in memory
conn = sqlite3.connect(':memory:')

# Load the DataFrame into the SQLite database
dictionary_df.to_sql('dictionary_table', conn, index=False, if_exists='replace')

# Function to execute SQL queries on the SQLite database and return the result as a DataFrame
def query_sqlite(query, conn):
    return pd.read_sql_query(query, conn)

# Create a custom query engine using SQLite
class SQLiteQueryEngine:
    def __init__(self, conn, instruction_str):
        self.conn = conn
        self.instruction_str = instruction_str
    
    def query(self, query_str):
        try:
            sql_query = f"SELECT * FROM dictionary_table WHERE English LIKE '%{query_str}%' OR Dagaare LIKE '%{query_str}%'"
            result_df = query_sqlite(sql_query, self.conn)
            return result_df.to_string(index=False)
        except Exception as e:
            return str(e)

    def update_prompts(self, prompts):
        self.instruction_str = prompts.get("pandas_prompt", self.instruction_str)

# Instantiate the SQLiteQueryEngine
dictionary_query_engine = SQLiteQueryEngine(conn, instruction_str)
dictionary_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Define the text query engine
txt_engine = TextQueryEngine(file_path='data/dagaare_dict.txt')

# Define the tools
tools = [
    QueryEngineTool(
        query_engine=dictionary_query_engine,
        metadata=ToolMetadata(
            name="Translation",
            description="This tool queries the dictionary for Dagaare and English translations.",
        ),
    ),
    QueryEngineTool(
        query_engine=txt_engine,
        metadata=ToolMetadata(
            name="Dagaare_dictionary",
            description="This tool provides detailed information about Dagaare.",
        ),
    ),
    note_engine,
]

# Initialize the language model
llm = Ollama(model="gemma:2b", request_timeout=300.0)

# Create the agent
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

def query_with_retry(agent, prompt, retries=3):
    for attempt in range(retries):
        try:
            return agent.query(prompt)
        except (ReadTimeout, ConnectTimeout):
            print(f"Attempt {attempt + 1} failed. Retrying...")
    return "Failed to get a response after multiple attempts."

# Main loop for prompting the user
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    if "translate" in prompt.lower():
        query_result = query_with_retry(agent, translation_prompt.format(query_str=prompt, context=context))
    else:
        query_result = query_with_retry(agent, prompt)
    print(query_result)

# Close the SQLite connection when done
conn.close()
