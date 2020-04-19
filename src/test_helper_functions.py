'''
Set of functions used for testing
'''
import string
import random
import auth
import message
import channels
import channel

#pylint compliant

# function to register user1
def reg_user1():
    'registers first user'
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    user1 = auth.register(payload)
    return user1

# function to register user2
def reg_user2():
    'registers second user'
    payload = {
        'email' : 'Cindy@gmail.com',
        'password': 'Tran123',
        'name_first': 'Cindy',
        'name_last': 'Tran'
    }
    user2 = auth.register(payload)
    return user2

# function to register user3
def reg_user3():
    'registers third user'
    payload = {
        'email' : 'Thomas@gmail.com',
        'password': 'Shelby123',
        'name_first': 'Thomas',
        'name_last': 'Shelby'
    }
    user3 = auth.register(payload)
    return user3

# function used to register a user and then create a channel
def register_and_create():
    'registers first user and creates a chanenl'
    payload1 = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    result1 = auth.register(payload1)

    payload2 = {
        'token' : result1['token'],
        'name': 'firstChannel',
        'is_public': True
    }
    new_channel = channels.create(payload2)
    return {
        'user':result1,
        'channel':new_channel
    }

def send_msg1(user1, channel1):
    '''
    Helper function to send a message
    '''
    payload = {
        'token':user1['token'],
        'channel_id': channel1['channel_id'],
        'message' : 'testing'
    }

    message_test = message.send(payload)
    return message_test

def create_ch1(user):
    '''
    Helper function to create a channel
    '''
    payload = {
        'token' : user['token'],
        'name': 'firstChannel',
        'is_public': True
    }
    new_channel = channels.create(payload)
    return new_channel


def invite_to_ch1(user1, user2, ch1):
    '''
    Function for user1 to invite user2 to
    channel
    '''
    channel.invite(user1['token'], ch1['channel_id'], user2['u_id'])

    return

def react_to_msg(react_id, msg, user):          #pylint: disable=W0613, R1711
    '''
    Function to react to 'message' with
    react id of 'react_id'
    '''
    message.react({
        'token': user['token'],
        'message_id': msg['message_id'],
        'react_id': 1
    })

    return

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    'generates a 6 character reset code'
    return ''.join(random.choice(chars) for _ in range(size))
