import auth
import channels
# import channel
import message
import pytest
from test_helper_functions import reg_user1, reg_user2, register_and_create
from data_stores import get_auth_data_store, get_channel_data_store, get_messages_store, reset_auth_store
from error import InputError,AccessError


#############################################################
#                   MESSAGE_SEND                            #      
#############################################################


def test_send1():
    # an owner of a channel sends a message
    reset_auth_store()
    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    payload = {
        'token':user['token'],
        'channel_id': channel['channel_id'],
        'message' : 'testing'
    }

    message_test = message.send(payload)

    message_store = get_messages_store()
    channels = get_channel_data_store()

    assert message_test in message_store
    assert message_test in channel['messages'] 


'''
def test_send2():
    # a member of a channel sends a message
    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    user2 =  reg_user2()

    channel.join({
        'token': user2['token'],
        'channel_id' : channel['channel_id'],
        'u_id': user2['u_id']
    })

    message_test = message.send({
        'token':user2['token'],
        'channel_id': channel['channel_id'],
        'message' : 'testing'
    })

    assert message_test in channel['messages'] 
'''
    

def test_long_msg():
    #sending a message more thatn 1000 characters, should raise an Input error
    reset_auth_store()
    auth_store = get_auth_data_store()
    print (auth_store)
    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']
    
    with pytest.raises(InputError):
        message.send({
            'token': user['token'], 
            'channel_id': channel['channel_id'],
            'message': 'To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment. Rather than re-invent the wheel, UNSW has decided that it finds the functionality of Slack to be nearly exactly what it needs. For this reason, UNSW has contracted out Lit Pty Ltd (a small software business run by Hayden) to build the new product. In UNSWs attempt to connect with the younger and more "hip" generation that fell in love with flickr, Tumblr, etc, they would like to call the new UNSW-based product slackr. Lit Pty Ltd has sub-contracted two software firms: Catdog Pty Ltd (two software developers, Sally and Bob, who will build the initial web-based GUI). YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 20T1), who will build the backend python server and possibly assist in the GUI later in the project. In summary, UNSW contracts Lit Pty Ltd, who sub contracts:Catdog (Sally and Bob) for front end work, YourTeam (you and others) for backend work'
        })






def test_unauthorised():
    # a user sending a message into a  channel in which they are not a 
    # part of causing an access error
    reset_auth_store()
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']
    
    user2 = reg_user2()


    with pytest.raises(InputError):
        message.send({
            'token': user2['token'], 
            'channel_id': channel1['channel_id'],
            'message':'testing'
        })


def test_badtoken1():
    # if a invalid token is provided when message.send is called
    # it should cause an input error
    reset_auth_store()
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()
    auth.logout({
        'token':user2['token']
    })

    with pytest.raises(InputError):
        message.send({
            'token': user2['token'], 
            'channel_id': channel1['channel_id'],
            'message':'testing'
        })
