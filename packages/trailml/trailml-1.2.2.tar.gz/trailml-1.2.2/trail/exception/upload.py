from trail.exception.trail import RemoteTrailException


class UploadError(RemoteTrailException):
    def __init__(self, filename: str):
        super().__init__(f"Error uploading file {filename}.")
