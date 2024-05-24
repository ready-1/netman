import pytest
from netman.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200