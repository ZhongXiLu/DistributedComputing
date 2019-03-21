import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Password

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
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(Password(user_id=0, password="pazzw0rd1"))
    db.session.add(Password(user_id=1, password="correct horse battery staple"))
    db.session.commit()


if __name__ == '__main__':
    cli()
