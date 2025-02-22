from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv



db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
    app.config['JSON_SORT_KEYS']=False
    

    # Import models here for Alembic setup
    from app.models.customer import Customer
    from app.models.rental import Rental
    from app.models.video import Video

    db.init_app(app)
    migrate.init_app(app, db)
    
    from .video_route import video_bp
    from .rental_route import rental_bp
    from .customer_route import customer_bp
    
    # Register Blueprints here
    app.register_blueprint(video_bp)
    app.register_blueprint(rental_bp)
    app.register_blueprint(customer_bp)

    return app