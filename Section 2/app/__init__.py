from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager


def get_locale():
    """Determine the language to use for localization."""
    # Get language from query parameters and save it in session
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    # Return the language from session or default to 'en'
    return session.get('lang', 'en')


# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config')  # Ensure you have a `config.py` file with required settings

# Initialize Flask extensions
db = SQLAlchemy(app)  
migrate = Migrate(app, db) 
babel = Babel(app, locale_selector=get_locale) 
admin = Admin(app, template_mode='bootstrap4') 
login_manager = LoginManager() 

# Configure Flask-Login
login_manager.init_app(app)
login_manager.login_view = 'login' 

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Retrieve the user from the database."""
    from app.models import User  
    return User.query.get(int(user_id))


# Register Flask-Admin models
def register_admin_views():
    """Add models to Flask-Admin."""
    from app.models import User, DiveSite, DiveEvent  # Import models
    from flask_admin.contrib.sqla import ModelView

    # Add models to Flask-Admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(DiveSite, db.session))
    admin.add_view(ModelView(DiveEvent, db.session))


# Import views and models (delay until after extensions are initialized)
from app import views, models

# Register admin views after models are imported
register_admin_views()
