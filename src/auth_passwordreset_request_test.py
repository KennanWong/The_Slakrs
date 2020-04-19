'this file is the integration tests for auth passwordreset request'

import auth
from other import workspace_reset
from test_helper_functions import reg_user1
from data_stores import get_reset_code_store


#pylint compliant
#############################################################
#                   AUTH_PASSWORDRESET_REQUEST              #
#############################################################
def test_request():

    'testing functionability of passwordreset request'

    workspace_reset()
    reg_user1()         #pylint disable = W0612

    auth.request({
        'email': 'Kennan@gmail.com'
    })

    reset_store = get_reset_code_store()

    email_match = 0 #if found = 1

    for i in reset_store:
        if i['email'] == 'Kennan@gmail.com':
            email_match = 1

    assert email_match == 1             #pylint disable = R0123
                                        #pylint disable = C0305
