from enum import Enum

class ContextKey(Enum):
    pass

class Context:
    def __init__(self):
        self._context = {}
