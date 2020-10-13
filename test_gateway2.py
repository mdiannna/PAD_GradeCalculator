import pytest
from Gateway import gateway

# def test_hello(client):
#     response = client.get('/')
#     assert response.data == b'Hello'




def test_hello2():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello!'