import queue
from typing import Optional
from app import db
from sqlalchemy import text

from app.models import user

class Post():
    def __init__(self, user_id: int, post_id: Optional[int] = None, content: Optional[str] = None):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
    
    def __repr__(self):
        return '<Post %r>' % self.content
    
    def __str__(self):
        return '<Post %r>' % self.content
    
    def __eq__(self, other):
        return self.post_id == other.post_id
    
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
        query = text('INSERT INTO Post (user_id, content) VALUES (:user_id, :content)')
        db.session.execute(query, {'user_id': self.user_id, 'content': self.content})
        db.session.commit()
    
    def edit_post(self):
        query = text('UPDATE Post SET content = :new_content, updated_at = CURRENT_TIMESTAMP WHERE post_id = :post_id AND user_id = :user_id')
        db.session.execute(query, {'new_content': self.content, 'post_id': self.post_id, 'user_id': self.user_id})
        db.session.commit()
    
    def delete_post(self):      
        query = text('UPDATE Post SET deleted_at = CURRENT_TIMESTAMP WHERE post_id = :post_id AND user_id = :user_id')
        db.session.execute(query, {'post_id': self.post_id, 'user_id': self.user_id})
        db.session.commit()