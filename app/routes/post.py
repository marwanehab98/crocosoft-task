from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app
from flask import jsonify, request

from app.models.post import Post
from app.utils.post import PostService
    
@app.route('/post', methods=['POST'])
@jwt_required()
def post():
    try:
        body = request.get_json()
        content = body['content']
        user_id = get_jwt_identity()
        
        post = Post(user_id=user_id, content=content)
        post_service = PostService(post=post)
        response = post_service.create_post()
        
        return jsonify(response), response['status']
        
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 500

    
@app.route('/post/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def post_id(post_id):
    try:
        user_id = get_jwt_identity()
        
        if request.method == 'GET':
            post = Post(post_id=post_id, user_id=user_id)
            post_service = PostService(post=post)
            response = post_service.get_post()
            
            return jsonify(response), response['status'], 
        
        elif request.method == 'PUT':
            body = request.get_json()
            new_content = body['new_content']
            user_id = get_jwt_identity()
            
            post = Post(user_id=user_id, content=new_content, post_id=post_id)
            post_service = PostService(post=post)
            response = post_service.edit_post()
            
            return jsonify(response), response['status']
            
        elif request.method == 'DELETE':
            post = Post(user_id=user_id, post_id=post_id)
            post_service = PostService(post=post)
            response = post_service.delete_post()
            
            return jsonify(response), response['status']
            
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 500