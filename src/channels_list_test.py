'this file is the integration tests for channels list'

import pytest # pylint: disable=W0611

import channels
from other import workspace_reset
from test_helper_functions import  register_and_create


#pylint compliant

#############################################################
#                   CHANNELS_LIST                           #
#############################################################
def test_list():

    'testing functionability of channels list'

    workspace_reset()


    ret = register_and_create()
    user = ret['user']

    token = user['token']

    channels.List(token)
  