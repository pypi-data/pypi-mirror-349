import argparse
import os
import sys
import click
from flask.cli import with_appcontext
from app import create_app
from app.auth.utils import create_default_roles, create_default_permissions, assign_default_permissions, create_admin_user
from app.extensions import db
from app.models import Role, Permission

def init_db(app):
    """Initialize the database with default data"""
    with app.app_context():
        db.create_all()
        create_default_roles()
        create_default_permissions()
        assign_default_permissions()
        print("Database initialized successfully!")

def create_admin(app, username, email, password):
    """Create an admin user"""
    with app.app_context():
        create_admin_user(username, email, password)
        print(f"Admin user '{username}' created successfully!")

def run_server(app, host='0.0.0.0', port=5000, debug=False):
    """Run the Flask development server"""
    app.run(host=host, port=port, debug=debug)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database with default roles and permissions."""
    # Create default roles
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', description='Regular user')
        db.session.add(user_role)
    
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
    
    # Create default permissions
    permissions = [
        ('view_maps', 'Can view maps'),
        ('create_maps', 'Can create maps'),
        ('edit_maps', 'Can edit maps'),
        ('delete_maps', 'Can delete maps'),
        ('manage_users', 'Can manage users'),
        ('manage_roles', 'Can manage roles')
    ]
    
    for name, description in permissions:
        permission = Permission.query.filter_by(name=name).first()
        if not permission:
            permission = Permission(name=name, description=description)
            db.session.add(permission)
    
    db.session.commit()
    click.echo('Initialized the database with default roles and permissions.')

def init_app(app):
    """Register database commands with the Flask app."""
    app.cli.add_command(init_db_command)

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description='GIS Flask CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Init DB command
    init_parser = subparsers.add_parser('init-db', help='Initialize the database')
    
    # Create admin command
    admin_parser = subparsers.add_parser('create-admin', help='Create an admin user')
    admin_parser.add_argument('--username', default='admin', help='Admin username')
    admin_parser.add_argument('--email', default='admin@example.com', help='Admin email')
    admin_parser.add_argument('--password', default='admin123', help='Admin password')
    
    # Run server command
    server_parser = subparsers.add_parser('run', help='Run the development server')
    server_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    server_parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    server_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create the Flask app
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    if args.command == 'init-db':
        init_db(app)
    elif args.command == 'create-admin':
        create_admin(app, args.username, args.email, args.password)
    elif args.command == 'run':
        run_server(app, args.host, args.port, args.debug)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()