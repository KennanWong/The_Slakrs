import sys
import re
import hashlib
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError

LOGGED_ON = 1
LOGGED_OFF = 0
is_success = True

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

def users_rest():
    global auth_data
    auth_data = []
    return 


'''
#############################################################
#                   GENERATE DATA STORES                    #      
#############################################################
'''

# to generate gloabl auth_data store
def get_auth_data_store():
    global auth_data
    return auth_data

# to get channel data store
def get_channel_data_store():
    global channels_store
    return channels_store


# to generate a token
def generate_token(u_id):
    return hashlib.sha256(str(u_id).encode()).hexdigest()


'''
#############################################################
#                TESTING VARIABLES                          #      
#############################################################
'''


# Function to validate a token and returns the users info
def validate_token(token):
    auth_store = get_auth_data_store()
    for i in auth_store:
        if i['token'] == token:
            return i
    else:
        raise InputError(description='Invalid Token')

# To test if an email is valid, courtesy of geeksforgeeks.org
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
    if (re.search(regex, email)):
        return email
    else:
        raise InputError(description='Invalid Email')


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

# Reset all users in a slack
@APP.route("/users/reset", methods=['POST'])
def users_reset():
    users_rest()
    return dumps({})


'''
#############################################################
#                   AUTH_REGISTER                           #      
#############################################################
'''


# Register a user and add it to the userStore
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    auth_store = get_auth_data_store()
    payload = request.get_json()
    handle = (payload['name_first']+payload['name_last'])
    if len(handle) > 24:
        handle = handle[0:20]

    # Test if valid email    
    email = test_email(payload['email'])

    # Test strength of password
    if len(payload['password']) > 6:
        password = payload['password']
    else:
        raise InputError (description = 'Password is too short')

    # Test length of first and last names
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

    # Test if an email is already taken
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
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    payload = request.get_json()
    channel_owner_info = {}
    new_channel_info ={}
   
    for i in auth_store:
        if i['token'] == payload['token']:
            print(i)           
            channel_owner_info = {
                'u_id': i['u_id'],
                'name_first': i['name_first'],
                'name_last': i['name_last'],
                'handle_str': i['handle_str']
            }
            if len(payload['name']) < 21:
                name = payload['name']
                if payload['is_public']: 
                    new_channel_info =  {
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
   
    print (channels_store)

    return dumps ({
        'channel_id': new_channel_info['channel_id']
    })


'''
#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################
'''


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))



#LOOK AT INVALID TOKEN
'''
#############################################################
#                   CHANNEL_INVITE                         #      
#############################################################
'''
@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    '''
    channel_owner_info = {}
    new_channel_info ={}
    '''
    
    #channelInfo = channels_create(token, 'The Slakrs', True)
    #channel_id = channelInfo['channel_id']
    
    for i in auth_store:
        if i['token'] == payload['token']:
            print(i)
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])
    
    #token = request.get_json('token')
    #channel_id = int(request.get_json('channel_id'))
    #user_id = int(request.get_json('u_id'))

    # Invite user to channel
    invite = channel_invite(token, channel_id, user_id)
   
    return dumps(invite)
     
    raise InputError(description='Invting someone to an invalid channel')
    raise InputError(description='Inviting someone with an invalid u_id')
    raise AccessError(description='Authorised user is not a member of channel')

'''
#############################################################
#                   CHANNEL_DETAILS                         #      
#############################################################
'''
@APP.route('/channel/details', methods=['GET'])
def channel_details():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])
    
    #token = request.args.get('token')
    #channel_id = int(request.args.get('channel_id'))
    #user_id = int(request.args.get('u_id'))

    details = channel_details(token, channel_id)
    
    '''    
    results = [
        {
            "name": 'The Slakrs',
            "owner_members": [{"u_id": 1, "name_first": "Hayden", 
                               "name_last": "Smith"}],
            "all_members": [{"u_id": 1, "name_first": "Hayden", 
                             "name_last": "Smith"}]
        }
    ]
    return dumps(details)
    '''
    raise InputError(description='Invalid channel')
    raise AccessError(description='Authorised user is not a member of channel with channel_id')
    
'''
#############################################################
#                   CHANNEL_MESSAGES                        #      
#############################################################
'''
@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])
    
    #token = request.args.get('token')
    #channel_id = int(request.args.get('channel_id'))
    #user_id = int(request.args.get('u_id'))

    # Send a message
    messages = message_send(token, channel_id, start)

    return dumps(messages)
    
    raise InputError(description='Invalid channel')
    raise InputError(description='Start is greater than or equal to the total number of messages in the channel')
    raise AccessError(description='Authorised user is not a member of channel with channel_id')
    
    #Refer to messages via index
    #message id is when u sent in within the entire server
    #channel['messages'][0] = hello
    #but hello could have a message id of 3
    
    #channel['messages'][start] loop until channel['messages'][end]
'''
#############################################################
#                   CHANNEL_LEAVE                           #      
#############################################################
'''
@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    #token = request.get_json('token')
    #channel_id = int(request.get_json('channel_id'))

    leave = channel_leave(token, channel_id)
    
    return dumps(leave)
    
    raise InputError(description='Invalid channel')
    raise AccessError(description='Authorised user is not a member of channel with channel_id')
    
'''
#############################################################
#                   CHANNEL_JOIN                            #      
#############################################################
'''
@APP.route('/channel/join', methods=['POST'])
def channel_join():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    #token = request.get_json('token')
    #channel_id = int(request.get_json('channel_id'))

    join = channel_join(token, channel_id)

    return dumps(join)
    
    raise InputError(description='Invalid channel')
    raise AccessError(description='Authorised user is not a member of channel with channel_id')
        
'''
#############################################################
#                   CHANNEL_ADDOWNER                         #      
#############################################################
'''
@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_adding = int(payload['u_id'])
    
    #token = request.get_json('token')
    #channel_id = int(request.get_json('channel_id'))
    #user_id_adding = int(request.get_json('u_id'))

    # Add owner with user_id to owner members
    addowner = channel_addowner(token, channel_id, user_id_adding)
    
    return dumps(addowner)
    
    raise InputError(description='Invalid channel')
    raise InputError(description='User with user id u_id is not an owner of channel')
    # cnat add an owner when ur not owner
    raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    
'''
#############################################################
#                   CHANNEL_REMOVEOWNER                     #      
#############################################################
'''
@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_removing = int(payload['u_id'])
    
    #token = request.get_json('token')
    #channel_id = int(request.get_json('channel_id'))
    #user_id_removing = int(request.get_json('u_id'))
    
    # Remove owner with user_id from owner members
    removeowner = channel_removeowner(token, channel_id, user_id_removing)

    return dumps(removeowner)
    
    raise InputError(description='Invalid channel')
    raise InputError(description='User with user id u_id is not an owner of channel')
    # cant remove an owner when ur not owner
    raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
