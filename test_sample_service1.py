import pytest
from sample_service_test import app


def test_hello2():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello!'