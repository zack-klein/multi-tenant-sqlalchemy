from flask import render_template, redirect, url_for
from flask_appbuilder import BaseView, expose
from flask_login import current_user

from app import appbuilder, db
from app.models import Post


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
        if not current_user.is_authenticated:
            return redirect(url_for("AuthDBView.login"))

        posts = db.session.query(Post).all()
        return self.render_template("list_posts.html", posts=posts)

    @expose("/post/<int:post_id>")
    def post(self, post_id):
        post = db.session.query(Post).get_or_404(post_id)
        return self.render_template("post.html", post=post)


appbuilder.add_view(
    FilteredPostView, "Filtered Posts", icon="fa-home",
)
