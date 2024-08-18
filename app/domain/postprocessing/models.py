from abc import ABC, abstractmethod
from typing import Any

class BasePostProcessing(ABC):
    
    @classmethod    
    @abstractmethod
    def do_process(cls, input: Any, *args, **kwargs):
        pass
    
    
class TranslatePostProcessing(BasePostProcessing):
    
    @classmethod
    def _translate(cls, input: str, lang: int):
        if lang == 0:
            return input
        if lang == 1:
            # TODO 영어로 번역 로직 구현
            return input
        else:
            raise ValueError("lang argument one choice.\n0: KOR, 1: ENG")
    
    @classmethod
    def do_process(cls, input: Any, *args, **kwargs):
        if not isinstance(input, str):
            raise ValueError(f"Input value only expected type str, but this type {type(input)}")
        
        lang = kwargs.get('lang')
        if not lang:
            raise ValueError(f"TranslatePostProcessing required lang argument")
        if not isinstance(lang, int):
            raise ValueError(f"lang argument only expected type str, but this type {type(lang)}")
        
        return cls._translate(input, lang)