import unittest
from unittest.mock import patch, AsyncMock
from core.exception_handler import CustomException
from domain.user.models import AccessToken
from domain.user.services import UserService
import base64

class TestAccessToken(unittest.TestCase):

    @patch('core.security.SecurityConfig.get_cipher')
    def test_generate_access_token(self, mock_get_cipher):
        # Given
        mock_cipher = mock_get_cipher.return_value
        mock_cipher.encrypt.return_value = b'encrypted_data'
        api_key = "test_api_key"
        model_name = "test_model"

        # When
        token = AccessToken.generate(api_key, model_name)

        # Then
        self.assertEqual(token, base64.urlsafe_b64encode(b'encrypted_data').decode())

    @patch('core.security.SecurityConfig.get_cipher')
    def test_decrypt_access_token(self, mock_get_cipher):
        # Given
        mock_cipher = mock_get_cipher.return_value
        mock_cipher.decrypt.return_value = "test_api_key:test_model".encode()
        token = base64.urlsafe_b64encode(b'encrypted_data').decode()

        # When
        result = AccessToken.decrypt(token)

        # Then
        self.assertEqual(result, ["test_api_key", "test_model"])

    @patch('core.security.SecurityConfig.get_cipher')
    @patch('core.custom_logger.logger')
    def test_decrypt_access_token_invalid(self, mock_logger, mock_get_cipher):
        # Given
        mock_cipher = mock_get_cipher.return_value
        mock_cipher.decrypt.side_effect = Exception("Decryption error")
        token = "invalid_token"

        # When / Then
        with self.assertRaises(CustomException):
            AccessToken.decrypt(token)
        mock_logger.exception.assert_called_once()

class TestUserService(unittest.TestCase):

    @patch('infrastructure.connector.open_ai.OpenAiConnector')
    @patch('domain.user.models.AccessToken.generate')
    async def test_generate_access_token(self, mock_generate_token, mock_connector):
        # Given
        mock_connector().test_connection = AsyncMock()
        mock_generate_token.return_value = "generated_token"

        # When
        token = await UserService.generate_access_token("api_key", "model_name")

        # Then
        mock_connector.assert_called_once_with("api_key", "model_name")
        mock_connector().test_connection.assert_awaited_once()
        mock_generate_token.assert_called_once_with("api_key", "model_name")
        self.assertEqual(token, "generated_token")

