# import schedule
import json
import threading
# This file contains our data and data structure for the server
channels_store = [
    # {
    #     'channel_id'
    #     'name'
    #     'is_public'
    #     'members':[
 	# 	    {
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


auth_store = [
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

MSG_COUNT=1

# need to load up a copy of the auth_data_store
# then save this copy at reguilar intevals


# does not mean we do not need a global varaible, the global variable 



# Function to generate gloabl auth_data store
def get_auth_data_store():
    global auth_store
    if len(auth_store) == 0:
        # initial startup of server, load up previous save
        try:
            with open ('auth_data_store.json', 'r') as FILE: 
                auth_store = json.load(FILE)
        except:
            pass
    return auth_store

# Function to get channel data store
def get_channel_data_store():
    global channels_store
    if len(channels_store) == 0:
        # initial startup of server, load up previous save
        try:
            with open ('channel_data_store.json', 'r') as FILE: 
                channels_store = json.load(FILE)
        except:
            pass
    return channels_store

# Function to get the mssage_data store
def get_messages_store():
    global messages_store
    if len(messages_store) == 0:
        # initial startup of server, load up previous save
        try:
            with open ('messages_data_store.json', 'r') as FILE: 
                messages_store = json.load(FILE)
        except:
            pass
    return messages_store

def get_message_count():
    global MSG_COUNT
    return MSG_COUNT

def reset_auth_store():
    global auth_store
    auth_store = []
    save_auth_store()
    return

def reset_channel_data_store():
    global channels_store
    channels_store = []
    save_channel_store()
    return

def reset_messages_store():
    global messages_store
    messages_store = []
    save_messages_store()
    return

def save_auth_store():
    global auth_store
    print ('saved auth store')
    with open('auth_data_store.json', 'w+') as AUTH_FILE:
        json.dump(auth_store, AUTH_FILE)
    return

def save_channel_store():
    global channels_store
    print ('saved channel store')
    with open('channel_data_store.json', 'w+') as CHANNEL_FILE:
        json.dump(channels_store, CHANNEL_FILE)
    return

def save_messages_store():
    global messages_store
    print ('saved messages store')
    with open('messages_data_store.json', 'w+') as MESSAGE_FILE:
        json.dump(messages_store, MESSAGE_FILE)

# save all data stores:
def save_data_stores():
    get_auth_data_store()
    save_auth_store()
    get_channel_data_store()
    save_channel_store()
    get_messages_store()
    save_messages_store()
    print("save data stores")
    threading.Timer(60.0, save_data_stores).start()
    return

    