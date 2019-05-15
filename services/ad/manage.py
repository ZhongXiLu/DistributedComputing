
import os
import unittest
from shutil import copyfile

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Ad

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
    uploadDir = os.path.abspath(os.path.basename('uploads'))
    if not os.path.exists(uploadDir):
        os.makedirs(uploadDir)

    for file in os.listdir("ads"):
        copyfile(os.path.join("ads", file), os.path.join("uploads", file))
        category = file.split('.')[0]
        db.session.add(Ad(category=category, image=file))
    db.session.commit()


if __name__ == '__main__':
    cli()
