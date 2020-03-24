import sys
import re
import hashlib
from datetime import datetime
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError
#from channels import channels_create

LOGGED_ON = 1
LOGGED_OFF = 0
is_success = True

channels_store = [
    # {
    #     'channel_id'
    #     'name'
    #     'is_public'
    #     'members':[
 	# 	    {
    #             u_id
    #             name_first
    #             Name_last
 	# 	        Handle_str
 	# 	    }
    #     ] 
    #     'owners':[
 	#         {
    #             u_id
    #             name_first
    #             Name_last
 	# 	        Handle_str
 	# 	    }
    #     ]
    #     'messages': [
    #         {
    #             message_id
    #             u_id, 
    #             message
    #             time_created
    #             reacts
    #             is_pinned
    #         }
 	#     ]
    # }
]


auth_data = [
    # user_data :{
    #     'u_id' : u_id,
    #     'email': email,
    #     'name_first': first_name,
    #     'name_last': last_name,
    #     'handle_str': handle.lower(),
    #     'password': password,
    #     'token': token,
    #     'status' : LOGGED_ON
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

def users_rest():
    global auth_data
    auth_data = []
    return 


'''
#############################################################
#                GENERATE/GETTING FUNCTIONS                 #      
#############################################################
'''

# Function to generate gloabl auth_data store
def get_auth_data_store():
    global auth_data
    return auth_data

# Function to get channel data store
def get_channel_data_store():
    global channels_store
    return channels_store


# Function to generate a token
def generate_token(u_id):
    return hashlib.sha256(str(u_id).encode()).hexdigest()

# Function to generate a blank message dictionary
def create_message():
    message = {
        'message_id' : 0,
        'u_id' : 0, 
        'message': '',
        'time_created':0,
        'reacts': [],
        'is_pinned': False,
    }
    return message

# Function to return the channel data suing a channel_id
def get_channel(channel_id):
    all_channels = get_channel_data_store()
    channel = {}
    for i in all_channels:
        if i['channel_id'] == int(channel_id):
            return i
    raise InputError(description='Invalid channel_id')

'''
#############################################################
#                TESTING VARIABLES                          #      
#############################################################
'''


# function to validate a token and returns the users info
# otherwise raises an error
def validate_token(token):
    auth_store = get_auth_data_store()
    user = {}
    for i in auth_store:
        if i['token'] == token:
            user = i
    if user != {}:
        return user
    else:
        raise InputError(description='Invalid Token')

# to test if an email is valid, courtesy of geeksforgeeks.org
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return email
    else:
        raise InputError(description='Invalid Email')

# function to test if a user is part of a channel
def test_in_channel(u_id, channel):
    for i in channel['members']:
        if i['u_id'] == u_id:
            return True
    for i in channel['owners']:
        if i['u_id'] == u_id:
            return True
    raise AccessError(description='User is not a part of this channel')

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


'''
#############################################################
#                   USER_RESET                              #      
#############################################################
'''

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

    u_id = int(len(auth_store)+1)
    token = generate_token(u_id)


    new_user_auth = {
        'u_id' : u_id,
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name,
        'handle_str': handle.lower(),
        'token': token,
        'status' : LOGGED_ON
    }

    #test if an email is alread taken
    for i in auth_store:
        if i['email'] == email:
            raise InputError(description='Email is already in use')
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

# to login a user and return a token
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
                    i['status'] = LOGGED_ON
                    i['token'] = generate_token(i['u_id'])
                else:
                    raise InputError(description="Incorrect password")
            else: 
                raise InputError(description="User already logged in")

    if emailMatch == 0:
        raise InputError(description="Email entered does not belong to a user")
    
    print(i)
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
                i['token'] = ''
                return dumps({})

    return dumps({})





'''
#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################
'''
@APP.route("/channels/create", methods=['POST'])
def channels_create():
    
    channel_store = get_channel_data_store()
    payload = request.get_json()
    channel_owner_info = {}
    new_channel_info = {}
   
    
    user = validate_token(payload['token'])

    channel_owner_info = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
    }
    
    if len(payload['name']) < 21:
        name = payload['name']
        if payload['is_public']: 
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name':  name,
                'is_public': True,
                'members':[],
                'owners':[],
                'messages': [],
            }
        else:
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name': name,
                'is_public': False,
                'members':[],
                'owners':[],
                'messages': [],
            }
    else: 
        raise InputError (description='Name is too long')
                     
    
    new_channel_info['owners'].append(channel_owner_info)
    channel_store.append(new_channel_info)
   
    return dumps ({
        'channel_id': new_channel_info['channel_id']
    })
'''
#############################################################
#                   CHANNELS_LIST                           #      
#############################################################
'''

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    channel_store = get_channel_data_store()
    payload = request.get.json()
    channels = []
    channel_info = {}

    user = validate_token(payload['token'])
    for user in channel_store:
        test_in_channel(u_id, channel)
        channel_info = {
            'channel_id': user['channel_id'],
            'name': user['name']
        }

    channels.append(channel_info)

    return dumps({
        'channel_id': channels['channel_id'],
        'name': channels['name']
    })
'''
#############################################################
#                   CHANNELS_LISTALL                        #      
#############################################################
'''
@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    
    channel_store = get_channel_data_store()
    payload = request.get_json()
    channels_return = []
    channel_info = {}

    user = validate_token(payload['token'])
    for user in channel_store:
        channel_info = {
            'channel_id': user['channel_id'],
            'name': user['name']
        }
   
    channels_return.append(channel_info)

    return dumps({
        'channel_id': channels_return['channel_id'],
        'name': channels_return['name']
    })
    


'''
#############################################################
#                   MESSAGE_PIN                             #      
#############################################################
'''

@APP.route("message/pin", methods=['POST'])
def channels_listall():
    
    payload = request.get_json()

    user = validate_token(payload['token'])
    channel_message_info = {
        'message_id',
        'u_id', 
        'message',
        'time_created',
        'reacts',
        'is_pinned',

    }

    return dumps ({
    })

'''
#############################################################
#                   MESSAGE_SEND                            #      
#############################################################
'''
@APP.route("/message/send", methods=['POST'])
def message_send():
    payload = request.get_json()
    user = validate_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    test_in_channel(user['u_id'], channel)
    


    # create a message data type, and fill in details
    # then append to the channels list of messages
    txt = payload['message']
    if len(txt) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    new_message = create_message()
    msg_id = int(len(channel['messages'])+1)
    new_message['message_id'] = msg_id
    new_message['u_id'] = user['u_id']
    new_message['message'] = txt
    new_message['time_created'] = datetime.now().time()
    channel['messages'].append(new_message)

    for msg in channel['messages']:
        print(msg['message'])

    return dumps({
        'message_id': msg_id
    })



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

