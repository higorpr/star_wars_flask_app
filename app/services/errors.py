# Exception class to pass exceptions from service to controllers
class CustomException(Exception):
    def __init__(self, message, statusCode):
        self.message = message
        self.statusCode = statusCode
        super().__init__(message)
