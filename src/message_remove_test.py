import message
import auth
import channel
import channels
import pytest
from error import InputError,AccessError

'''
#############################################################
#                   MESSAGE_REMOVE                          #      
#############################################################
'''

def test_remove1():
    #the person who sent the message is trying to remove the message
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    msg1_id = message.send(user1_tk,channel_id1,'testing')['message_id']

    message.remove(user1_tk,msg1_id)

    successRemove = 0

    for a in messages['messageDict']:
        if a['message_id'] == msg1_id:
            successRemove = 1
    

    assert successRemove == 1 

def test_remove2():
    #the admin of a channel is attempting to remove a message

    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    
    user2 = auth.register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth.login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    channel.channel_join(user2_tk, channel_id1)

    msg2_id = message.send(user2_tk,channel_id1,'testing')['message_id']
    
    message.remove(user1_tk,msg2_id)

    successRemove = 0

    for a in messages['messageDict']:
        if a['message_id'] == msg2_id:
            successRemove = 1
    
    assert successRemove == 1 
    
def test_no_msg():
    # attempting to remove a message that has been already removed or does
    # not exist causing an input error
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    msg1_id = message.send(user1_tk,channel_id1,'testing')['message_id']

    msg2_id = msg1_id + 1

    with pytest.raises(InputError):
        message.remove(user1_tk,msg2_id)
    

def test_unauth_remove1():
    # if someone is trying to remove another person message causing
    # an access error

    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    
    user2 = auth.register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth.login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    channel.channel_join(user2_tk, channel_id1)

    msg1_id = message.send(user1_tk,channel_id1,'testing')['message_id']

    with pytest.raises(AccessError):
        message.remove(user2_tk,msg1_id)
    
'''
def test_badtoken2():
    # if a invalid token is provided when message.remove is called
    # it should cause an input error
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    bad_tk = int(user1_tk) + 1

    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    msg1_id = message.send(user1_tk,channel_id1,'testing')['message_id']

    with pytest.raises(InputError):
        message.remove(bad_tk,msg1_id)
'''
