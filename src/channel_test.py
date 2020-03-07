import channel
import auth
import channels
import pytest
from error import InputError

'''
#############################################################
#                   CHANNEL_ADDOWNER                        #      
#############################################################
'''


def test_addowner():
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']

    user2 = auth.register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth.login('dean.yu@gmail.com','password2')
    user2_id = user2['u_id']
    user2_tk = user2['token']
        
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    
    channel.addowner(user2_tk, channel_id1, user2_id)

    channel_owners = channel.details(user2_tk, channel_id1)['owner_members']
    
    print(channel.details(user2_tk, channel_id1))
    print(channel_owners[0]['u_id'])

    inList = 0
    counter = 0

    for i in channel_owners:
        if user2_id == channel_owners[counter]['u_id']:
            inList = 1
        counter=+ 1

    assert inList == 1