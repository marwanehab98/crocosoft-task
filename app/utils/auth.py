
from abc import ABC, abstractmethod
import stat

from flask_jwt_extended import create_access_token
from app import bcrypt, jwt
from app.models.user import User

class BaseAuthentication(ABC):
    @abstractmethod
    def register(self):
        pass
    
    def login(self):
        pass
    
class EmailPasswordAuthentication(BaseAuthentication):
    def __init__(self, user: User):
        self.user = user
        
    def register(self) -> dict:
        if not self.user.username or not self.user.email or not self.user.password:
            return { 'message': 'missing data', 'status': 402 }
        
        if self.user.find_by_email():
            return { 'message': 'email already exists', 'status': 403 }
        
        hashedPassword = bcrypt.generate_password_hash(self.user.password)
        self.user.password = hashedPassword
        self.user.create_user()
        
        result = { 'message': 'user created successfully', 'status': 201 }
        
        return result
        
    def login(self):
        user_from_db = self.user.find_by_email()
                
        if user_from_db is None:
            return { 'message': 'user does not exist', 'status': 404 }
        
        password_match = bcrypt.check_password_hash(user_from_db['password'], self.user.password)
        
        if password_match:
            access_token = create_access_token(identity=user_from_db['user_id'])
            return { 'access_token': access_token, 'status': 200 }
        else:
            return { 'message': 'invalid password', 'status': 401 }
        