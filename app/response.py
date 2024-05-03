from flask import jsonify, make_response

def success(values, message):
    return make_response(
        jsonify({
            "status": {
                "code": 200,
                "message": message,
            },
            "data": values
        })
    ), 200

def error(message, code):
    return make_response(
        jsonify({
            "status": {
                "code": code,
                "message": message,
            },
        }), code
    )