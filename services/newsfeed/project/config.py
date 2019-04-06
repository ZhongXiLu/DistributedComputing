import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = 'my_precious'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    pass

class TestingConfig(BaseConfig):
    """Testing configuration"""
    # TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    pass

class ProductionConfig(BaseConfig):
    """Production configuration"""
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    pass
