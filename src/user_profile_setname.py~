import pytest
from error import InputError
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
		
'''
#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################
'''

def test_user_profile_setname_working():
    
    email1 = "varun@gmail.com"
    name_first1 = "Varun"
    name_last1 = "Kashyap"   
    details = auth_register(email1, "password1", name_first1, name_last1)
    
    token = details['token']    
    uid = details['u_id']

    #do some tests to test that everying is running fine
    
    #initially the user's name is varun kashyap, and is changed to jeff jefferson
    name_first2 = "Jeff"
    name_last2 = "Jefferson"
    
    assert (user_profile_setname(token, name_first2, name_last2) == {})

    profile2 = user_profile(token, uid)
    assert(profile2['name_first']) == name_first2
    assert(profile2['name_last']) == name_last2
    
def test_user_profile_setname_same_name():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    uid = details['u_id']
    user_profile_setname(token, "Varun", "Kashyap") 
    
    profile2 = user_profile(token, uid)
    assert(profile2['name_first']) == "Varun"
    assert(profile2['name_last']) == "Kashyap"
    
def test_user_profile_setname_length_border():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    string_50 = "a" * 50
    string_1 = "a"
    
    assert (user_profile_setname(token, "ValidSTRING", string_50) == {})
    assert (user_profile_setname(token, "ValidString", string_1) == {})
    assert (user_profile_setname(token, string_50, "ValidString") == {})
    assert (user_profile_setname(token, string_1, "ValidString") == {})
    assert (user_profile_setname(token, string_1, string_50) == {})        

def test_user_profile_setname_name_first_short():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    valid_last = "THISISAVALIDLASTNAME"
    
    
    with pytest.raises(InputError):
        user_profile_setname(token, "", valid_last)
        
def test_user_profile_setname_name_last_short():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    valid_first = "THISISAVALIDFIRSTNAME"
    
    
    with pytest.raises(InputError):
        user_profile_setname(token, "", valid_first)
        
def test_user_profile_setname_name_both_short():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    with pytest.raises(InputError):
        user_profile_setname(token, "", "")
        
def test_user_profile_setname_name_first_long():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    string_51 = "a" * 51
    with pytest.raises(InputError):
        user_profile_setname(token, string_51, "THISISAVALIDNAME")
    
def test_user_profile_setname_name_last_long():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    string_51 = "a" * 51
    with pytest.raises(InputError):
        user_profile_setname(token, "THISISAVALIDNAME", string_51)
        
def test_user_profile_setname_name_both_long():
    details = auth_register("varun@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    string_51 = "a" * 51
    with pytest.raises(InputError):
        user_profile_setname(token, string_51, string_51)
        
def test_user_profile_setname_invalidToken():
    with pytest.raises(InputError):
        user_profile_setname("THISISANINVALIDTOKEN", "VALID", "NAME")
