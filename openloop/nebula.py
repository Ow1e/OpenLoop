from flask_socketio import SocketIO, emit, ConnectionRefusedError, disconnect
from flask_login import current_user
import functools
from types import BuiltinFunctionType, FunctionType, MethodType

# A replacement to Flow, made with SocketIO instead of normal HTTP

class Nebula:
    def __init__(self, shared) -> None:
        self.socket = SocketIO(shared.app)
        self._flow = shared.flow
        self._auth = shared.vault

        @self.socket.on("resource")
        @self.authenticated_only
        def get_data(data):
            package = {}
            for i in data:
                package[i] = (self.find(i))

            return {"data": package}

    def authenticated_only(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                emit("login_request", None)
                disconnect()
            else:
                return f(*args, **kwargs)
        return wrapped

    def find(self, element):
        current = self._flow
        for i in element.split("."):
            if i in current:
                current = current[i]
            else:
                current = {}

        if not element in self._flow.admin_only:
            current = self._flow.flow_transit(current)
        else:
            user = self.auth.auth.current_user()
            if user['admin']:
                pack = self.flow_transit(current)
                pack['authed'] = True
                current = pack
            else:
                current = {"value": None, "error": "Admin Only Object!", "user": user["username"]}
        
        return current["value"]