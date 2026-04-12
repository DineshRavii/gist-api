import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_gists_valid_user(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": "abc123",
            "description": "Test gist",
            "html_url": "https://gist.github.com/testuser/abc123",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
            "files": {
                "test.py": {"filename": "test.py"}
            }
        }
    ]

    with patch('app.requests.get', return_value=mock_response):
        response = client.get('/testuser')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_gists_response_structure(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": "abc123",
            "description": "Test gist",
            "html_url": "https://gist.github.com/testuser/abc123",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-02T00:00:00Z",
            "files": {
                "test.py": {"filename": "test.py"}
            }
        }
    ]

    with patch('app.requests.get', return_value=mock_response):
        response = client.get('/testuser')

    data = response.get_json()
    gist = data[0]

    assert "id" in gist
    assert "description" in gist
    assert "url" in gist
    assert "created_at" in gist
    assert "updated_at" in gist
    assert "files" in gist
    assert isinstance(gist["files"], list)

def test_get_gists_user_not_found(client):
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch('app.requests.get', return_value=mock_response):
        response = client.get('/nonexistentuser999')

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_get_gists_github_api_failure(client):
    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch('app.requests.get', return_value=mock_response):
        response = client.get('/testuser')

    assert response.status_code == 502
    data = response.get_json()
    assert "error" in data

def test_get_gists_integration_octocat(client):
    response = client.get('/octocat')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

    gist = data[0]
    assert "id" in gist
    assert "url" in gist
    assert "files" in gist
    assert "created_at" in gist
    assert "updated_at" in gist