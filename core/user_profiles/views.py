from datetime import datetime
from flask import request

from .. import db, auth, utils
from ..auth.models import User

from . import user_profiles
from .models import UserProfile, UserFollow, UserBlock, \
                    UserSocialLinks, UserSocialLinkOther

                  
from .decorators import current_user_blocking_target_user_required, \
                        current_user_not_blocking_target_user_required, \
                        current_user_following_target_user_required, \
                        current_user_not_following_target_user_required




@user_profiles.route('/users/<username>/profile/create', methods=['POST'])
@auth.decorators.target_user_required
def create_user_profile(target_user, username):
    profile = UserProfile.query.filter_by(user_id=target_user.id).first()
    if (profile):
        return utils.response(msg='profile already exists for user', status_code=409)
    
    now = datetime.utcnow()
    profile = UserProfile(user_id=target_user.id, bio="", created=now, updated=now)

    try:
        db.session.add(profile)
        db.session.commit()
        return utils.response(msg='user profile created', status_code=201, profile=profile.serialized)
    except Exception as e:
        return utils.response(msg='unknown error', status_code=500, error=str(e))
    




@user_profiles.route('/users/<username>/profile', methods=['GET'])
@auth.decorators.target_user_required
def get_user_profile(target_user, username):
    """ Return user information from multiple tables. """
    profile = UserProfile.query.filter_by(user_id=target_user.id).first()
    followers = UserFollow.query.filter_by(target_id=target_user.id)
    following = UserFollow.query.filter_by(user_id=target_user.id)
    social = UserSocialLinks.query.filter_by(user_id=target_user.id).first()
    more_social = UserSocialLinkOther.query.filter_by(user_id=target_user.id)
    
    
    results = {
        'profile': profile.serialized if profile else None,
        'followers': [follower.serialized for follower in followers] if followers else None,
        'following': [follow.serialized for follow in following] if following else None,
    }
    for key, value in profile.serialized.items():
        results[key] = value
        
    return utils.response(**results)





@user_profiles.route('/users/<username>/follow', methods=['POST', 'DELETE'])
@auth.decorators.token_required
@auth.decorators.target_user_required
def follow_user(token, current_user, target_user, username):

    """ Follow or unfollow the target user from the current. """
    # Follow the user only if not already following
    if (request.method == 'POST'):
        if UserFollow.query.filter_by(user_id=current_user.id, target_id=target_user.id).first():
            msg = "user '{}' is already following '{}'".format(current_user.username, target_user.username)
            return auth.utils.response(token, msg, status_code=409)
            
        follow = UserFollow(user_id=current_user.id, target_id=target_user.id, created=datetime.utcnow(), updated=datetime.utcnow())
        db.session.add(follow)
        db.session.commit()
        msg = "user '{}' is now following '{}'".format(current_user.username, target_user.username)
        return auth.utils.response(token, msg, 201)
        
    # Unfollow the user
    elif request.method == 'DELETE':
        follow = UserFollow.query.filter_by(user_id=current_user.id, target_id=target_user.id).first()
        if not follow:
            msg = "user '{}' was not following '{}'".format(current_user.username, target_user.username)
            return auth.utils.response(token, msg, 409)

        db.session.delete(follow)
        db.session.commit()

        msg = "user '{}' is no longer following '{}'".format(current_user.username, target_user.username)
        return auth.utils.response(token, msg, 201)
    msg = 'Unexpected Error - unwanted reach of function folower_user().'
    return auth.utils.response (token, msg, 500)
    
    
    

# @target_lookup
@user_profiles.route('/users/<username>/block', methods=['POST', 'DELETE'])
@auth.decorators.token_required
@auth.decorators.target_user_required
def block_user(token, current_user, target_user, username):
    """ Create a Block relationship between the current_user and the target_user. """

    block = UserBlock.query.filter_by(user_id=current_user.id, target_id=target_user.id).first()
    
    # Create a block relationship if one does not exists.
    if request.method == 'POST':
        if block:
            msg = 'user {} has already blocked user {}'.format(current_user.username, target_user.username)
            return auth.utils.response(token, msg, 409)
        
        block = UserBlock(user_id=current_user.id, target_id=target_user.id, created=datetime.utcnow(), updated=datetime.utcnow())
        db.session.add(block)
        db.session.commit()

        msg = "user {} has successfully blocked user {}".format(current_user.username, target_user.username)
        return auth.utils.response(token, msg, 201)
    
    # Destroy the block relationship between current_user and target_user
    elif request.method == 'DELETE':
        if not block:
            msg = 'user {} was not blocking user {}'.format(current_user.username, target_user.username)
            return auth.utils.response(token, msg, 409)

        db.session.delete(block)
        db.session.commit()
        
        msg = 'user {} is no longer blocking user {}'.format(current_user.username, target_user.username)
        return auth.utils.response(token, msg, 201)
    
    
    
    


    
    