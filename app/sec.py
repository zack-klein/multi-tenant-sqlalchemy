from flask_appbuilder.security.sqla.manager import SecurityManager
from .sec_models import TenantUser
from .sec_views import TenantUserModelView


class TenantSecurityManager(SecurityManager):
    user_model = TenantUser
    userdbmodelview = TenantUserModelView
