'this file is the http testing for standup active'

import urllib
import json
from urllib.error import HTTPError
from datetime import datetime, timedelta
import flask                     # pylint: disable=W0611


import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1

#pylint compliant
#############################################################
#                   STANDUP_ACTIVE                          #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_active():
    'successful case'
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data1 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/standup/start",
        data=data1,
        headers={'Content-Type':'application/json'}
    ))

    req = urllib.request.Request(
        f"{BASE_URL}/standup/active?token="+str(user1['token'])+"&channel_id="+str(channel1['channel_id'])
    )

    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))

    assert response['is_active'] is True

    length = 30
    time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")

    assert response['time_finish'] == time_finish


def test_invalid_channel_id():
    'error test'
    reset_workspace()

    user1 = reg_user1()
   # channel1 = create_ch1(user1)

    with pytest.raises(HTTPError):
        req = urllib.request.Request(
            f"{BASE_URL}/standup/active?token="+str(user1['token'])+"&channel_id=1"
        )
        req.get_method = lambda: 'GET'
        json.load(urllib.request.urlopen(req))
