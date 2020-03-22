import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError



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


def get_channel_data_store():
    global channels_store
    return channels_store

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
                        'members': [],
                        'owners': [],                        
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
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    payload = request.get_json()

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
