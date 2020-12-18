import logging

from flask import Flask
from flask_appbuilder import AppBuilder

from app.database import db
from app.sec import TenantSecurityManager

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARNING)

app = Flask(__name__)
app.config.from_object("config")

with app.app_context():
    db.create_all()
    appbuilder = AppBuilder(
        app, db.session, security_manager_class=TenantSecurityManager
    )
    from app import views, listeners  # noqa:F401


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""
