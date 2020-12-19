from flask_appbuilder.security.sqla.models import User

from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm.query import Query

from app.models import Tenant, users_tenants, TenantMixin

from flask_login import current_user


@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    if query._execution_options.get("cross_tenant"):
        return query

    for ent in query.column_descriptions:
        entity = ent["entity"]
        if entity is None:
            continue
        insp = inspect(ent["entity"])
        mapper = getattr(insp, "mapper", None)
        if mapper and issubclass(mapper.class_, TenantMixin):

            # This is where the magic happens. Every time we query a
            # TenantMixin'd object, we filter for objects where this
            # user is a user in the tenant.

            # Equivalent to:
            # SELECT *
            # FROM {table}
            # JOIN USERS_TO_TENANTS
            # ON {table}.tenant_id = USERS_TO_TENANTS.tenant_id
            # WHERE USERS_TO_TENANTS.user_id = {user_id}
            query = (
                query.enable_assertions(False)
                .join(Tenant)
                .join(users_tenants)
                .join(User)
                .filter(users_tenants.c.user_id == current_user.id)
            )

    return query


@event.listens_for(TenantMixin, "load", propagate=True)
def load(obj, context):
    if not context.query._execution_options.get("cross_tenant", False):
        if current_user not in obj.tenant.users:
            raise TypeError(
                "private object %s was loaded, did you use "
                "joined eager loading?" % obj
            )
