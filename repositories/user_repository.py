from data_validation_auth import User, UserInDB
from database.db_protocol import Database


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, user: User, password_hash: str) -> int:
        """Add a new user to the database"""
        query = """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (user.username, user.email, password_hash, user.role, user.is_active)
        self.db.execute(query, params)
        self.db.commit()
        
        # Get the inserted user ID
        result = self.db.execute(
            "SELECT id FROM users WHERE username = ?",
            (user.username,)
        ).fetchone()
        return result[0] if result else None

    def get_by_username(self, username: str) -> dict:
        """Get user by username"""
        query = "SELECT id, username, email, password_hash, role, is_active FROM users WHERE username = ?"
        result = self.db.execute(query, (username,)).fetchone()
        
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'password_hash': result[3],
                'role': result[4],
                'is_active': result[5]
            }
        return None

    def get_by_id(self, user_id: int) -> dict:
        """Get user by ID"""
        query = "SELECT id, username, email, role, is_active FROM users WHERE id = ?"
        result = self.db.execute(query, (user_id,)).fetchone()
        
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'role': result[3],
                'is_active': result[4]
            }
        return None

    def get_all(self):
        """Get all users"""
        query = "SELECT id, username, email, role, is_active FROM users"
        results = self.db.execute(query).fetchall()
        users = []
        for result in results:
            users.append({
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'role': result[3],
                'is_active': result[4]
            })
        return users

    def update(self, user_id: int, user_data: dict) -> bool:
        """Update user information"""
        allowed_fields = ['email', 'role', 'is_active']
        updates = {k: v for k, v in user_data.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        self.db.execute(query, values)
        self.db.commit()
        return True

    def delete(self, user_id: int) -> bool:
        """Delete user"""
        query = "DELETE FROM users WHERE id = ?"
        self.db.execute(query, (user_id,))
        self.db.commit()
        return True

    def user_exists(self, username: str) -> bool:
        """Check if username exists"""
        query = "SELECT id FROM users WHERE username = ?"
        result = self.db.execute(query, (username,)).fetchone()
        return result is not None
