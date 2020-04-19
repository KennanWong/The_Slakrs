'This file contains the implementation of all channels functions for the server'


from error import InputError
from helper_functions import get_user_token, test_in_channel, get_user_from
from data_stores import get_channel_data_store, save_channel_store

#pylint compliant
#############################################################
#                   CHANNELS_CREATE                         #
#############################################################

def create(payload):
    'implementations of channels create function'
    channel_store = get_channel_data_store()
    channel_owner_info = {}
    new_channel_info = {}

    user = get_user_token(payload['token'])

    new_channel_info = {}
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
                'standup' : {
                    'is_active': False,
                    'messages': [],
                    'time_finish': [],
                },
                'hangman_active': False
            }
        else:
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name': name,
                'is_public': False,
                'members':[],
                'owners': [],
                'messages': [],
 	            'standup' : {                       # pylint: disable=C0330
                    'is_active': False,             # pylint: disable=C0330
                    'messages': [],                 # pylint: disable=C0330
                    'time_finish': [],              # pylint: disable=C0330
                },                                  # pylint: disable=C0330
                'hangman_active': False
            }
    else:
        raise InputError(description='Name is too long')

    new_channel_info['owners'].append(channel_owner_info)

    channel_store.append(new_channel_info)
    save_channel_store()

    return new_channel_info

#############################################################
#                   CHANNELS_LIST                           #
#############################################################

def List(token): # pylint: disable=C0103
    'implementations of channels all functions'
    channel_store = get_channel_data_store()

    channels = []
    channel_info = {}

    user = get_user_token(token)

    u_id = user['u_id']

    for channel in channel_store:
        if test_in_channel(u_id, channel):
            channel_info = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            channels.append(channel_info)
    print(channels)

    return channels

#############################################################
#                   CHANNELS_LISTALL                        #
#############################################################


def Listall(token): # pylint: disable=W0613, C0103
    'implementations of channels listall function'
    channel_store = get_channel_data_store()

    user = get_user_from('token', token)
    channels_return = []
    channel_info = {}

    if len(channel_store) == 0: # pylint: disable=C1801
        # the channel store is empty
        return channels_return

    for channel in channel_store:
        channel_info = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        if channel['is_public']:
            channels_return.append(channel_info)
        elif test_in_channel(user['u_id'], channel):
            channels_return.append(channel_info)

    return channels_return
