'''
File contains all functions relating to hangman
'''
# pylint: disable=W0603
# pylint: disable=W0702
# pylint: disable=C0103
# pylint: disable=C0303
# pylint: disable=R1711
from random import randint

import auth
from helper_functions import create_message, get_user_from

#############################################################
#                        HANGMAN                            #
#############################################################

HANGMAN_STATES = (
    r"""
    _______________________________
	






    _______________________________
        """,
    r"""
    _______________________________
	    





        ----------
    _______________________________
        """,
    r"""
    _______________________________
	    
            |   
	    |	    
	    |	   
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    
	    |	   
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	   
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	    |
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	   /|
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	   /|\
	    |      
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	   /|\
	    |      / 
	    |
        ----------
    _______________________________
        """,
    r"""
    _______________________________
	     _______
            |       |
	    |	    O
	    |	   /|\
	    |      / \
	    |
        ----------
    _______________________________
        """,
)

STATE = 0

FINAL_STATE = 9

PHRASE = ''

EMPTY_GUESS = []

def start(channel):
    '''
    Function inititates a game of hangman, by generating
    a phrase and reseting the game state
    '''
    hangman = get_hangman()
    hangman_join(channel)
    generate_phrase()
    global PHRASE
    global EMPTY_GUESS
    global STATE 
    STATE = 0
    EMPTY_GUESS = '_'*len(PHRASE)
    message(channel, display_hangman())
    
    return

def guess(channel, new_guess):
    '''
    Function used when players makes a guess
    searches if that letter is found within the phrase,
    and fills it in otherwise it advances the game state
    '''
    global PHRASE
    global EMPTY_GUESS
    if new_guess not in PHRASE:
        global STATE
        STATE += 1
        if STATE == FINAL_STATE:
            # reached hangman, end the game, expose the word with losing message
            EMPTY_GUESS = PHRASE
            message(channel, display_hangman() + '\n' + 'The hangman is dead. Game Over')
            channel['hangman_active'] = False
        else:
            message(channel, display_hangman())
    else:
        if new_guess == PHRASE:
            # if the guess is the phrase fill in all blanks
            EMPTY_GUESS = PHRASE
        else:
            EMPTY_GUESS = list(EMPTY_GUESS)
            i = 0
            while i < len(PHRASE):
                if PHRASE[i] == new_guess:
                    EMPTY_GUESS[i] = new_guess
                i += 1
        if str(EMPTY_GUESS) == PHRASE:
            message(channel, display_hangman()+ '\n'  + 'You win! Game Over')
            channel['hangman_active'] = False
        else: 
            message(channel, display_hangman())
    return


# create the 'Hangman'
# have the hangman send messages to a channel
# reuse send_message 

def message(channel, msg):
    '''
    Function for the hangman to message the channel with the game state
    '''
    hangman = get_hangman()
    new_msg = create_message()
    new_msg['u_id'] = hangman['u_id']
    new_msg['channel_id'] = channel['channel_id']
    new_msg['message'] = msg

    channel['messages'].append(new_msg)
    return

def get_hangman():
    '''
    Function to get the hangman details, otherwise we need to register the hangman
    '''
    hangman = get_user_from('name_first', 'Hangman')
    if hangman == None:
        # if we get returned an empty dictionary register hangman
        print('if we get returned an empty dictionary register hangman')
        payload = {
            'email': 'hangman@bot.com',
            'password': 'Hangman',
            'name_first': 'Hangman',
            'name_last': 'Bot'
        }
        hangman = auth.register(payload)
    return hangman

def hangman_join(channel):
    '''
    let the hangman join the channel
    '''
    hangman = get_hangman()
    hangman_dets = {
        'u_id' : hangman['u_id'],
        'name_first': hangman['name_first'],
        'name_last': hangman['name_last']
    }
    if hangman_dets not in channel['members']:
        channel['members'].append(hangman_dets)
    print('Hangman has joined channel')
    return

def display_hangman():
    ''' 
    Function used to generate the raw message file for displaying the game
    '''
    #print(HANGMAN_STATES[STATE])

    global EMPTY_GUESS
    guess_revised = " ".join(EMPTY_GUESS)
    # print ('\t'+ str(guess_revised))

    display_msg = HANGMAN_STATES[STATE] + "\n\t" + str(guess_revised)

    return display_msg

def generate_phrase():
    '''
    Function used to generate 
    '''
    global PHRASE
    wl = open('hangman_words.txt', 'r')
    wordlist = wl.readlines()
    wl.close()
    index = randint(0, (len(wordlist) -1))

    PHRASE = wordlist[index][:-1]
    print(PHRASE)

    return 

def get_phrase():
    global PHRASE
    return PHRASE

def get_empty_guess():
    global EMPTY_GUESS
    return EMPTY_GUESS
