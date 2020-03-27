
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

# function to format a list of dictionaries into a members data type
def format_to_members(members):
    members = []
    for i in members:
        add = {
            'u_id':i['u_id'],
            'name_first':i['name_first'],
            'name_last':i['name_last']
        }
        members.append(add)
    return members

# get message count
def get_message_count():
    global msg_count
    return msg_count

# helper function for send later, to automatically generate a message 
# and append it
def append_later(argument):
    message_id = argument
    message = find_message(message_id)
    channel = get_channel(message['channel_id'])

    # append it to the channels file
    channel['messages'].append(message)

    for msg in channel['messages']:
        print(msg['message'])

    return