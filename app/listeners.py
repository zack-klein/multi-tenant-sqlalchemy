from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm.query import Query

from app.sec_models import Tenant, users_tenants, TenantUser
from app.mixins import TenantMixin

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

            # Effectively, every time we query a `TenantMixin` object, we
            # first join with the users_tenants table to get a list of all
            # the

            # Equivalent to:
            # SELECT *  // This can be whatever
            # FROM {table}
            # JOIN USERS_TO_TENANTS
            # ON {table}.tenant_id = USERS_TO_TENANTS.tenant_id
            # WHERE USERS_TO_TENANTS.user_id = {user_id}
            query = (
                query.enable_assertions(False)
                .join(Tenant)
                .join(users_tenants)
                .join(TenantUser)
                .filter(users_tenants.c.user_id == current_user.id)
            )

    return query
