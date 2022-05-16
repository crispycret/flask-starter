
from flask import Response, jsonify

from . import app


@app.route('/', methods=['GET'])
def test_response():
    response = Response(response={'test':'testing'}, status=201, )
    return response

@app.route('/204', methods=['GET'])
def test_204():
    response = Response({}, status=204)
    return response
    
    
    
@app.route('/test', methods=['GET'])
def test():
    return jsonify({}), 201


