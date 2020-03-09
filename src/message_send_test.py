import message
import auth
import channel
import channels
import pytest
from error import InputError,AccessError

'''
#############################################################
#                   MESSAGE_SEND                            #      
#############################################################
'''

def test_send1():
    # an owner of a channel sends a message
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']


    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    message_test = message.send(user1_tk,channel_id1,'testing')
    
    assert message_test['message_id'] == 1

def test_send2():
    # a member of a channel sends a message
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    
    user2 = auth.register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth.login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    channel.channel_join(user2_tk, channel_id1)

    msg2_id = message.send(user2_tk,channel_id1,'testing')['message_id']

    assert msg2_id == 1
    

def test_long_msg():
    #sending a message more thatn 1000 characters, should raise an Input error
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)
    with pytest.raises(InputError):
        message_test = message.send(user1_tk, channel_id1, 'To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment. Rather than re-invent the wheel, UNSW has decided that it finds the functionality of Slack to be nearly exactly what it needs. For this reason, UNSW has contracted out Lit Pty Ltd (a small software business run by Hayden) to build the new product. In UNSWs attempt to connect with the younger and more "hip" generation that fell in love with flickr, Tumblr, etc, they would like to call the new UNSW-based product slackr. Lit Pty Ltd has sub-contracted two software firms: Catdog Pty Ltd (two software developers, Sally and Bob, who will build the initial web-based GUI). YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 20T1), who will build the backend python server and possibly assist in the GUI later in the project. In summary, UNSW contracts Lit Pty Ltd, who sub contracts:Catdog (Sally and Bob) for front end work, YourTeam (you and others) for backend work')
    

def test_unauthorised():
    # a user sending a message into a  channel in which they are not a 
    # part of causing an access error

    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    
    
    user2 = auth.register('dean.yu@gmail.com', 'password2','Dean', 'Yu')
    user2 = auth.login('dean.yu@gmail.com','password2')
    user2_tk = user2['token']
    
    
    channel_id1 = channels.create(user1_tk,'firstchannel',True)

    with pytest.raises(InputError):
        message_test = message.send(user2_tk, channel_id1,'testing')

'''    
def test_badtoken1():
    # if a invalid token is provided when message.send is called
    # it should cause an input error
    user1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    user1 = auth.login('John.smith@gmail.com','password1')
    user1_tk = user1['token']
    bad_tk = int(user1) + 1

    channel_id1 = channels.create(user1_tk,'firstchannel',True)

    with pytest.raises(InputError):
        message_test = message.send(bad_tk, channel_id1,'testing')
'''