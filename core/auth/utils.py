
from datetime import datetime
import jwt

from .. import utils, Configuration




def response(token, msg='success', status_code=200, **kwargs):
    return utils.response(msg, status_code, token=token, **kwargs)


def create_token_data(public_id):
    return {
        'public_id': public_id,
        'created': datetime.utcnow().isoformat(),
        'expires': utils.time.future(hours=1).isoformat(),
    }


def encode_token_data(token_data):
    """ Encode token data with the SECRET_KEY HS256 SHA256 """
    return jwt.encode(token_data, Configuration.SECRET_KEY, 'HS256')
    
    
def decode_token(token):
    """ Dencode token with the SECRET_KEY using HS256 """
    return jwt.decode(token, Configuration.SECRET_KEY, algorithms=['HS256'])
    
    
    
