from utils.response import set_response
from flask import current_app as app

def handle_invalid_usage(error):
    app.logger.info(error)
    return set_response(error=error.to_dict(), status=error.status_code)
