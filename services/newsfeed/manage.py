
import os
import unittest

from flask.cli import FlaskGroup

from project import create_app
app = create_app()
cli = FlaskGroup(create_app=create_app)

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


if __name__ == '__main__':
    cli()
