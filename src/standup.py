from data_stores import get_messages_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel
from helper_functions import test_in_channel, get_user_token
from helper_functions import find_message, check_owner
from data_stores import get_channel_data_store
from datetime import datetime, timedelta
import threading
import time
from helper_functions import addSecs

#############################################################
#                   STANDUP_START                           #      
#############################################################
def start(payload):

    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])

    standup = channel['standup']


    if standup['is_active'] is False:
        if test_in_channel(user['u_id'], channel) is True:
            if payload['length'] > 0:
                length = payload['length']
                standup['is_active'] = True

                time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")

                standup['time_finish'] = time_finish

                timer = threading.Timer(length, end_standup, args=[payload])
                timer.start()
            
            else:
                raise InputError(description='Negative length is invalid')
        
        else:
            raise AccessError(description='User not in channel')

    else:
        raise InputError(description='An active standup is running')


    return time_finish


#run this function where it collates all messages into one
def end_standup(payload):

    messages = get_messages_store()

    standup_message = ''

    channel = get_channel(payload['channel_id'])
    standup = channel['standup']
    user = get_user_token(payload['token'])
    
    # formating all the messages into one message package
    for msg in standup['messages']:
        standup_message += msg['Name_first']
        standup_message += ': '
        standup_message += msg['Message']
        standup_message += '\n'

    standup_message = standup_message[0:(len(standup_message)-1)]

    new_message = create_message()
    new_message['channel_id'] = channel['channel_id']
    new_message['u_id'] = user['u_id']
    new_message['message'] = standup_message

    messages.append(new_message)
    channel['messages'].append(new_message)

    # reset standup
    standup['is_active'] = False
    standup['time_finish'] = 'N/A'
    print('finished standup')
    return

        
#############################################################
#                   STANDUP_ACTIVE                          #      
#############################################################
def active(payload):
    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])

    standup = channel['standup']


    if standup['is_active']:
        standup_info = {
            'is_active': True,
            'time_finish': standup['time_finish']
        }
    else:
        standup_info = {
            'is_active': False,
            'time_finish': 'N/A'
        }
    return standup_info




#############################################################
#                   STANDUP_SEND                            #      
#############################################################

def send(payload):
    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    
    standup = channel['standup']

    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='User is not part of channel')

    if standup['is_active'] is not True:
        raise InputError(description='Active standup is not running')

    message = payload['message']
    if len(message) > 1000:
        raise InputError(description='Message too long')

    new_message = {
        'Name_first': user['name_first'],
        'Message': message
    }

    standup['messages'].append(new_message)

    return
    


   