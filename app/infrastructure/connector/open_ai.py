from langchain_openai import ChatOpenAI
from enum import Enum

from core.exception_handler import CustomException
from infrastructure.connector.base import BaseConnector

class OpenAiModel(Enum):
    GPT_4O = ("gpt-4o", "gpt-4o-2024-05-13", "gpt-4o-2024-08-06")
    GPT_3_5 = ("gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-instruct")
    GPT_4 = ("gpt-4-turbo", "gpt-4-turbo-2024-04-09", "gpt-4-turbo-preview", "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4", "gpt-4-0613", "gpt-4-0314")
    
    def __init__(self, *model_names) -> None:
        self.model_names = model_names

class OpenAiConnector(BaseConnector):
    _test_message = "Hello, are you working?"
    
    def __init__(self, open_ai_key: str, model_name: str) -> None:
        self._valide_model(model_name)
        self.connector = ChatOpenAI(api_key=open_ai_key, model=model_name)
    
    def _valide_model(self, model_name: str) -> None:
        if not any(model_name in model.model_names for model in OpenAiModel):
            raise ValueError(f"Invalid model name: {model_name}")
        
    async def test_connection(self) -> bool:
        try:
            await self.connector.ainvoke(self._test_message)
        except Exception as e:
            raise CustomException(e.status_code, e.body.get('message') or e.message)
        
    def get_connector(self):
        return self.connector
    