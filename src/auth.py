'''
This file contains the code for all the 'auth_' functions
server
'''
import smtplib
from error import InputError
from helper_functions import test_email, generate_token, id_generator, get_user_from
from data_stores import get_auth_data_store, get_reset_code_store, save_auth_store

LOGGED_ON = 1
LOGGED_OFF = 0

EMAIL = "slakrs1531@gmail.com"
PASSWORD = "1531python"

#pylint compliant
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
        'slack_owner' : False,
        'profile_img_url': "https://img.buzzfeed.com/buzzfeed-static/static/2020-04/15/19/campaign_images/fdc9b0680e75/the-social-media-shame-machine-is-in-overdrive-ri-2-4824-1586980284-7_dblbig.jpg"
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

    # for debugging
    save_auth_store()


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
    if user['password'] != payload['password']:
        raise InputError(description="Incorrect password")

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
    user = get_user_from('token', payload['token'])
    if user['status'] == LOGGED_ON:
        user['status'] = LOGGED_OFF
        user['token'] = ''
        return True
    return False

#############################################################
#                   AUTH_PASSWORDRESET_REQUEST              #
#############################################################
def request(payload):                       # pylint disable=R1771
    '''
    Function to request a reset code
    '''

    reset_store = get_reset_code_store()
    send_to_email = test_email(payload['email'])

    email_match = 0  # if found = 1

    user = get_user_from('email', send_to_email)    # pylint: disable=W0612

    email_match = 1
    reset_code = id_generator()

    code_password = {
        'email': send_to_email,
        'reset_code': reset_code,
    }

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL, PASSWORD)
    server.sendmail(
        EMAIL,
        send_to_email,
        reset_code)
    server.quit()

    if email_match == 0:
        raise InputError(description="Email entered does not belong to a user")

    reset_store.append(code_password)


#############################################################
#                   AUTH_PASSWORDRESET_RESET                #
#############################################################
def reset(payload):                 # pylint disable=R1771
    '''
    Function to reset the user's password
    '''
    reset_store = get_reset_code_store()

    for code in reset_store:
        if code['reset_code'] == payload['reset_code']:
            requested_email = code['email']
            user = get_user_from('email', requested_email)
            if len(payload['new_password']) > 6:
                new_password = payload['new_password']
                user['password'] = new_password


            else:
                raise InputError(description='Password is too short')

        else:
            raise InputError(description='Reset code is incorrect')
