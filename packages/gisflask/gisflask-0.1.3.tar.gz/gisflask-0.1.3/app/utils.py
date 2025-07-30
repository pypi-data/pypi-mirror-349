from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User, Role, Permission

def has_permission(permission_name):
    """
    Decorator to check if the user has the required permission
    Usage: @has_permission('can_view_maps')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Verify JWT
            verify_jwt_in_request()
            
            # Get the current user
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({"msg": "User not found"}), 404
            
            # Check if user has the required permission through roles
            has_required_permission = any(
                permission.name == permission_name
                for role in user.roles
                for permission in role.permissions
            )
            
            if not has_required_permission:
                return jsonify({"msg": "Permission denied"}), 403
                
            return f(*args, **kwargs)
        return decorated
    return decorator

def admin_required(f):
    """
    Decorator to check if the user has admin role
    Usage: @admin_required
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Verify JWT
        verify_jwt_in_request()
        
        # Get the current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        # Check if user has admin role
        has_admin_role = any(role.name == 'admin' for role in user.roles)
        
        if not has_admin_role:
            return jsonify({"msg": "Admin privileges required"}), 403
            
        return f(*args, **kwargs)
    return decorated
