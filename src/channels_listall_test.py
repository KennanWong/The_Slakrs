import pytest

import message
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store


#def test_listall_and_details():
 #   results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
  # u_id1 = results['u_id']
#
 #   result2 = auth_register("sidsat@gmail.com", '123!Asdf', 'Sid', 'Sat')
  #  token2 = results['token']
   # u_id2 = results['u_id']
#
 #   channel_info1 = channels_create(token1, 'Slakrs', True)
  #  channel_info2 = channels_create(token2, 'Kings Landing', True)
#
 #   all_channels = channels_listall(token2)
#
 #   flag = 0
  #  j = 0
#
 #   for i in all_channels:
  #      if (channel_info1 or channel_info2) == all_channels[j]:
   #         flag = 1   
    #assert flag == 1


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