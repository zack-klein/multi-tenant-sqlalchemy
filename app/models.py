from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from app.database import db
from app.mixins import TenantMixin


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
            "TenantUser",
            primaryjoin="%s.author_id == TenantUser.id" % cls.__name__,
            enable_typechecks=False,
        )

    def __repr__(self):
        return self.name
