import os
from flask import Flask

import config
from .extensions import db, csrf, login_manager
from .models import User as user
from .common import response, COMMON_CONSTANTS
from .api import auth
from .frontend import frontend


#__all__ = ['create_app']

# TODO: default blueprints
DEFAULT_BLUEPRINTS = [
    auth,
    frontend,
]


def create_app(cfg=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = config.DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name) # TODO: check params
    configure_app(app, cfg)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app

def configure_app(app, cfg=None):
    app.config.from_object(config.DefaultConfig)

    if cfg:
        app.config.from_object(cfg)
        return

    application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
    app.config.from_object(config.get_config(application_mode))

def configure_extensions(app):
    db.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user.query.get(id)

    login_manager.setup_app(app)

    @login_manager.unauthorized_handler
    def unauthorized(msg=None):
        '''Handles unauthorized request.'''
        return response.make_error_resp(msg="You're not authorized.", code=401)

    csrf.init_app(app)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_logging(app):
    pass


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(500)
    def server_error_page(error):
        return response.make_error_resp(msg=str(error), code=500)

    @app.errorhandler(422)
    def semantic_error(error):
        return response.make_error_resp(msg=str(error.description), code=422)

    @app.errorhandler(404)
    def page_not_found(error):
        return response.make_error_resp(msg=str(error.description), code=404)

    @app.errorhandler(403)
    def page_forbidden(error):
        return response.make_error_resp(msg=str(error.description), code=403)

    @app.errorhandler(400)
    def page_bad_request(error):
        return response.make_error_resp(msg=str(error.description), code=400)
