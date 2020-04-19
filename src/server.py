'''
Main serve file for flask server
Contains all routes
'''

#pylint: disable=W0611
#pylint: disable=C0103

import sys
import re
import datetime
import threading
from json import dumps

from flask_cors import CORS
from flask import Flask, request, jsonify
import auth
import message
import channel
import channels
import standup
import other
import user
from admin_user_remove import user_remove
from data_stores import save_data_stores
from error import InputError
from admin_user_remove import user_remove

def defaultHandler(err):
    'Given from gitlab'
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
#                       AUTH_REGISTER                       #
#############################################################

@APP.route("/auth/register", methods=['POST'])
def auth_register():
    '''
    Function to register a new user to the slack
    '''
    payload = request.get_json()
    new_user = auth.register(payload)

    return dumps({
        'u_id': new_user['u_id'],
        'token': new_user['token'],
    })


#############################################################
#                        AUTH_LOGIN                         #
#############################################################

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    '''
    Function to login a user to a slack
    '''
    payload = request.get_json()
    user1 = auth.login(payload)

    return dumps({
        'u_id' : user1['u_id'],
        'token' : user1['token']
    })


#############################################################
#                        AUTH_LOGOUT                        #
#############################################################

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    Function logout a user from a slack
    '''
    payload = request.get_json()
    if auth.logout(payload):
        return dumps({
            'is_success':True
        })
    else:
        return dumps({
            'is_success':False
        })


#############################################################
#                      CHANNELS_CREATE                      #
#############################################################

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    '''
    Function to create a new channel in the slack
    '''
    payload = request.get_json()
    new_channel = channels.create(payload)
    return dumps({
        'channel_id': new_channel['channel_id']
    })


#############################################################
#                       CHANNELS_LIST                       #
#############################################################

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    '''
    Function to list all channels a user is a part of
    '''
    token = request.args.get('token')
    chann_inf = channels.List(token)

    return dumps({
        'channels': chann_inf
    })


#############################################################
#                     CHANNELS_LISTALL                      #
#############################################################

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    'To display all the channels created on the server'
    token = request.args.get('token')
    chann_inf2 = channels.Listall(token)

    return  dumps({
        'channels':chann_inf2
    })


#############################################################
#                        MESSAGE_PIN                        #
#############################################################

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    'To pin a users message'
    payload = request.get_json()
    message.pin(payload)

    return dumps({})


#############################################################
#                       MESSAGE_UNPIN                       #
#############################################################

@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    'To unpin a users message'
    payload = request.get_json()
    message.unpin(payload)

    return dumps({})


#############################################################
#                       MESSAGE_SEND                        #
#############################################################

@APP.route("/message/send", methods=['POST'])
def message_send():
    '''
    Function to send a message to a channel
    '''
    payload = request.get_json()
    new_message = message.send(payload)

    return dumps({
        'message_id': new_message['message_id']
    })


#############################################################
#                     MESSAGE_SENDLATER                     #
#############################################################

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    '''
    Function to send a message to a channel at a specified time 
    in the future
    '''
    payload = request.get_json()

    new_message_id = message.sendlater(payload)

    return dumps({
        'message_id':new_message_id
    })


#############################################################
#                      MESSAGE_REMOVE                       #
#############################################################

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    '''
    Function to remove a message from a channel
    '''
    payload = request.get_json()
    message.remove(payload)

    return dumps({})


#############################################################
#                       MESSAGE_EDIT                        #
#############################################################

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    '''
    Function to edit a given message in a channel
    '''
    payload = request.get_json()

    payload = request.get_json()
    message.edit(payload)

    return dumps({})


#############################################################
#                       MESSAGE_REACT                       #
#############################################################

@APP.route("/message/react", methods=['POST'])
def message_react():
    '''
    Function to react to a given message in a channel
    '''
    payload = request.get_json()
    message.react(payload)

    return dumps({})


#############################################################
#                      MESSAGE_UNREACT                      #
#############################################################

@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    '''
    Function to unreact to a given message in a channel
    '''
    payload = request.get_json()
    message.unreact(payload)

    return dumps({})


#############################################################
#                       STANDUP_START                       #
#############################################################

@APP.route("/standup/start", methods=['POST'])
def standup_start():
    'To start a standup'
    payload = request.get_json()
    end_time = standup.start(payload)

    return dumps({
        'time_finish':end_time
    })


#############################################################
#                      STANDUP_ACTIVE                       #
#############################################################

@APP.route("/standup/active", methods=['GET'])
def standup_active():
    'To check if a standup is currently active'
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    payload = {
        'token': token,
        'channel_id': channel_id
    }
    standup_info = standup.active(payload)

    return dumps(standup_info)


#############################################################
#                       STANDUP_SEND                        #
#############################################################

@APP.route("/standup/send", methods=['POST'])
def standup_send():
    'To send messages during a standup'
    payload = request.get_json()
    standup.send(payload)

    return ({})

#############################################################
#                      CHANNEL_INVITE                       #
#############################################################

@APP.route('/channel/invite', methods=['POST'])
def channel_invite_server():
    'Invite user to a channel'
    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id = int(payload['u_id'])

    # Invite user to channel
    channel.invite(token, channel_id, user_id)

    return dumps({})


#############################################################
#                      CHANNEL_DETAILS                      #
#############################################################

@APP.route('/channel/details', methods=['GET'])
def channel_details_server():
    'Get details of a channel'

    # Information from request
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    details = channel.details(token, channel_id)

    return dumps(details)


#############################################################
#                     CHANNEL_MESSAGES                      #
#############################################################

@APP.route('/channel/messages', methods=['GET'])
def channel_messages_server():
    'Returns messages from channel'

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
    'User leaves channel'

    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Leave the channel
    channel.leave(token, channel_id)

    return dumps({})


#############################################################
#                       CHANNEL_JOIN                        #
#############################################################

@APP.route('/channel/join', methods=['POST'])
def channel_join_server():
    'User joins channel'

    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])

    # Join the channel
    channel.join(token, channel_id)

    return dumps({})


#############################################################
#                     CHANNEL_ADDOWNER                      #
#############################################################

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner_server():
    'Able to add a member as an owner'

    payload = request.get_json()

    # Information from request
    token = payload['token']
    channel_id = int(payload['channel_id'])
    user_id_adding = int(payload['u_id'])

    # Add owner with user_id to owner members
    channel.addowner(token, channel_id, user_id_adding)

    return dumps({})


#############################################################
#                    CHANNEL_REMOVEOWNER                    #
#############################################################

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner_server():
    'Able to remove an owner as an owner'

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
    'Resetting the workspace'

    other.workspace_reset()
    return dumps({})


#############################################################
#                          SEARCH                           #
#############################################################

@APP.route('/search', methods=['GET'])
def search():
    'Return messages'

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    payload = {
        'token' : token,
        'query_str' : query_str
    }
    messages = other.search(payload)
    return dumps({
        'messages': messages
    })


#############################################################
#                  USER PERMISSION CHANGE                   #
#############################################################

@APP.route('/admin/userpermission/change', methods=['POST'])
def user_permission_change():
    "Return empty dictionary, change user's permission"

    payload = request.get_json()
    user.permission_change(payload)
    return dumps({})


#############################################################
#                       USER_PROFILE                        #
#############################################################

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    "Return 'email', 'name_first', 'name_last', 'handle_str', unpin a message"
    '''
    MIGHT NEED TO BE CHANGED; should it return the person who makes the call or the profile of the u_id
    '''

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    payload = {
        'token': token,
        'u_id': u_id
    }
    user_info = user.profile(payload)
    return dumps ({
        'user': user_info
    })


#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    "Return empty dictionary, change user's name"

    payload = request.get_json()
    user.profile_setname(payload)

    return dumps({})


#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    "Return empty dictionary, change user's email"

    payload = request.get_json()
    user.profile_setemail(payload)

    return dumps({})


#############################################################
#                  USER_PROFILE_SETHANDLE                   #
#############################################################

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    "Return empty dictionary, change user's handle"

    payload = request.get_json()
    user.profile_sethandle(payload)

    return dumps({})


#############################################################
#                         USERS_ALL                         #
#############################################################

@APP.route('/users/all', methods=['GET'])
def all_users():
    "Returns a list of all users and their associated details"

    token = request.args.get('token')

    payload = {
        'token': token
    }
    ret = other.users_all(payload)
    return dumps({
        'users':ret
    })


#############################################################
#                     ADMIN_USER_REMOVE                     #
#############################################################

@APP.route('/admin/user/remove', methods=['DELETE'])
def admin_user_remove_server():
    'Remove user from slackr'
    payload = request.get_json()

    # Remove owner with user_id from slack
    user_remove(payload)

    return dumps({})


#############################################################
#                AUTH_PASSWORDRESET_REQUEST                 #
#############################################################

@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_request():
    'To request a resetcode to reset a users password'

    payload = request.get_json()
    auth.request(payload)

    return dumps({})


#############################################################
#                 AUTH_PASSWORDRESET_RESET                  #
#############################################################

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_reset():
    'To reset the users password'
    payload = request.get_json()
    auth.reset(payload)

    return dumps({})

if __name__ == "__main__":
    threading.Timer(60.0, save_data_stores).start()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
