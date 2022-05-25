import uuid
import secrets
from datetime import datetime

from functools import wraps
from flask import request

from .. import utils
from . import auth, utils as auth_utils
from .models import User, UserPrivilege
          
        

def target_user_required(f):
    """ return a user in the field target_user by filtering a username or forward a response error to the api caller. """
    @wraps(f)
    def decorator(username, *args, **kwargs):
        target_user = auth.views.User.query.filter_by(username=username).first()
        if not target_user: 
            msg='username {} does not exists'.format(username)
            return utils.response(msg, status_code=404)
        
        return f(*args, target_user=target_user, username=username, **kwargs)
    return decorator


    



# Decorator function that require the request to include a valid a token
# Allow arguments to be passed but do not handle them.
def token_required(f):
    """ 
    Decorate views that require user authentication using this function.
    Checks headers for a valid access key and updates token when nearing expiration.
    returns:
        current_user -> User
        token -> String
        *args, **kwargs
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        if not token: 
            return utils.response('token is missing', status_code=401)
        

        try:
            # Decode the given token and find the current user.
            token_data = auth_utils.decode_token(token)
            expires_timestamp = utils.time.decode_timestamp(token_data['expires'])
            target_timestamp = utils.time.future(minutes=30)
            
            # Token has expired.
            if datetime.utcnow() > expires_timestamp:
                return utils.response('token has expired', status_code=401)
            
            # Token is expiring soon, create a new token and update the header
            if expires_timestamp > target_timestamp:
                token_data = auth_utils.create_token_data(token_data['public_id'])
                token = auth_utils.encode_token_data(token_data)

            # Find the user with the public id
            current_user = User.query.filter_by(public_id=token_data['public_id']).first()

        except Exception as e:
            return utils.response('token is invalid', status_code=401)
    
        return f(*args, token=token, current_user=current_user, **kwargs)
    return decorator
            
      
      
      
      
      
      