
from app.models.post import Post


class PostService():
    def __init__(self, post: Post):
        self.post = post
        
    def get_post(self):
        response = self.post.find_by_id()
            
        if response is None:
            return { 'message': 'post does not exist', 'status': 404 }
        
        return { 'post': response, 'status': 200 }
    
    def create_post(self):
        if not self.post.content or not self.post.user_id:
            return { 'message': 'missing data', 'status': 402 }
        
        self.post.create_post()
        
        result = { 'message': 'post created successfully', 'status': 201 }
        
        return result
    
    def edit_post(self):
        if not self.post.post_id or not self.post.content:
            return { 'message': 'missing data', 'status': 402 }
        
        current_post = self.post.find_by_id()
        
        if current_post is None:
            return { 'message': 'post does not exist', 'status': 404 }
        
        if current_post['user_id'] != self.post.user_id:
            return { 'message': 'you do not have permission to edit this post', 'status': 403 }
        
        self.post.edit_post()
        
        result = { 'message': 'post edited successfully', 'status': 200 }
        
        return result
    
    def delete_post(self):
        if not self.post.post_id:
            return { 'message': 'missing data', 'status': 402 }
        
        current_post = self.post.find_by_id()
        
        if current_post is None:
            return { 'message': 'post does not exist', 'status': 404 }
        
        if current_post['user_id'] != self.post.user_id:
            return { 'message': 'you do not have permission to delete this post', 'status': 403 }
        
        self.post.delete_post()
        
        result = { 'message': 'post deleted successfully', 'status': 200 }
        
        return result