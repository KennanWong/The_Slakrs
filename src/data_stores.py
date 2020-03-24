
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
 	# 	        Handle_str
 	# 	    }
    #     ] 
    #     'owners':[
 	#         {
    #             u_id
    #             name_first
    #             Name_last
 	# 	        Handle_str
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
    # }
]


auth_data = [
    # user_data :{
    #     'u_id' : u_id,
    #     'email': email,
    #     'name_first': first_name,
    #     'name_last': last_name,
    #     'handle_str': handle.lower(),
    #     'password': password,
    #     'token': token,
    #     'status' : LOGGED_ON
    #     'messages' : []
    #     'channels': []
    # }
]

messages_store = [
    # 'channel_id'
    # 'message_id'
    # 'u_id, 
    # 'message'
    # 'time_created'
    # 'reacts'
    # 'is_pinned'
]


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