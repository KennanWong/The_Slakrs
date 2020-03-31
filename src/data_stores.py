
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

MSG_COUNT=1
# Function to generate gloabl auth_data store
def get_auth_data_store():
    global auth_data
    return auth_data

# Function to get channel data store
def get_channel_data_store():
    global channels_store
    return channels_store

# Function to get the mssage_data store
def get_messages_store():
    global messages_store
    return messages_store

def get_message_count():
    global MSG_COUNT
    return MSG_COUNT

def reset_auth_store():
    global auth_data
    auth_data = []
    return

def reset_channel_data_store():
    global channels_store
    channels_store = []
    return

def reset_messages_store():
    global messages_store
    messages_store = []
    return
