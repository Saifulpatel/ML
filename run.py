import os
from flask import Flask
from app.routes import main  # Ensure routes are imported

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Register blueprint
    app.register_blueprint(main)

    # Get the port from the environment variable (default: 5000)
    port = int(os.environ.get("PORT", 5000))

    return app, port
