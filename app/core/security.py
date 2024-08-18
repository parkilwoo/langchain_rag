from cryptography.fernet import Fernet

class SecurityConfig:
    _cihper = Fernet(Fernet.generate_key())
    
    @classmethod
    def get_cipher(cls):
        return cls._cihper