from flask import request, jsonify, render_template, redirect, url_for, flash
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
            if request.is_json:
                # Handle JSON API request
                data = request.get_json()
                user_schema = UserSchema()
                user_data = user_schema.load(data)
            else:
                # Handle form submission
                user_data = {
                    'username': request.form.get('username'),
                    'email': request.form.get('email'),
                    'password': request.form.get('password')
                }
                # Simple validation for form data
                if not all(user_data.values()):
                    flash('All fields are required', 'error')
                    return render_template('register.html'), 400
            
            # Check if user already exists
            if User.query.filter_by(email=user_data['email']).first():
                if request.is_json:
                    return jsonify({'message': 'User already exists'}), 400
                flash('Email already registered', 'error')
                return render_template('register.html'), 400
            
            if User.query.filter_by(username=user_data['username']).first():
                if request.is_json:
                    return jsonify({'message': 'Username already taken'}), 400
                flash('Username already taken', 'error')
                return render_template('register.html'), 400
                
            # Create new user
            password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            new_user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=password_hash
            )
            
            # Add default role if it exists
            default_role = Role.query.filter_by(name='user').first()
            if default_role:
                new_user.roles.append(default_role)
            
            db.session.add(new_user)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'message': 'User registered successfully'}), 201
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except ValidationError as e:
            if request.is_json:
                return jsonify(e.messages), 400
            flash('Validation error', 'error')
            return render_template('register.html'), 400
        except Exception as e:
            if request.is_json:
                return jsonify({'message': str(e)}), 500
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


