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
import user
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
#                   WORKSPACE_RESET                         #      
#############################################################
@APP.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    other.workspace_reset()
    return dumps({})

    
#############################################################
#                         SEARCH                            #      
#############################################################   
@APP.route('/search', methods=['GET'])
def search():
    """ return messages """
    payload = request.get_json()
    messages = user.search(payload)
    return dumps({messages})
    
#############################################################
#                USER PERMISSION CHANGE                     #      
#############################################################
@APP.route('/admin/userpermission/change', methods=['POST'])
def userpermission_change():
    """ return empty dic, change user's permission """
    payload = request.get_json()
    user.user_permission_change(payload)
    return dumps({})


#############################################################
#                      USER_PROFILE                         #      
#############################################################

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    """ 
    return 'email', 'name_first', 'name_last', 'handle_str', unpin a msg 
    """
    payload = request.get_json()
    user_info = user.profile(payload)
    return dumps ({user_info})
    

#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    """ 
    return empty dic, change user's name 
    """
    payload = request.get_json()
    user.profile_setname(payload)
    return({})

#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    """ 
    return empty dic, change user's email 
    """
    payload = request.get_json()
    user.profile_setemail(payload)
    return({})

#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    """ 
    return empty dic, change user's handle 
    """
    payload = request.get_json()
    user.profile_sethandle(payload)
    return({})
    
#############################################################
#                        USERS_ALL                          #
#############################################################

@APP.route('/users/all', methods=['GET'])
def all_users():
    """ 
    Returns a list of all users and their associated details
    """
    payload = request.get_json()
    ret = user.users_all(payload)
    return({ret})
    
    
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080)) 

