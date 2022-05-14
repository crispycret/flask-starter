import uuid
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from functools import wraps

from flask import make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from .models import future_time, \
    User, UserProfile, UserFollower, \
    UserSocialLinks, UserSocialLinkOther
    
from .. import db, Configuration






def refresh_expiring_token(token_data):
    """ Create a new token if the current token is near expiring. """
    # future_time = datetime.utcnow() + timedelta(minutes=30)
    
    # # Token is not expiring soon, return token data
    # if (token_data['expires'] > future_time):
    #     return token_data
    
    # token_data['']
    return
    
    

# Decorator function that require the request to include a valid a token
# Allow arguments to be passed but do not handle them.
def token_required(f):
    """ Decorate views that require user authentication using this function. """
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        if not token: 
            return jsonify ({'message': 'missing a valid token'})
        
        try:
            # Decode the given token and find the current user.
            token_data = jwt.decode(token, Configuration.SECRET_KEY, algorithms=['HS256'])
            
            print ('\n\n\n{}\n\n\n'.format(token_data))

            # Check to see if the token has expired
            if (datetime.fromisoformat(token_data['expires']) < datetime.utcnow()):
               return jsonify({'message': 'token has expired'})

            current_user = User.query.filter_by(public_id=token_data['public_id']).first()
                
        except Exception as e:
            print (e)
            return jsonify({'message': 'token is invalid'})
    
        return f(current_user, *args, **kwargs)
    return decorator
            
            
            
            
            


@auth.route('/register', methods=['POST'])
def sign_up():
    """
    Create a new user to store in the databased database
    
    Expected Request in json -> 
    {
        email: 'email@address.com'
        username, 'YourUserName', 
        password: 'YourPassword'
    } 
    """
    data = request.get_json()
    
    REQUIRED = ['username', 'email', 'password']
    for tag in REQUIRED:
        if tag not in data: 
            return jsonify({'message': 'missing required key {}'.format(tag)})

    # generate password hash using sha256 algorithm
    password_hash = generate_password_hash(data['password'], method='sha256')

    # Check if  username has been used.
    existing_user = User.query.filter_by(username=data['username']).first()      
    if existing_user:
        return jsonify({'message': 'username already used'})
    
    # Check if email has been used.
    existing_user =  User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'email already used'})
    
    # Create the user
    new_user = User(
        public_id=str(uuid.uuid4()), password=password_hash,
        email=data['email'], username=data['username'], 
    )
        
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify ({'message': 'registered successfully'})
    except Exception as e:
        return jsonify({'message':'unknown database error'})


@auth.route('/login', methods=['POST'])
def login_user():
    """
    Login the user and return an access token
    Expected Request in json ->
    {
        username: 'YourUserName', 
        password: 'YourPassword'
    }
    """
    data = request.authorization
    
    if not data or not data.username or not data.password: 
        return make_response('could not verify', 401, {'Authorization': 'login required'})


    user = User.query.filter_by(username=data.username).first()
    if not check_password_hash(user.password, data.password):#, algorithms='sha256'):
        return make_response('Could not verify', 401, {'Authorization': 'login requied'})
    
    
    # Create token object with the users public_id and the token expiration 
    token_data = {
        'public_id': user.public_id,
        'created': datetime.utcnow(),
        'expires': future_time(hours=1)
    }

    # Format datetime objects to strings
    token_data['created'] = token_data['created'].isoformat()
    token_data['expires'] = token_data['expires'].isoformat()
    
    # Encode the token with the SECRET_KEY using SHA256 
    token = jwt.encode(token_data, Configuration.SECRET_KEY, 'HS256')

    # Format string datetimes into datetime objects
    # token_data['created'] = datetime.fromisoformat(token_data['created'])
    # token_data['expires'] = datetime.fromisoformat(token_data['expires'])
    
    # Return to the token
    return jsonify({'token': token})





@auth.route('/users', methods=['GET'])
def get_all_users():
    """ Return a list of all users. VERY INSECURE! """
    users = User.query.all()
    results = [ user.serialized for user in users ]
    
    return jsonify({'users': results})
            


@auth.route('/users/<username>', methods=['GET'])
def get_user(username):
    """ Return user information from multiple tables. """
    user = User.query.filter_by(username=username).first()
    
    if not user: 
        return make_response('no such user', 404, {})
    
    profile = UserProfile.query.filter_by(user_id=user.id).first()
    followers = UserFollower.query.filter_by(target_id=user.id)
    following = UserFollower.query.filter_by(user_id=user.id)
    social = UserSocialLinks.query.filter_by(user_id=user.id)
    more_social = UserSocialLinkOther.query.filter_by(user_id=user.id)
    
    results = {
        'user': user.serialized if user else {},  
        'profile': profile.serialized if profile else {},
        'followers': [follower.serialized for follower in followers] if followers else [],
        'following': [follow.serialized for follow in following] if following else [],
    }
    return jsonify(results)
    




@auth.route('/users/<username>/follow', methods=['POST', 'DELETE'])
@token_required
def follow_user(current_user, username):

    # Cannot follow or unfollow a non exiting user
    target = User.query.filter_by(username=username).first()

    if not target: 
        return make_response('username {} does not exists'.format(username), 404, {})

    """ Follow or unfollow the target user from the current. """
    # Follow the user only if not already following
    if (request.method == 'POST'):
        if UserFollower.query.filter_by(user_id=current_user.id, target_id=target.id).first():
            output = "user '{}' is already following '{}'".format(current_user.username, target.username)
            return jsonify ({'message': output})
            
        follow = UserFollower(user_id=current_user.id, target_id=target.id, created=datetime.utcnow(), updated=datetime.utcnow())
        db.session.add(follow)
        db.session.commit()
        output = "user '{}' is now following '{}'".format(current_user.username, target.username)
        return jsonify ({'message': output})
        
    # Unfollow the user
    elif request.method == 'DELETE':
        follow = UserFollower.query.filter_by(user_id=current_user.id, target_id=target.id).first()
        if not follow:
            output = "user '{}' was not following '{}'".format(current_user.username, target.username)
            return make_response(output, 404, {})

        db.session.delete(follow)
        db.session.commit()

        output = "user '{}' is no longer following '{}'".format(current_user.username, target.username)
        return jsonify ({'message': output})
    
    return jsonify ({'message': 'Unexpected Error - unwanted reach of function folower_user().'})
    
    
    
    
    
    
    

    
            
    
