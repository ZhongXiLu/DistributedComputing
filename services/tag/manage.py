
import os
import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Tag

app = create_app()
cli = FlaskGroup(create_app=create_app)


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
    # db.session.add(User(username='michael', email="hermanmu@gmail.com"))
    # db.session.add(User(username='michaelherman', email="michael@mherman.org"))
    # db.session.commit()
    pass


if __name__ == '__main__':
    cli()
