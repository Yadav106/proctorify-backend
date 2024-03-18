class CustomException(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None, payload=None):
        super(CustomException, self).__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InternalError(CustomException):
    status_code = 500
