import msgpack
from celery import Celery
import logging
from inference.task_logger import LoggingTask
from inference.embedding_model import EmbeddingModel

app = Celery('inference', 
            broker='amqp://guest@localhost//',
            backend='rpc://')

@on_after_configure.connect
def load_model(sender, **kwargs):
    EmbeddingModel.load_model("all-MiniLM-L6-v2")

@task(name='embedding_inference', base=LoggingTask)
def embedding_inference(serialized_data):
    try:
        unpack_data: str = msgpack.unpackb(serialized_data)
        model = EmbeddingModel(unpack_data)
        inference_result = model.thread_safe_encode(unpack_data)
        packed_data = msgpack.packb(inference_result)
        return (200, {"status": "success", "data": packed_data})
    except Exception as exc:
        logging.exception(exc)
        return (500, {"status": "failed"})