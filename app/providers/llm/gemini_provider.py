import string
from google import genai
from core.config import settings
from providers.llm.base_provider import BaseLLmProvider
from providers.llm.rag_prompt import RAG_PROMPT

class GeminiProvider(BaseLLmProvider):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate(self, context: str, question: str) -> str:
        prompt = RAG_PROMPT.substitute(context=context, question=question)
        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        return response.text
