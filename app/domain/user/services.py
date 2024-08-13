from infrastructure.connector.open_ai import OpenAiConnector
from domain.user.models import AccessToken

class UserService:
    _user_repository = None
    
    @classmethod
    async def generate_access_token(cls, api_key: str, model_name: str) -> str:
        """_summary_
        Access token 만드는 service
        Args:
            api_key (str): 입력받은 api key
            model_name (str): 입력받은 사용할 모델 name

        Returns:
            str: token값 
        """
        # 1. api_key와 model_name으로 connection test
        connector = OpenAiConnector(api_key, model_name)
        await connector.test_connection()
        
        # 2. Access Token 생성
        return AccessToken.generate(api_key, model_name)