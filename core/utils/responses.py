from flask import jsonify


def auth_response(token, msg='success', status_code=200, data={}):
    return jsonify({'token': token, 'message': msg, 'data': data}), status_code

def response(msg='success', status_code=200, data={}):
    return jsonify({'message': msg, 'data': data}), status_code