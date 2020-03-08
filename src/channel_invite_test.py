import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_invite
from channels import channels_create

'''
#############################################################
#                      CHANNEL_INVITE                       #      
#############################################################

InputError when any of:
**  channel_id does not refer to a valid channel that the authorised user is part of.
**  u_id does not refer to a valid user

AccessError when:
** the authorised user is not already a member of the channel
'''

def test_channel_invite_successful():
    # CASE 1: Successful invite
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']
    u_id2 = user2['u_id']

    # Create a channel, takes in token, name, is_public
    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

	# Inviting user2 to channel
    channel_invite(token1, channel_id, u_id2)
    
def test_channel_invite_invalid_channel():
    # CASE 2: Inviting user to invalid channel
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']
    u_id2 = user2['u_id']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    # InputError when user2 is invited to an invalid channel
    with pytest.raises(InputError) as e:
        channel_invite(token1, invalidChannelID, u_id2)

def test_channel_invite_invaliduserID():   
    # CASE 3: Inviting user with invalid userID
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']
    invalidUserID = 1

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # InputError when user tries to invite someone with an invalid user ID
    with pytest.raises(InputError) as e:
        channel_invite(token1, channel_id, invalidUserID)

def test_channel_invite_unauthorised():
    # CASE 4: Inviting a user when the authorised user is not a member of channel
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']
    u_id2 = user2['u_id']
    
    user3 = auth_register("user3@gmail.com", 'nkoim$#475', 'user3', 'Shelby')
    token3 = user3['token']
    u_id3 = user3['u_id']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # AccessError when authorised user is not a member of the channel
    with pytest.raises(AccessError) as e:
        channel_invite(token1, channel_id, u_id3)

def test_channel_invite_existing_user(): 
    # CASE 5: Inviting a user who is already a member of channel
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']
    u_id2 = user2['u_id']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # InputError when user tries to invite someone who is already a member of the channel
    with pytest.raises(InputError) as e:
        channel_invite(token1, channel_id, u_id2)