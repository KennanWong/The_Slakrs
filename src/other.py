'''
This file contains all function stubs for 'other_' functions and misclaneous
'''

from data_stores import reset_auth_store, reset_channel_data_store
from data_stores import reset_messages_store
from helper_functions import reset_message_count


def workspace_reset():
    '''
    Function to reset the workspace
    '''
    reset_auth_store()
    reset_channel_data_store()
    reset_messages_store()   
    reset_message_count()

    return