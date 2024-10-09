
from flask import jsonify
from sqlalchemy import text
from app import db

class User():
    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        
    def __repr__(self):
        return '<User %r>' % self.username
    
    def __str__(self):
        return '<User %r>' % self.username
    
    def __eq__(self, other):
        return self.username == other.username
    
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
        if not self.username or not self.email or not self.password:
            return { 'message': 'missing data', 'status': 402 }
        
        if self.find_by_email():
            return { 'message': 'email already exists', 'status': 403 }
        
        query = text('INSERT INTO User (username, email, password) VALUES (:username, :email, :password)')
        db.session.execute(query, {'username': self.username, 'email': self.email, 'password': self.password})
        db.session.commit()
        
        result = { 'message': 'user created successfully', 'status': 201 }
        
        return result
