import pytest
import urllib
import json
import flask
from urllib.error import HTTPError

import server
import user
import other
from system_helper_functions import reset_workspace, reg_user1
from data_stores import get_auth_data_store, reset_auth_store
from helper_functions import get_user_token
from error import InputError
from system_helper_functions import reg_user1, reg_user2, send_msg1

'''
#############################################################
#                   ADMIN_PERMISSION_CHANGE                 #
#############################################################
'''