from flask_mailman import Mail
from flask_caching import Cache
from flask_socketio import SocketIO
from .tasks import celery

mail = Mail()
cache = Cache(config={"CACHE_TYPE": "simple"})
socketio = SocketIO(async_mode="eventlet", cors_allowed_origins="*")
