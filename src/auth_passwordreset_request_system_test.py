'''
Pytest file to test auth_passwordreset on a system level
'''

import urllib
import json
import flask        #pylint disable = W0611
import pytest       #pylint disable = W0611



from system_helper_functions import reg_sid, reset_workspace


#############################################################
#                     AUTH_PASSWORDRESET_REQUEST            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_request():
    '''
    Test valid case of test_password_request
    '''
    reset_workspace()

    user1 = reg_sid()         #pylint disable = W0612

    data = json.dumps({
        'email': 'sidu2000@gmail.com'
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/passwordreset/request",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req)

    assert payload == {}                #pylint disable = C0304
    