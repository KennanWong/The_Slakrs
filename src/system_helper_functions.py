import pytest
import urllib
import json
import flask

import server

BASE_URL = 'http://127.0.0.1:8080'

def reset_workspace():
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data = [],  
        headers = {'Content-Type':'application/json'}
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
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))

    response = json.load(req)
    return response

