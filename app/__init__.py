from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect  # already imported

csrf = CSRFProtect()  # Initialize CSRF globally
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
