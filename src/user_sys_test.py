'''
Pytest file to test functionality of user_ functions on a system 
level
'''

import pytest
import urllib
import json
import flask
from urllib.error import HTTPError

import server
import user
from system_helper_functions import reset_workspace, reg_user1
from data_stores import get_auth_data_store, reset_auth_store
from helper_functions import get_user_token
from error import InputError
from system_helper_functions import reg_user1, reg_user2, send_msg1



'''
#############################################################
#                   USER_PROFILE                            #
#############################################################
'''

BASE_URL = 'http://127.0.0.1:3542'

def test_profile_working():
    # create a user

    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token': user1['token'],
        'u_id': user1['u_id']
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))

    assert response['email'] == 'Kennan@gmail.com'
    assert response['name_first'] == 'Kennan'
    assert response['name_last'] == 'Wong'

def test_profile_invalid_u_id():
    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token': user1['token'],
        'u_id': 3
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

def test_user_profile_setname_working():
    reset_workspace()   
        
    
    details = reg_user1()
      
    uid = details['u_id']
    
    data = json.dumps({
        'token': details['token'],
        'name_first': "Jeff",
        'name_last': "Son"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))   
    assert response == {}
    
    
def test_user_profile_setname_short():

    reset_workspace()   
        
    
    details = reg_user1()
      
    uid = details['u_id']
    
    data = json.dumps({
        'token': details['token'],
        'name_first': "",
        'name_last': "Son"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        response = json.load(urllib.request.urlopen(req))
 

'''
#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################
''' 
    
def test_user_profile_setemail_working():
    reset_workspace()   
      
    details = reg_user1()
      
    uid = details['u_id']
    
    data = json.dumps({
        'token': details['token'],
        'email': "varun@gmail.com"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setemail",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))   
    assert response == {}
    
    
def test_user_profile_setemail_inval1():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'email': "varungmail.com"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        response = json.load(urllib.request.urlopen(req))
        
        
def test_user_profile_setemail_inval2():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'email': ".com"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        response = json.load(urllib.request.urlopen(req))
        
        
def test_user_profile_setemail_inval3():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'email': "varunkash@"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        response = json.load(urllib.request.urlopen(req))


'''
#############################################################
#                  USER_PROFILE_SETHANLE                    #
#############################################################
'''
    
def test_user_profile_sethandle():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'handle_str': "validhandle"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/sethandle",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))   
    assert response == {}
    

def test_user_profile_sethandle_invalhandle():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'handle_str': "A"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/sethandle",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))   
    assert response == {}
    
def test_user_profile_sethandle_invalhandle2():

    reset_workspace()   
            
    details = reg_user1()
    string_50 = "a" * 50
    data = json.dumps({
        'token': details['token'],
        'handle_str': string_50
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/profile/sethandle",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    response = json.load(urllib.request.urlopen(req))   
    assert response == {}


