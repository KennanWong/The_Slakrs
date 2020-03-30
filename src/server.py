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
#                   MESSAGE_SEND                            #      
#############################################################


@APP.route("/message/send", methods=['POST'])
def message_send():
    payload = request.get_json()
    new_message = message.send(payload)

    return dumps({
        'message_id': new_message['message_id']
    })
    



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))

#############################################################
#                   MESSAGE_REMOVE                          #      
#############################################################

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    payload = request.get_json()
    message.remove(payload)

    return dumps({})
    
    
    
    
#############################################################
#                         SEARCH                            #      
#############################################################   
@APP.route('/search', methods=['GET'])
def message_search():
    """ return messages """
    result = search(request.args.get('token'), request.args.get('query_str'))
    return dumps(result)
    
#############################################################
#                USER PERMISSION CHANGE                     #      
#############################################################
@APP.route('/admin/userpermission/change', methods=['POST'])
def userpermission_change():
    """ return empty dic, change user's permission """
    result = permission(request.form.get('token'), int(request.form.get('u_id')),
                        int(request.form.get('permission_id')))
    return dumps(result)


#############################################################
#                      USER_PROFILE                         #      
#############################################################

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    """ 
    return 'email', 'name_first', 'name_last', 'handle_str', unpin a msg 
    """
    result = profile(request.args.get('token'), request.args.get('u_id'))
    result['profile_img_url'] = str(request.base_url) + result['profile_img_url']
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    """ 
    return empty dic, change user's name 
    """
    result = setname(request.form.get('token'), request.form.get('name_first'),request.form.get('name_last'))
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    """ 
    return empty dic, change user's email 
    """
    result = setemail(request.form.get('token'), request.form.get('email'))
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    """ 
    return empty dic, change user's handle 
    """
    result = sethandle(request.form.get('token'), request.form.get('handle_str'))
    return dumps(result)
    
#############################################################
#                        USERS_ALL                          #
#############################################################

@APP.route('/users/all', methods=['GET'])
def all_users():
    """ 
    show all users 
    """
    result = all_user(request.args.get('token'))
    return dumps(result) 
