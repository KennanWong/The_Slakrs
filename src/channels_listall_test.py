import pytest

import message
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store


#############################################################
#                   CHANNELS_LISTALL                        #
#############################################################
def test_listall():

    workspace_reset()
    channel_store = get_channel_data_store()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']
    
    user2 = reg_user2()

    #user2 creating a channel
    payload1 = {
        'token': user2['token'],
        'name': 'Slackrs',
        'is_public': True
    }

    
    token = user1['token']
    
    channels.Listall(token)