import pytest
from auth import auth_register, auth_login
from channel import channel_details, channel_addowner, channel_removeowner
from channels import channels_create
from error import InputError, AccessError


'''
#############################################################
#                   CHANNEL_ADDOWNER                       #      
#############################################################
'''

def test_channel_add_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    channel_addowner(token1, channel_info3, u_id2)

    owners = channel_details(token2, channel_info3)['owner_members']

    print(channel_details(token2, channel_info3))
    print(owners[0]['u_id'])

    is_owner = 0
    j = 0

    for i in owners:
        if u_id2 == owners[j]['u_id']:
            is_owner = 1
        j =+ 1

    assert is_owner == 1

def test_already_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    u_id1 = results['u_id']
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    with pytest.raises(InputError):
        channel_addowner(token1, channel_info3, u_id1)

def test_not_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    with pytest.raises(AccessError):
        channel_addowner(token2, channel_info3, u_id2)


def test_invalid_channel():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)
    invalidChannelID = 1
    
    with pytest.raises(InputError):
        channel_addowner(token2, invalidChannelID, u_id2)
'''
#############################################################
#                   CHANNEL_REMOVEOWNER                    #      
#############################################################
'''
def test_channel_remove_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    u_id1 = results['u_id']
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    channel_addowner(token1, channel_info3, u_id2)

    channel_removeowner(token2 ,channel_info3, u_id1)
    
    owners = channel_details(token2, channel_info3)['owner_members']

    print(channel_details(token2, channel_info3))
    print(owners[0]['u_id'])

    is_owner = 0
    j = 0

    for i in owners:
        if u_id2 == owners[j]['u_id']:
            is_owner = 0
        j =+ 1

    assert is_owner == 0

def test_invalid_channel2():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    u_id1 = results['u_id']
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)
    channel_addowner(token1, channel_info3, u_id2)
    invalidChannelID = 1
    
    with pytest.raises(InputError):
        channel_removeowner(token2, invalidChannelID, u_id1)

def test_userid_not_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2 = results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)
    channel_addowner(token1, channel_info3, u_id2)
    invalidUser_id = 1
    with pytest.raises(InputError):
        channel_removeowner(token2, channel_info3, invalidUser_id)

def test_not_owner2():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    u_id1 = results['u_id']
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2 = results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    with pytest.raises(AccessError):
        channel_removeowner(token2, channel_info3, u_id1)
    
    