import message
import pytest
from error import InputError,AccessError

'''
#############################################################
#                   MESSAGE_SEND                            #      
#############################################################
'''

def test_send1():
    pass

def test_long_msg():
    #input error
    pass

def test_unauthorised():
    #access error
    pass

'''
#############################################################
#                   MESSAGE_REMOVE                          #      
#############################################################
'''

def test_remove1():
    #the person who sent the message is trying to remove the message
    pass

def test_remove2():
    #the admin of a channel is attempting to remove a message
    pass

def test_no_msg():
    #input error
    pass

def test_unauth_remove1():
    #if someone is trying to remove another person message
    #access error
    pass

def test_unauth_remove2():
    #if someone is trying to remove another person message and 
    #is not an admin
    #access error
    pass

'''
#############################################################
#                   MESSAGE_EDIT                            #      
#############################################################
'''

def test_edit1():
    pass

def test_edit2():
    #the person editing is an admin of the channel
    pass

def test_unauth_edit1():
    #if someone is trying to edit another persons message
    #access error
    pass

def test_unauth_edit2():
    #if someone is trying to edit another persons message and 
    #is not an admin
    #access error
    pass


