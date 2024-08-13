from celery import Task
import logging

class LoggingTask(Task):
    def before_start(self, task_id, args, kwargs):
        logging.debug(f'Task {task_id} starting with args: {args} and kwargs: {kwargs}')
        super().before_start(task_id, args, kwargs)
        
    def on_success(self, retval, task_id, args, kwargs):
        logging.info(f'Task {task_id} succeeded with result: {retval}')
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f'Task {task_id} failed: {exc}')
        super().on_failure(exc, task_id, args, kwargs, einfo)