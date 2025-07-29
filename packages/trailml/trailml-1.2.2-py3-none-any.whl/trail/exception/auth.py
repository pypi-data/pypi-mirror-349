from trail.exception.trail import TrailException


class InvalidCredentialsException(TrailException):
    def __init__(self, msg: str = "Invalid credentials."):
        super().__init__(msg)
