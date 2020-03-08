import pytest
from error import InputError
import user
import auth
import other

'''
#############################################################
#                   USERS_ALL                                #
#############################################################
'''
    
def test_users_all_working
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
    
    user1 = list_user[0]
    assert (user['u_id'] == uid1)
    assert (user['email'] == "email1@gmail.com")
    assert (user['name_first'] == "firstOne")
    assert (user['name_last'] == "lastOne")
    assert (user['handle_str'] == "handleOne")
    
    
    




