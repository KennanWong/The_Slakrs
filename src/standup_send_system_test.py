'this file is the http testing for standup send'

import urllib
import json
from urllib.error import HTTPError # pylint: disable=C0412
import flask                      # pylint: disable=W0611


import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1, reg_user2

#pylint compliant
#############################################################
#                   STANDUP_SEND                            #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_send():
    'successful case for standup send'

    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(            # pylint: disable=W0612
        f"{BASE_URL}/standup/start",
        data=data,
        headers={'Content-Type':'application/json'}
    ))


    data2 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'testing'
    }).encode('utf-8')

    req2 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/standup/send",
        data=data2,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req2)               # pylint: disable=W0612

    assert payload == {}

def test_invalid_id():
    'error case'

    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(            # pylint: disable=W0612
        f"{BASE_URL}/standup/start",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data2 = json.dumps({
        'token': user1['token'],
        'channel_id': 100,
        'message': 'testing'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/send",
            data=data2,
            headers={'Content-Type':'application/json'}
        ))

def test_long_message():
    'error case '

    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(               # pylint: disable=W0612
        f"{BASE_URL}/standup/start",
        data=data,
        headers={'Content-Type':'application/json'}
    ))


    data2 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'To manage the transition from trimesters to hexamesters in 2020,'+               # pylint: disable=C0330
                        'UNSW has established a new focus on building an in-house digital'+     # pylint: disable=C0330
                        ' collaboration and communication tool for groups and teams to support'+        # pylint: disable=C0330
                        'the high intensity learning environment. Rather than re-invent the wheel,'+ # pylint: disable=C0330
                        ' UNSW has decided that it finds the functionality of Slack to be nearly'+  # pylint: disable=C0330
                        ' exactly what it needs. For this reason, UNSW has contracted out Lit Pty '+    # pylint: disable=C0330
                        'Ltd (a small software business run by Hayden) to build the new product.In'+    # pylint: disable=C0330
                        ' UNSWs attempt to connect with the younger and more "hip" generation that'+    # pylint: disable=C0330
                        ' fell in love with flickr, Tumblr, etc, they would like to call the new '+ # pylint: disable=C0330
                        'UNSW-based product slackr. Lit Pty Ltd has sub-contracted two software '+  # pylint: disable=C0330
                        'firms: Catdog Pty Ltd (two software developers, Sally and Bob, who will ' +    # pylint: disable=C0330
                        'build the initial web-based GUI). YourTeam Pty Ltd (a team of talented '+  # pylint: disable=C0330
                        'misfits completing COMP1531 in 20T1), who will build the backend python '+ # pylint: disable=C0330
                        'server and possibly assist in the GUI later in the project. In summary, '+ # pylint: disable=C0330
                        'UNSW contracts Lit Pty Ltd, who sub contracts:Catdog (Sally and Bob) '+    # pylint: disable=C0330
                        'for front end work, YourTeam (you and others) for backend work'    # pylint: disable=C0330
    }).encode('utf-8')  # pylint: disable=C0330

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/send",
            data=data2,
            headers={'Content-Type':'application/json'}
        ))

def test_no_active():
    'error case'

    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data2 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'testing'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/send",
            data=data2,
            headers={'Content-Type':'application/json'}
        ))

def test_unauthor_member():
    'error case'

    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    user2 = reg_user2()

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(            # pylint: disable=W0612
        f"{BASE_URL}/standup/start",
        data=data,
        headers={'Content-Type':'application/json'}
    ))


    data2 = json.dumps({
        'token': user2['token'],
        'channel_id': channel1['channel_id'],
        'message': 'testing'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/send",
            data=data2,
            headers={'Content-Type':'application/json'}
        ))                                                          # pylint: disable=C0304