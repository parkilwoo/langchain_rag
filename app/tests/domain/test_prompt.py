import unittest
from domain.prompter.models import ChatPrompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class TestChatPrompt(unittest.TestCase):

    def test_get_contextualize_q_prompt(self):
        # When
        prompt = ChatPrompt.get_contextualize_q_prompt()

        # Then
        assert isinstance(prompt, ChatPromptTemplate)
        assert prompt.messages[0] == ("system", ChatPrompt._contextualize_q_system_prompt)
        assert isinstance(prompt.messages[1], MessagesPlaceholder)
        assert prompt.messages[2] == ("human", "{input}")

    def test_get_qa_prompt(self):
        # When
        prompt = ChatPrompt.get_qa_prompt()

        # Then
        assert isinstance(prompt, ChatPromptTemplate)
        assert prompt.messages[0] == ("system", ChatPrompt._qa_system_prompt.format(context="{context}"))
        assert isinstance(prompt.messages[1], MessagesPlaceholder)
        assert prompt.messages[2] == ("human", "{input}")

