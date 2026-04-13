import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    MODEL_NAME: str = "gpt-4o-mini"
    MAX_SEARCH_RESULTS: int = 5


settings = Settings()