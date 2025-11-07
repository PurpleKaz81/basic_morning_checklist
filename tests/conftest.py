import pytest


@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    with app.test_client() as client:
        yield client
