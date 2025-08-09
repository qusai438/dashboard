from celery import Celery
import os

celery = Celery(__name__)

def init_celery(app=None):
    app = app or {}
    celery.conf.update(
        broker_url=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        timezone="UTC",
        enable_utc=True
    )

    if app and hasattr(app, "app_context"):
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

    return celery
