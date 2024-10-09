from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app
from flask import jsonify, request

from app.models.post import Post
    
@app.route('/post', methods=['POST'])
@jwt_required()
def post():
    try:
        body = request.get_json()
        content = body['content']
        user_id = get_jwt_identity()
        
        post = Post(user_id=user_id, content=content, post_id=None)
        response = post.create_post()
        
        return jsonify(response), response['status']
        
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 500

    
@app.route('/post/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def post_id(post_id):
    try:
        user_id = get_jwt_identity()
        
        if request.method == 'GET':
            post = Post(post_id=post_id, user_id=user_id, content=None)
            response = post.find_by_id()
            
            if response is None:
                return { 'message': 'post does not exist', 'status': 404 }, 404
            
            return jsonify(response), response['status']
        
        elif request.method == 'PUT':
            body = request.get_json()
            new_content = body['new_content']
            user_id = get_jwt_identity()
            
            post = Post(user_id=user_id, content=new_content, post_id=post_id)
            response = post.edit_post()
            
            return jsonify(response), response['status']
            
        elif request.method == 'DELETE':
            post = Post(user_id=user_id, post_id=post_id, content=None)
            response = post.delete_post()
            
            return jsonify(response), response['status']
            
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 500