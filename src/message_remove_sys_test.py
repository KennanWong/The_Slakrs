'''
Pytest file to test message_react on a system level
'''
import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1


#############################################################
#                   MESSAGE_REMOVE                          #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_remove1():
    '''
    Test a valid use of message.remove
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id']
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/remove",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'DELETE'
    response = json.load(urllib.request.urlopen(req))

    assert response == {}

'''
def test_remove2():
    # the admin of a channel attempting to remove another users emssage
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user2, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id']
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/remove", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'DELETE'
    response = json.load(urllib.request.urlopen(req))

    assert response == {}
'''

def test_no_msg():
    '''
    Attempting to remove a message that has been already removed or does
    not exist causing an input error
    '''
    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token': user1['token'],
        'message_id': 6
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/remove",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'DELETE'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

'''
def test_unauth_remove1():

    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id']
    }).encode('utf-8')

    req = urllib.request.Request(
            f"{BASE_URL}/message/remove", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        )
    req.get_method = lambda: 'DELETE'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
'''

def test_unauth_remove2():
    '''
    Attempting remove another users message in a channel
    they are not a part of
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id']
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/remove",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'DELETE'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
