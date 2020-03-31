import urllib
import json
import flask
from urllib.error import HTTPError

import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1


#############################################################
#                   CHANNELS_LIST                           #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_list():
    '''
    Test a valid use of react on your own message
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/channels/list",
        data=data,
        headers={'Content-Type':'application/json'}
    )

    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))


