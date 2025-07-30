# GIS Flask

A Flask-based GIS backend package with JWT authentication, role-based permissions, interactive maps, health monitoring, and API documentation.

![API Documentation](app/auth/APIDOCS.png)

## Features

- **JWT Authentication**: Secure authentication using JSON Web Tokens (JWT) for API access control
- **Role-Based Access Control**: Comprehensive permissions system for secure user access management
- **Interactive Maps**: Integration with Folium for interactive map visualizations
- **API Documentation**: Automatic Swagger/OpenAPI documentation
- **PostgreSQL Database**: Robust data storage with UUID primary keys
- **Health Monitoring**: Built-in health check endpoint
- **Modular Architecture**: Well-organized codebase with clear separation of concerns

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL database
- Required Python packages (see installation)

### Installation Options

#### Option 1: Install as a Python Package

1. Install directly from GitHub (or PyPI once published):
   ```bash
   pip install git+https://github.com/KimutaiLawrence/gisflask.git
   ```

2. Set up environment variables:
   ```bash
   # Copy .env.example to .env and fill in your values
   cp .env.example .env
   # Database connection
   export DATABASE_URL=postgresql://username:password@localhost:5432/gisflask
   
   # JWT secret
   export JWT_SECRET_KEY=your-secret-key
   
   # Session secret
   export SESSION_SECRET=your-session-secret
   ```

3. Initialize the database and create admin user:
   ```bash
   # Initialize the database with default roles and permissions
   gisflask init-db

   # Run migrations to create tables (only needed once after setup)
   flask db upgrade
   
   # Create an admin user (defaults to admin/admin123 if not specified)
   gisflask create-admin --username admin --email admin@example.com --password admin123
   ```

4. Run the application:
   ```bash
   gisflask run
   ```

#### Option 2: Clone and Run Directly

1. Clone the repository:
   ```bash
   git clone https://github.com/KimutaiLawrence/gisflask.git
   cd gisflask
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows: or other: source venv/bin/activate
   ```

3. Install dependencies (choose one method):
   ```bash
   # Method 1: Install using requirements.txt
   pip install -r requirements.txt

   # Method 2: Install in development mode (recommended for development)
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   # Copy .env.example to .env and fill in your values
   cp .env.example .env
   # Database connection
   export DATABASE_URL=postgresql://username:password@localhost:5432/gisflask
   
   # JWT secret
   export JWT_SECRET_KEY=your-secret-key
   
   # Session secret
   export SESSION_SECRET=your-session-secret
   ```

5. Initialize the database:
   ```bash
   # Initialize migrations (creates migrations folder)
   flask db init
   
   # Create initial migration
   flask db migrate -m "Initial migration"
   
   # Apply migrations to create tables
   flask db upgrade
   
   # Create an admin user (defaults to admin/admin123 if not specified)
   gisflask create-admin --username admin --email admin@example.com --password admin123
   ```

6. Run the application:
   ```bash
   python run.py
   # OR
   gisflask run --debug
   ```

The application will be available at `http://localhost:5000`.

## Important Notes

- Make sure your PostgreSQL database is running and accessible before running the application.
- The default admin credentials (admin/admin123) should be changed in production.
- If you get an error about migrations folder already existing, you can safely delete the `migrations/` folder and run `flask db init` again.

## Project Structure

```
app/
├── auth/               # Authentication related modules
│   ├── routes.py       # Auth endpoints (register, login, etc.)
│   ├── schemas.py      # Data validation schemas
│   └── utils.py        # Auth helper functions
├── main/               # Main application modules
│   ├── routes.py       # Main routes including map endpoints
│   └── schemas.py      # Data validation schemas
├── users/              # User management (placeholder)
│   └── routes.py       # User CRUD operations
├── products/           # Product management (placeholder) 
│   └── routes.py       # Product CRUD operations
├── services/           # Service modules
│   └── email.py        # Email service
├── templates/          # HTML templates
│   └── ...            
├── __init__.py         # Application factory
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── models.py           # Database models
└── utils.py            # Utility functions
```

