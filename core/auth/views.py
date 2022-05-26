import uuid
import secrets

from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db, utils

from . import auth
from . import utils as auth_utils
from .models import User, UserPrivilege
from .decorators import target_user_required, token_required


            
@auth.route('/logout', methods=['POST'])
@token_required
def logout(token, current_user):
# def logout():
    return utils.response()
    
    

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
            msg = 'missing required parameter {}'.format(tag)
            return utils.response(msg, status_code=400)

    # generate password hash using sha256 algorithm
    password_hash = generate_password_hash(data['password'], method='sha256')

    # Check if  username has already been used.
    existing_user = User.query.filter_by(username=data['username']).first()      
    if existing_user:
        msg = 'username {} is already taken'.format(data['username'])
        return utils.response(msg, status_code=409)
    
    # Check if email has already been used.
    existing_user =  User.query.filter_by(email=data['email']).first()
    if existing_user:
        msg = 'email {} is already in use'.format(data['email'])
        return utils.response(msg, status_code=409)
    
    # Create the user
    new_user = User(
        public_id=str(uuid.uuid4()), password=password_hash,
        email=data['email'], username=data['username'], 
    )
        
    try:
        db.session.add(new_user)
        db.session.commit()
        return utils.response('registerd successfully', 201)
    except Exception as e:
        return utils.response('unknown database error', 500, error=str(e))







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
        return utils.response('could not verify', status_code=401, Authorization='login required')


    user = User.query.filter_by(username=data.username).first()
    if not user:
        msg = 'no such user {}'.format(data.username)
        return utils.response(msg, status_code=401)
        
    if not check_password_hash(user.password, data.password):#, algorithms='sha256'):
        return utils.response('incorrect password', status_code=401)
    
    # Create an access token for the user using their public_id.
    token_data = auth_utils.create_token_data(user.public_id)
    token = auth_utils.encode_token_data(token_data)
    
    # Return the token
    return auth_utils.response(token, 'login success', user=user.serialized)




@auth.route('/token/validate', methods=['POST'])
@token_required
def validate_token(token, current_user):
    return auth_utils.response(token, msg='success', status_code=200, isValid=True)






@auth.route('/users', methods=['GET'])
def get_all_users():
    """ Return a list of all users. VERY INSECURE! """
    users = User.query.all()
    results = [ user.serialized for user in users ]
    return utils.response(users=results)
            

@auth.route('/users/<username>', methods=['GET'])
@target_user_required
def get_user(username, target_user):
    """ Return the found user object. """
    return utils.response(user=target_user.serialized)
    
    
    



    
    
    

    
            
    
