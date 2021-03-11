class Route:
    def __init__(self, method: str, path: str, handler, name: str, description: str = ''):
        self.method = method
        self.path = path
        self.handler = handler
        self.name = name
        self.description = description
