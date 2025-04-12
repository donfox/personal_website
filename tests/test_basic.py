import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from app import app, db
from app import app as flask_app, db as _db
from models import EmailRequest

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # ✅ Right here
        "SECRET_KEY": "test-secret",
        "WTF_CSRF_ENABLED": False,
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Resume" in response.data


def test_resume_submission(client):
    response = client.post('/resume', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'format': 'pdf'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert EmailRequest.query.count() == 1


def test_admin_login_success(client):
    with client.session_transaction() as session:
        session['admin_logged_in'] = True
    response = client.get('/admin/dashboard')
    assert response.status_code == 200


def test_admin_redirect_without_login(client):
    response = client.get('/admin/dashboard')
    assert response.status_code == 302  # Should redirect to login


def test_invalid_email_format(client):
    response = client.post('/resume', data={
        'name': 'Bad Email',
        'email': 'not-an-email',
        'format': 'pdf'
    }, follow_redirects=True)
    assert b"Please provide a valid email address!" in response.data


def test_duplicate_email_request(client, app):
    with app.app_context():
        from models import EmailRequest, db
        db.session.add(EmailRequest(name='Test', email='dup@example.com'))
        db.session.commit()

    response = client.post('/resume', data={
        'name': 'Test',
        'email': 'dup@example.com',
        'format': 'pdf'
    }, follow_redirects=True)
    assert b"You have already requested a resume" in response.data


def test_admin_logout(client):
    with client.session_transaction() as sess:
        sess['admin_logged_in'] = True

    response = client.get('/admin/logout', follow_redirects=True)
    assert b"Resume" in response.data  # home page or resume should show
    with client.session_transaction() as sess:
        assert not sess.get('admin_logged_in')


def test_admin_dashboard_data(client, app):
    with app.app_context():
        from models import EmailRequest, db
        db.session.add(EmailRequest(name='Viewer', email='view@example.com'))
        db.session.commit()

    with client.session_transaction() as sess:
        sess['admin_logged_in'] = True

    response = client.get('/admin/dashboard')
    assert b"view@example.com" in response.data


def test_admin_delete_entry(client, app):
    with app.app_context():
        from models import EmailRequest, db
        entry = EmailRequest(name='ToDelete', email='del@example.com')
        db.session.add(entry)
        db.session.commit()
        entry_id = entry.id

    with client.session_transaction() as sess:
        sess['admin_logged_in'] = True

    response = client.post(f'/admin/delete/{entry_id}', follow_redirects=True)
    assert b"Entry deleted" in response.data


