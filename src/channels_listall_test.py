'this file is the integration tests for channels listall'

import pytest # pylint: disable=W0611


import channels
from other import workspace_reset
from test_helper_functions import register_and_create, reg_user2


#pylint compliant
#############################################################
#                   CHANNELS_LISTALL                        #
#############################################################
def test_listall():
    'testing functionability of channels listall'

    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']


    user2 = reg_user2()

    #user2 creating a channel
    payload1 = {
        'token': user2['token'],
        'name': 'Slackrs',
        'is_public': True
    }
    result1 = channels.create(payload1) # pylint: disable=W0612
    token = user1['token']
    channels.Listall(token) # pylint: disable=C0304