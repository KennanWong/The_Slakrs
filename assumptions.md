## Auth_login:
* Assume register works
* will assume that 
* Assume users_all works and we are able to check emails of existing users
* Assumes that a check is in place to see if an email is valid or not
* Assumes that there will be a dictionary that contains all of users account details, i.e their email
* and their password which is checked before a user is able to login (currently in the users_all dict there is 
* No place to log that information

## Auth_logout:
* Assume register and login works
* Assumes that users_all function is working and is called upon within the auth_logout in order to check who is and is not currently logged in, to determine valid or invalid tokens

## Auth_register:
* Assumes users_all function is working and that when the register function is called, it will use users_all to check for an existing email address
* Assumes that when registering a user, there is an email check in place to tell if an email is valid or not, i.e  an email would be invalid if it did not contain a string before the .com sign , or if it did not contain an @ symbol, or if its suffix was not from a listed of now valid email suffixes such as .com, .org, .edu
* Assumes that the u_id provided to each user is set and locked when they register, but their token varies every time they log in
* Assumes that length of the password is checked during register function
* Assumes that the length of a first name is checked during register function
* Assumes that the length of a last name is checked during register function
* Assumes that registering with the same email is not permitted and causes an error
* Assumes that someone is unable to re-register with the same details


## Message_send
* Assumes that every time a message is sent, that the u_id of the person who sent the message, message_id, the message, and time created are appended to a list called messages
* Assumes that message_id’s start at 1 and increment with every message sent
* Assumes that a function would be added under the ‘message’ header which will update as messages are sent and removed
* Assumes messages is a list of dictionaries with format
    'messageDict' : [
        {
            'message_id':,
            'u_id':,
            'message':,
            'time_created':
        }
        ]
* Assumes that if you send a message with an invalid token it causes an input error


## Message_remove
* Assumes that in order to remove a message, you must be either the owner/admin of a channel, or you are the one who sent the message, or both 
* Assumes that if you send a message with an invalid token it causes an input error

## Message_edit
* Assumes that in order to edit a message, you must be either the owner/admin of a channel, or you are the one who sent the message, or both 
* Assumes that if someone edits a text and is replaced with an empty string, the message is deleted, and message_remove function is called
* Assumes that if you send a message with an invalid token it causes an input error


## Channel_invite
* Assumes that you can invite anyone unless the person you are trying to invite is already in the channel
* Assumes that you must be part of the channel to invite someone to said channel
* Assumes that user gets given a token and can’t implement a ‘bad’ token
* Assumes user is logged in

## Channel_details
* Assumes that new members who are added to the channel will be added to the end of the ‘all_members’ list
* Assumes that user gets given a token and can’t implement a ‘bad’ token

## Channel_messages
* Assumes that the user who is sending messages has already joined the channel
* Assumes that user gets given a token and can’t implement a ‘bad’ token
* Assumes user is logged in

## Channel_leave
* Assumes that you can’t leave the channel twice
* Assumes that you can’t leave a channel that you aren’t in to begin with
* Assumes that user gets given a token and can’t implement a ‘bad’ token

## Channel_join
* Assumes that the user is only able to join public channels
* Assumes that you can’t join the channel twice
* Assumes that user gets given a token and can’t implement a ‘bad’ token

HARJAS → set invalidChannelID = 1, set invalidUserID = 1


## Channel_addowner
* Assumes that the creator of a channel is also the owner
* Assumes that in order to add new owners to the channel, you must be the initial owner of the channel.
* Assumes that when adding an owner to a channel, the channel_id is of a valid channel.

## Channel_removeowner
* Assumes that a user must be one of the owners of the channel to change the permissions of other owners such as removing them.
* Assumed that the user being removed is currently an owner
* Assumes that when removing an owner of a channel, the channel_id is of a valid channel.

## Channels_list
* Assumes when the user calls the function, the user has successfully joined at least one channel which can be displayed.
* Assumes the maximum channels a user can create is 1

## Channells_listall
* Assumes that an user is able to see the full list of channels (public and private) regardless if they’re not part of it.

## Channels_create
* Assumes that when creating a new channel, the name does not go above 20 characters long.
* Assumes that all users can create a public or private channel


## User_profile
* Assumes that auth_register is working [applies to all testing for user functions]
* Assumes that a u_id will only contain numbers. Thus, u_id contain special characters, letters and spaces is an invalid u_id

## User_profile_setname
* Assumes that the user already has an existing name from when the user was first registered
* Assumes that the specification means that the length 1 and 50 is included in the range for the string
* Assumes that the user is logged in

## User_profile_setemail
* Assumes that the user already has an existing email from when the user was first registered
* Assumes that user is logged in 

* Assumes that an invalid email will not contain ‘@’ and/or ‘no prefix’ and/or ‘no suffix’  and/or no ‘.com’

## User_profile_sethandle
* Assumes that the user needs to be logged in to set handle
* Assumes that strings of length 3 and 20 are within the valid range

## Users_all
* Assumes that the function will list all members of the slackr, not just limited to people within channels the user is a member of
* Assumes that the list will include members who are both logged out and logged in
* Assumes that user must be logged in to call function, thus there will never be zero users in the slackr.


## Search
* Assumes empty queries will work and return the empty messages
* Assumes user is logged in
* Assumes that if no messages have been sent that match the query, an empty list is returned.