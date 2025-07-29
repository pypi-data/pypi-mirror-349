"""
SQL Code Generator using LLM

This module generates and executes SQL queries using LLM (Language Learning Model).
It handles database connections, query generation, and execution with error handling.
"""

import logging
import os
from typing import Dict, Any
# import psycopg2
# import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from codex import CodeExecutor
from langchain_core.utils.input import print_text as pt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SQLCodeGenerator:
    def __init__(self, max_retries: int = 5):
        """
        Initialize the SQL Code Generator.

        Args:
            max_retries (int): Maximum number of retries for code execution
        """
        self.MAX_RETRIES = max_retries

        # Database configuration templates
        self.DB_CONFIG_TEMPLATE = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "6543")),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }

        self.DB_CONFIG_REAL = {
            "host": os.getenv("DB_HOST", "aws-0-ap-south-1.pooler.supabase.com"),
            "port": int(os.getenv("DB_PORT", "6543")),
            "database": os.getenv("DB_NAME", "postgres"),
            "user": os.getenv("DB_USER", "postgres.wcaersuqyvrwwpztwynt"),
            "password": os.getenv("DB_PASSWORD", "Datachamps@2025")
        }

        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4.1-2025-04-14",
            temperature=0
        )

        # Initialize code executor
        self.code_executor = CodeExecutor()

    def get_db_config_str(self, config: Dict[str, Any]) -> str:
        """Convert database config dictionary to string representation."""
        return f"""db_config = {{
    "host": "{config['host']}",
    "port": {config['port']},
    "database": "{config['database']}",
    "user": "{config['user']}",
    "password": "{config['password']}"
}}"""

    def get_python_code_prefix(self, db_config: Dict[str, Any]) -> str:
        """Generate the Python code prefix with database configuration."""
        return f"""import psycopg2
import os
import pandas as pd
import numpy as np
import json

{self.get_db_config_str(db_config)}

conn = psycopg2.connect(**db_config)
cur = conn.cursor()

# START OF YOUR CODE
"""

    def get_main_prompt_template(self) -> str:
        """Get the main prompt template for LLM."""
        return """
You are a python and sql expert. You will be given the following information and you have to generate a python code to solve the user's query.
Information provided:
 - Info about the database, schemas, tables, columns, etc.
 - Clearly defined user query
 - Relavent info (similar queries, additional context, etc.)
 - Python code prefix (this code is already written you have to write the next bit this contains the database connection code and imports)

<DATABASE SCHEMA>
{db_schema}
</DATABASE SCHEMA>

<QUERY>
{query}
</QUERY>

<RELEVANT INFO>
{relevant_info}
</RELEVANT INFO>

{previous_code_with_errors}

### PREFIX
{prompt_code_prefix}

DO NOT MAKE UNNECESSARY IMPORTS
The code prefix already set up the connection and cursor. 
Only write code from the next line onwards. 
To execute a query use cur.execute(query)
To fetch the result use cur.fetchone()
AVOID TRY CATCH BLOCKS, we have to see the error to fix it.
Convert the numbers, arrays and other data types to the correct format. when running calculations (float (x) , int (x))
Feel free to split the query into multiple queries if it is too complex. Add intermidiate prints.

the last part of the code is this function: you must put the results in this and the last line is ALWAYS generate_response(answer, relevant_info, dataframe)
def generate_response(answer, relevant_info, dataframe):
    return {{
        'answer': answer,
        'relevant_info': relevant_info,
        'dataframe': dataframe
    }}

result = generate_response(answer, relevant_info, dataframe)
#YOUR CODE HERE
"""

    def get_error_template(self, code_response: Dict[str, Any], generated_code: str) -> str:
        """Generate error template for failed code execution."""
        return f"""
        The following code generated an error: {generated_code}

        Original code:
        {generated_code}
        """

    def execute_query(self, query: str, db_schema: str, relevant_info: str) -> Dict[str, Any]:
        """
        Execute a SQL query using LLM-generated code.

        Args:
            query: The SQL query to execute
            db_schema: Database schema information
            relevant_info: Additional relevant information for query generation
        """
        main_prompt_template = self.get_main_prompt_template()
        prompt_code_prefix = self.get_python_code_prefix(self.DB_CONFIG_TEMPLATE)
        real_code_prefix = self.get_python_code_prefix(self.DB_CONFIG_REAL)

        # Initial code generation
        main_prompt = main_prompt_template.format(
            db_schema=db_schema,
            query=query,
            relevant_info=relevant_info,
            prompt_code_prefix=prompt_code_prefix,
            previous_code_with_errors=""
        )

        response = self.llm.invoke(main_prompt)
        response = response.content.replace("```python", "").replace("```", "").strip()
        full_code = real_code_prefix + response

        # Execute and retry logic
        retry_count = 0
        code_response = self.code_executor.smart_executor(full_code, query)
        print("SMART EXE: \n\n", code_response)
        pt(full_code, color='green')

        while retry_count < self.MAX_RETRIES:
            if code_response.get("answer_in_result"):
                final_output = {
                    "success": True,
                    "output": code_response.get("output"),
                    "result": code_response.get("result"),
                    "error": code_response.get("error"),
                    "full_code": response
                }
                return final_output

            print(f"Attempt {retry_count + 1} of {self.MAX_RETRIES}: trying to fix the code")
            complaint = self.get_error_template(code_response, full_code)
            main_prompt_redo = main_prompt_template.format(
                db_schema=db_schema,
                query=query,
                relevant_info=relevant_info,
                prompt_code_prefix=prompt_code_prefix,
                previous_code_with_errors=complaint
            )

            response = self.llm.invoke(main_prompt_redo)
            response = response.content.replace("```python", "").replace("```", "").strip()
            full_code = real_code_prefix + response
            # print("FULL CODE:\n\n")
            # print(full_code)
            # print("\n\n--------------------------------\n\n")
            code_response = self.code_executor.smart_executor(full_code, query)
            pt(code_response, color='blue')
            # print("SMART EXE: \n\n", code_response)

            pt(full_code, color='green')
            retry_count += 1

        if not code_response.get("answer_in_result"):
            print(f"Failed to fix the code after {self.MAX_RETRIES} attempts")
            final_output = {
                "success": False,
                "output": code_response.get("output"),
                "result": code_response.get("result"),
                "error": code_response.get("error"),
                "full_code": response
            }
            return final_output


if __name__ == "__main__":
    # Example usage
    db_schema = open('python_sql_prompt.txt', 'r').read()
    query = "what are the top 5 products of 2024 by sales?"
    relevant_info = """"""

    sql_generator = SQLCodeGenerator(max_retries=5)
    result = sql_generator.execute_query(query, db_schema, relevant_info)
    print(result['output'])




