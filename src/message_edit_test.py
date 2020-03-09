from message import *
from auth import *
from channel import *
from channels import *
import pytest
from error import InputError,AccessError



'''
#############################################################
#                   MESSAGE_EDIT                            #      
#############################################################
'''

def test_edit1():
    # an admin is editing their own message
    user1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth_login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    channel_id1 = channels_create(user1_tk,'firstchannel',True)
    msg1_id = message_send(user1_tk,channel_id1,'testing')['message_id']
    message_edit(user1_tk, msg1_id, 'testing-edit')

    successEdit = 0


    for a in messages['messageDict']:
        if a['message'] == 'testing-edit':
            successEdit = 1
    

    assert successEdit == 1
    

def test_edit2():
    # a member is editing their own message
    user1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth_login('John.smith@gmail.com','password1')
    user1_tk = user1['token']   
    
    user2 = auth_register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth_login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels_create(user1_tk,'firstchannel',True)
    channel_join(user2_tk, channel_id1)
    msg2_id = message_send(user2_tk,channel_id1,'testing')['message_id']
    message_edit(user2_tk, msg2_id, 'testing-edit')

    successEdit = 0

    
    for a in messages['messageDict']:
        if a['message'] == 'testing-edit':
            successEdit = 1
    

    assert successEdit == 1

def test_edit3():
    # someone attempts to edit a message by replacing it witha a blank string
    user1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth_login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    channel_id1 = channels_create(user1_tk,'firstchannel',True)
    msg1_id = message_send(user1_tk,channel_id1,'testing')['message_id']
    message_edit(user1_tk, msg1_id, '')

    successRemove = 1

    for a in messages['messageDict']:
        if a['message'] == 'testing':
            successRemove == 0
    

    assert successRemove == 1 

def test_edit4():
    # an owner of a channel is editing a message that one of its members had sent
    user1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth_login('John.smith@gmail.com','password1')
    user1_tk = user1['token']   
    
    user2 = auth_register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth_login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels_create(user1_tk,'firstchannel',True)
    channel_join(user2_tk, channel_id1)
    msg2_id = message_send(user2_tk,channel_id1,'testing')['message_id']
    message_edit(user1_tk, msg2_id, 'testing-edit')

    successEdit = 0


    for a in messages['messageDict']:
        if a['message'] == 'testing-edit':
            successEdit = 1
    
    assert successEdit == 1


def test_unauth_edit1():
    # someone who tried to edit another persons message should cause an
    # access error
    user1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth_login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    user2 = auth_register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth_login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels_create(user1_tk,'firstchannel',True)
    channel_join(user2_tk, channel_id1)

    msg1_id = message_send(user1_tk,channel_id1,'testing')['message_id']

    with pytest.raises(AccessError):
        message_edit(user2_tk, msg1_id, 'testing-edit')
    
'''
def test_badtoken3():
    # if a invalid token is provided when message.edit is called
    # it should cause an input error
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    bad_tk = int(user1_tk) + 1

    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    msg1_id = message.send(user1_tk,channel_id1,'testing')['message_id']

    with pytest.raises(InputError):
        message.edit(bad_tk,msg1_id,'testing-edit')

'''