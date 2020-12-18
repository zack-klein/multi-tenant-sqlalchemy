from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose

from app import appbuilder, db
from app import models, sec_models


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder,
        ),
        404,
    )


class FilteredPostView(BaseView):
    route_base = "/"
    default_view = "posts"

    @expose("/posts/")
    def posts(self):
        print(db.session.query(models.Post).statement.compile())
        print(db.session.query(models.Post).statement.compile().params)
        posts = db.session.query(models.Post).all()
        return self.render_template("list_posts.html", posts=posts)

    @expose("/post/<int:post_id>")
    def post(self, post_id):
        post = db.session.query(models.Post).get_or_404(post_id)
        return self.render_template("post.html", post=post)


class TenantView(ModelView):
    datamodel = SQLAInterface(sec_models.Tenant)

    list_columns = ["name", "users"]


class PostView(ModelView):
    datamodel = SQLAInterface(models.Post)

    list_columns = ["id", "name", "author.username", "tenant.name"]


appbuilder.add_view(
    TenantView, "Tenants", icon="fa-home",
)

appbuilder.add_view(
    FilteredPostView, "Filtered Posts", icon="fa-home",
)

appbuilder.add_view(
    PostView, "Posts", icon="fa-edit",
)
