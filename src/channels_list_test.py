import pytest

import message
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store


#def test_list_channel_one():
#    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
#    token1 = results['token']
#    u_id1 = results['u_id']

    #returns channel_id
#    channel_info1 = channels_create(token1, 'Slakrs', True)

 #   my_channel_id1 = channel_info1['channel_id']


 #   assert (channels_list(token1)["channels"][0]['channel_id']) == my_channel_id1

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
    
  