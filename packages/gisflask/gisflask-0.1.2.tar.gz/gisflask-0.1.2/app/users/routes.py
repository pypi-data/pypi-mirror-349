from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.users import users_bp
from app.extensions import db
from app.models import User
from app.utils import admin_required

@users_bp.route('/')
def index():
    """
    Users List Page
    ---
    tags:
      - Users
    responses:
      200:
        description: Users list page rendered
    """
    # Example code (commented out):
    # users = User.query.all()
    # return render_template('users/index.html', users=users)
    
    # Placeholder implementation:
    return render_template('users/index.html')

@users_bp.route('/<user_id>')
def view(user_id):
    """
    User Details Page
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: User UUID
    responses:
      200:
        description: User details page rendered
      404:
        description: User not found
    """
    # Example code (commented out):
    # user = User.query.get(user_id)
    # if not user:
    #     flash('User not found', 'error')
    #     return redirect(url_for('users.index'))
    # return render_template('users/view.html', user=user)
    
    # Placeholder implementation:
    return render_template('users/view.html', user_id=user_id)

@users_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """
    Create User Page
    ---
    tags:
      - Users
    responses:
      200:
        description: Create user form rendered
      201:
        description: User created successfully
      400:
        description: Invalid form data
    """
    # Example code (commented out):
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     
    #     if not all([username, email, password]):
    #         flash('All fields are required', 'error')
    #         return render_template('users/create.html'), 400
    #     
    #     # Check if user already exists
    #     if User.query.filter_by(username=username).first():
    #         flash('Username already taken', 'error')
    #         return render_template('users/create.html'), 400
    #     
    #     if User.query.filter_by(email=email).first():
    #         flash('Email already registered', 'error')
    #         return render_template('users/create.html'), 400
    #         
    #     # Create new user
    #     from app.extensions import bcrypt
    #     password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    #     new_user = User(
    #         username=username,
    #         email=email,
    #         password_hash=password_hash
    #     )
    #     
    #     # Add user role
    #     from app.models import Role
    #     user_role = Role.query.filter_by(name='user').first()
    #     if user_role:
    #         new_user.roles.append(user_role)
    #     
    #     db.session.add(new_user)
    #     db.session.commit()
    #     
    #     flash('User created successfully', 'success')
    #     return redirect(url_for('users.index')), 201
    
    # Placeholder implementation:
    return render_template('users/create.html')

@users_bp.route('/edit/<user_id>', methods=['GET', 'POST'])
@admin_required
def edit(user_id):
    """
    Edit User Page
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: User UUID
    responses:
      200:
        description: Edit user form rendered or user updated successfully
      404:
        description: User not found
      400:
        description: Invalid form data
    """
    # Example code (commented out):
    # user = User.query.get(user_id)
    # if not user:
    #     flash('User not found', 'error')
    #     return redirect(url_for('users.index')), 404
    # 
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     
    #     if not all([username, email]):
    #         flash('Username and email are required', 'error')
    #         return render_template('users/edit.html', user=user), 400
    #     
    #     # Check if username already exists for another user
    #     existing_user = User.query.filter_by(username=username).first()
    #     if existing_user and existing_user.id != user.id:
    #         flash('Username already taken', 'error')
    #         return render_template('users/edit.html', user=user), 400
    #     
    #     existing_email = User.query.filter_by(email=email).first()
    #     if existing_email and existing_email.id != user.id:
    #         flash('Email already registered to another user', 'error')
    #         return render_template('users/edit.html', user=user), 400
    #     
    #     # Update user data
    #     user.username = username
    #     user.email = email
    #     
    #     # Optional password update
    #     new_password = request.form.get('password')
    #     if new_password:
    #         from app.extensions import bcrypt
    #         user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    #     
    #     db.session.commit()
    #     flash('User updated successfully', 'success')
    #     return redirect(url_for('users.view', user_id=user.id))
    #     
    # return render_template('users/edit.html', user=user)
    
    # Placeholder implementation:
    return render_template('users/edit.html', user_id=user_id)

@users_bp.route('/delete/<user_id>', methods=['POST'])
@admin_required
def delete(user_id):
    """
    Delete User
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: User UUID
    responses:
      302:
        description: User deleted and redirected to users list
      404:
        description: User not found
    """
    # Example code (commented out):
    # user = User.query.get(user_id)
    # if not user:
    #     flash('User not found', 'error')
    #     return redirect(url_for('users.index')), 404
    # 
    # db.session.delete(user)
    # db.session.commit()
    # 
    # flash('User deleted successfully', 'success')
    # return redirect(url_for('users.index'))
    
    # Placeholder implementation:
    return redirect(url_for('users.index'))