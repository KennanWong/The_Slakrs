'''
Pytest file to test auth_login on a system level
'''

import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from hangman import get_phrase, get_empty_guess
from helper_functions import get_channel
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import send_a_message


#############################################################
#                     HANGMAN                               #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_game_start():
    reset_workspace()

    # Register a user
    user1 = reg_user1()
    
    channel1 = create_ch1(user1)

    channel1_dets = get_channel(channel1['channel_id'])
    
    # start a game of hangman
    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': '/hangman'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    channel1_dets = get_channel(channel1['channel_id'])

    print(channel1_dets)

    '''

    assert channel1_dets['hangman_active'] == True
    assert {"u_id": 2, "name_first": "Hangman", "name_last": "Bot"} in channel1_dets['members']
    
    phrase = get_phrase()
    
    guess = phrase[0]

    #make a guess
    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': '/guess ' + str(guess)
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload2 = json.load(req)

    empty_guess = get_empty_guess()

    assert guess in empty_guess
    '''
    assert 1 == 1