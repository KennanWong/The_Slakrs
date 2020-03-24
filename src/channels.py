import sys
import re
import hashlib
from datetime import datetime
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError, AccessError


'''
#############################################################
#                   CHANNELS_CREATE                         #      
#############################################################
'''

def channels_create():

channel_owner_info = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
    }
    
    if len(payload['name']) < 21:
        name = payload['name']
        if payload['is_public']: 
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name':  name,
                'is_public': True,
                'members':[],
                'owners':[],
                'messages': [],
            }
        else:
            new_channel_info = {
                'channel_id': int(len(channel_store)+1),
                'name': name,
                'is_public': False,
                'members':[],
                'owners':[],
                'messages': [],
            }
    else: 
        raise InputError (description='Name is too long')
        