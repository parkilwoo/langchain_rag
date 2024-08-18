from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
class ChatPrompt:
    _contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )
    
    _qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use "
        "the following pieces of retrieved context to answer the "
        "question. If you don't know the answer, just say that you "
        "don't know. Use three sentences maximum and keep the answer "
        "concise."
        "\n\n"
        "{context}"
    )
    HISTORY_MESSAGE_KEY = "chat_history"
    INPUT_MESSAGE_KEY = "input"
    
    
    @classmethod
    def get_contextualize_q_prompt(cls):
        return ChatPromptTemplate.from_messages(
                    [
                        ("system", cls._contextualize_q_system_prompt),
                        MessagesPlaceholder(cls.HISTORY_MESSAGE_KEY),
                        ("human", f"{{{cls.INPUT_MESSAGE_KEY}}}"),
                    ]
                )
    @classmethod
    def get_qa_prompt(cls):
        return ChatPromptTemplate.from_messages(
                    [
                        ("system", cls._qa_system_prompt),
                        MessagesPlaceholder(cls.HISTORY_MESSAGE_KEY),
                        ("human", f"{{{cls.INPUT_MESSAGE_KEY}}}"),
                    ]
                )
