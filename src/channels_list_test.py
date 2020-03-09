import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError


def test_list_channel_one():
    results = auth_register("guest123@gmail.com", '123!Asdf', 'John', 'Smith')
    token1 = results['token']
    u_id1 = results['u_id']

    #returns channel_id
    channel_info1 = channels_create(token1, 'Slakrs', True)

    my_channel_id1 = channel_info1['channel_id']


    assert (channels_list(token1)["channels"][0]['channel_id']) == my_channel_id1