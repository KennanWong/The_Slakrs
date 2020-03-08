import pytest
from error import InputError
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register

'''
#############################################################
#                   USER_PROFILE                            #
#############################################################
'''
#assume auth_register is working

def test_profile_working():
    #create a user    
    
    email1 = "varun@gmail.com"
    name_first1 = "Varun"
    name_last1 = "Kashyap"
    
    details = auth_register(email1, "password1", name_first1, name_last1)
    
    token1 = details['token']    
    uid1 = details['u_id']
    
    #test that the returned values are correct
    
    profile = user_profile(token1, uid1)
    
    assert(profile['email']) == email1
    assert(profile['name_first']) == name_first1
    assert(profile['name_last']) == name_last1
    assert(profile['handle_str']) == name_first1
    
#ending with _ID must be an integer
   
def test_profile_invalid_uID1():      
    details = auth_register("user@gmail.com", "password1", "Test", "User")	
    token1 = details['token']
       
    with pytest.raises(InputError):
        user_profile(token1, "NOT_VALID_UID")
		
def test_profile_invalid_uID2():   
    details = auth_register("user@gmail.com", "password1", "Test", "User")	
    token2 = details['token']
    	
    with pytest.raises(InputError):
        user_profile(token2, "2t62te63te36et")
		
def test_profile_invalid_uID3():
    details = auth_register("user@gmail.com", "password1", "Test", "User")	
    token3 = details['token']
    
    with pytest.raises(InputError):
        user_profile(token3, "29382938---2392398")
		
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
        user_profile_setname('THISISANINVALIDTOKEN', "VALID", "NAME")

    
'''
#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################
'''   

def test_user_profile_setemail_working():
    details = auth_register("email@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    uid = details['u_id']
    
    #tests under working conditions
    
    assert (user_profile_setemail(token, "new_email@gmail.com") == {})
    profile = user_profile(token1, uid1)
    newEmail = profile['email']
    assert newEmail == "email@gmail.com"
    

def test_user_profile_setemail_invalidEmail():

    #create some users
    details = auth_register("email@gmail.com", "password1", "Varun", "Kashyap")
    token = details['token']
    uid = details['u_id']

    #function will fail if the email provided is invalid
    
    # No prefix
    with pytest.raises(InputError):
        user_profile_setemail(token, "@gmail.com")
    # No suffix
    with pytest.raises(InputError):
        user_profile_setemail(token, "email@.com")
    # No .com
    with pytest.raises(InputError):
        user_profile_setemail(token, "email@gmail.")
    # no @
    with pytest.raises(InputError):
        user_profile_setemail(token, "emailgmail.com")
        
def test_user_profile_setemail_already_used():

    #create some users
    email1 = "email1@gmail.com"
    
    details1 = auth_register(email1, "password1", "Varun", "Kashyap")
    token1 = details1['token']
    uid1 = details1['u_id']
    
    email2 = "email2@gmail.com"
    token2 = details2['token']
    uid2 = details2['u_id']
     
    #changing email to one already in use causes function to fail
    with pytest.raises(InputError):
        user_profile_setemail(token1, email2)
        
    with pytest.raises(InputError):
        user_profile_setemail(token2, email1)
        
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

    

