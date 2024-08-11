from langchain import hub

class ChatPrompt:
    _prompt = hub.pull("rlm/rag-prompt")
    
    @classmethod
    def get_prompt(cls):
        return cls._prompt