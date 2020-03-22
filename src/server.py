import sys
import re
import hashlib
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

LOGGED_ON = 1
LOGGED_OFF = 0
is_success = True

users = [
]

auth_data = [
    # user_data :{
    #     'u_id',
    #     'email',
    #     'password',
    #     'token'
    #     'status'
    # }
]


channels_store = [
    #new_channel_info
    #{
     #   'channel_id'
      #  'name'
       # 'is_public' 
        #'members': {
         #   u_id
          #  name_first
           # name_last
        #}
        #'owners': {
         #   u_id
          #  name_first
           # name_last
        #}
        #'messages': {
         #   message_id
          #  u_id, message
           # time_created
            #reacts
            #is_pinned

        #}
    #}
]
<<<<<<< HEAD

auth_data = [
    #user_data :{
    #    'u_id' : u_id,
    #    'email': email,
    #    'name_first': first_name,
    #    'name_last': last_name,
    #    'handle_str': handle.lower(),
    #    'password': password,
    #    'token': token,
    #    'status' : LOGGED_ON
    # }
]


def get_auth_data_store():
    global auth_data
    return auth_data
=======


def users_rest():
    global users
    users = []
    global auth_data
    auth_data = []
    return users
>>>>>>> 5dbb30a21c754e6c27d9ef0c928f61fdaef0876f


# to get global users
def get_user_store():
    global users
    return users

# to get gloabl auth_data store
def get_auth_data_store():
    global auth_data
    return auth_data

# to get channel data store
def get_channel_data_store():
    global channels_store
    return channels_store


# to test if an email is valid, courtesy of geeksforgeeks.org
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
    if (re.search(regex, email)):
        return email
    else:
        raise InputError(description='Invalid Email')

# to generate a token
def generate_token(u_id):
    return hashlib.sha256(str(u_id).encode()).hexdigest()


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


# reset all users in a slack
@APP.route("/users/reset", methods=['POST'])
def users_reset():
    users_rest()
    return dumps({})


'''
#############################################################
#                   AUTH_REGISTER                           #      
#############################################################
'''


#register a user and add it to the userStore
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    users_store = get_user_store()
    auth_store = get_auth_data_store()
    payload = request.get_json()
    handle = (payload['name_first']+payload['name_last'])
    if len(handle) > 24:
        handle = handle[0:20]

    #test if valid email    
    email = test_email(payload['email'])

    #test strength of password
    if len(payload['password']) > 6:
        password = payload['password']
    else:
         raise InputError (description='Password is too short')
    
    #test length of Last and First names
    if 1 <= len(payload['name_first']) <= 50:
        first_name = payload['name_first']
    else:
        raise InputError(description='Not a valid first name')

    if 1 <= len(payload['name_last']) <= 50:
        last_name = payload['name_last']
    else:
        raise InputError(description='Not a valid last name')

    u_id = int(len(users_store)+1)
    token = generate_token(u_id)

    new_user = {
        'u_id': u_id,
        'email': email,
        'name_first': first_name,
        'name_last': last_name,
        'handle_str': handle.lower(),
    }

    new_user_auth = {
        'u_id' : u_id,
        'email': email,
        'password': password,
        'token': token,
        'status' : LOGGED_ON
    }

    #test if an email is alread taken
    for i in users_store:
        if i['email'] == email:
            raise InputError(description='Email is already in use')

    users_store.append(new_user)
    auth_store.append(new_user_auth)

    return dumps({
        'u_id': u_id,
       'token': token
    })

'''
#############################################################
#                   AUTH_LOGIN                              #      
#############################################################
'''

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    auth_store = get_auth_data_store()
    payload = request.get_json()

    email = test_email(payload['email'])

    emailMatch = 0  # if found = 1
    passwordMatch = 0 # if match, password = 1

    user_auth_data = {}

    for i in auth_store:
        if i['email'] == email:
            emailMatch = 1
            if i['status'] == LOGGED_OFF:
                if i['password'] == payload['password']:
                    user_auth_data = i
                    i['status'] == LOGGED_ON
                else:
                    raise InputError(description="Incorrect password")
            else: 
                raise InputError(description="User already logged in")

    if emailMatch == 0:
        raise InputError(description="Email entered does not belong to a user")
    
    return dumps({
        'u_id' : user_auth_data['u_id'],
        'token' : user_auth_data['token']
    })

'''
#############################################################
#                   AUTH_LOGOUT                             #      
#############################################################
'''
@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    auth_store = get_auth_data_store()
    payload = request.get_json()


    for i in auth_store:
        if i['token'] == payload['token']:

            if i['status'] == LOGGED_ON:

                i['status'] = LOGGED_OFF
 
                return dumps({
                })

    return dumps({
    })

'''
#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################
'''
@APP.route("/channels/create", methods=['POST'])
def channels_create():
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    payload = request.get_json()

    for i in auth_store:
        if i['token'] == payload['token']:
            channel_owner_info = {
                'u_id': i['u_id'],
                'name_first': i['name_first'],
                'name_last': i['name_last'],
                'handle_str': i['handle_str']
            }
            if len(payload['name']) < 21:
                name = payload['name']
<<<<<<< HEAD
                if payload['is_public']:
                    new_channel_info = {
=======

                if payload['is_public']: 
                    new_channel_info =  {
>>>>>>> 5dbb30a21c754e6c27d9ef0c928f61fdaef0876f
                        'channel_id': int(len(channel_store)+1),
                        'name':  name,
                        'is_public': True,
                        'members':[],
<<<<<<< HEAD
                        'owners':[],
=======

                        'owners':[],
                           
                        
>>>>>>> 5dbb30a21c754e6c27d9ef0c928f61fdaef0876f
                        'messages': [],

                    }

                else:
                    new_channel_info = {
                        'channel_id': int(len(channel_store)+1),
                        'name': name,
                        'is_public': False,
<<<<<<< HEAD
                        'members': [],
                        'owners': [],                        
=======
                        'members':[],

                        'owners':[],
                           
                        
>>>>>>> 5dbb30a21c754e6c27d9ef0c928f61fdaef0876f
                        'messages': [],

                    }

            else:
                raise InputError(description='Name is too long')
    new_channel_info['owners'].append(channel_owner_info)
    channel_store.append(new_channel_info)
    return dumps({
        'channel_id': new_channel_info['channel_id']
    })


'''
#############################################################
#                   CHANNELS_LIST                           #      
#############################################################
'''
@APP.route("/channels/listall", methods=['GET'])
def channels_list():
<<<<<<< HEAD
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    payload = request.get_json()
=======
    return
>>>>>>> 5dbb30a21c754e6c27d9ef0c928f61fdaef0876f

   for i in auth_store:
       if i['token'] == payload['token']:
           j = 0
           while j <= (len(channel_store)+1):
               info_channels = {
                   'channel_id': int(channel_store['channel_id'])[j]
                   'name': channel_store['name'][j]
               }
                j = j+1

 
  
    return dumps({
        'channel_id': info_channels['channel_id'][j]
        'name': info_channels['name'][j]
    })























if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

