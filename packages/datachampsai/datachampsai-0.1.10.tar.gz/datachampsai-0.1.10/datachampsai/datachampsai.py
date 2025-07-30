from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv
import re
from langchain_openai import ChatOpenAI

import json
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlcoder import SQLCodeGenerator

# Load environment variables from .env file

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

sql_generator = SQLCodeGenerator(max_retries=5)
py_db_schema = open('python_sql_prompt.txt', 'r').read()

model = ChatOpenAI(
    model="gpt-4.1-2025-04-14",
    temperature=0
)

schema = open("schema.txt", "r").read()
reference_doc = open("b_doc.txt", "r").read()


class DCAI:
    def __init__(self, api_key: str, schema: str, py_db_schema: str, reference_document: str = "", model: str = "gpt-4",
                 temperature: float = 0.3):
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
        self.schema = schema
        self.py_db_schema = py_db_schema
        self.reference_document = reference_document

    def main_agent(self, chat_context: List[Dict[str, str]]) -> Tuple[str, List[Dict[str, str]]]:
        main_prompt = """ You are an expert technical assistant. you are given chat context, a reference doc.
        and your job is to return 2 things:
        1. A rephrased query that accurately reflects the user's intent. based on the chat_context and the reference doc.
        2. additional information that will help answer the question.

        Here is the chat_context:
        {chat_context}

        Here is the reference doc:
        {reference_doc}

        STRICT INSTRUCTIONS: 
        use the tags <query> and <additional_information> to return the query and the additional information respectively.
        Example :
        <query>
        A PRESCISE QUESTION THAT REFLECTS THE USER'S INTENT IN PLAIN ENGLISH, INCLUDE ANY ENTITY NAMES (table names, column names etc)IF APPROPRIATE. 
        </query>
        <additional_information>
        Hint for solving the query. PLAIN ENGLISH HINT LOGIC. DO NOT WRITE ANY CODE OR SQL.
        </additional_information>


        today's date: {date}
        """

        main_prompt = main_prompt.format(reference_doc=reference_doc, chat_context=chat_context,
                                         date=datetime.now().strftime("%Y-%m-%d"))
        response = model.invoke(main_prompt)

        # Extract content between tags
        query_match = re.search(r'<query>(.*?)</query>', response.content, re.DOTALL)
        additional_info_match = re.search(r'<additional_information>(.*?)</additional_information>', response.content,
                                          re.DOTALL)

        # Extract and clean the content
        query = query_match.group(1).strip() if query_match else ""
        additional_info = additional_info_match.group(1).strip() if additional_info_match else ""

        # Combine into a structured response
        structured_response = f"Query: {query}\n\nAdditional Information: {additional_info}"
        print("STRUCTURED RESPONSE: ", structured_response)

        output = sql_generator.execute_query(query, py_db_schema, additional_info)

        sql_result = output.get("result")
        sql_answer = sql_result.get("answer")
        sql_relevant_info = sql_result.get("relevant_info")
        sql_dataframe = sql_result.get("dataframe")

        post_processed_response = self.post_process_response(query, output)

        return post_processed_response, output.get("full_code")

    def post_process_response(self, query: str, raw_response: str):
        prompt = """ Sometimes, the response from the agent is not in the correct format. or is not user readable.
        Here is the query:
        {query}
        Here is the response:
        {raw_response}
        Please post process the response to make it more user readable. make sure to format the response appropriately. with new lines or lists in markdown format. 
        ONLY RETURN THE POST PROCESSED RESPONSE, NOTHING ELSE.
        """
        prompt = prompt.format(query=query, raw_response=raw_response)
        response = model.invoke(prompt)
        return response.content

    # def process_delegation(main_agent_response: str, chat_context: List[Dict[str, str]]):

    def get_ai_response(self, chat_context: List[Dict[str, str]]):
        main_agent_response, usage_metadata = self.main_agent(chat_context)
        print("MAIN AGENT RESPONSE: ", main_agent_response)

        return main_agent_response, usage_metadata
        # content, retrieved_context = process_delegation(main_agent_response, chat_context)
        # return content, retrieved_context


if __name__ == "__main__":
    chat_context = [{"role": "user", "content": "what are the top 5 products of 2024 by sales?"}]
    api_key = os.getenv("OPENAI_API_KEY")
    reference_doc = open("b_doc.txt", "r").read()
    dcai = DCAI(
        api_key="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",
        schema=open("schema.txt").read(),
        py_db_schema=open("python_sql_prompt.txt").read(),
        reference_document=open("b_doc.txt").read()
    )

    res = dcai.get_ai_response(chat_context)
    print(res)
