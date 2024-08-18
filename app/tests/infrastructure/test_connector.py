import pytest
from unittest import TestCase
from unittest.mock import patch, AsyncMock
from infrastructure.connector.open_ai import OpenAiConnector
from core.exception_handler import CustomException

class TestOpenAiConnector(TestCase):

    @patch('infrastructure.connector.open_ai.ChatOpenAI')
    def test_openai_connector_initialization(self, MockChatOpenAI):
        # Given
        api_key = "test_api_key"
        model_name = "gpt-4"

        # When
        connector = OpenAiConnector(api_key, model_name)

        # Then
        MockChatOpenAI.assert_called_once_with(api_key=api_key, model=model_name)
        assert isinstance(connector, OpenAiConnector)

    def test_valide_model(self):
        # Given
        valid_model_name = "gpt-4"
        invalid_model_name = "invalid-model"

        # When / Then
        connector = OpenAiConnector("test_api_key", valid_model_name)
        
        with self.assertRaises(ValueError):
            connector._valide_model(invalid_model_name)

    @patch('infrastructure.connector.open_ai.ChatOpenAI.ainvoke', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_test_connection_success(self, mock_ainvoke):
        # Given
        connector = OpenAiConnector("test_api_key", "gpt-4")

        # When
        result = await connector.test_connection()

        # Then
        mock_ainvoke.assert_awaited_once_with(connector._test_message)
        assert result is None

    @patch('infrastructure.connector.open_ai.ChatOpenAI.ainvoke', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, mock_ainvoke):
        # Given
        mock_ainvoke.side_effect = Exception("Connection error")
        connector = OpenAiConnector("test_api_key", "gpt-4")

        # When / Then
        with self.assertRaises(CustomException):
            await connector.test_connection()

    def test_get_connector(self):
        # Given
        connector = OpenAiConnector("test_api_key", "gpt-4")

        # When
        result = connector.get_connector()

        # Then
        assert result == connector.connector
