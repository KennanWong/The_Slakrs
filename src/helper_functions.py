'''
A file thatcontains helper function to simplify code and
do repetitive tasks
'''

import re
import hashlib
from datetime import datetime
from error import InputError
from data_stores import get_auth_data_store, get_channel_data_store
from data_stores import get_messages_store

MSG_COUNT = 1


def generate_token(u_id):
    '''
    Function to generate a token
    '''
    return hashlib.sha256(str(u_id).encode()).hexdigest()


def create_message():
    '''
    Function to generate a blank message dictionary
    '''
    global MSG_COUNT
    message = {
        'channel_id' : 0,
        'message_id' : MSG_COUNT,
        'u_id' : 0,
        'message': '',
        'time_created':datetime.now().time(),
        'reacts': [],
        'is_pinned': False,
    }
    MSG_COUNT = MSG_COUNT + 1
    return message

def get_channel(channel_id):
    '''
    Function to return the channel data suing a channel_id
    '''
    all_channels = get_channel_data_store()

    for i in all_channels:
        if i['channel_id'] == int(channel_id):
            return i
    raise InputError(description='Invalid channel_id')

def get_user_token(token):
    '''
    Function to validate a token and returns the users info
    otherwise raises an error
    '''
    auth_store = get_auth_data_store()
    for i in auth_store:
        if i['token'] == token:
            return i
    raise InputError(description='Invalid Token')

def test_email(email):
    '''
    Functionto to test if an email is valid, courtesy of geeksforgeeks.org
    '''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return email
    else:
        raise InputError(description='Invalid Email')


def test_in_channel(u_id, channel):
    '''
    Function to test if a user is part of a channel
    '''
    for i in channel['members']:
        if i['u_id'] == u_id:
            return True
    for i in channel['owners']:
        if i['u_id'] == u_id:
            return True
    return False

def find_message(message_id):
    '''
    Function to find a message and return its details
    '''
    messages_store = get_messages_store()
    for i in messages_store:
        if i['message_id'] == int(message_id):
            return i

    raise InputError(description='Message not found')
            

# function to see if a user is an owner of a channel
def check_owner(user, channel):
    '''
    Function to see if a user is an owner of a channel
    '''
    for i in channel['owners']:
        if i['u_id'] == user['u_id']:
            return True
    
    return False


# Function to check valid userID
def is_valid_user_id(u_id):
    auth_store = get_auth_data_store()
    for user in auth_store:
        if user['u_id'] == u_id:
            return 1
    else:
        raise InputError(description='Invalid u_id')



# Fucntion to get details of a user
def user_details(u_id):
    auth_store = get_auth_data_store()
    for user in auth_store:
        if u_id == user['u_id']:
            return {
                'u_id': u_id,
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }
    return False


#to get current time and add seconds, courtesy of stackoverflow
def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate - fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()
    return False


# function to format a list of dictionaries into a members data type

def format_to_members(members):
    '''
    Function to format a list of dictionaries into a members data type
    '''
    members = []
    for i in members:
        add = {
            'u_id':i['u_id'],
            'name_first':i['name_first'],
            'name_last':i['name_last']
        }
        members.append(add)
    return members

def get_message_count():
    '''
    Function to get message_count
    '''
    global MSG_COUNT
    return MSG_COUNT


def append_later(argument):
    '''
    Function for send later, to automatically generate a message
    and append it
    '''
    message_id = argument
    message = find_message(message_id)
    channel = get_channel(message['channel_id'])

    # append it to the channels file
    channel['messages'].append(message)

    for msg in channel['messages']:
        print(msg['message'])

    return

#function to see if a u_id is valid
def validate_uid(u_id):
    user_store = get_auth_data_store()
    for i in user_store:
        if i['u_id'] == u_id:
            return True
    
    return False

#function returns 1 if email has not been used before    
def check_used_email(email):
    email_store = get_auth_data_store()
    for i in email_store:
        if i['email'] == email:
            raise InputError(description='Email is already in use')
    else:
        return 1
        
#function returns 1 if handle has not been used before    
def check_used_handle(handle_str):
    handle_store = get_auth_data_store()
    for i in handle_store:
        if i['handle_str'] == handle_str:
            raise InputError(description='Handle is already in use')
    else:
        return 1
        
# function to validate a token and returns the users info
# otherwise raises an error
def get_user_uid(u_id):
    auth_store = get_auth_data_store()
    user = {}
    for i in auth_store:
        if i['u_id'] == u_id:
            user = i
    if user != {}:
        return user
    else:
        raise InputError(description='Invalid u_id')
def reset_message_count():
    global MSG_COUNT
    MSG_COUNT = 1
    return
