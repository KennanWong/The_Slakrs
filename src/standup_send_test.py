import pytest

import standup
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store
import time
from datetime import datetime, timedelta
from helper_functions import addSecs

#############################################################
#                   STANDUP_SEND                            #
#############################################################
def test_send():
    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)

    payload2 = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    result2 = standup.active(payload2)

    standup.send({
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'test'
    })

def test_invalid_id():

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']
    

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)

    payload2 = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    result2 = standup.active(payload2)

    with pytest.raises(InputError):
        standup.start ({
            'token': user['token'],
            'channel_id': 100,
            'message': 'test'
        })

def test_message_too_long():

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']
    

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)

    payload2 = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    result2 = standup.active(payload2)

    with pytest.raises(InputError): 
        standup.send({
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message':  'To manage the transition from trimesters to hexamesters in 2020,'+
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
        })

def test_no_active():
    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    with pytest.raises(InputError):
        standup.send({
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'message': 'test'
        })

def test_unauthor_member():
    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    user2 = reg_user2()

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)

    payload2 = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    result2 = standup.active(payload2)

    with pytest.raises(AccessError):
        standup.send({
            'token': user2['token'],
            'channel_id': channel['channel_id'],
            'message': 'test'
        })