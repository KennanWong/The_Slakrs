'This file is for admin_user_remove (iteration 3)'

from data_stores import get_auth_data_store, get_channel_data_store, get_messages_store
from helper_functions import get_user_uid, user_details, is_valid_user_id, check_owner_slackr
from helper_functions import message_belong_user
from error import InputError, AccessError

# pylint compliant

def user_remove(payload):
    'This is the function for admin_user_remove'

    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    messages_store = get_messages_store()

    # remover_id = user_id_from_token(payload['token'])
    # remover_dets = user_details(remover_id)

    removee = get_user_uid(payload['u_id'])
    removee_dets = user_details(payload['u_id'])

    # InputError for invalid user ID of the person we are removing
    if not is_valid_user_id(int(payload['u_id'])):
        raise InputError(description='Invalid user_id')

    removee_token = removee['token']
    
    # Removing any messages the user had sent
    for messages in messages_store:
        if message_belong_user(removee_token, messages['message_id']):
            messages_store.remove(messages)
    
    # Removing user from any channels they were in
    for channel in channel_store:
        if removee_dets in channel['members']:
            channel['members'].remove(removee_dets)
        if removee_dets in channel['owners']:
            channel['owners'].remove(removee_dets)
        for message in channel['messages']:
            if message['u_id'] == removee['u_id']:
                channel['messages'].remove(message)

    # AccessError when the authorised user is not an owner of the slackr
    if not check_owner_slackr(payload['token']):
        raise AccessError(description='User is not an owner of the slackr')
    else:
        auth_store.remove(removee)
    
    return{}


    
