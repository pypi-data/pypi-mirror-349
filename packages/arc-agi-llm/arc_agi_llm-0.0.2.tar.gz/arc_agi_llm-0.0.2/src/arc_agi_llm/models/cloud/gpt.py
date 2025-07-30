from ..llm import LLM
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


class GPT(LLM):
    def __init__(self):
        super().__init__()

    def init_client(self):
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in .env")

        return OpenAI()

    def ask(self, prompt: str) -> str:
        print(prompt)
        response = (
            OpenAI().responses.create(model="gpt-3.5-turbo", input=prompt).output_text
        )
        print(response)
        return response
