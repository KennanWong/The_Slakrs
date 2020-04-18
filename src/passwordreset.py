'''

This file contains all 'passwordreset' functions

'''
from datetime import datetime, timedelta
import threading
from data_stores import get_messages_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel
from helper_functions import test_in_channel, get_user_token



#############################################################
#                   PASSWORDRESET_REQUEST                   #
#############################################################
def request(payload)