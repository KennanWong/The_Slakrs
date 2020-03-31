'this file is the http testing for channels listall'
import urllib
import json
from urllib.error import HTTPError          # pylint: disable=W0611, C0412
import flask                                # pylint: disable=W0611


import pytest                               # pylint: disable=W0611
from system_helper_functions import reg_user1, reset_workspace
from system_helper_functions import reg_user2

#pylint compliant

#############################################################
#                   CHANNELS_LISTALL                        #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_listall():
    'successful case for channels listall'
    reset_workspace()

    user1 = reg_user1()

    user2 = reg_user2()

    data = json.dumps({
        'token':user2['token'],
        'name': 'new_channel',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user1['token'],
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/channels/listall",
        data=data1,
        headers={'Content-Type':'application/json'}
    )

    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))

    assert response
    