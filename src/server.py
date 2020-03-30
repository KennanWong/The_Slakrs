'''
Main serve file for flask server
Contains all routes
'''

import sys
import re
from json import dumps
from flask import Flask, request
from flask_cors import CORS

import auth
import message
import channels
import other
from error import InputError

#test

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




#############################################################
#                   AUTH_REGISTER                           #      
#############################################################


#register a user and add it to the userStore
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    payload = request.get_json()
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
            'is_success':True
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
    
    new_message_id = message.sendlater(payload)

    return dumps({
        'message_id':new_message_id
    })



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
@APP.route("/message/react", methods=['POST'])
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


#LOOK AT INVALID TOKEN
#############################################################
#                   CHANNEL_INVITE                          #      
#############################################################

@APP.route('/channel/invite', methods=['POST'])
def channel_invite_server():
    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])

    # Invite user to channel
    invite = channel.invite(token, channel_id, user_id)
    
    return dumps(invite)


#############################################################
#                   CHANNEL_DETAILS                         #      
#############################################################

@APP.route('/channel/details', methods=['GET'])
def channel_details_server():
    # Information from request
    token = request.args.get('token')
    print(token)
    channel_id = request.args.get('channel_id')
    
    
    details = channel.details(token, channel_id)

    
    return dumps(details)
    

#############################################################
#                     CHANNEL_MESSAGES                      #      
#############################################################

@APP.route('/channel/messages', methods=['GET'])
def channel_messages_server():
    
    # Information from request
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    messages = channel.messages(token, channel_id, start)


    return dumps(messages)


#############################################################
#                       CHANNEL_LEAVE                       #      
#############################################################

@APP.route('/channel/leave', methods=['POST'])
def channel_leave_server():
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Leave the channel
    leave = channel.leave(token, channel_id)
    
    return dumps(leave)
    

#############################################################
#                   CHANNEL_JOIN                            #      
#############################################################

@APP.route('/channel/join', methods=['POST'])
def channel_join_server():
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Join the channel
    join = channel.join(token, channel_id)

    return dumps(join)
        

#############################################################
#                   CHANNEL_ADDOWNER                        #      
#############################################################

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner_server():
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_adding = int(payload['u_id'])

    # Add owner with user_id to owner members
    channel.addowner(token, channel_id, user_id_adding)
    
    #return dumps(addowner)
    return dumps({})
    

#############################################################
#                   CHANNEL_REMOVEOWNER                     #      
#############################################################

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner_server():
    payload = request.get_json()
    
    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_removing = int(payload['u_id'])

    # Remove owner with user_id from owner members
    channel.removeowner(token, channel_id, user_id_removing)

    return dumps({})


#############################################################
#                   WORKSPACE_RESET                         #      
#############################################################
@APP.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    other.workspace_reset()
    return dumps({})

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080)) 
