'this file is the http testing for channels list'
import urllib
import json
from urllib.error import HTTPError # pylint: disable=W0611, C0412
import flask             # pylint: disable=W0611


import pytest   # pylint: disable=W0611
from system_helper_functions import reg_user1, reset_workspace
from system_helper_functions import reg_user2, create_ch1

#pylint compliant
#############################################################
#                   CHANNELS_LIST                           #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_list():
    '''
    Test for successful case of channels list
    '''
    reset_workspace()

    user1 = reg_user1()
    reg_user2()

    create_ch1(user1)


    req = urllib.request.Request(
        f"{BASE_URL}/channels/list?token="+str(user1['token'])
    )

    req.get_method = lambda: 'GET'

    response = json.load(urllib.request.urlopen(req))['channels']

    expected = {
        'channel_id' : 1,
        'name': 'new_channel'
    }

    assert expected in response
