
from functools import wraps


from .. import auth
from .. import utils

from .models import UserBlock, UserFollow




def current_user_blocking_target_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """ Require that the current user is blocking the target user"""
        try:
            block = UserBlock.query.filter_by(user_id=kwargs['current_user'].id, target_id=kwargs['target_user'].id).first()
            if not block:
                msg = "user {} is not blocking the user {}".format(kwargs['current_user'].username, kwargs['target_user'].username)
                return auth.utils.response(kwargs['token'], msg, 409)
            return f(*args, token=kwargs['token'], current_user=kwargs['current_user'], target_user=kwargs['target_user'], **kwargs)
        except:
            return utils.response('Unexpected error in user_blocked_required() decorator', 500)        
    return decorator



def current_user_not_blocking_target_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """ Require that the current user is not blocking the target user"""
        try:
            block = UserBlock.query.filter_by(user_id=kwargs['current_user'].id, target_id=kwargs['target_user'].id).first()
            if block:
                msg = "user {} is blocking the user {}".format(kwargs['current_user'].username, kwargs['target_user'].username)
                return auth.utils.response(kwargs['token'], msg, 409)
            return f(*args, token=kwargs['token'], current_user=kwargs['current_user'], target_user=kwargs['target_user'], **kwargs)
        except:
            return utils.response('Unexpected error in current_user_not_blocking_target_user_required() decorator', 500)        
    return decorator







def current_user_following_target_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """ Require that the current user is blocking the target user"""
        try:
            follow = UserFollow.query.filter_by(user_id=kwargs['current_user'].id, target_id=kwargs['target_user'].id).first()
            if not follow:
                msg = "user {} is not following the user {}".format(kwargs['current_user'].username, kwargs['target_user'].username)
                return auth.utils.response(kwargs['token'], msg, 409)
            return f(*args, token=kwargs['token'], current_user=kwargs['current_user'], target_user=kwargs['target_user'], **kwargs)
        except:
            return utils.response('Unexpected error in current_user_following_target_user_required() decorator', 500)        
    return decorator



def current_user_not_following_target_user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """ Require that the current user is not blocking the target user"""
        try:
            follow = UserFollow.query.filter_by(user_id=kwargs['current_user'].id, target_id=kwargs['target_user'].id).first()
            if follow:
                msg = "user {} is blocking the user {}".format(kwargs['current_user'].username, kwargs['target_user'].username)
                return auth.utils.response(kwargs['token'], msg, 409)
            return f(*args, token=kwargs['token'], current_user=kwargs['current_user'], target_user=kwargs['target_user'], **kwargs)
        except:
            return utils.response('Unexpected error in current_user_not_following_target_user_required() decorator', 500)        
    return decorator





