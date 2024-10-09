
from typing import Optional
from sqlalchemy import text
from app import db

class User():
    def __init__(self, email: str, password: str, user_id: Optional[int] = None, username: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        
    def __repr__(self):
        return '<User %r>' % self.username
    
    def __str__(self):
        return '<User %r>' % self.username
    
    def __eq__(self, other):
        return self.user_id == other.user_id
    
    def find_by_email(self):
        result = db.session.execute(text('SELECT * FROM User WHERE email = :email'), {'email': self.email})
        row = result.fetchone()
        column_names = result.keys()
        
        if row is None:
            return None
                
        user = dict(zip(column_names, row))

        return user
    

    
    def find_by_id(self):
        result = db.session.execute(text('SELECT * FROM User WHERE user_id = :user_id'), {'user_id': self.user_id})
        row = result.fetchone()
        column_names = result.keys()
        
        if row is None:
            return None
        
        user = dict(zip(column_names, row))

        return user
    
    def create_user(self):
        query = text('INSERT INTO User (username, email, password) VALUES (:username, :email, :password)')
        db.session.execute(query, {'username': self.username, 'email': self.email, 'password': self.password})
        db.session.commit()
