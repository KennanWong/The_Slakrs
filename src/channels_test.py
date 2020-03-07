import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create
from error import InputError, AccessError


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
    u_id1 = results['u_id']

    channel_info1 = channels_create(token1, 'Slakrs', False)
    

def test_create_channel_public():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    channel_info3 = channels_create(token1, 'Slakrs', True)
    

def test_channel_name_too_long():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    with pytest.raises(InputError) as e:
        channel_info4 = channels_create(token1, 'a' * 21, True)