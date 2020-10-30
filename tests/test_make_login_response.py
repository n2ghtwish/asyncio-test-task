import pytest
from att.requests import make_login_response


@pytest.mark.parametrize('user_id', ['1', 2, None, True, '5'])
def test_make_login_response(user_id):
    make_login_response(user_id)
