from data_stores import get_messages_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel, test_in_channel, get_user_token, find_message, check_owner
from data_stores import get_channel_data_store 
import datetime
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

    if channel['is_active'] is False:
        if test_in_channel(user, channel) is True:
            if payload['length'] > 0:
                length = payload['length']
                channel['is_active'] = True
                timer = threading.Timer(length, end_standup)
                timer.start()
            

                current_time = datetime.datetime.now().time()
                time_finish = addSecs(current_time, length)

    else:
        raise InputError(description='An active standup is running')

    return time_finish


#run this function where it collates all messages into one
def end_standup(payload):
    
    messages = get_messages_store()
    channel = get_channel(payload['channel_id'])
    standup_message = []

    if channel['is_active'] is True:
        #unsure what to do here

def active(payload):
    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])

    if channel['is_active'] is True:
        length = payload['length']
        current_time = datetime.datetime.now().time()
        time_finish = addSecs(current_time, length)

        return True, time_finish

def send(payload):
    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    
    if channel['is_active'] is True:
        if test_in_channel(user, channel) is True:
            message = payload['message']
            if len(message) < 1000:
                standup_message = create_message()
                standup_message['time_created'] = time
                standup_message['u_id'] = user['u_id']
                standup_message['message'] = message
                standup_message['channel_id'] = payload['channel_id']

            else:
                raise InputError(description='Message too long')
        else:
            raise AccessError(description = 'User is not part of channel')

    else:
        raise InputError(description='Active standup is not running')


    messages.append(standup_message)
    channel['messages'].append(standup_message)

    return 
    


   