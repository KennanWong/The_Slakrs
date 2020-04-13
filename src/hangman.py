from random import randint

from helper_functions import create_message

#############################################################
#                        HANGMAN                            # 
#############################################################


HANGMAN_STATES =(
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
    generate_phrase()
    global PHRASE
    global EMPTY_GUESS
    global STATE 
    STATE = 0
    EMPTY_GUESS = '_'*len(PHRASE)
    display_hangman()

    return


def guess(channel, new_guess):
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
        if EMPTY_GUESS == PHRASE:
            message(channel, display_hangman()+'\n' + 'You win! Game Over')
            channel['hangman_active'] = False
        else: 
            message(channel, display_hangman())
    return


# create the 'Hangman'
# have the hangman send messages to a channel
# reuse send_message 

def message(channel, msg):
    new_msg = create_message()
    new_msg['u_id'] == 'HANGMAN'
    new_msg['channel_id'] = channel['channel_id']
    new_msg['message'] = msg

    channel['messages'].append(new_msg)
    return


def display_hangman():
    #print(HANGMAN_STATES[STATE])

    global EMPTY_GUESS
    guess_revised = " ".join(EMPTY_GUESS)
    # print ('\t'+ str(guess_revised))

    display_msg = HANGMAN_STATES[STATE] + "\n\t" + str(guess_revised)

    return display_msg

def generate_phrase():
    global PHRASE
    wl = open('hangman_words.txt', 'r')
    wordlist = wl.readlines()
    wl.close
    index = randint(0, (len(wordlist) -1))

    PHRASE = wordlist[index][:-1]
    print(PHRASE)

    return 



