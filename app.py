from flask import Flask, jsonify, request
import traceback

app = Flask(__name__, static_url_path='', static_folder='.')


@app.errorhandler(404)
def not_found(error=None):
    """
        404 handler
    """
    message = {
        'status': 404,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res


@app.errorhandler(403)
def forbidden(error=None):
    """
        403 handler
    """
    message = {
        'status': 403,
        'message': 'Forbidden',
    }
    res = jsonify(message)
    res.status_code = 403
    return res


@app.errorhandler(500)
def internal_server_error(error=None):
    """
        500 handler
    """
    message = {
        'status': 500,
        'message': 'Failed to process request',
    }
    res = jsonify(message)
    res.status_code = 500
    traceback.print_exc()
    return res

@app.errorhandler(505)
def firebase_error(error=None):
    """
        505 handler
    """
    message = {
        'status': 505,
        'message': 'Firebase Error',
        "reason": error
    }
    res = jsonify(message)
    res.status_code = 505
    traceback.print_exc()
    return res


@app.after_request
def after_request_func(response):
    """
        CORS Section
    """
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


# Add your API endpoints here
from routes import users
from routes import mentors
from routes import mentees
from routes import admin

@app.route('/')
def homeRoute():
    try:
        res = "<h1 style='position: fixed; top: 50%;  left: 50%; transform: translate(-50%, -50%);'>Syndeo API</h1>"
        return res

    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(debug=True)
