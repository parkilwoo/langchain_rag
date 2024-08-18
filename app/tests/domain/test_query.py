import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from domain.query.models import Query, QueryInput
from infrastructure.connector.base import BaseConnector
from domain.postprocessing.models import BasePostProcessing
from domain.prompter.models import ChatPrompt
from langchain_core.vectorstores.base import VectorStoreRetriever

@pytest.mark.asyncio
class TestQueryInput:

    @patch.object(BasePostProcessing, 'do_process', return_value="processed_input")
    def test_query_input_with_postprocessing(self, mock_do_process):
        # Given
        input_data = "input_data"
        query_input = QueryInput(input_data, BasePostProcessing, lang=1)

        # When
        result = query_input.get_input()

        # Then
        mock_do_process.assert_called_once_with(input_data, lang=1)
        assert result == "processed_input"

    def test_query_input_without_postprocessing(self):
        # Given
        input_data = "input_data"
        query_input = QueryInput(input_data, None)

        # When
        result = query_input.get_input()

        # Then
        assert result == input_data

@pytest.mark.asyncio
class TestQuery:

    @patch('domain.query.models.RedisChatMessageHistory', new_callable=AsyncMock)
    @patch('domain.query.models.create_retrieval_chain')
    @patch('domain.query.models.create_stuff_documents_chain')
    @patch('domain.query.models.create_history_aware_retriever')
    @patch.object(BaseConnector, 'get_connector')
    async def test_setting_rag_chain(self, mock_get_connector, mock_history_retriever, mock_documents_chain, mock_retrieval_chain, mock_redis_history):
        # Given
        mock_connector = mock_get_connector.return_value
        mock_retriever = MagicMock(VectorStoreRetriever)
        query_input = MagicMock(QueryInput)
        key = "test_key"
        query = Query(query_input, mock_connector, key, mock_retriever)

        # When
        query.setting_rag_chain()

        # Then
        mock_history_retriever.assert_called_once_with(mock_connector, mock_retriever, ChatPrompt.get_contextualize_q_prompt())
        mock_documents_chain.assert_called_once_with(mock_connector, ChatPrompt.get_qa_prompt())
        mock_retrieval_chain.assert_called_once_with(mock_history_retriever.return_value, mock_documents_chain.return_value)
        assert query.rag_history_chain is not None

    @patch('domain.query.models.RunnableWithMessageHistory.ainvoke', new_callable=AsyncMock)
    async def test_get_result_success(self, mock_ainvoke):
        # Given
        mock_ainvoke.return_value = {'answer': "expected_answer"}
        query_input = MagicMock(QueryInput)
        query_input.get_input.return_value = "query_input"
        query = Query(query_input, MagicMock(), "test_key", MagicMock())
        query.rag_history_chain = MagicMock()

        # When
        result = await query.get_result()

        # Then
        query.rag_history_chain.ainvoke.assert_awaited_once_with(
            {ChatPrompt.INPUT_MESSAGE_KEY: "query_input"},
            config={"configurable": {"session_id": "test_key"}}
        )
        assert result == "expected_answer"

    @patch('domain.query.models.RunnableWithMessageHistory.ainvoke', new_callable=AsyncMock)
    async def test_get_result_failure(self, mock_ainvoke):
        # Given
        mock_ainvoke.return_value = None
        query_input = MagicMock(QueryInput)
        query = Query(query_input, MagicMock(), "test_key", MagicMock())
        query.rag_history_chain = MagicMock()

        # When / Then
        with pytest.raises(ConnectionError):
            await query.get_result()

    async def test_get_result_without_setting_rag_chain(self):
        # Given
        query_input = MagicMock(QueryInput)
        query = Query(query_input, MagicMock(), "test_key", MagicMock())

        # When / Then
        with pytest.raises(ConnectionError):
            await query.get_result()
