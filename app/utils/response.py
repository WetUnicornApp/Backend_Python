class Response:
    def __init__(self, message: str, success: bool, data=None):
        self.message = message
        self.success = success
        self.data = data
