import pytest
from auth import auth_register
from channel import channel_details
from channels import channels_create, channels_list, channels_listall
from error import InputError, AccessError


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
