from flask import jsonify

def response(msg='success', status_code=200, **kwargs):
    return jsonify({'message': msg, **kwargs}), status_code