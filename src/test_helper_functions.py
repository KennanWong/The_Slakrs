'''
Set of functions used for testing 
'''
import auth
import message
import channels


# function to register user1
def reg_user1():
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    user1 = auth.register(payload)
    return user1

# function to register user2
def reg_user2():
    payload = {
        'email' : 'Cindy@gmail.com',
        'password': 'Tran123',
        'name_first': 'Cindy',
        'name_last': 'Tran'
    }
    user2 = auth.register(payload)
    return user2

# function used to register a user and then create a channel
def register_and_create():
    payload1 = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    result1 = auth.register(payload1)

    payload2 = {
        'token' : result1['token'],
        'name': 'firstChannel',
        'is_public': True
    }
    new_channel = channels.create(payload2)
    return {
        'user':result1,
        'channel':new_channel
    }