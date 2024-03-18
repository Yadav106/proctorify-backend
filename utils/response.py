from flask import jsonify 


def set_response(data=None, error=None, status=200, headers=None):
    response = format_response(data=data, error=error, status=status)
    return jsonify(response), status

def format_response(data=None, error=None, status=200):
    if 200 <= status < 400:
        code = True
    else:
        code = False

    response = {
        'data': data,
        'success': code,
        'error': error,
    }

    return response
