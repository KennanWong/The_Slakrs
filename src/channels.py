# This file contains the implementation of all 'channel_' functions for the
# server

from error import InputError
from helper_functions import get_user_token
from data_stores import get_channel_data_store

#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################

def create(payload):
    channel_store = get_channel_data_store()
    channel_owner_info = {}
    new_channel_info ={}
   
    user = get_user_token(payload['token'])
    
    new_channel_info = {}
    channel_owner_info = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
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