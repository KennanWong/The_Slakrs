import pytest
from error import InputError
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
from test_helper_functions import reg_user1, reg_user2, register_and_create, send_msg1
from other import workspace_reset

'''
#############################################################
#                   USER_PROFILE                            #
#############################################################
'''
#assume auth_register is working

def test_profile_working():
    #create a user    
    workspace_reset()
    
    details = reg_user1()
    
    token = details['token']    
    uid = details['u_id']
    
    #test that the returned values are correct
    payload = {
        'token' : register['token'],
        'u_id' : uid    
    }
    
    profile = user_profile(payload)
    
    assert(profile['email'] == email)
    assert(profile['name_first'] == name_first)
    assert(profile['name_last'] == name_last)

    
#ending with _ID must be an integer
   
def test_profile_invalid_uID1():          
    
    workspace_reset()
    
    details = reg_user1()	
       
    payload = {
        'token' : details['token'],
        'u_id' : "NOT_VALID_UID"
    
    }
    
    with pytest.raises(InputError):
        user_profile(payload)
		
def test_profile_invalid_uID2():   
    workspace_reset()
    
    details = reg_user1()
    
    payload = {
        'token' : details['token'],
        'u_id' : "22tt3t3tt3r4r"
    }    
    	
    with pytest.raises(InputError):
        user_profile(payload)
		
def test_profile_invalid_uID3():
    workspace_reset()
    
    details = reg_user1()
    
        
    payload = {
        'token' : details['token'],
        'u_id' : "126261261----22322323"
    }    
    	
    with pytest.raises(InputError):
        user_profile(payload)
		
'''
#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################
'''

def test_user_profile_setname_working():
    workspace_reset()   
    
    details = reg_user1()
    
    token = details['token']    
    uid = details['u_id']

    #do some tests to test that everying is running fine
    
    #initially the user's name is varun kashyap, and is changed to jeff jefferson
    name_first2 = "Jeff"
    name_last2 = "Jefferson"
    
    payload5 = {
        'token' : details['token'],
        'name_first' : name_first2,
        'name_last' : name_last2     
    }
        
    assert (user_profile_setname(payload5) == {})

    payload3 = {
        'token' : details['token'],
        'u_id' : details['u_id']       
    }
    
    profile2 = user_profile(payload3)
    assert(profile2['name_first']) == name_first2
    assert(profile2['name_last']) == name_last2
    
def test_user_profile_setname_same_name():
    workspace_reset()
    
    details = reg_user1()
    token = details['token']
    uid = details['u_id']
    first = details['name_first']
    last = details['name_last']
    
    payload = {
        'token' : details['token'],
        'name_first' : first,
        'name_last' : last       
    }
    
    user_profile_setname(payload) 
    
    payload2 = {
        'token' : details['token'],
        'u_id' : uid 
    }
    
    profile2 = user_profile(payload2)
    assert(profile2['name_first']) == first
    assert(profile2['name_last']) == last
    
def test_user_profile_setname_length_border():
    workspace_reset()
    
    details = reg_user1()
    token = details['token']
    string_50 = "a" * 50
    string_1 = "a"
    
    payload1 = {
        'token' : details['token'],
        'name_first' : "ValidString",
        'name_last' : string_50       
    }
    
    payload2 = {
        'token' : details['token'],
        'name_first' : "ValidString",
        'name_last' : string_1       
    }
    payload3 = {
        'token' : details['token'],
        'name_first' : string_50,
        'name_last' : "ValidString"       
    }
    payload4 = {
        'token' : details['token'],
        'name_first' : string_1,
        'name_last' : string_50       
    }
    
    assert (user_profile_setname(payload1) == {})
    assert (user_profile_setname(payload2) == {})
    assert (user_profile_setname(payload3) == {})
    assert (user_profile_setname(payload4) == {})

def test_user_profile_setname_name_first_short():
    workspace_reset()
    
    details = reg_user1()
    valid_last = "THISISAVALIDLASTNAME"
    
    payload = {
        'token' : details['token'],
        'name_first' : "",
        'name_last' : valid_last       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)
        
def test_user_profile_setname_name_last_short():
    workspace_reset()
    
    details = reg_user1()
    valid_first = "THISISAVALIDFIRSTNAME"
    
    payload = {
        'token' : details['token'],
        'name_first' : valid_first,
        'name_last' : ""       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)
        
def test_user_profile_setname_name_both_short():
    workspace_reset()
    
    details = reg_user1()
    payload = {
        'token' : details['token'],
        'name_first' : "",
        'name_last' : ""       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)
        
def test_user_profile_setname_name_first_long():
    workspace_reset()
    
    details = reg_user1()
    token = details['token']
    string_51 = "a" * 51
    
    payload = {
        'token' : details['token'],
        'name_first' : string_51,
        'name_last' : "THISISAVALIDNAME"       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)
    
