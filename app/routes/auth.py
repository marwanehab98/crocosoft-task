from flask import jsonify, request
from app import app
from app.models.user import User
from app.utils import auth

@app.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        email = body['email']
        password = body['password']
        
        user = User(email=email, password=password)
        auth_service = auth.EmailPasswordAuthentication(user)
        response = auth_service.login()
        
        return jsonify(response), response['status']
    
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        email = body['email']
        password = body['password']
        username = body['username']
        
        user = User(username=username, password=password, email=email)
        auth_service = auth.EmailPasswordAuthentication(user)
        response = auth_service.register()
        
        return jsonify(response), response['status']
        
    except Exception as e:
        return jsonify({ 'message': str(e), 'status': 500 }), 400
        