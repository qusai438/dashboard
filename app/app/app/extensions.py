from flask_mailman import Mail
from flask_caching import Cache
from flask_socketio import SocketIO

mail = Mail()
cache = Cache()
socketio = SocketIO(cors_allowed_origins="*")
