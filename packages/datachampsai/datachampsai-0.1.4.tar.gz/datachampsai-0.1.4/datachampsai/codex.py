import sys
import io
import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI


class CodeExecutor:
    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)
        # Initialize a shared namespace for all executions
        self.shared_namespace = {}

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and return results as JSON.

        Args:
            code (str): Python code to execute

        Returns:
            Dict[str, Any]: Dictionary containing:
                - success (bool): Whether execution was successful
                - output (str): Captured stdout output
                - error (str): Any error message if execution failed
                - result (Any): The result of the last expression (if any)
        """
        # Initialize response dictionary
        response = {
            "success": False,
            "output": "",
            "error": "",
            "result": None
        }

        # Create string buffers to capture stdout and stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        try:
            # Redirect stdout and stderr to our buffers
            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer

            # Setup code with necessary imports and environment verification
            setup_code = """
import os
import sys
import site
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
# Print environment information
# print("Python version:", sys.version)
# print("Python executable:", sys.executable)
# print("Current working directory:", os.getcwd())
# print("Python path:", sys.path)

# Verify pandas import
# print("Pandas version:", pd.__version__)
test_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
# print("Test DataFrame created successfully:", test_df)


def generate_response(answer: str, relevant_info: str, dataframe: pd.DataFrame):
    return {
        'answer': answer,
        'relevant_info': relevant_info,
        'dataframe': dataframe
    }

# User's code follows
"""
            # Combine setup code and user code
            full_code = setup_code + "\n" + code  # THIS \n IS IMPORTANT!!!! else the code combines with debug statements and gets screwed up.

            # Execute the combined code in the shared namespace
            exec(full_code, self.shared_namespace)

            # If we get here, execution was successful
            response["success"] = True
            response["output"] = stdout_buffer.getvalue()

            # Get the result of the last expression
            if 'result' in self.shared_namespace:
                response["result"] = self.shared_namespace['result']

        except Exception as e:
            # Capture any errors
            response["error"] = str(e)
            response["output"] = stdout_buffer.getvalue()

        finally:
            # Restore original stdout and stderr
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr

            # Close the buffers
            stdout_buffer.close()
            stderr_buffer.close()

        return response

    def execute_code_json(self, code: str) -> str:
        """
        Execute Python code and return results as JSON string.

        Args:
            code (str): Python code to execute

        Returns:
            str: JSON string containing execution results
        """
        result = self.execute_code(code)
        return result  # json.dumps(result, indent=2)

    def smart_executor(self, code, query):
        result = self.execute_code_json(code)
        prompt_temp = """We have run the following Python code


        ###
        {code}
        ###
        and got this result from the executor:
        {result} 

        Keep in mind, success just means the code ran. 

        I want to know if the result actually contains a satisfactory answer to the query:
        {query}
        return a True or False value
        Fromat:
        Only return the word 'True' or 'False'
        """
        prompt = prompt_temp.format(code=code, result=result, query=query)
        res = self.llm.invoke(prompt)
        tf = "true" in res.content.lower()

        exe_result = {
            "code_ran": result.get("success"),
            "answer_in_result": tf,
            "output": result.get("output"),
            "error": result.get("error"),
            "result": result.get("result")
        }
        return exe_result


if __name__ == "__main__":
    code_executor = CodeExecutor()

    code = """
    print(1/0)
    """

    print(code_executor.execute_code_json(code))
