from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    
    # Load configurations from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from auth import auth_bp
    from movie import movie_bp
    from rating import rating_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(movie_bp, url_prefix='/movies')
    app.register_blueprint(rating_bp, url_prefix='/ratings')

    return app



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables in the database
        print("App context successfully pushed and database initialized")
        
        # Use 'engine' to fetch the SQLAlchemy database URL
        bind = db.engine.url
        print(f"SQLAlchemy is bound to database: {bind}")

    app.run(debug=True, port=5001)

