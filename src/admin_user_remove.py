'This file is for admin_user_remove (iteration 3)'

from data_stores import get_auth_data_store, get_channel_data_store, get_messages_store
from helper_functions import get_user_uid, user_details, is_valid_user_id, check_owner_slackr
from helper_functions import message_belong_user
from error import InputError, AccessError

def user_remove(payload):
    'This is the function for admin_user_remove'
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()
    messages_store = get_messages_store()

    #remover_id = user_id_from_token(payload['token'])
    #remover_dets = user_details(remover_id)

    removee = get_user_uid(payload['u_id'])
    removee_dets = user_details(payload['u_id'])

    # InputError for invalid user ID of the person we are removing
    if not is_valid_user_id(int(payload['u_id'])):
        raise InputError(description='Invalid user_id')

    # AccessError when the authorised user is not an owner of the slackr
    if not check_owner_slackr(payload['token']):
        raise AccessError(description='User is not an owner of the slackr')
    else:
        auth_store.remove(removee)

    # Removing user from any channels they were in
    for channel in channel_store:
        if removee_dets in channel['members']:
            channel['members'].remove(removee_dets)
        if removee_dets in channel['owners']:
            channel['owners'].remove(removee_dets)

    # Removing any messages the user had sent
    removee_token = removee['token']

    for messages in messages_store:
        if message_belong_user(removee_token, messages['message_id']):
            messages_store.remove(messages)

    return{}

'''
def user_remove(token, u_id):
    'This is the function for admin_user_remove'
    auth_store = get_auth_data_store()
    channel_store = get_channel_data_store()

    #for i in channel_store:
    #    channel = i['channel_id']
    #    return channel


    payload1 = {
        'email': remover['email'],
        'password': remover['password'],
        'name_first': remover['name_first'],
        'name_last': remover['name_last']
    }


    remover_id = user_id_from_token(token)
    print(remover_id)
    remover_dets = user_details_email_pw(remover_id)
    print(remover_dets)
    removee_dets = user_details_email_pw(u_id)
    print(removee_dets)
    #auth.register(remover_dets)
    #auth.register(removee_dets)

    # InputError for invalid user ID of the person we are removing
    if not is_valid_user_id(u_id):
        raise InputError(description='Invalid user_id')

    #so we have a slackr owner who can remove users from slackr
    # the remover is the person removing, removee does not have to be owner, can be anyone
    #trying to wipe someone's existence
    # remove email, password, auth_data, token

    # AccessError when the authorised user is not an owner of the slackr
    if not check_owner_slackr(token):
        raise AccessError(description='User is not an owner of the slackr')
    else:
        del removee_dets


    payload = {
        'token': token,
        'name': 'Slackrs',
        'is_public': True
    }
    channel_new = channels.create(payload)
    channel_id = channel_new['channel_id']

    # From helper function
    channel = get_channel(channel_id)
    print(channel['members'])
    if test_in_channel(u_id, channel):
        # we want to remove them from channel
        channel['members'].remove(removee_dets)


    removee_token = get_token_uid(u_id)

    if message_belong_user(removee_token, message_id):
        payload2 = {
            'token': removee_token,
            'message_id': message_id
        }
        message.remove(payload2)

    return{}

    def check_member_slackr(token):
        user = get_user_token(token)
        user_permission = user['permission_id']        

        if user_permission == 2:
            return True
        return False

    #auth_store.remove(removee_dets)

    # remover user from all cahnnels
    # delete their msgs


    # AccessError when the authorised user is not an owner of the slackr
    #if remover_dets not in channel['owners']:
    #    raise AccessError(description='User is not an owner of the slackr')
    #elif removee_dets in channel['owners']:
    #   channel['owners'].remove(removee_dets)
        # No need to append to members as they're removed from channel/slackr
    #elif removee_dets in channel['members']:
    #else:
    #    channel['members'].remove(removee_dets)


    if message_belong_user(removee_token, message_id):
        message_info = {
            'token': removee_token,
            'message_id': message_id
        }
        message.remove(message_info)

        #if messages['message_id'] == message_belong_user(removee_token, messages['message_id']):
'''
  