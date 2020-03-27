import sys
import re
import auth
import message
import channels
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError


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
#                   CHANNELS_LIST                           #      
#############################################################

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    
    payload = request.get.json()
    chann_inf = channels.List(payload)
    
    return dumps({
        chann_inf
    })


#############################################################
#                   CHANNELS_LISTALL                        #      
#############################################################

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    
    payload = request.get_json()
    chann_inf2 = channels.Listall(payload)

    return  dumps({
        chann_inf2
    })


#############################################################
#                   MESSAGE_PIN                             #      
#############################################################

@APP.route("message/pin", methods=['POST'])
def message_pin():
    
    payload = request.get_json()
    message.pin(payload)

    return dumps({})

#############################################################
#                   MESSAGE_UNPIN                             #      
#############################################################

@APP.route("message/pinall", methods=['POST'])
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
#                   MESSAGE_REMOVE                          #      
#############################################################

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    payload = request.get_json()
    message.remove(payload)

    return dumps({})

#############################################################
#                   STANDUP_START                           #      
#############################################################
#@APP.route("/standup/start", methods=['POST'])
#def standup_start():
    

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))