from .. import db



class UserProfile (db.Model):
    """ Data extension of a User. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    bio = db.Column(db.String(255))
    
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
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

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
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

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
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

    
    
    
    
class UserFollow(db.Model):
    """ Tracks the action of one user following another user. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'target_id': self.target_id,

            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()            
        }


class UserBlock(db.Model):
    """ Tracks when a user blocks another user. """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)