## Key Components

### Authentication System

The application uses JWT-based authentication:

- **Registration**: Create a new user account
- **Login**: Authenticate and receive access/refresh tokens
- **Token Refresh**: Get a new access token using refresh token
- **Protected Routes**: Access control using JWT authentication

Default admin credentials:
- Username: `admin`
- Password: `admin123`

### Role-Based Access Control

The application implements a flexible permission system:

- **Roles**: Admin, User, etc.
- **Permissions**: Fine-grained control over actions
- **Access Control Decorators**: `@jwt_required()`, `@admin_required`

### Map Visualization

Interactive maps using Folium:

- View maps at `/map`
- Customize center coordinates and zoom level
- Save map preferences per user

### API Documentation

Swagger/OpenAPI documentation is available at `/docs/`.

![API Documentation](app/auth/APIDOCS.png)

The API documentation provides:
- Interactive testing of all endpoints
- Detailed request/response schemas
- Authentication requirements
- Example requests and responses

#### Functional Endpoints

These endpoints are fully implemented and can be tested immediately from a frontend application:

- **Authentication**: `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/protected`
- **Map Services**: `/map`, `/api/map/preferences`
- **Health Check**: `/health`

#### Placeholder Endpoints

The following modules contain placeholder endpoints that need to be uncommented in their respective route files to work:

- **Users Module**: All endpoints under `/users/*`
- **Products Module**: All endpoints under `/products/*`

To activate these endpoints:
1. Open the corresponding route files (`app/users/routes.py`, `app/products/routes.py`)
2. Uncomment the example code sections
3. Implement any additional functionality you need

### Extending the Application

The application includes placeholder modules for adding custom functionality:

- **Users Module**: Example of user management functionality
- **Products Module**: Example of product management functionality

Each module includes placeholder templates and commented example code to help you understand how to implement your own features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Creating Your Own Package

This project is designed to be used as a template for your own GIS-enabled backend. Here's how to create your own package based on this template:

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/KimutaiLawrence/gisflask.git 
   cd gisflask
   ```

2. **Customize the package details**
   
   Edit the `setup.py` file to change:
   - package name
   - version
   - author information
   - description
   - repository URL
   - other metadata

3. **Customize the application**
   
   - Add your own models to `app/models.py`
   - Create new blueprint modules for your features
   - Customize templates and views
   - Add additional services as needed

4. **Build and publish your package**
   ```bash
   # Build the package
   python -m build
   
   # Install locally for testing
   pip install -e .
   
   # Publish to PyPI (once ready)
   python -m twine upload dist/*
   ```

## Customization Guide

### Adding New Models

1. Edit `app/models.py` to add your new model class:
   ```python
   class YourModel(db.Model):
       __tablename__ = "your_models"
       
       id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
       name = db.Column(db.String(100), nullable=False)
       # Add more fields as needed
   ```

2. Create migrations:
   ```bash
   flask db migrate -m "Add YourModel"
   flask db upgrade
   ```

### Creating a New Module

1. Create a new directory structure:
   ```bash
   mkdir -p app/your_module
   touch app/your_module/__init__.py
   touch app/your_module/routes.py
   ```

2. Define your blueprint in `__init__.py`:
   ```python
   from flask import Blueprint
   your_module_bp = Blueprint('your_module', __name__, url_prefix='/your-module')
   from app.your_module import routes
   ```

3. Register the blueprint in `app/__init__.py`:
   ```python
   from app.your_module import your_module_bp
   app.register_blueprint(your_module_bp)
   ```

4. Create templates for your module:
   ```bash
   mkdir -p app/templates/your_module
   ```

5. Implement your routes and views in `routes.py`

## Deployment

For production deployment, consider:

1. Using a proper WSGI server like Gunicorn or uWSGI
2. Setting up a reverse proxy with Nginx
3. Configuring proper environment variables for production
4. Setting up database backups and monitoring

## Acknowledgments

- Flask and its extensions
- Folium for interactive maps
- Swagger/OpenAPI for API documentation