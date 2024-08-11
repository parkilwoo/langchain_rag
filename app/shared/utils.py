import hashlib

class Utils:
    @staticmethod
    def generate_hash(self, **kwargs) -> str:
        """_summary_
        
        Returns:
            str: _description_
        """
        combined = ":".join(kwargs.values)
        return hashlib.sha256(combined.encode()).hexdigest()    