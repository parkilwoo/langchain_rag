import msgpack
from celery import Celery
import logging
from task_logger import LoggingTask
from embedding_model import EmbeddingModel

app = Celery('inference', 
            broker='amqp://iwpark:qkrdlfdn1!@localhost:5672//',
            backend='rpc://')

@app.on_after_configure.connect
def load_model(sender, **kwargs):
    EmbeddingModel.load_model("all-MiniLM-L6-v2")

@app.task(name='embedding_inference', base=LoggingTask)
def embedding_inference(serialized_data):
    try:
        unpack_data: str = msgpack.unpackb(serialized_data)
        model = EmbeddingModel(unpack_data)
        inference_result = model.thread_safe_encode()
        return (200, {"status": "success", "data": inference_result.tobytes()})
    except Exception as exc:
        logging.exception(exc)
        return (500, {"status": "failed"})