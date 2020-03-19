import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import re

users = [
]
user = {
    'u_id',
    'email',
    'name_last',
    'name_first',
    'handle_str',
}

def useres_rest():
    global users
    users = []
    return users


# to get global users
def getUserStore():
    global users
    return users

# to test if an email is valid, courtesy of geeksforgeeks.org
def testEmail(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
    if (re.search(regex, email)):
        return email
    else:
        raise InputError

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

#register a user and add it to the userStore
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    usersStore = getUserStore()
    payload = request.get_json()
    handle = (payload['name_first']+payload['name_last'])
    if len(handle) > 24:
        handle = handle[0:20]

    #test if valid email    
    email = testEmail(payload['email'])


    
    new_user = {
        'u_id': int(len(usersStore)+1),
        'email': email,
        'name_first': payload['name_first'],
        'name_last': payload['name_last'],
        'handle_str': handle.lower()
    }
    usersStore.append(new_user)

    print(usersStore)
    return dumps({
        'u_id':new_user['u_id'],
        'token': 1
    })


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))



