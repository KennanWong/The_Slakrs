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
    
    
    if standup['is_active'] is False:
        if test_in_channel(user, channel) is True:
            if payload['length'] > 0:
                length = payload['length']
                current_time = datetime.datetime.now().time()
                new_time = addSecs(current_time, length)
                

    else:
        raise InputError(description='An active standup is running')

    
