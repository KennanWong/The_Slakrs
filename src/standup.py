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

    standup = channel['standup']


    if standup['is_active'] is False:
        if test_in_channel(user, channel) is True:
            if payload['length'] > 0:
                length = payload['length']
                standup['is_active'] = True
                timer = threading.Timer(length, end_standup)
                timer.start()
            
                current_time = datetime.datetime.now().time()
                time_finish = addSecs(current_time, length)
                standup['time_finish'] = time_finish
            
            else:
                raise InputError(description='Negative length is invalid')
        
        else:
            raise AccessError(description='User not in channel')

    else:
        raise InputError(description='An active standup is running')


    return time_finish


#run this function where it collates all messages into one
def end_standup(payload):

    channel_store = get_channel_data_store()
    messages = get_messages_store()

    standup_message = []

    channel = get_channel(payload['channel_id'])
    standup = channel['standup']
    
    standup_message.append(standup['messages'])
    channel['messages'].append(standup['messagesß'])
    channel_store.append(standup['messages'])
        
#############################################################
#                   STANDUP_ACTIVE                          #      
#############################################################
        
def active(payload):
    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])


    standup = channel['standup']

    if standup['is_active'] is True:
        standup_info = {
            'is_active': True,
            'time_finish': standup['time_finish']
        }

    return standup_info



#############################################################
#                   STANDUP_SEND                            #      
#############################################################

def send(payload):
    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    
    standup = channel['standup']

    if standup['is_active'] is True:
        if test_in_channel(user, channel) is True:
            message = payload['message']
            if len(message) < 1000:
                new_message = {
                    'Name_first': user['name_first'],
                    'Message': message
                }
                
            else:
                raise InputError(description='Message too long')
        else:
            raise AccessError(description='User is not part of channel')

    else:
        raise InputError(description='Active standup is not running')

    standup['messages'].append(new_message)

    return
    


   