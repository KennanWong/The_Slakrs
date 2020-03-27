# This file contains the implementation of all 'channel_' functions for the
# server

from error import InputError
from helper_functions import get_user_token
from data_stores import get_channel_data_store
from helper_functions import test_in_channel

#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################

def create(payload):
    channel_store = get_channel_data_store()
    channel_owner_info = {}
    new_channel_info = {}
   
    user = get_user_token(payload['token'])

    channel_owner_info = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        
    }
        
    if len(payload['name']) < 21:
        name = payload['name']
        if payload['is_public']: 
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name':  name,
                'is_public': True,
                'members':[],
                'owners':[],
                'messages': [],
            }
        else:
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name': name,
                'is_public': False,
                'members':[],
                'owners':[],
                'messages': [],
             }
    else: 
        raise InputError (description='Name is too long')
    new_channel_info['owners'].append(channel_owner_info)
    channel_store.append(new_channel_info)

    return new_channel_info


#############################################################
#                   CHANNELS_LIST                           #      
#############################################################

def List(payload):
    channel_store = get_channel_data_store()
   
    channels = []
    channel_info = {}

    user = get_user_token(payload['token'])
    

    u_id = user['u_id']

    for channel in channel_store:
        if test_in_channel(u_id, channel):
            channel_info = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
        channels.append(channel_info)
    
    return channels

#############################################################
#                   CHANNELS_LISTALL                        #      
#############################################################


def Listall(payload):
    
    channel_store = get_channel_data_store()

    channels_return = []
    channel_info = {}

    user = get_user_token(payload['token'])

    u_id = user['u_id']

    for channel in channel_store:
        channel_info = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
   
        channels_return.append(channel_info)

    return channels_return





