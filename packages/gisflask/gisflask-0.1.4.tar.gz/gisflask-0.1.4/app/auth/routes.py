from flask import request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.auth import auth_bp
from app.extensions import bcrypt, db
from app.models import User, Role
from app.auth.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
import uuid
import logging

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User successfully registered
      400:
        description: Bad request
    """
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = {
                    'username': request.form.get('username'),
                    'email': request.form.get('email'),
                    'password': request.form.get('password')
                }
            
            current_app.logger.info(f"Registration data: {data}")  # Log the incoming data
            
            # Validate data
            if not data or not all(k in data for k in ['username', 'email', 'password']):
                if request.is_json:
                    return jsonify({'message': 'Missing required fields'}), 400
                flash('All fields are required', 'error')
                return render_template('register.html'), 400
            
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                if request.is_json:
                    return jsonify({'message': 'Email already registered'}), 400
                flash('Email already registered', 'error')
                return render_template('register.html'), 400
            
            # Create new user
            new_user = User(
                username=data['username'],
                email=data['email'],
                password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8')
            )
            db.session.add(new_user)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'message': 'User registered successfully'}), 201
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            current_app.logger.error(f"Registration error: {str(e)}")  # Log the error
            if request.is_json:
                return jsonify({'message': 'An error occurred during registration'}), 500
            flash('An error occurred during registration', 'error')
            return render_template('register.html'), 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        try:
            if request.is_json:
                # Handle JSON API request
                data = request.get_json()
                login_schema = LoginSchema()
                login_data = login_schema.load(data)
            else:
                # Handle form submission
                login_data = {
                    'username': request.form.get('username'),
                    'password': request.form.get('password')
                }
                # Simple validation for form data
                if not all(login_data.values()):
                    flash('All fields are required', 'error')
                    return render_template('login.html'), 400
            
            # Find user by username
            user = User.query.filter_by(username=login_data['username']).first()
            if not user or not bcrypt.check_password_hash(user.password_hash, login_data['password']):
                if request.is_json:
                    return jsonify({'message': 'Invalid credentials'}), 401
                flash('Invalid username or password', 'error')
                return render_template('login.html'), 401
            
            # Generate tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            if request.is_json:
                return jsonify({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }), 200
            
            # For form-based login, store token in session and redirect
            flash('Login successful', 'success')
            return redirect(url_for('main.index'))
            
        except ValidationError as e:
            if request.is_json:
                return jsonify(e.messages), 400
            flash('Validation error', 'error')
            return render_template('login.html'), 400
        except Exception as e:
            if request.is_json:
                return jsonify({'message': str(e)}), 500
            flash('An error occurred during login', 'error')
            return render_template('login.html'), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh Access Token
    ---
    tags:
      - Authentication
    security:
      - JWT: []
    responses:
      200:
        description: New access token generated
      401:
        description: Invalid token
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected Route Example
    ---
    tags:
      - Authentication
    security:
      - JWT: []
    responses:
      200:
        description: Access granted
      401:
        description: Missing or invalid token
    """
    current_user_id = get_jwt_identity()
    try:
        user_id = uuid.UUID(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        return jsonify({'logged_in_as': user.username}), 200
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400


