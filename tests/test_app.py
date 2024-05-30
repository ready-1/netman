import pytest
from flask import session
from netman.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index(client):
    # Log in as a test user
    with client.session_transaction() as sess:
        sess['user_id'] = 'test_user'

    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to NetMan" in response.data

def test_login(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b"User not found in local storage" in response.data

def test_logout(client):
    # Log in as a test user
    with client.session_transaction() as sess:
        sess['user_id'] = 'test_user'

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register(client):
    response = client.post('/register', data=dict(
        username='new_user',
        password='new_password'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"User registered successfully" in response.data