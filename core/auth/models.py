import secrets
from datetime import datetime


from .. import db


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
    
    
    





