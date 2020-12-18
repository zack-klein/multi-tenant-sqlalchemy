from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


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
