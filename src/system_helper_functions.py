'''
A series of helper functions to automate server testing
'''
import string
import random
import urllib
import json

BASE_URL = 'http://127.0.0.1:8080'

def reset_workspace():
    '''
    Helper function to run the /workspace/reset request
    '''
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type':'application/json'}
    ))
    return

def reg_user1():
    '''
    Registers a user and returns the reponse from the request
    '''
    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    response = json.load(req)
    return response

def logout_user1(token):
    '''
    Function to logout a user, given a token
    '''
    data = json.dumps({
        'token': token
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/logout",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    return

def reg_user2():
    '''
    Registers a user and returns the reponse from the request
    '''
    data = json.dumps({
        'email' : 'Dean@gmail.com',
        'password': 'Wong123',
        'name_first': 'Dean',
        'name_last': 'Wong'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    response = json.load(req)
    return response

def reg_user3():
    '''
    Registers a user and returns the reponse from the request
    '''
    data = json.dumps({
        'email' : 'Thomas@gmail.com',
        'password': 'Shelby123',
        'name_first': 'Thomas',
        'name_last': 'Shelby'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    response = json.load(req)
    return response

def create_ch1(user1):
    '''
    Function returns the payload of channels/create request
    '''
    data = json.dumps({
        'token':user1['token'],
        'name': 'new_channel',
        'is_public': True
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)
    return payload

def create_pvt_ch(user1):
    '''
    Function returns the payload of channels/create request
    '''
    data = json.dumps({
        'token':user1['token'],
        'name': 'new_channel',
        'is_public': False
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)
    return payload

def send_msg1(user, channel):
    '''
    Function to send a message to a specified channel
    Returns the payload of a message_send request
    '''
    data = json.dumps({
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'testing'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)
    return payload


def invite_to_channel(inviter, invitee, channel):
    data = json.dumps({
        'token': inviter['token'],
        'channel_id': channel['channel_id'],
        'u_id': invitee['u_id']
    }).encode('utf-8')
    
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/invite", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))
    return

def react_to_msg(user, message, react_id):
    '''
    Function to have a 'user' to react to a 'message' with react_id
    'react_id'
    '''
    data = json.dumps({
        'token': user['token'],
        'message_id': message['message_id'],
        'react_id': react_id
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/react",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    return

def send_a_message(user, channel, message):
    '''
    Function to send a specific message to a specified channel
    Returns the payload of a message_send request
    '''
    data = json.dumps({
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': message
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)
    return payload

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
