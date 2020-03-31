import pytest
from error import InputError
from user import user_profile_sethandle
from auth import auth_register
from user import users_all, search
from channels import channels_create
from message import message_send
from test_helper_functions import reg_user1, reg_user2, register_and_create, send_msg1
from other import workspace_reset


'''
#############################################################
#                   USERS_ALL                               #
#############################################################
'''
    
def test_users_all_working():
    
    workspace_reset()
    
    details1 = reg_user1()
    token1 = details1['token']
    uid1 = details1['u_id']
    user_profile_sethandle(token1, "handleOne")
    
    details2 = reg_user2()
    token2 = details2['token']
    uid2 = details2['u_id']
    user_profile_sethandle(token2, "handleTwo")
    
    # test if the function works properly
    list_user = users_all(token1)
    # List of dictionaries, where each dictionary contains types 
    # u_id, email, name_first, name_last, handle_str
    
    #userOne = list_user
    #print (userOne)
    
    #assert (userOne['u_id'] == uid1)
    #assert (userOne['email'] == "email1@gmail.com")
    #assert (userOne['name_first'] == "firstOne")
    #assert (userOne['name_last'] == "lastOne")
    #assert (userOne['handle_str'] == "handleOne")
    
    print(list_user)
    assert list_user == {'users': [{
        'u_id': 'uid1',
        'email' : 'Kennan@gmail.com',
        'name_first': 'Kennan',
        'name_last': 'Wong'
        'handle_str': "handleOne",
        },{ 
        'u_id': 'uid2',
        'email' : 'Cindy@gmail.com',
        'name_first': 'Cindy',
        'name_last': 'Tran'
        'handle_str': "handleTwo",
        }]
    }
    
    
'''
#############################################################
#                   SEARCH                                  #
#############################################################
'''

def test_search_one_channel():
    
    #create user
    workspace_reset()
    
    
    reg_cre = register_and_create()
    user = reg_cre['user']
    chan = reg_cre['channel']
    
    msg_test = send_msg1(user, chan)
    
    #test to see if search will return the messages that have helloworld
    query = "Testing"
    messages = search(token, query)

    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == "Testing"
        
def test_search_multiple_channel():
    #create user
    workspace_reset()
    register = reg_user1()
    
    token = register['token']
    u_id = register['u_id']
    
    payload1{
        'token' : register['token'],
        'name': 'firstChannel',
        'is_public': True
    
    }
    
    channel_id = channels_create(payload1)
    payload2{
        'token':register['token'],
        'channel_id': channel_id,
        'message' : 'HelloWorld'
    
    }
    
    #make channel for user to be in and send message
    message_id = message_send(payload2)
    
    #make another channel for user to be in and send message
    payload3{
        'token' : register['token'],
        'name': 'firstChannel',
        'is_public': True
    
    }
    channel_id2 = channels_create(payload3)
    
    payload4{
        'token':register['token'],
        'channel_id': channel_id2,
        'message' : 'HelloWorld'
    
    }  
    
    message_id2 = message_send(payload4)
    
    #test to see if search will return the messages that have helloworld
    query = "HelloWorld"
    
    payload5{
        'token':register['token'],
        'query': query    
    }
    
    messages = search(payload5)
    
    counter = 0
    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == "HelloWorld"
        counter=+1
        
    assert (counter == 2)
        
        
def test_search_short_query():
    
    #create user

    #make channel for user to be in and send message
    
    workspace_reset()
    register = reg_user1()
    
    token = register['token']
    u_id = register['u_id']
    
    payload = {
        'token' : register['token'],
        'name': 'firstChannel',
        'is_public': True
    }
    channel_id = channels_create(payload)
    
    payload1{
        'token':register['token'],
        'channel_id': channel_id,
        'message' : ""
    
    } 
    message_send(payload1)
       
    
    #test to see if search will return the messages that have ""
    query = ""
    
    payload2{
        'token':register['token'],
        'query': query    
    }
    
    messages = search(payload2)

    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == ""
    
def test_search_no_message():
    
    #create user
    register = reg_user1()
    
    token = register['token']
    u_id = register['u_id']

    #make channel for user to be in and send message
    channel_id = channels_create(token, "validChannel", True)
    message_send(token, channel_id['channel_id'], "HelloWorld")

    #test to see if search will return the messages that have helloworld
    query = "NotAMessage"
    
    messages = search(token, query)
    
    counter = 0
    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == "NotAMessage"
        counter=+1
        
    assert (counter == 0)
        
    


