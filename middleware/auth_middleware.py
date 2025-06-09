from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from models.user import User

def login_required(f):
    """Decorator untuk mengharuskan user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Jika request adalah AJAX, return JSON response
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({
                    'success': False,
                    'message': 'Authentication required',
                    'redirect': url_for('auth.login')
                }), 401
            
            # Jika request biasa, redirect ke login
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def guest_only(f):
    """Decorator untuk mengharuskan user belum login (guest)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('dashboard'))  # Sesuaikan dengan route dashboard Anda
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current logged in user"""
    if 'user_id' in session:
        return User.get_by_id(session['user_id'])
    return None

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

class AuthContext:
    """Context processor untuk template"""
    
    @staticmethod
    def inject_auth_context():
        return {
            'current_user': get_current_user(),
            'is_authenticated': is_authenticated()
        }