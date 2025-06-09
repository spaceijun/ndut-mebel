from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models.user import User
from validators.auth_validator import AuthValidator
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Check if user is already logged in
        if 'user_id' in session:
            return redirect(url_for('dashboard'))  # Sesuaikan dengan route dashboard Anda
        return render_template('login.html')
    
    elif request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            remember_me = request.form.get('rememberMe') == 'on'
            
            # Validate input
            validation_result = AuthValidator.validate_login(email, password)
            if not validation_result['valid']:
                return jsonify({
                    'success': False,
                    'message': validation_result['message']
                }), 400
            
            # Check user credentials
            user = User.get_by_email(email)
            if not user or not user.check_password(password):
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                }), 401
            
            # Set session
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            
            # Set session permanent if remember me is checked
            if remember_me:
                session.permanent = True
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict()
            })
            
        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({
                'success': False,
                'message': 'An error occurred during login'
            }), 500

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Check if user is already logged in
        if 'user_id' in session:
            return redirect(url_for('dashboard'))  # Sesuaikan dengan route dashboard Anda
        return render_template('register.html')
    
    elif request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            # Validate input
            validation_result = AuthValidator.validate_register(name, email, password)
            if not validation_result['valid']:
                return jsonify({
                    'success': False,
                    'message': validation_result['message']
                }), 400
            
            # Check if user already exists
            existing_user = User.get_by_email(email)
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already registered'
                }), 409
            
            # Create new user
            user = User.create_user(name, email, password)
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Failed to create user account'
                }), 500
            
            # Auto login after registration
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user': user.to_dict()
            })
            
        except Exception as e:
            print(f"Registration error: {e}")
            return jsonify({
                'success': False,
                'message': 'An error occurred during registration'
            }), 500

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    })