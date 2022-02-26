import pytest
from app import db
import os
from flask import Flask
from guestbooks.model import GuestBook


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.
   :return: Flask app
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_uri = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    if '_test' not in 'sqlite:///' + os.path.join(basedir, 'db.sqlite'):
        db_uri = '{0}_test'.format('sqlite:///' + os.path.join(basedir, 'db.sqlite'))

    params = {
        'DEBUG': False,
        'TESTING': True,
        'APM_ACTIVE': False,
        'CELERY_ALWAYS_EAGER': True,
        'LOG_LEVEL': 'DEBUG',
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

    _app = Flask(__name__, instance_relative_config=True)
    _app.config.update(params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.
   :param app: Pytest fixture
   :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope="class")
def all_guestbooks():
    db.session.query(GuestBook).delete()
    db.session.commit()

    guestbooks = [
        {
            "name": "Warby Parker",
            "subject": "Ornare suspendisse",
            "message": "Sodales neque sodales ut etiam sit. Eu nisl nunc mi ipsum faucibus vitae aliquet nec ullamcorper. Sodales neque sodales ut etiam sit. Feugiat in fermentum posuere urna nec. Risus viverra adipiscing at in tellus integer feugiat. Faucibus nisl tincidunt eget nullam. Diam ut venenatis tellus in metus. Massa enim nec dui nunc mattis. In hendrerit gravida rutrum quisque. Pharetra sit amet aliquam id diam maecenas ultricies mi. Ut pharetra sit amet aliquam id diam maecenas ultricies."
        },
        {
            "name": "Eater Boston",
            "subject": "Purus gravida quis blandit",
            "message": "Arcu ac tortor dignissim convallis aenean. Mi in nulla posuere sollicitudin. Aliquet risus feugiat in ante metus dictum at. Et magnis dis parturient montes nascetur ridiculus mus. Nulla facilisi cras fermentum odio. Viverra adipiscing at in tellus integer feugiat scelerisque. Vulputate dignissim suspendisse in est ante. Vitae semper quis lectus nulla at volutpat."
        }
    ]

    for gbook in guestbooks:
        db.session.add(GuestBook(**gbook))
    db.session.commit()

    return db
