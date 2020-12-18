from flask_appbuilder.security.sqla.models import User

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.database import db


users_tenants = db.Table(
    "users_tenants",
    db.Model.metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("ab_user.id")),
    db.Column("tenant_id", db.Integer, db.ForeignKey("tenant.id")),
)


class Tenant(db.Model):
    __tablename__ = "tenant"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship(
        "TenantUser",
        secondary=users_tenants,
        backref="users",
        doc="The users for a tenant.",
    )

    def __repr__(self):
        return self.name


class TenantUser(User):
    __tablename__ = "ab_user"
    tenant_id = Column(Integer, ForeignKey("tenant.id"),)

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username

    @declared_attr
    def tenant(cls):
        return relationship(
            "Tenant",
            primaryjoin="%s.tenant_id == Tenant.id" % cls.__name__,
            enable_typechecks=True,
        )
