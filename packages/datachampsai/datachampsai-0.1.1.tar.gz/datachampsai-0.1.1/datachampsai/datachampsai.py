from langchain_openai import ChatOpenAI

class DCAI:
    def __init__(self, api_key: str, reference_document: str, model: str = "gpt-4", temperature: float = 0.3):
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
        self.reference_document = reference_document

    def rephrase_query(self, user_input: str, chat_history: list[str] = []) -> str:


        chat_context = ""
        for i in range(0, len(chat_history), 2):
            user = chat_history[i]
            bot = chat_history[i + 1] if i + 1 < len(chat_history) else ""
            chat_context += f"User: {user}\nBot: {bot}\n"

        full_prompt = f"""
---BEGIN CHAT CONTEXT---
{chat_context}
User: {user_input}
---END CHAT CONTEXT---

---BEGIN REFERENCE DOCUMENT---
{self.reference_document}
---END REFERENCE DOCUMENT---

Respond in format:

<refined_query>
...
</refined_query>

<additional_info>
...
</additional_info>
"""

        try:
            response = self.llm.invoke(full_prompt)

            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)

        except Exception as e:
            return f"ERROR: {e}"
