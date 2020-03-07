import auth
import pytest
from error import InputError


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

    channel_addowner(token2, channel_info3, u_id2)

    owners = channel_details(token2, channel_info3)['owner_members']

    print(channel_details(token2, channel_info3))
    print(owners[0]['u_id'])

    is_owner = 0
    j = 0

    for j in owners:
        if u_id2 == owners[j]['u_id']:
            is_owner = 1
        j =+ 1

    assert is_owner == 1

def test_already_owner():
    with pytest.raises(InputError) as e:
        channel_addowner(token1, channel_info3, u_id1)

def test_invalid_channel():
    invalidChannelID = 1
    with pytest.raises(InputError) as e:
        channel_addowner(token2, invalidChannelID, u_id2)
'''
#############################################################
#                   CHANNEL_REMOVEOWNER                    #      
#############################################################
'''
def test_channel_remove_owner():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    results = auth_login('guest123@gmail.com', '123!Asdf')
    token1 = results['token']

    results2 = auth_register('bobbuilder@gmail.com', 'zxc123asd','Bob', 'Builder')
    results2 = auth_login('bobbuilder@gmail.com','zxc123asd')
    u_id2= results2['u_id']
    token2 = results2['token']

    channel_info3 = channels_create(token1, 'Slakrs', True)

    channel_addowner(token2, channel_info3, u_id2)

    channel_removeowner(token1 ,channel_info3, u_id1)
    
    owners = channel_details(token2, channel_info3)['owner_members']

    print(channel_details(token2, channel_info3))
    print(owners[0]['u_id'])

    is_owner = 0
    j = 0

    for j in owners:
        if u_id2 == owners[j]['u_id']:
            is_owner = 1
        j =+ 1

    assert is_owner == 0

def test_invalid_channel():
    invalidChannelID = 1
    with pytest.raises(InputError) as e:
        channel_addowner(token2, invalidChannelID, u_id2)

def test_not_owner():
    with pytest.raises(InputError) as e:
        channel_removeowner(token1 ,channel_info3, u_id1)
    
'''
#############################################################
#                   CHANNELS_LIST                           #      
#############################################################
'''
def test_list_and_details():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    channel_info1 = channels_create(token1, 'Slakrs', False)

    channel = channel_details(token1, channel_info1)

    channel_member = channels_list(token1)
    
    flag = 0
    j = 0

    for j in channel_member:
        if channel_info1 == channel_member[j]:
            flag = 1
        j =+ 1
    
    assert flag == 1

'''
#############################################################
#                   CHANNELS_LISTALL                        #      
#############################################################
'''
def test_listall_and_details():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    result2 = auth_register("sidsat@gmail.com", '123!Asdf', 'Sid', 'Sat')
    token2 = results['token']
    u_id2 = results['u_id']

    channel_info1 = channels_create(token1, 'Slakrs', False)
    channel_info2 = channels_create(token2, 'Kings Landing' , True)

    channel1 = channel_details(token1, channel_info1)
    channel2 = channel_details(token2, channel_info2)

    channel_member1 = channels_listall(token1)
    
    
    flag = 0
    j = 0

    for j in channel_member:
        if (channel_info1 or channel_info2) == channel_member1[j]:
            flag = 1
        j =+ 1
    
    assert flag == 1

'''
#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################
'''
#channel can either be public or private
def test_create_channel_private():

    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['user']

    channel_info1 = channels_create(token1, 'Slakrs', False)
    

    #channel name must be 20 characters or smaller
    with pytest.raises(InputError) as e:
        channel_info2 = channels_create(token1, 'a' * 21, False)

def test_create_channel_public():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['user']

    channel_info3 = channels_create(token1, 'Slakrs', True)
    

    with pytest.raises(InputError) as e:
        channel_info4 = channels_create(token1, 'a' * 21, True)

