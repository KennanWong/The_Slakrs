import re
import hashlib
from datetime import datetime
from error import InputError
from data_stores import get_auth_data_store, get_channel_data_store

# Function to generate a token
def generate_token(u_id):
    return hashlib.sha256(str(u_id).encode()).hexdigest()

# Function to generate a blank message dictionary
def create_message():
    message = {
        'message_id' : 0,
        'u_id' : 0, 
        'message': '',
        'time_created':datetime.now().time(),
        'reacts': [],
        'is_pinned': False,
    }
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

# Function to check valid userID
def is_valid_user_id(u_id):
    auth_store = get_data_auth_store
    for user in auth_store:
        if user['u_id'] == u_id:
            return 1
    else:
        raise InputError(description='Invalid u_id')