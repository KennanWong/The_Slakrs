# This file contains the implementation of all 'user_' functions for the
# server

from error import InputError, AccessError
from data_stores import get_channel_data_store
from channel import addowner, removeowner
from helper_functions import get_user_from, validate_uid, test_email, get_user_token
from helper_functions import test_in_channel, check_channel_permission
from helper_functions import check_used_email, check_used_handle, get_user_from

import urllib.request
import sys

from PIL import Image
import imghdr
import requests

image_index = 0
#############################################################
#                      USER_PROFILE                         #      
#############################################################

def profile(payload):
    '''
    For a valid user, returns information about their user id, 
    email, first name, last name,  handle and profile_img_url
    '''
    
    if validate_uid(payload['u_id']) is False:
        raise InputError(description='Invalid u_id')

    user = get_user_from('token', payload['token'])
    #returns user information
    
    user2 = get_user_from('u_id', int(payload['u_id']))


    return ({
        'u_id' : user['u_id'],
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle_str'],
        'profile_img_url' : user['profile_img_url'] 
    })


#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

def profile_setname(payload):
    
    '''
    Update the authorised user's first and last name
    '''
    user = get_user_token(payload['token'])
    
    if not (1 < len(payload['name_first']) < 50):
        raise InputError(description='Invalid name_first, above the range of 50 characters')
    if not (1 < len(payload['name_last']) < 50):
        raise InputError(description='Invalid name_last, above the range of 50 characters')    
    
    user['name_first'] = payload['name_first']
    user['name_last'] = payload['name_last']
    return ({})
    
#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

def profile_setemail(payload):
    '''
    Update the authorised user's email address
    '''
    
    #test email is valid and not been used before
    new_email = test_email(payload['email'])
    assert check_used_email(new_email) == 1
    
    user = get_user_token(payload['token'])
    user['email'] = new_email
    return {}
    
#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################

def profile_sethandle(payload):
    
    '''
    Update the authorised user's handle (i.e. display name)
    '''
    #test handle is valid and not been used before
    if len(payload['handle_str']) < 3 or len(payload['handle_str']) > 20:
        raise InputError(description='handle_str should be between 3-20 characters')
    
    assert check_used_handle(payload['handle_str']) == 1
    
    user = get_user_token(payload['token'])
    user['handle_str'] = payload['handle_str']
    return {}

#############################################################
#                   USER_PROFILE_UPLOADPHOTO                #
#############################################################

def user_profile_uploadphoto(payload):

    '''
    Given a URL of an image on the internet, crops the image within bounds
    '''
    #Do a check to see if token is valid and to check if image is jpg

    global image_index
    image_index += 1

    user = get_user_token(payload['token'])
    u_id = user['u_id']

    port = sys.argv[1]

    url = f"http://localhost:{port}/static/"
    filePath = './static/' + str(image_index) +'.jpg'
    
    try:
        urllib.request.urlretrieve(payload['img_url'], filePath)
    except Exception as e:
        if type(e) != 200:
            raise InputError(description = "HTTP status not 200")
        elif imghdr.what(filePath) != 'jpg':
            raise InputError(description = "Image not a jpg image")
        else:
            pass

    #crop the url image
    imageobject = Image.open(filePath)    
    width, height = imageobject.size
    
    x_start = payload['x_start']
    y_start = payload['y_start']
    x_end = payload['x_end']
    y_end = payload['y_end']

    if x_start is None and x_end is None and y_start is None and y_end is None:
        x_start = 0
        x_end = width
        y_start = 0
        y_end = height

    #raises an input error if the values provided are outside
    #the bounds of the image
    if x_end > width or y_end > height or x_start >= x_end or y_start >= y_end:
        raise InputError("Crop has to be within the dimensions of the photo")
    cropped = imageobject.crop((x_start, y_start, x_end, y_end))

    cropped.save(filePath)

    user['profile_img_url'] = url + ".jpg"
    return {}


