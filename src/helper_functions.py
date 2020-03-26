import re
import hashlib
from datetime import datetime
from error import InputError
from data_stores import get_auth_data_store, get_channel_data_store, get_messages_store

msg_count = 1

# Function to generate a token
def generate_token(u_id):
    return hashlib.sha256(str(u_id).encode()).hexdigest()

# Function to generate a blank message dictionary
def create_message():
    global msg_count
    message = {
        'channel_id' : 0,
        'message_id' : msg_count,
        'u_id' : 0, 
        'message': '',
        'time_created':datetime.now().time(),
        'reacts': [],
        'is_pinned': False,
    }
    msg_count = msg_count + 1
    return message

# Function to return the channel data suing a channel_id
def get_channel(channel_id):
    all_channels = get_channel_data_store()

    for i in all_channels:
        if i['channel_id'] == int(channel_id):
            return i
    raise InputError(description='Invalid channel_id')

# Function to validate a token and returns the users info
# otherwise raises an error
def get_user_token(token):
    auth_store = get_auth_data_store()
    user = {}
    for i in auth_store:
        if i['token'] == token:
            user = i
    if user != {}:
        return user
    else:
        raise InputError(description='Invalid Token')

# to test if an email is valid, courtesy of geeksforgeeks.org
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return email
    else:
        raise InputError(description='Invalid Email')

# function to test if a user is part of a channel
def test_in_channel(u_id, channel):
    for i in channel['members']:
        if i['u_id'] == u_id:
            return True
    for i in channel['owners']:
        if i['u_id'] == u_id:
            return True
    return False

# Function to find a message and return its details
def find_message(message_id):
    messages_store = get_messages_store()
    for i in messages_store:
        if i['message_id'] == int(message_id):
            return i
    
    raise InputError(description='Message not found')

# Function to see if a user is an owner of a channel
def check_owner(user, channel):
    for i in channel['owners']:
        if i['u_id'] == user['u_id']:
            return True
    
    return False

# Function to check valid userID
def is_valid_user_id(u_id):
    auth_store = get_data_auth_store
    for user in auth_store:
        if user['u_id'] == u_id:
            return 1
    else:
        raise InputError(description='Invalid u_id')

# Function to get userID from token
def user_id_from_token(token):
    auth_store = get_data_auth_store
    for user in auth_store:
        if token == user['token']:
            return user['u_id']
    else:
        raise InputError(description='Could not find u_id')

# Fucntion to get details of a user
def user_details(u_id):
    for user in auth_store:
        if u_id == user['u_id']:
            return {
                'u_id': u_id,
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }
