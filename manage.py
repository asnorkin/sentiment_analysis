from flask_script import Manager, Shell, Server
from flask import current_app
from app import create_app
from app.extensions import db
import app.models as models
from app.config import DefaultConfig
import os


def create_my_app(cfg=DefaultConfig):
    return create_app(cfg)


manager = Manager(create_my_app)


manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


@manager.shell
def make_shell_context():
    return dict(app=current_app, db=db, models=models)


@manager.command
def initdb():
    db.drop_all(bind=None)
    db.create_all(bind=None)

    user = models.User(
        first_name=u'Sam',
        last_name=u'Chuang',
        user_name=u'spchuang',
        password=u'123456',
        email=u"test@gmail.com"
    )
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
