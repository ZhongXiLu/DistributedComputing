# services/users/manage.py

import os
import unittest

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import User  # new

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    os.environ['TESTING'] = "True"
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    os.environ['TESTING'] = "False"
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='user', email="user@user.com"))        # id=1
    db.session.add(User(username='admin', email="admin@admin.com"))     # id=2
    db.session.commit()


if __name__ == '__main__':
    cli()
