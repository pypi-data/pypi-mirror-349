from app.extensions import db
from app.models import User, Role, Permission

def create_default_roles():
    """Create default roles if they don't exist"""
    roles = {
        'admin': 'Administrator with full access',
        'user': 'Regular user with limited access',
        'moderator': 'User with moderation privileges'
    }
    
    for role_name, description in roles.items():
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name, description=description)
            db.session.add(role)
    
    db.session.commit()

def create_default_permissions():
    """Create default permissions if they don't exist"""
    permissions = {
        'create_map': 'Create new maps',
        'edit_map': 'Edit existing maps',
        'delete_map': 'Delete maps',
        'view_map': 'View maps',
        'admin_access': 'Full administrative access'
    }
    
    for perm_name, description in permissions.items():
        if not Permission.query.filter_by(name=perm_name).first():
            permission = Permission(name=perm_name, description=description)
            db.session.add(permission)
    
    db.session.commit()

def assign_default_permissions():
    """Assign default permissions to roles"""
    # Get roles
    admin_role = Role.query.filter_by(name='admin').first()
    user_role = Role.query.filter_by(name='user').first()
    moderator_role = Role.query.filter_by(name='moderator').first()
    
    # Get permissions
    create_map = Permission.query.filter_by(name='create_map').first()
    edit_map = Permission.query.filter_by(name='edit_map').first()
    delete_map = Permission.query.filter_by(name='delete_map').first()
    view_map = Permission.query.filter_by(name='view_map').first()
    admin_access = Permission.query.filter_by(name='admin_access').first()
    
    # Assign permissions to admin role
    if admin_role and not admin_role.permissions:
        for permission in [create_map, edit_map, delete_map, view_map, admin_access]:
            if permission and permission not in admin_role.permissions:
                admin_role.permissions.append(permission)
    
    # Assign permissions to user role
    if user_role and not user_role.permissions:
        if view_map and view_map not in user_role.permissions:
            user_role.permissions.append(view_map)
    
    # Assign permissions to moderator role
    if moderator_role and not moderator_role.permissions:
        for permission in [create_map, edit_map, view_map]:
            if permission and permission not in moderator_role.permissions:
                moderator_role.permissions.append(permission)
    
    db.session.commit()

def create_admin_user(username, email, password):
    """Create an admin user if doesn't exist"""
    if not User.query.filter_by(username=username).first():
        from app.extensions import bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            admin_user.roles.append(admin_role)
            
        db.session.add(admin_user)
        db.session.commit()
