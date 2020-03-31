#############################################################
#                         SEARCH                            #      
#############################################################   
@APP.route('/search', methods=['GET'])
def message_search():
    """ return messages """
    result = search(request.args.get('token'), request.args.get('query_str'))
    return dumps(result)
    
#############################################################
#                USER PERMISSION CHANGE                     #      
#############################################################
@APP.route('/admin/userpermission/change', methods=['POST'])
def userpermission_change():
    """ return empty dic, change user's permission """
    result = permission(request.form.get('token'), int(request.form.get('u_id')),
                        int(request.form.get('permission_id')))
    return dumps(result)


#############################################################
#                      USER_PROFILE                         #      
#############################################################

@APP.route('/user/profile', methods=['GET'])
def user_profile():
    """ 
    return 'email', 'name_first', 'name_last', 'handle_str', unpin a msg 
    """
    result = profile(request.args.get('token'), request.args.get('u_id'))
    result['profile_img_url'] = str(request.base_url) + result['profile_img_url']
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    """ 
    return empty dic, change user's name 
    """
    result = setname(request.form.get('token'), request.form.get('name_first'),request.form.get('name_last'))
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    """ 
    return empty dic, change user's email 
    """
    result = setemail(request.form.get('token'), request.form.get('email'))
    return dumps(result)

#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    """ 
    return empty dic, change user's handle 
    """
    result = sethandle(request.form.get('token'), request.form.get('handle_str'))
    return dumps(result)
    
#############################################################
#                        USERS_ALL                          #
#############################################################

@APP.route('/users/all', methods=['GET'])
def all_users():
    """ 
    show all users 
    """
    result = all_user(request.args.get('token'))
    return dumps(result) 
=======


<<<<<<< HEAD
    
    return False
    
#function to see if a u_id is valid
def validate_uid(u_id):
    user_store = get_auth_data_store()
    for i in user_store:
        if i['u_id'] == u_id:
            return True
    
    return False

#function returns 1 if email has not been used before    
def check_used_email(email):
    email_store = get_auth_data_store()
    for i in email_store:
        if i['email'] == email;
            raise InputError(description='Email is already in use')
    else:
        return 1
        
#function returns 1 if handle has not been used before    
def check_used_handle(handle_str):
    handle_store = get_auth_data_store()
    for i in handle_store:
        if i['handle_str'] == handle_str;
            raise InputError(description='Handle is already in use')
    else:
        return 1
        
# function to validate a token and returns the users info
# otherwise raises an error
def get_user_uid(u_id):
    auth_store = get_auth_data_store()
    user = {}
    for i in auth_store:
        if i['u_id'] == u_id:
            user = i
    if user != {}:
        return user
    else:
        raise InputError(description='Invalid u_id)  
             
    
=======



