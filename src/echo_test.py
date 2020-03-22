import json
import urllib.request
from urllib.error import HTTPError
import pytest


def test_echo_success():
    response = urllib.request.urlopen('http://127.0.0.1:8080/echo?data=hi')
    payload = json.load(response)
    assert payload['data'] == 'hi'

<<<<<<< HEAD

=======
>>>>>>> 9b77c84e4874a9acacb094e4ab3df3f68e1c0441
def test_echo_failure():
    with pytest.raises(HTTPError):
        response = urllib.request.urlopen('http://127.0.0.1:8080/echo?data=echo')
