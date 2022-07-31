from flask_socketio import SocketIO, emit
from types import BuiltinFunctionType, FunctionType, MethodType

# A replacement to Flow, made with SocketIO instead of normal HTTP

class Nebula:
    def __init__(self, shared) -> None:
        self.socket = SocketIO(shared.app)
        self._flow = shared.flow

        @self.socket.on("resource")
        def get_data(data):
            package = {}
            for i in data:
                package[i] = (self.find(i))

            return {"data": package}

    def find(self, element):
        current = self._flow
        for i in element.split("."):
            if i in current:
                current = current[i]
            else:
                current = {}

        func = [BuiltinFunctionType, MethodType, FunctionType]

        if current == {}:
            current = None
        elif type(current) == dict:
            current = None
        elif type(current) in func:
            current = current()
        
        return current