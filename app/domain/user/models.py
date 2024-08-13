import base64
from core.security import SecurityConfig

class AccessToken:
    __seperator = ":"
        
    @classmethod
    def generate(cls, api_key:str, model_name: str) -> str:
        plain = f"{api_key}{cls.__seperator}{model_name}".encode("utf-8")
        encrypt_data = SecurityConfig.get_cipher().encrypt(plain)
        return base64.urlsafe_b64encode(encrypt_data).decode()
    
    @classmethod
    def decrypt(cls, token: str):
        encrypt_data = base64.urlsafe_b64decode(token.encode("utf-8"))
        plain = SecurityConfig.get_cipher().decrypt(encrypt_data).decode()
        
        return plain.split(cls.__seperator)