'''
This file contains our data and data structure for the server. Responsible for creating, loading,
saving and generating the data stores
'''


# pylint: disable=W0603
# pylint: disable=W0702
# pylint: disable=C0103
# pylint: disable=R1711
import json
import threading

#pylint compliant
#############################################################
#                   DATA_STORES                             #
#############################################################

channels_store = []

auth_store = []

messages_store = []

# This file contains our data and data structure for the server
channels_store = [
    # {
    #     'channel_id'
    #     'name'
    #     'is_public'
    #     'members':[
    #{
    #             u_id
    #             name_first
    #             Name_last
    # 	    }
    #     ]
    #     'owners':[
    #         {
    #             u_id
    #             name_first
    #             Name_last
    # 	    }
    #     ]
    #     'messages': [
    #         {
    #             channel_id
    #             message_id
    #             u_id,
    #             message
    #             time_created
    #             reacts
    #             is_pinned
    #         }
    #     ]
    #       'standup': [
    #           {
    #              is_active
    #              messages
    #              time_finish
    #           }
    #        ]
    #     }
]


auth_data = [
    # new_user = {
    #     'u_id' : u_id,
    #     'email': email,
    #     'password': password,
    #     'name_first': first_name,
    #     'name_last': last_name,
    #     'handle_str': handle.lower(),
    #     'token': token,
    #     'status' : LOGGED_ON,
    #     'messages':[],
    #     'permission_id': 2,
    #     'slack_owner' : False
    # }
]

messages_store = [
    # 'channel_id'
    # 'message_id'
    # 'u_id,
    # 'message'
    # 'time_created'
    # 'reacts'
        # {
        #     'react_id'
        #     'u_ids' # a list of u_id
        #     'is_user_reacted'
        # }
    # 'is_pinned'
]

reset_data = [
    #'email':
    # 'reset_code':
]

MSG_COUNT = 1
# Function to generate gloabl auth_data store
def get_auth_data_store():
    '''
    Function to generate gloabl auth_data store
    '''
    global auth_store
    if len(auth_store) == 0:                #pylint: disable = C1801
        # initial startup of server, load up previous save
        try:
            with open('auth_data_store.json', 'r') as FILE:
                auth_store = json.load(FILE)
        except:
            pass
    return auth_store

def get_channel_data_store():
    '''
    Function to get channel data store
    '''
    global channels_store
    if len(channels_store) == 0:            #pylint: disable = C1801
        # initial startup of server, load up previous save
        try:
            with open('channel_data_store.json', 'r') as FILE:
                channels_store = json.load(FILE)
        except:
            pass
    return channels_store

def get_messages_store():
    '''
    Function to generate messages_store
    '''
    global messages_store
    if len(messages_store) == 0:                        #pylint: disable = C1801
        # initial startup of server, load up previous save
        try:
            with open('messages_data_store.json', 'r') as FILE:
                messages_store = json.load(FILE)
        except:
            pass
    return messages_store

#Function to get reset data store
def get_reset_code_store():
    'saves the users email and reset code for those who request a reset code'
    global reset_data
    return reset_data

def get_message_count():
    'This retrieves the message count for the server'
    global MSG_COUNT
    return MSG_COUNT

def reset_auth_store():
    '''
    Function to reset the auth store to an empty list
    '''
    global auth_store
    auth_store = []
    save_auth_store()
    return

def reset_channel_data_store():
    '''
    Function to reset the channel store to an empty list
    '''
    global channels_store
    channels_store = []
    save_channel_store()
    return

def reset_messages_store():
    '''
    Function to reset the messages store to an empty list
    '''
    global messages_store
    messages_store = []
    save_messages_store()
    return

def save_auth_store():
    '''
    Function to save the auth store to a .json file
    '''
    global auth_store
    with open('auth_data_store.json', 'w+') as AUTH_FILE:
        json.dump(auth_store, AUTH_FILE)
    return

def save_channel_store():
    '''
    Function to save the channel store to a .json file
    '''
    global channels_store
    with open('channel_data_store.json', 'w+') as CHANNEL_FILE:
        json.dump(channels_store, CHANNEL_FILE)
    return

def save_messages_store():
    '''
    Function to save the messages store to a .json file
    '''
    global messages_store
    with open('messages_data_store.json', 'w+') as MESSAGE_FILE:
        json.dump(messages_store, MESSAGE_FILE)

# save all data stores:
def save_data_stores():
    '''
    Function to save all the data stores to their .json file
    '''
    get_auth_data_store()
    save_auth_store()
    get_channel_data_store()
    save_channel_store()
    get_messages_store()
    save_messages_store()
    threading.Timer(60.0, save_data_stores).start()
    return
