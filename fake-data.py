from faker import Faker

from flask import current_app
from flask_appbuilder.security.sqla.models import Role, User

from random import choice, randint
from tqdm import tqdm

from werkzeug.security import generate_password_hash

from app import app
from app.database import db
from app.models import Post, Tenant


def add_user(username, firstname, lastname, email, role, password, tenant_id):
    user = User()
    user.first_name = firstname
    user.last_name = lastname
    user.password = generate_password_hash(password)
    user.username = username
    user.email = email
    user.active = True
    user.roles.append(role)
    user.current_tenant_id = tenant_id
    return user


def create_fake_data(
    num_tenants, num_posts, max_users_per_tenant, min_users_per_tenant,
):
    fake = Faker()
    db.drop_all()
    db.create_all()

    current_app.appbuilder.sm.create_db()
    current_app.appbuilder.add_permissions(update_perms=True)
    current_app.appbuilder.sm.create_db()

    # Users & Tenants
    # Create an admin first
    admin_role = db.session.query(Role).filter(Role.name == "Admin").first()
    admin = add_user(
        "admin", "admin", "admin", "admin", admin_role, "admin", None
    )
    users = [admin]
    used_usernames = []
    tenants = []

    public_role = db.session.query(Role).filter(Role.name == "Public").first()

    print("Creating tenants...")
    for _ in tqdm(range(0, num_tenants)):
        this_tenant_users = []
        tenant = Tenant(name=fake.company() + " " + fake.job().title() + "s")

        this_tenant_users_num = randint(
            min_users_per_tenant, max_users_per_tenant
        )

        # Create users
        for _ in range(this_tenant_users_num):
            firstname = fake.first_name()
            lastname = fake.last_name()
            username = f"{firstname}.{lastname}".lower()
            email = f"{username}@{fake.word()}.com"
            password = username

            if username not in used_usernames:
                user = add_user(
                    username,
                    firstname,
                    lastname,
                    email,
                    public_role,
                    password,
                    None,
                )
                used_usernames.append(username)

            this_tenant_users.append(user)
            users.append(user)

        # Add users for this tenant
        this_tenant_users.append(admin)
        tenant.users = this_tenant_users
        tenants.append(tenant)

    db.session.add_all(users)
    db.session.commit()

    db.session.add_all(tenants)
    db.session.commit()

    posts = []
    for _ in tqdm(range(0, num_posts)):
        tenant = choice(tenants)
        user = choice(tenant.users)
        post = Post(
            name=f"{fake.bs()} {fake.word()}".title(),
            text="\n\n".join(fake.paragraphs()),
            tenant_id=tenant.id,
            author_id=user.id,
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()
    print("All done!")


with app.app_context():
    create_fake_data(
        num_tenants=5,
        num_posts=1000,
        max_users_per_tenant=12,
        min_users_per_tenant=2,
    )
