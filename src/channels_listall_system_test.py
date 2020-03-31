import urllib
import json
import flask
from urllib.error import HTTPError

import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1


#############################################################
#                   CHANNELS_LISTALL                        #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_listall():

    