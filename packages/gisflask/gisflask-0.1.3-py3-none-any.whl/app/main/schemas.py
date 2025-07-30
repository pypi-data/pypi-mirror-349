from marshmallow import Schema, fields, validate

class MapPreferenceSchema(Schema):
    """Schema for map preferences"""
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    map_type = fields.String(validate=validate.OneOf(['folium', 'leafmap']))
    center_lat = fields.Float()
    center_lng = fields.Float()
    zoom_level = fields.Integer(validate=validate.Range(min=1, max=18))
    
    class Meta:
        strict = True

class MapPointSchema(Schema):
    """Schema for map points/markers"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    
    class Meta:
        strict = True
