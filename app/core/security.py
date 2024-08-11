from cryptography.fernet import Fernet

class SecurityConfig:
    __secret_key = Fernet.generate_key()
    
    @classmethod
    def get_cipher(cls):
        return Fernet(cls.__secret_key)