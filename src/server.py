import sys
import re
import auth
import message
import channels
import datetime
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError

LOGGED_ON = 1
LOGGED_OFF = 0
is_success = True

msg_count = 1

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
    #     'messages' : []
    # }
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

# Function to generate global auth_data store
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

# Function to return the channel data using a channel_id
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

# Function to validate a token and returns the users info otherwise raises an 
# error
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

# To test if an email is valid, courtesy of geeksforgeeks.org
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return email
    else:
        raise InputError(description='Invalid Email')

# Function to test if a user is part of a channel
def test_in_channel(u_id, channel):
    for i in channel['members']:
        if i['u_id'] == u_id:
            return True
    for i in channel['owners']:
        if i['u_id'] == u_id:
            return True
    return False

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


#############################################################
#                   AUTH_REGISTER                           #      
#############################################################


# Register a user and add it to the userStore
@APP.route("/auth/register", methods=['POST'])
def auth_register():
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
        'status' : LOGGED_ON,
        'messages':[]
    }

    # Test if an email is already taken
    for i in auth_store:
        if i['email'] == email:
            raise InputError(description='Email is already in use')
    auth_store.append(new_user_auth)

    return dumps({
        'u_id': u_id,
        'token': token

    new_user = auth.register(payload)

    return dumps({
        'u_id': new_user['u_id'],
       'token': new_user['token'],
    })


#############################################################
#                   AUTH_LOGIN                              #      
#############################################################


# to login a user and return a token
@APP.route("/auth/login", methods=['POST'])
def auth_login():
    payload = request.get_json()
<<<<<<< HEAD

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

    user = auth.login(payload)

    return dumps({
        'u_id' : user['u_id'],
        'token' : user['token']
    })


#############################################################
#                   AUTH_LOGOUT                             #      
#############################################################

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    payload = request.get_json()
    if auth.logout(payload):
        return dumps({
            'is_succes':True
        })
    else:
        return dumps ({
            'is_success':False
        }) 



#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################



@APP.route("/channels/create", methods=['POST'])
def channels_create():
    
    payload = request.get_json()
    new_channel = channels.create(payload)
    return dumps ({
        'channel_id': new_channel['channel_id']
    })


#############################################################
#                   MESSAGE_SEND                            #      
#############################################################


@APP.route("/message/send", methods=['POST'])
def message_send():
    payload = request.get_json()
    new_message = message.send(payload)

    return dumps({
        'message_id': new_message['message_id']
    })
    
#############################################################
#                   MESSAGE_SENDLATER                       #      
#############################################################
@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    payload = request.get_json()
    
    new_message = message.sendlater(payload)

    return dumps({
        'message_id':new_message['message_id']
    })





#LOOK AT INVALID TOKEN
'''
#############################################################
#                   CHANNEL_INVITE                          #      
#############################################################
'''
@APP.route('/channel/invite', methods=['POST'])
def channel_invite_server():
    auth_store = get_auth_data_store
    channel_info = get_channel()
    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])

    # Invite user to channel
    invite = channel_invite(token, channel_id, user_id)
    
    return dumps(invite)

'''
#############################################################
#                   CHANNEL_DETAILS                         #      
#############################################################
'''
@APP.route('/channel/details', methods=['GET'])
def channel_details_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])

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
    '''
    return dumps(details)
    
'''
#############################################################
#                   CHANNEL_MESSAGES                        #      
#############################################################
'''
@APP.route('/channel/messages', methods=['GET'])
def channel_messages_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])
    start = int(payload['start'])

    messages = channel_messages(token, channel_id, start)

    #Refer to messages via index
    #message id is when u sent in within the entire server
    #channel['messages'][0] = hello
    #but hello could have a message id of 3
    
    #channel['messages'][start] loop until channel['messages'][end]

    return dumps(messages)
'''
#############################################################
#                   CHANNEL_LEAVE                           #      
#############################################################
'''
@APP.route('/channel/leave', methods=['POST'])
def channel_leave_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Leave the channel
    leave = channel_leave(token, channel_id)
    
    return dumps(leave)
    
'''
#############################################################
#                   CHANNEL_JOIN                            #      
#############################################################
'''
@APP.route('/channel/join', methods=['POST'])
def channel_join_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Join the channel
    join = channel_join(token, channel_id)

    return dumps(join)
        
'''
#############################################################
#                   CHANNEL_ADDOWNER                         #      
#############################################################
'''
@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_adding = int(payload['u_id'])

    # Add owner with user_id to owner members
    addowner = channel_addowner(token, channel_id, user_id_adding)
    
    return dumps(addowner)
    
'''
#############################################################
#                   CHANNEL_REMOVEOWNER                     #      
#############################################################
'''
@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner_server():
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store()
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_removing = int(payload['u_id'])

    # Remove owner with user_id from owner members
    removeowner = channel_removeowner(token, channel_id, user_id_removing)

    return dumps(removeowner)
    
#############################################################
#                   MESSAGE_REMOVE                          #      
#############################################################

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    payload = request.get_json()
    message.remove(payload)

    return dumps({})

#############################################################
#                   MESSAGE_EDIT                            #      
#############################################################
@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    payload = request.get_json()

    message.edit(payload)

    return dumps({})


#############################################################
#                    MESSAGE_REACT                          #      
#############################################################
@APP.route("/message/react", methods=['PUT'])
def message_react():
    payload = request.get_json()
    message.react(payload)

    return dumps({})


#############################################################
#                   MESSAGE_UNREACT                         #      
#############################################################
@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    payload = request.get_json()
    message.unreact(payload)

    return dumps({})


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

    