
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

# function to validate a token and returns the users info
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

# function to find a message and return its details
def find_message(message_id):
    messages_store = get_messages_store()
    for i in messages_store:
        if i['message_id'] == int(message_id):
            return i
    
    raise InputError(description='Message not found')

# function to see if a user is an owner of a channel
def check_owner(user, channel):
    for i in channel['owners']:
        if i['u_id'] == user['u_id']:
            return True
    
    return False
    
#function to see if a u_id is valid
def validate_uid(u_id):
    user_store = get_auth_data_store()
    for i in user_store:
        if i['u_id'] == u_id:
            return True
    
    return False
    
