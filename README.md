# Multi tenancy with SQLalchemy

I recently read the [AWS Whitepaper on Multitenancy for SAAS applciations](https://d1.awsstatic.com/whitepapers/saas-tenant-isolation-strategies.pdf) (I'm generally fascinated with how to build SAAS products) and I became really interested with the *Pool* model of isolating tenants in a SAAS platform. Basically, when building a SAAS product, you need to keep customer data separate from each other (duh). There are different ways of doing this, and the pool model relies entirely on logic in the application for this separation.

One implementation of this strategy is to have all customer data share the same tables and rely on smart filtering in database queries to segregate data properly.  While this felt scary to me at first (huge blast radius?!), the idea has really grown on me. If you can pull it off, you can save so much time, money, and effort by keeping everything in one place. The whitepaper seems to like this model as well (though they don't say it outright).

Coincidentally, I also recently read [this wonderful book on SQLAlchemy](https://learning.oreilly.com/library/view/essential-sqlalchemy/9780596516147/) (the magical Python ORM).  I was poking around StackOverflow and found [this cool SQLAlchemy Recipe](https://github.com/sqlalchemy/sqlalchemy/wiki/FilteredQuery) that touches on exactly this point! It was kismet -- I decided to make a simple app that simulates fully isolated tenants of a SAAS application.

# Test drive

First, clone the code and create a virtualenv:

```bash
python -m venv venv
```

Enter the env and pip install the requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

Create some fake data:
```bash
python fake-data.py
```

Run the webserver:
```bash
python run.py
```

Head to http://localhost:8080!  Navigate to the `Posts` page. :warning: You'll hit a login page. By default, an admin user is created with the fake data script. You can log in with the credentials:
```
user: admin
password: admin
```

On the posts page, you'll see a whole bunch of posts.  This is because the admin user can see everything!  Grab the username of one of the *Authors* of a blog post. Logout, then login again using this Author's username and password. :warning: The password for each user is just their username. For example, for the username `zack.klein`, the password would also be `zack.klein`.

You'll see for this user, they only see posts from one tenant!
