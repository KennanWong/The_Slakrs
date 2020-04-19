'''
Pytest file to test auth_logout on a system level
'''

# pylint: disable=W0611
import urllib
import json
import flask

from system_helper_functions import reg_user1, reset_workspace


#############################################################
#                   AUTH_LOGOUT                             #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_logout1():
    '''
    Test a valid use of auth/logout
    '''
    reset_workspace()
    payload = reg_user1()

    data2 = json.dumps({
        'token': payload['token']
    }).encode('utf-8')

    req2 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/logout",
        data=data2,
        headers={'Content-Type':'application/json'}
    ))

    payload2 = json.load(req2)

    # asserts that the u_id's of the one return matches the user found
    assert payload2['is_success'] is True
