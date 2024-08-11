from abc import ABC, abstractmethod

class BaseConnector(ABC):
    
    @abstractmethod
    def _valide_model(self, model_name: str) -> None:
        """_summary_
        Valide model name
        Args:
            model_name (str): _description_
        """
    
    @abstractmethod
    def test_connection(self) -> bool:
        """_summary_
        Test API Connection
        Returns:
            bool: _description_
        """