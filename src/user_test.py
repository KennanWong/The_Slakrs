import pytest
from error import InputError
import user
import auth

'''
#############################################################
#                   USER_PROFILE                            #
#############################################################
'''
#assume auth_register is working


def test_profile_normal():
    #create a user    
    
    email1 = "varun@gmail.com"
    name_first1 = "Varun"
    name_last1 = "Kashyap"
    
    details1 = auth_register(email1, "password1 ", name_first1, name_last1)
    
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
    details = auth_register("user@gmail.com", "password1 ", "Test", "User")	
    token1 = details['token']
       
    with pytest.raises(InputError):
        user_profile(token1, "NOT_VALID_UID")
		
def test_profile_invalid_uID2():   
    details = auth_register("user@gmail.com", "password1 ", "Test", "User")	
    token2 = details['token']
    	
    with pytest.raises(InputError):
        user_profile(token2, "2t62te63te36et")
		
def test_profile_invalid_uID3():
    details = auth_register("user@gmail.com", "password1 ", "Test", "User")	
    token3 = details['token']
    
    with pytest.raises(InputError):
        user_profile(token3, "29382938---2392398")
		
'''
#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################
'''



    
    
    
    
    
    
    
    
    
    
    
