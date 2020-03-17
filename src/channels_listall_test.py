import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError

def test_listall_and_details():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    result2 = auth_register("sidsat@gmail.com", '123!Asdf', 'Sid', 'Sat')
    token2 = results['token']
    u_id2 = results['u_id']

    channel_info1 = channels_create(token1, 'Slakrs', True)
    channel_info2 = channels_create(token2, 'Kings Landing' , True)

    all_channels = channels_listall(token2)
    
    flag = 0
    j = 0

    for i in all_channels:
        if (channel_info1 or channel_info2) == all_channels[j]:
            flag = 1
        j =+ 1
    
    assert flag == 1
