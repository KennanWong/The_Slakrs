'''
This file contains the code for all the 'auth_' functions
server
'''
from error import InputError
from helper_functions import test_email, generate_token, get_user_token
from data_stores import get_auth_data_store


LOGGED_ON = 1
LOGGED_OFF = 0


#############################################################
#                   AUTH_REGISTER                           #
#############################################################

def register(payload):
    '''
    Function to register a user to the slack
    '''
    auth_store = get_auth_data_store()
    handle = (payload['name_first']+payload['name_last'])
    if len(handle) > 24:
        handle = handle[0:20]

    #test if valid email
    email = test_email(payload['email'])

    #test strength of password
    if len(payload['password']) > 6:
        password = payload['password']
    else:
        raise InputError(description='Password is too short')

    #test length of Last and First names
    if 1 <= len(payload['name_first']) <= 50:
        first_name = payload['name_first']
    else:
        raise InputError(description='Not a valid first name')

    if 1 <= len(payload['name_last']) <= 50:
        last_name = payload['name_last']
    else:
        raise InputError(description='Not a valid last name')

    u_id = int(len(auth_store)+1)
    token = generate_token(u_id)

    new_user = {
        'u_id' : u_id,
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name,
        'handle_str': handle.lower(),
        'token': token,
        'status' : LOGGED_ON,
        'messages':[]
    }

    #test if an email is alread taken
    for i in auth_store:
        if i['email'] == email:
            raise InputError(description='Email is already in use')

    auth_store.append(new_user)

    return new_user


#############################################################
#                   AUTH_LOGIN                              #
#############################################################

def login(payload):
    '''
    Function to login a user
    '''
    auth_store = get_auth_data_store()

    email = test_email(payload['email'])

    email_match = 0  # if found = 1

    user = {}
    for i in auth_store:
        if i['email'] == email:
            email_match = 1
            if i['status'] == LOGGED_OFF:
                if i['password'] == payload['password']:
                    user = i
                    i['status'] = LOGGED_ON
                    i['token'] = generate_token(i['u_id'])
                else:
                    raise InputError(description="Incorrect password")
            else:
                raise InputError(description="User already logged in")

    if email_match == 0:
        raise InputError(description="Email entered does not belong to a user")

    return user



#############################################################
#                   AUTH_LOGOUT                             #
#############################################################

def logout(payload):
    '''
    Function to logout a user
    '''
    user = get_user_token(payload['token'])
    if user['status'] == LOGGED_ON:
        user['status'] = LOGGED_OFF
        user['token'] = ''
        return True
    return False
