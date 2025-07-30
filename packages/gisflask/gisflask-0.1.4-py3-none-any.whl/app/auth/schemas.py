from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    """Schema for user registration"""
    username = fields.String(required=True, validate=validate.Length(min=3, max=64))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    
    class Meta:
        strict = True

class LoginSchema(Schema):
    """Schema for user login"""
    username = fields.String(required=True)
    password = fields.String(required=True)
    
    class Meta:
        strict = True

class RoleSchema(Schema):
    """Schema for roles"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    
    class Meta:
        strict = True

class PermissionSchema(Schema):
    """Schema for permissions"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    
    class Meta:
        strict = True
