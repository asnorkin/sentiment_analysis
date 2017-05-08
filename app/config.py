import os


class BaseConfig(object):
    PROJECT = "app"

    # Get app root path, also can use flask.root_path.
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    TESTING = False

    ADMINS = ['youremail@yourdomain.com']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'secret key'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DefaultConfig(BaseConfig):
    # Statement for enabling the development environment
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

    # Secret key for signing cookies
    SECRET_KEY = 'development key'


class LocalConfig(DefaultConfig):
    # config for local development
    pass


class StagingConfig(DefaultConfig):
    # config for staging environment
    pass


class ProdConfig(DefaultConfig):
    # config for production environment
    pass


def get_config(MODE):
    SWITCH = {
        'LOCAL': LocalConfig,
        'STAGING': StagingConfig,
        'PRODUCTION': ProdConfig
    }
    return SWITCH[MODE]
