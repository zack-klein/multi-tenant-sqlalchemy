# Multi Tenant Example

I recently read the [AWS Whitepaper on Multitenancy for SAAS applciations](https://d1.awsstatic.com/whitepapers/saas-tenant-isolation-strategies.pdf) (I'm generally fascinated with how to build SAAS products) and I became really interested with the *Pool* model of isolating tenants in a SAAS platform. Basically, when building a SAAS product, you need to keep customer data separate from each other (duh). There are different ways of doing this, and the pool model relies entirely on logic in the application for this separation.

One implementation of this strategy is to have all customer data share the same tables and rely on smart filtering in database queries to segregate data properly.  While this felt scary to me at first (huge blast radius?!), the idea has really grown on me. If you can pull it off, you can save so much time, money, and effort by keeping everything in one place. The whitepaper seems to like this model as well (though they don't say it outright).

Coincidentally, I also recently read [this wonderful book on SQLAlchemy](https://learning.oreilly.com/library/view/essential-sqlalchemy/9780596516147/) (the magical Python ORM).  I was poking around StackOverflow and found [this cool SQLAlchemy Recipe](https://github.com/sqlalchemy/sqlalchemy/wiki/FilteredQuery) that touches on exactly this point! It was kismet -- I decided to make a simple app that simulates fully isolated tenants of a SAAS application.

# How does it work?

There are actually a couple ways to do this. I chose to use listeners here.
