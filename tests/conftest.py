import pytest
import sys
from os.path import abspath, dirname

# Add the parent directory to the Python path
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app import app as flask_app, db
from config import Config

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for tests."""
    flask_app.config.from_object(TestConfig)
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope="module")
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()