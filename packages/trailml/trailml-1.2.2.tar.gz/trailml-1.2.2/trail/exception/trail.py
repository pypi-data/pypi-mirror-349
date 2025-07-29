class TrailException(Exception):
    pass


class RemoteTrailException(TrailException):
    def __init__(self, msg: str):
        super().__init__(f"{msg} Please contact us if the problem persists.")


class TrailUnavailableException(RemoteTrailException):
    def __init__(self):
        super().__init__(
            "Apologies, trail is currently unavailable. We are working on the problem "
            "and will be up and running as soon as possible."
        )
