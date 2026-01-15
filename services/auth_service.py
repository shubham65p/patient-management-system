import bcrypt
from data_validation_auth import User, UserLogin, UserInDB
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def register_user(self, user: User) -> dict:
        """Register a new user"""
        # Check if user already exists
        if self.user_repo.user_exists(user.username):
            return {
                'success': False,
                'message': 'Username already exists'
            }

        # Hash password
        password_hash = self.hash_password(user.password)

        # Add user to database
        user_id = self.user_repo.add(user, password_hash)

        if user_id:
            return {
                'success': True,
                'message': 'User registered successfully',
                'user_id': user_id
            }
        
        return {
            'success': False,
            'message': 'Failed to register user'
        }

    def login_user(self, login_data: UserLogin) -> dict:
        """Authenticate user login"""
        user = self.user_repo.get_by_username(login_data.username)

        if not user:
            return {
                'success': False,
                'message': 'Invalid username or password'
            }

        if not user['is_active']:
            return {
                'success': False,
                'message': 'User account is inactive'
            }

        if not self.verify_password(login_data.password, user['password_hash']):
            return {
                'success': False,
                'message': 'Invalid username or password'
            }

        return {
            'success': True,
            'message': 'Login successful',
            'user_id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'email': user['email']
        }

    def get_user(self, user_id: int) -> dict:
        """Get user information"""
        return self.user_repo.get_by_id(user_id)

    def update_user(self, user_id: int, user_data: dict) -> dict:
        """Update user information"""
        success = self.user_repo.update(user_id, user_data)
        return {
            'success': success,
            'message': 'User updated successfully' if success else 'Failed to update user'
        }

    def delete_user(self, user_id: int) -> dict:
        """Delete user"""
        success = self.user_repo.delete(user_id)
        return {
            'success': success,
            'message': 'User deleted successfully' if success else 'Failed to delete user'
        }
