import pytest
from error import InputError
from user import user_profile_sethandle
from auth import auth_register
from other import users_all, search
from channels import channels_create
from message import message_send
'''
#############################################################
#                   USERS_ALL                               #
#############################################################
'''
    
def test_users_all_working():
    details1 = auth_register("email1@gmail.com", "password1", "firstOne", "lastOne")
    token1 = details1['token']
    uid1 = details1['u_id']
    user_profile_sethandle(token1, "handleOne")
    
    
    details2 = auth_register("email2@gmail.com", "password2", "firstTwo", "lastTwo")
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
        'u_id': uid1,
        'email': "email1@gmail.com",  
        'name_first': "firstOne", 
        'name_last': "lastOne", 
        'handle_str': "handleOne",
        },{ 
        'u_id': uid2,
        'email': "email2@gmail.com", 
        'name_first': "firstTwo", 
        'name_last': "lastTwo", 
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
    register = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
    token = register['token']
    u_id = register['u_id']

    #make channel for user to be in and send message
    channel_id = channels_create(token, "validChannel", True)
    message_send(token, channel_id['channel_id'], "HelloWorld")

    #test to see if search will return the messages that have helloworld
    query = "HelloWorld"
    messages = search(token, query)

    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == "HelloWorld"
        
def test_search_multiple_channel():
    #create user
    register = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
    token = register['token']
    u_id = register['u_id']

    #make channel for user to be in and send message
    channel_id = channels_create(token, "validChannel", True)
    message_id = message_send(token, channel_id['channel_id'], "HelloWorld")
    
    #make another channel for user to be in and send message

    channel_id2 = channels_create(token, "validChannelTwo", True)
    message_id2 = message_send(token, channel_id2['channel_id'], "HelloWorld")
    
    #test to see if search will return the messages that have helloworld
    query = "HelloWorld"
    messages = search(token, query)
    
    counter = 0
    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == "HelloWorld"
        counter=+1
        
    assert (counter == 2)
        
        
def test_search_short_query():
    
    #create user
    register = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
    token = register['token']
    u_id = register['u_id']

    #make channel for user to be in and send message
    channel_id = channels_create(token, "validChannel", True)
    message_send(token, channel_id['channel_id'], "")

    #test to see if search will return the messages that have ""
    query = ""
    messages = search(token, query)

    #test to see if the query string used found messages in channels
    for i in messages['messages']:
        assert i['message'] == ""        
        
def test_search_not_in_channel():
    #create user
    register = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
    token = register['token']
    u_id = register['u_id']

    #make channel for user to be in and send message
    channel_id = channels_create(token, "validChannel", True)
    message_id = message_send(token, channel_id['channel_id'], "HelloWorld")
    
    #make another user and channel for user to be in and send message
    register2 = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
    token2 = register2['token']
    u_id2 = register2['u_id']

    
    channel_id2 = channels_create(token2, "validChannelTwo", False)
    message_id2 = message_send(token2, channel_id2['channel_id'], "HelloWorld")
    
    #test to see if search will return the messages that have helloworld
    query = "HelloWorld"
    messages = search(token, query)
    
    counter = 0
    for i in messages['messages']:
        assert i['message'] == "HelloWorld"
        counter=+1
        
    assert (counter == 1)
    
def test_search_no_message():
    
    #create user
    register = auth_register("user@gmail.com", "password1", "firstOne", "lastOne")
    
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
        
    


