from unittest import TestCase
from unittest.mock import patch, MagicMock
from infrastructure.celery_client import CeleryClient
import msgpack

class TestCeleryClient(TestCase):

    @patch('infrastructure.celery_client.Celery')
    def test_connect(self, MockCelery):
        # Given
        broker = "redis://localhost:6379/0"
        backend = "redis://localhost:6379/1"
        
        # When
        CeleryClient.connect(broker, backend)
        
        # Then
        MockCelery.assert_called_once_with(broker=broker, backend=backend)
    
    @patch('infrastructure.celery_client.CeleryClient._instance.send_task')
    @patch('infrastructure.celery_client.AsyncResult')
    def test_sync_send_task(self, MockAsyncResult, mock_send_task):
        # Given
        plain_data = {"data": "test"}
        serialized_data = msgpack.packb(plain_data)
        mock_task_result = MagicMock()
        mock_task_result.get.return_value = (200, {"data": b'numpy_bytes'})
        mock_send_task.return_value = mock_task_result
        MockAsyncResult.return_value = mock_task_result
        
        # When
        result = CeleryClient.sync_send_task(plain_data)
        
        # Then
        mock_send_task.assert_called_once_with('embedding_inference', args=(serialized_data,))
        MockAsyncResult.assert_called_once_with(mock_task_result.id, app=CeleryClient._instance)
        assert result == b'numpy_bytes'