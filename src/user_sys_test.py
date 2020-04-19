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
import other
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

BASE_URL = 'http://127.0.0.1:2345'

def test_profile_working():
    # create a user

    reset_workspace()

    user1 = reg_user1()

    req = urllib.request.Request(
        f"{BASE_URL}/user/profile?token=6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b&u_id=1"
    )
    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))['user']

    assert response['email'] == 'Kennan@gmail.com'
    assert response['name_first'] == 'Kennan'
    assert response['name_last'] == 'Wong'

def test_profile_invalid_u_id():
    reset_workspace()

    user1 = reg_user1()

    req = urllib.request.Request(
        f"{BASE_URL}/user/profile?token=6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b&u_id=2"
    )

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
        'name_first': "I",
        'name_last': "Son"
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/setname",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
 

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
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))   
    
def test_user_profile_sethandle_invalhandle2():

    reset_workspace()   
            
    details = reg_user1()
    string_50 = "a" * 50
    data = json.dumps({
        'token': details['token'],
        'handle_str': string_50
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/sethandle",
        data=data,
        headers={'Content-Type':'application/json'}
    )
    req.get_method = lambda: 'PUT'
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))  



def test_users_all_working():
    reset_workspace()

    user1 = reg_user1()

    # get a users data
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile?token="+str(user1['token'])+"&u_id="+str(user1['u_id'])
    )
    req.get_method = lambda: 'GET'
    user1_dets = json.load(urllib.request.urlopen(req))


    req = urllib.request.Request(
        f"{BASE_URL}/users/all?token=6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    )
    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))['users']
    
    test_user = {
        'u_id': 1,
        'email': 'Kennan@gmail.com',
        'name_first': 'Kennan',
        'name_last': 'Wong',
        'handle_str': 'kennanwong',
        'profile_img_url':'https://img.buzzfeed.com/buzzfeed-static/static/2020-04/15/19/campaign_images/fdc9b0680e75/the-social-media-shame-machine-is-in-overdrive-ri-2-4824-1586980284-7_dblbig.jpg'
    }
    print(user1_dets)
    print(test_user)
    print(response)
    
    assert test_user in response
'''
#############################################################
#                  USER_PROFILE_UPLOADPHOTO                 #
#############################################################
'''

def test_user_uploadphoto_valurl():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'img_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg",
        'x_start': 1,
        'y_start': 1,
        'x_end': 1,
        'y_end': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/uploadphoto",
        data=data,
        headers={'Content-Type':'application/json'}
    )

    payload = json.load(req)

    assert details['img_url'] == payload['img_url']


def test_user_uploadphoto_invalurl():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details['token'],
        'img_url': "invalid.url.google",
        'x_start': 1,
        'y_start': 1,
        'x_end': 1,
        'y_end': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/uploadphoto",
        data=data,
        headers={'Content-Type':'application/json'}
    )

def test_user_uploadphoto_invaltoken():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': invalidtoken,
        'img_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg",
        'x_start': 1,
        'y_start': 1,
        'x_end': 1,
        'y_end': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/uploadphoto",
        data=data,
        headers={'Content-Type':'application/json'}
    )

def test_user_uploadphoto_invalborders():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details[token],
        'img_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg",
        'x_start': d,
        'y_start': adef,
        'x_end': aded,
        'y_end': pizza
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/uploadphoto",
        data=data,
        headers={'Content-Type':'application/json'}
    )

def test_user_uploadphoto_invalborderstwo():

    reset_workspace()   
            
    details = reg_user1()
    
    data = json.dumps({
        'token': details[token],
        'img_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg",
        'x_start': -50,
        'y_start': -50,
        'x_end': -50,
        'y_end': -50
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f"{BASE_URL}/user/profile/uploadphoto",
        data=data,
        headers={'Content-Type':'application/json'}
    )

