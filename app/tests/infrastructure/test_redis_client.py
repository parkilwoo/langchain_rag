import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from infrastructure.database import RedisClient, VectorRedisClient

@pytest.mark.asyncio
class TestRedisClient:

    @patch('infrastructure.database.aioredis.from_url', new_callable=AsyncMock)
    async def test_redis_client_initialization(self, mock_from_url):
        # Given
        url = "redis://localhost:6379"
        RedisClient._instance = None

        # When
        redis_instance = RedisClient(url)

        # Then
        mock_from_url.assert_called_once_with(url, encoding='utf-8', decode_responses=True)
        assert redis_instance == RedisClient._instance

    @patch('infrastructure.database.RedisClient._instance.get', new_callable=AsyncMock)
    async def test_redis_get(self, mock_get):
        # Given
        key = "test_key"
        mock_get.return_value = "test_value"
        
        # When
        result = await RedisClient.get(key)
        
        # Then
        mock_get.assert_awaited_once_with(key)
        assert result == "test_value"

    @patch('infrastructure.database.RedisClient._instance.set', new_callable=AsyncMock)
    async def test_redis_set(self, mock_set):
        # Given
        key = "test_key"
        value = "test_value"
        
        # When
        await RedisClient.set(key, value)
        
        # Then
        mock_set.assert_awaited_once_with(key, value, RedisClient._ttl)

@pytest.mark.asyncio
class TestVectorRedisClient:

    @patch('infrastructure.database.aioredis.from_url', new_callable=AsyncMock)
    async def test_vector_redis_client_initialization(self, mock_from_url):
        # Given
        url = "redis://localhost:6379"
        VectorRedisClient._instance = None

        # When
        redis_instance = VectorRedisClient(url)

        # Then
        mock_from_url.assert_called_once_with(url, encoding='utf-8', decode_responses=True)
        assert redis_instance == VectorRedisClient._instance

    @patch('infrastructure.database.VectorRedisClient._instance.execute_command', new_callable=AsyncMock)
    async def test_generate_index(self, mock_execute_command):
        # When
        await VectorRedisClient.generate_index()

        # Then
        mock_execute_command.assert_awaited_once_with(
            'FT.CREATE', VectorRedisClient._index_name,
            'ON', 'HASH', 
            'PREFIX', '1', 'question:', 
            'SCHEMA', 
            'embedding', 'VECTOR', 'FLAT', '6', 'TYPE', 'FLOAT32', 'DIM', '384', 'DISTANCE_METRIC', 'COSINE'
        )

    @patch('infrastructure.database.VectorRedisClient._instance.execute_command', new_callable=AsyncMock)
    async def test_vector_redis_get(self, mock_execute_command):
        # Given
        key = "test_key"
        mock_execute_command.return_value = ["result"]
        
        # When
        result = await VectorRedisClient.get(key)
        
        # Then
        mock_execute_command.assert_awaited_once()
        assert result == ["result"]

    @patch('infrastructure.database.VectorRedisClient._instance.hset', new_callable=AsyncMock)
    async def test_vector_redis_set(self, mock_hset):
        # Given
        key = "test_key"
        value = "test_value"
        
        # When
        await VectorRedisClient.set(key, value)
        
        # Then
        mock_hset.assert_awaited_once()