def test_user_profile_setname_name_last_long():
    workspace_reset()
    
    details = reg_user1()
    token = details['token']
    string_51 = "a" * 51
    
    payload = {
        'token' : details['token'],
        'name_first' : "THISISAVALIDNAME",
        'name_last' : string_51       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)
        
def test_user_profile_setname_invalidToken():
    workspace_reset()
    
    details = reg_user1()
    payload = {
        'token' : "INVALID",
        'name_first' : "THISISAVALIDNAME",
        'name_last' : "ValidName"       
    }
    
    with pytest.raises(InputError):
        user_profile_setname(payload)

    
'''
#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################
'''   

def test_user_profile_setemail_working():
    workspace_reset()
    
    details = reg_user1()
    token = details['token']
    uid = details['u_id']
    
    payload = {
        'token' : token,
        'email' : "new_email@gmail.com"     
    }
    
    #tests under working conditions
    
    assert (user_profile_setemail(payload) == {})
    payload2 = {
        'token' : token,
        'u_id' : uid 
    }
    
    profile = user_profile(payload2)
    newEmail = profile['email']
    assert (newEmail == "new_email@gmail.com")
    

def test_user_profile_setemail_invalidEmail():

    #create some users
    workspace_reset()
    
    details = reg_user1()
    
    token = details['token']
    uid = details['u_id']

    #function will fail if the email provided is invalid
    payload1 = {
        'token' : token,
        'email' : "@gmail.com"     
    }
    payload2 = {
        'token' : token,
        'email' : "email@.com"     
    }
    payload3 = {
        'token' : token,
        'email' : "new_email@gmail."     
    }
    payload4 = {
        'token' : token,
        'email' : "new_emailgmail.com"     
    }
    
    
    # No prefix
    with pytest.raises(InputError):
        user_profile_setemail(payload1)
    # No suffix
    with pytest.raises(InputError):
        user_profile_setemail(payload2)
    # No .com
    with pytest.raises(InputError):
        user_profile_setemail(payload3)
    # no @
    with pytest.raises(InputError):
        user_profile_setemail(payload4)
        
def test_user_profile_setemail_already_used():

    
    workspace_reset()
    
    details1 = reg_user1()
    token1 = details1['token']
    uid1 = details1['u_id']
    email1 = details1['email']
    
    details2 = reg_user2()
    token2 = details2['token']
    uid2 = details2['u_id']
    email2 = details2['email']
    #changing email to one already in use causes function to fail
    
    payload1 = {
        'token' : token1,
        'email' : email2     
    }
    
    payload2 = {
        'token' : token2,
        'email' : email1     
    }
    
    with pytest.raises(InputError):
        user_profile_setemail(payload1)
        
    with pytest.raises(InputError):
        user_profile_setemail(payload2)
        
def test_user_profile_setemail_invalidToken():
    with pytest.raises(InputError):
        user_profile_setemail('THISISANINVALIDTOKEN', 'email@gmail.com')
        
'''
#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################
'''

def test_user_profile_sethandle_working():
    #create user 
    workspace_reset()
    
    details = reg_user1()
    
    token = details['token']
    uid = details['u_id']
    
    assert(user_profile_sethandle(token, "handleOne") == {})
    assert(user_profile_sethandle(token, "handleTwo") == {})
    
    assert(user_profile(token,["handle_str"] == "handleTwo"))

def test_user_profile_sethandle_length():
    workspace_reset()
    
    string_3 = "aaa"
    string_20 = "x" * 20
    
    string_2 = "aa"
    string_21 = "q" * 21
    string_long = "w" * 50
    
    
    
    details = reg_user1()
    token = details['token']
    uid = details['u_id']
    
    assert(user_profile_sethandle(token, string_3) == {})
    #check handle has been changed
    assert(user_profile(token,["handle_str"] == string_3))
    assert(user_profile_sethandle(token, string_20) == {})
    assert(user_profile(token,["handle_str"] == string_20))
    
    
    with pytest.raises(InputError):
        user_profile_sethandle(token, string_2)
        
    with pytest.raises(InputError):
        user_profile_sethandle(token, string_21)
    
    with pytest.raises(InputError):
        user_profile_sethandle(token, string_long)
	    
def test_user_profile_sethandle_already_used():
    workspace_reset()
    
    details1 = reg_user1()
    token1 = details1['token']
    uid1 = details1['u_id']
    
    details2 = reg_user2()
    token2 = details2['token']
    uid2 = details2['u_id']
    
    valid_handle = "ValidHandle"    
    
    #test handle already used
    payload1 = {
        'token' : token1,
        'handle_str' : valid_handle     
    }
    payload2 = {
        'token' : token1,
        'u_id' : uid1     
    }
    payload3 = {
        'token' : token2,
        'handle_str' : valid_handle     
    }
    
    
    user_profile_sethandle(payload1)
    
    assert(user_profile(payload2)=={})
    
    with pytest.raises(InputError):
        user_profile_sethandle(payload3)

    
