'''
Pytest file to test message_send on a system level
'''

import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2


#############################################################
#                   MESSAGE_SEND                            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_send1():
    '''
    Test valid use of message_send
    '''
    reset_workspace()

    user1 = reg_user1()
    ch1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': ch1['channel_id'],
        'message': 'testing'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    assert payload['message_id'] == 1

def test_long_msg():
    '''
    Test to send a message more thatn 1000 characters, should raise an Input error
    '''
    reset_workspace()

    user1 = reg_user1()
    ch1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': ch1['channel_id'],
        'message': 'To manage the transition from trimesters to hexamesters in 2020,'+
                   'UNSW has established a new focus on building an in-house digital'+
                   ' collaboration and communication tool for groups and teams to support'+
                   ' the high intensity learning environment. Rather than re-invent the wheel,'+
                   ' UNSW has decided that it finds the functionality of Slack to be nearly'+
                   ' exactly what it needs. For this reason, UNSW has contracted out Lit Pty '+
                   'Ltd (a small software business run by Hayden) to build the new product. In'+
                   ' UNSWs attempt to connect with the younger and more "hip" generation that'+
                   ' fell in love with flickr, Tumblr, etc, they would like to call the new '+
                   'UNSW-based product slackr. Lit Pty Ltd has sub-contracted two software '+
                   'firms: Catdog Pty Ltd (two software developers, Sally and Bob, who will ' +
                   'build the initial web-based GUI). YourTeam Pty Ltd (a team of talented '+
                   'misfits completing COMP1531 in 20T1), who will build the backend python '+
                   'server and possibly assist in the GUI later in the project. In summary, '+
                   'UNSW contracts Lit Pty Ltd, who sub contracts:Catdog (Sally and Bob) '+
                   'for front end work, YourTeam (you and others) for backend work'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/send",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_unauthorised():
    '''
    Test a user sending a message into a channel in which they are not a part of
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    ch1 = create_ch1(user1)

    data = json.dumps({
        'token': user2['token'],
        'channel_id': ch1['channel_id'],
        'message': 'testing'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/send",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
