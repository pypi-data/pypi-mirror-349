import folium
from flask import render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.main import main_bp
from app.extensions import db
from app.models import User, MapPreference
import uuid

@main_bp.route('/')
def index():
    """
    Home Page
    ---
    tags:
      - Main
    responses:
      200:
        description: Home page rendered
    """
    return render_template('index.html')



@main_bp.route('/map')
def map_page():
    """
    Map Visualization Page
    ---
    tags:
      - Main
    parameters:
      - name: lat
        in: query
        type: number
        required: false
        default: 0
        description: Latitude for map center
      - name: lng
        in: query
        type: number
        required: false
        default: 0
        description: Longitude for map center
      - name: zoom
        in: query
        type: integer
        required: false
        default: 2
        description: Zoom level for map
    responses:
      200:
        description: Map page rendered
    """
    # Get map parameters from query string
    center_lat = float(request.args.get('lat', 0))
    center_lng = float(request.args.get('lng', 0))
    zoom_level = int(request.args.get('zoom', 2))
    
    # Create map with Folium
    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_level)
    folium.TileLayer('openstreetmap').add_to(m)
    
    # Add sample marker
    folium.Marker(
        [center_lat, center_lng], 
        popup='Center', 
        tooltip='Center Point'
    ).add_to(m)
    
    # Add another sample marker
    folium.Marker(
        [center_lat + 0.1, center_lng + 0.1], 
        popup='Sample Point', 
        tooltip='Sample Point',
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    # Save map to a temporary HTML string
    from io import BytesIO
    map_html = m.get_root().render()
    
    return render_template(
        'map.html', 
        map_html=map_html,
        map_type='folium',
        center_lat=center_lat,
        center_lng=center_lng,
        zoom_level=zoom_level
    )

@main_bp.route('/api/map/preferences', methods=['GET', 'POST'])
@jwt_required()
def map_preferences():
    """
    Get or Update Map Preferences
    ---
    tags:
      - Maps
    security:
      - JWT: []
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            center_lat:
              type: number
            center_lng:
              type: number
            zoom_level:
              type: integer
    responses:
      200:
        description: Map preferences retrieved or updated
      401:
        description: Missing or invalid token
    """
    current_user_id = get_jwt_identity()
    try:
        user_id = uuid.UUID(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if user has map preferences
        map_pref = MapPreference.query.filter_by(user_id=user_id).first()
        
        if request.method == 'GET':
            if not map_pref:
                return jsonify({
                    'center_lat': 0.0,
                    'center_lng': 0.0,
                    'zoom_level': 2,
                    'map_type': 'folium'
                }), 200
            
            return jsonify({
                'center_lat': map_pref.center_lat,
                'center_lng': map_pref.center_lng,
                'zoom_level': map_pref.zoom_level,
                'map_type': getattr(map_pref, 'map_type', 'folium')
            }), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if not map_pref:
                # Create a new map preference for the user
                map_pref = MapPreference()
                map_pref.user_id = user_id
                map_pref.map_type = 'folium'
                map_pref.center_lat = 0.0
                map_pref.center_lng = 0.0
                map_pref.zoom_level = 2
                db.session.add(map_pref)
            
            # Update preferences
            if 'map_type' in data:
                map_pref.map_type = data['map_type']
            if 'center_lat' in data:
                map_pref.center_lat = data['center_lat']
            if 'center_lng' in data:
                map_pref.center_lng = data['center_lng']
            if 'zoom_level' in data:
                map_pref.zoom_level = data['zoom_level']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Map preferences updated',
                'center_lat': map_pref.center_lat,
                'center_lng': map_pref.center_lng,
                'zoom_level': map_pref.zoom_level,
                'map_type': map_pref.map_type
            }), 200
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400
