import pytest

import message
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store



#############################################################
#                   CHANNELS_LIST                           #
#############################################################
def test_list():

    workspace_reset()
    channel_store = get_channel_data_store()


    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    
    token = user['token']
    
    channels.List(token)
    
  