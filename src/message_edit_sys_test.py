'''
Pytest file to test message_edit on a system level
'''

# pylint: disable=W0611

import urllib
import json
from urllib.error import HTTPError

import flask
import pytest

from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1, invite_to_channel


#############################################################
#                   MESSAGE_EDIT                            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_edit1():
    '''
    Test valid use of message.edit where someone is editing their
    own message
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/edit",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))

    assert response == {}


def test_edit2():
    '''
    The owner of a slack is editing a message
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user2, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/edit",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))

    assert response == {}

def test_edit3():
    '''
    Someone attempts to edit a message by replacing it witha a blank string
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': ''
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/edit",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))

    assert response == {}

def test_unauth_edit1():
    '''
    Someone who is not an owner is attempting to edit a message
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/edit",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))


def test_unauth_edit2():
    '''
    Someone attempting to edit a message in a channel they are not a part of
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/message/edit",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
