import logging

from flask import Flask
from flask_appbuilder import AppBuilder, IndexView

from app.database import db


# Logging
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARNING)


# Define an index
class Index(IndexView):
    index_template = "mt_index.html"


# Init flask app
app = Flask(__name__)
app.config.from_object("config")

with app.app_context():
    db.init_app(app)
    db.create_all()
    appbuilder = AppBuilder(app, db.session, indexview=Index)

    from app import views  # noqa:F401
