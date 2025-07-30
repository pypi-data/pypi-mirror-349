from app.extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

# Association table for user-role relationship
user_roles = db.Table('user_roles',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('roles.id'), primary_key=True)
)

# Association table for role-permission relationship
role_permissions = db.Table('role_permissions',
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', UUID(as_uuid=True), db.ForeignKey('permissions.id'), primary_key=True)
)

class User(db.Model):
    """User model for storing user related details"""
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f"<User {self.username}>"

class Role(db.Model):
    """Role model for storing role related details"""
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    # Relationships
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f"<Role {self.name}>"

class Permission(db.Model):
    """Permission model for storing permission related details"""
    __tablename__ = "permissions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<Permission {self.name}>"

class MapPreference(db.Model):
    """Map preference model for storing user map preferences"""
    __tablename__ = "map_preferences"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    map_type = db.Column(db.String(50), default="folium")
    center_lat = db.Column(db.Float, default=0.0)
    center_lng = db.Column(db.Float, default=0.0)
    zoom_level = db.Column(db.Integer, default=2)
    
    # Relationships
    user = relationship("User", backref="map_preference")
    
    def __repr__(self):
        return f"<MapPreference {self.id}>"
