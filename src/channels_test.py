import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError


'''
#############################################################
#                   CHANNELS_LIST                           #      
#############################################################
'''
def test_list_channel_one():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    #returns channel_id
    channel_info1 = channels_create(token1, 'Slakrs', True)

    my_channel_id1 = channel_info1['channel_id']

    assert (channels_list(token1)["channels"][0]['channel_id']) == my_channel_id1


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

    channel_info1 = channels_create(token1, 'Slakrs', True)
    channel_info2 = channels_create(token2, 'Kings Landing' , True)

    #channel1 = channel_details(token1, channel_info1)
    #channel2 = channel_details(token2, channel_info2)

    all_channels = channels_listall(token2)
    
    flag = 0
    j = 0

    for i in all_channels:
        if (channel_info1 or channel_info2) == all_channels[j]:
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