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
    
    email = "varun@gmail.com"
    name_first = "Varun"
    name_last = "Kashyap"
    
    details = auth_register(email, "password1", name_first, name_last)
    
    token = details['token']    
    uid = details['u_id']
    
    #test that the returned values are correct
    
    profile = user_profile(token, uid)
    
    assert(profile['email'] == email)
    assert(profile['name_first'] == name_first)
    assert(profile['name_last'] == name_last)

    
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
