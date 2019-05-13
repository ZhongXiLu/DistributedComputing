
import os
import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Post

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
    # db.session.add(Post(creator='0', content='Hello World!'))
    # db.session.add(Post(creator='0', content='Hello World again!'))
    # db.session.add(Post(creator='1', content='Some other post'))
    # db.session.add(Post(creator='69', content='Yet another another post :)'))
    # db.session.commit()
    pass


if __name__ == '__main__':
    cli()
