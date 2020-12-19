from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from app.database import db


class TenantMixin(object):
    """
    Mixin that ties a model to a tenant.
    """

    # Override to allow cross tenant access on an object.
    cross_tenant = False

    @declared_attr
    def tenant_id(cls):
        return Column(Integer, ForeignKey("tenant.id"), nullable=False,)

    @declared_attr
    def tenant(cls):
        return relationship(
            "Tenant",
            primaryjoin="%s.tenant_id == Tenant.id" % cls.__name__,
            enable_typechecks=False,
        )


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
        "User",
        secondary=users_tenants,
        backref="users",
        doc="The users for a tenant.",
    )

    def __repr__(self):
        return self.name


class Post(db.Model, TenantMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    text = Column(Text, nullable=False)

    @declared_attr
    def author_id(cls):
        return Column(Integer, ForeignKey("ab_user.id"), nullable=False,)

    @declared_attr
    def author(cls):
        return relationship(
            "User",
            primaryjoin="%s.author_id == User.id" % cls.__name__,
            enable_typechecks=False,
        )

    def __repr__(self):
        return self.name
