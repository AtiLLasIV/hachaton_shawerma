from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    from .routes import bp as receiver_bp
    app.register_blueprint(receiver_bp)
    return app 