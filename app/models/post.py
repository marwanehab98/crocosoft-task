import queue
from app import db
from sqlalchemy import text

from app.models import user

class Post():
    def __init__(self, post_id, user_id: int, content):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
    
    def __repr__(self):
        return '<Post %r>' % self.content
    
    def __str__(self):
        return '<Post %r>' % self.content
    
    def __eq__(self, other):
        return self.content == other.content
    
    def find_by_id(self):
        query = text('SELECT * FROM Post WHERE post_id = :post_id AND deleted_at IS NULL')
        result = db.session.execute(query, {'post_id': self.post_id})
        row = result.fetchone()
        column_names = result.keys()
        
        if row is None:
            return None
                
        post = dict(zip(column_names, row))

        return post

    def create_post(self):
        if not self.content or not self.user_id:
            return { 'message': 'missing data', 'status': 402 }
        
        query = text('INSERT INTO Post (user_id, content) VALUES (:user_id, :content)')
        db.session.execute(query, {'user_id': self.user_id, 'content': self.content})
        db.session.commit()
        
        result = { 'message': 'post created successfully', 'status': 201 }
        
        return result
    
    def edit_post(self):
        if not self.post_id or not self.content:
            return { 'message': 'missing data', 'status': 402 }
        
        current_post = self.find_by_id()
        
        if current_post is None:
            return { 'message': 'post does not exist', 'status': 404 }
        
        if current_post['user_id'] != self.user_id:
            return { 'message': 'you do not have permission to edit this post', 'status': 403 }
                
        query = text('UPDATE Post SET content = :new_content, updated_at = CURRENT_TIMESTAMP WHERE post_id = :post_id AND user_id = :user_id')
        db.session.execute(query, {'new_content': self.content, 'post_id': self.post_id, 'user_id': self.user_id})
        db.session.commit()
        
        result = { 'message': 'post edited successfully', 'status': 200 }
        
        return result
    
    def delete_post(self):
        if not self.post_id:
            return { 'message': 'missing data', 'status': 402 }
        
        current_post = self.find_by_id()
        
        if current_post is None:
            return { 'message': 'post does not exist', 'status': 404 }
        
        if current_post['user_id'] != self.user_id:
            return { 'message': 'you do not have permission to delete this post', 'status': 403 }
        
        query = text('UPDATE Post SET deleted_at = CURRENT_TIMESTAMP WHERE post_id = :post_id AND user_id = :user_id')
        db.session.execute(query, {'post_id': self.post_id, 'user_id': self.user_id})
        db.session.commit()
        
        result = { 'message': 'post deleted successfully', 'status': 200 }
        
        return result