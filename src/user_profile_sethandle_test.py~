import pytest
from error import InputError
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register

'''
#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################
'''

def test_user_profile_sethandle_working():
    #create user 
    details = auth_register("email@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    uid = details['u_id']
    
    assert(user_profile_sethandle(token, "handleOne") == {})
    assert(user_profile_sethandle(token, "handleTwo") == {})
    
    assert(user_profile(token,["handle_str"] == "handleTwo"))

def test_user_profile_sethandle_length():
    string_3 = "aaa"
    string_20 = "x" * 20
    
    string_2 = "aa"
    string_21 = "q" * 21
    string_long = "w" * 50
    
    
    details = auth_register("email@gmail.com", "password1", "Varun", "Kashyap")
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
    details1 = auth_register("email@gmail.com", "password1", "Varun", "Kashyap")
    token1 = details1['token']
    uid1 = details1['u_id']
    
    details2 = auth_register("email2@gmail.com", "password2", "Email", "Time")
    token2 = details2['token']
    uid2 = details2['u_id']
    
    valid_handle = "ValidHandle"    
    
    #test handle already used
    user_profile_sethandle(token1, valid_handle)
    assert(user_profile(token1,["handle_str"] == valid_handle))
    
    with pytest.raises(InputError):
        user_profile_sethandle(token2, valid_handle)
