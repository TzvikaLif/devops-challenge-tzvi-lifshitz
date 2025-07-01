import os
import sys  # required for adding src/ to path for tests
import pytest
from botocore.exceptions import ClientError

# Ensure src directory is on the path so we can import app.py
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))

from app import create_app

# Helper to set common environment variables for testing
def _set_env(monkeypatch):
    monkeypatch.setenv('AWS_REGION', os.getenv('AWS_REGION', 'eu-west-1'))
    monkeypatch.setenv('DYNAMODB_TABLE', os.getenv('DYNAMODB_TABLE', 'devops-challenge'))
    monkeypatch.setenv('CODE_NAME', os.getenv('CODE_NAME', 'thedoctor'))
    monkeypatch.setenv('DOCKER_HUB_REPO', os.getenv('DOCKER_HUB_REPO', ''))
    monkeypatch.setenv('PROJECT_URL', os.getenv('PROJECT_URL', ''))

@pytest.fixture
def client(monkeypatch):
    # Apply common environment settings
    _set_env(monkeypatch)

    # Fake DynamoDB Table for testing
    class FakeTable:
        def get_item(self, Key):
            if Key.get('code_name') == os.getenv('CODE_NAME'):
                return {'Item': {'secret_code': 'XYZ123'}}
            return {}

    # Patch boto3.resource to use our FakeTable
    monkeypatch.setattr(
        'boto3.resource',
        lambda *args, **kwargs: type('R', (), {'Table': lambda self, name: FakeTable()})()
    )

    # Instantiate and configure the app for testing
    app = create_app()
    app.testing = True
    return app.test_client()

# Test the health endpoint returns the correct JSON based on env vars
def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {
        'status': 'healthy',
        'container': os.getenv('DOCKER_HUB_REPO'),
        'project': os.getenv('PROJECT_URL')
    }

# Test the secret endpoint returns the mocked secret under normal conditions
def test_secret_success(client):
    resp = client.get('/secret')
    assert resp.status_code == 200
    assert resp.get_json() == {'secret_code': 'XYZ123'}

# Test the secret endpoint returns 404 when no secret is found
def test_secret_not_found(monkeypatch):
    # Apply common environment settings
    _set_env(monkeypatch)

    # EmptyTable simulates no data in DynamoDB
    class EmptyTable:
        def get_item(self, Key):
            return {}

    # Patch boto3.resource to use EmptyTable
    monkeypatch.setattr(
        'boto3.resource',
        lambda *args, **kwargs: type('R', (), {'Table': lambda self, name: EmptyTable()})()
    )

    # Instantiate and configure the app for testing
    app = create_app()
    app.testing = True
    client = app.test_client()

    resp = client.get('/secret')
    assert resp.status_code == 404
