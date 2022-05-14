import secrets
from datetime import datetime, timezone, timedelta



from .. import app, db


def future_time(**kwargs):
    """ Adds datetime.now + timedelta(**kwargs) """
    now = datetime.utcnow()
    time = timedelta(**kwargs)
    return now + time




class User(db.Model):
    """ Simple User Model. """
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    admin = db.Column(db.Boolean, default=False)
    
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialized(self):
        return {
            'public_id': self.public_id,
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()
        }





class UserPrivilege (db.Model):
    """ User privileges extendability. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True) 
    privilege = db.Column(db.Integer, default=0, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'privilege': self.privilege,          
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()
        }
    
    
    



class UserProfile (db.Model):
    """ Data extension of a User. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    bio = db.Column(db.String(255))
    
    created = db.Column(db.DateTime,)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'bio': self.bio,
            
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()        }
    
    
    
class UserSocialLinks (db.Model):
    """ The following fields should be the username for the varying platforms. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    twitter = db.Column(db.String(128))
    instagram = db.Column(db.String(128))
    facebook = db.Column(db.String(128))

    created = db.Column(db.DateTime,)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'twitter': self.twitter,
            'instagram': self.instagram,
            'facebook': self.facebook,
            
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()
        }
    
    

class UserSocialLinkOther (db.Model):
    """ 
    For support of an additional social link require the host, path, and username for a complete link.
    Examples:
        {
            platform='stackoverflow.com',
            path='users/0000000',
            username='username',
            as_url() -> stackoverflow.com/users/1367160/crispycret
        },
        {
            platform='linkedin.com'
            path='in'
            username='firstnamelastname'
            as_url() -> linkedin.com/in/firstnamelastname
        }
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    platform = db.Column(db.String(128), primary_key=True)
    path = db.Column(db.String(128))
    username = db.Column(db.String(128))

    created = db.Column(db.DateTime,)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'platform': self.platform,
            'path': self.path,
            'username': self.username,

            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()            
        }

    
    
    
    
class UserFollower(db.Model):
    """ Tracks the action of one user following another user. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    created = db.Column(db.DateTime,)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'target_id': self.target_id,

            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()            
        }
