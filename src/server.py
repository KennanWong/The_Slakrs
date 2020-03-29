import sys
import re
import auth
import message
import channels
import standup
import datetime
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
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
#                   CHANNELS_LIST                           #      
#############################################################

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    
    token = request.args.get('token')
    chann_inf = channels.List(token)
    
    return dumps(
        chann_inf
    )


#############################################################
#                   CHANNELS_LISTALL                        #      
#############################################################

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    
    token = request.args.get('token')
    chann_inf2 = channels.Listall(token)

    return  dumps(
        chann_inf2
    )


#############################################################
#                   MESSAGE_PIN                             #      
#############################################################

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    
    payload = request.get_json()
    message.pin(payload)

    return dumps({})

#############################################################
#                   MESSAGE_UNPIN                             #      
#############################################################

@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    
    payload = request.get_json()
    message.unpin(payload)

    return dumps({})
    


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

#############################################################
#                   STANDUP_START                           #      
#############################################################
@APP.route("/standup/start", methods=['POST'])
def standup_start():
    payload = request.get_json()
    active = standup.start(payload)
    standup.end_standup(payload)

    return dumps ({
        'time_finish': active['time_finish']
    })


#############################################################
#                   STANDUP_ACTIVE                          #      
#############################################################
@APP.route("/standup/active", methods=['GET'])
def standup_active():
    payload = request.get_json()
    active = standup.active(payload)
    if active:
        return dumps({
            'is_active':True,
            'time_finish': active['time_finish']
        })
    else:
        return dumps ({
            'is_active':False,
            'time_finish': None
        })

#############################################################
#                   STANDUP_SEND                            #      
#############################################################
@APP.route("/standup/send", methods=['POST'])
def standup_send():
    payload = request.get_json()
    standup.send(payload)

    return ({
    })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080)) 
