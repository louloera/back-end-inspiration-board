from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {"origins": "*"}}, headers='Content-Type')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        # "SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DB_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.card import Card
    from app.models.board import Board

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.cards_routes import cards_bp
    from .routes.boards_route import boards_bp

    app.register_blueprint(cards_bp)
    app.register_blueprint(boards_bp)



    CORS(app)
    return app
