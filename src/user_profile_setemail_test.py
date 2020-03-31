import pytest
from error import InputError
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register

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
    details2 = auth_register(email2, "password2", "Vince", "Kash")
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
