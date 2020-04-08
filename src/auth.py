'''
This file contains the code for all the 'auth_' functions
server
'''
from error import InputError
from helper_functions import test_email, generate_token, get_user_from
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
    if 1 < len(payload['name_first']) <= 50:
        first_name = payload['name_first']
    else:
        raise InputError(description='Not a valid first name')

    if 1 < len(payload['name_last']) <= 50:
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
        'messages':[],
        'permission_id': 2,
        'slack_owner' : False
    }

    if u_id == 1:
        # this is the first person in a slack they are now an owner
        new_user['slack_owner'] = True
        new_user['permission_id'] = 1

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
    email = test_email(payload['email'])

    user = get_user_from('email', email)

    # if the user is not currently logged off, raise error
    if user['status'] != LOGGED_OFF:
        raise InputError(description = "User already logged in")

    if user['password'] != payload['password']:
        raise InputError(description = "Incorrect password")

    user['status'] = LOGGED_ON
    user['token'] = generate_token(user['u_id'])

    return user



#############################################################
#                   AUTH_LOGOUT                             #
#############################################################

def logout(payload):
    '''
    Function to logout a user
    '''
    user = get_user_from('token',payload['token'])
    if user['status'] == LOGGED_ON:
        user['status'] = LOGGED_OFF
        user['token'] = ''
        return True
    return False
