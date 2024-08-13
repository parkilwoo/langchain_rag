from sentence_transformers import SentenceTransformer
import threading
import logging

class SingletonMeta(type):
    _instances = {}
    _lock: threading.Lock = threading.Lock()    

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class EmbeddingModel(metaclass=SingletonMeta):
    _model = None
    _encode_lock = threading.Lock()

    def __init__(self, input: str) -> None:
        self.input = input

    @classmethod
    def load_model(cls, model_name: str):
        logging.info("Loading Model :: %s", model_name)
        cls._model = SentenceTransformer(model_name)
        logging.info("Model Loaded Successfully")
    
    def thread_safe_encode(self):
        with self._encode_lock:
            return self._model.encode(self.input)