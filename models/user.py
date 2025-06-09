from werkzeug.security import generate_password_hash, check_password_hash
from models.database_manager import DatabaseManager
from datetime import datetime

class User:
    def __init__(self, id=None, name=None, email=None, password=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at

    @staticmethod
    def create_user(name, email, password):
        """Create a new user"""
        try:
            db = DatabaseManager()
            connection = db.get_connection()
            cursor = connection.cursor()
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            query = """
                INSERT INTO users (name, email, password) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, email, hashed_password))
            connection.commit()
            
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            
            return User.get_by_id(user_id)
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        try:
            db = DatabaseManager()
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    created_at=user_data['created_at']
                )
            return None
            
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            db = DatabaseManager()
            connection = db.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    created_at=user_data['created_at']
                )
            return None
            
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<User {self.email}>"