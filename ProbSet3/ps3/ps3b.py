from ps3a import *
import time
from perm import *
if __name__ == '__main__':
    word_list = load_words()

#
#
# Problem #6A: Computer chooses a word
#
#

def valid_perms(hand, n):
    trues = []
    for i in range(2, n+1):
        addie = get_perms(hand, i)
        for i in addie:
            if word_list.__contains__(i) is True:
                trues.append(i)
    return trues

def trues_battle(trues, n):
    while len(trues) > 1:
        if get_word_score(trues[0], n) >= get_word_score(trues[1], n):
            trues.pop(1)
        else:
            trues.pop(0)
    return trues[0]

def comp_choose_word(hand, n):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    trues = valid_perms(hand, n)
    if len(trues) == 0:
        print 'No possible answers.'
        print
        return ''
    top = trues_battle(trues, n)
    return top


# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, n, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    
    display_hand(hand)
    word = comp_choose_word(hand, n)
    if word == '':
        play_game(word_list, n)
    print "Computer chooses", word
    points = get_word_score(word, n)
    print word, "scores", points, "points."
    update_hand(hand, word)
    if calculate_handlen(hand) == 0:
        print 'Hand cleared.'
        print
        play_game(word_list, n, hand)
    else:
        print
        comp_play_hand(hand, n, word_list)
        
    
def play_hand(hand, n, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    total = 0
    
    display_hand(hand)
    word = raw_input("Spot a word? - ")
    if word == '.':
        print
        play_game(word_list, n, hand)
    if word == ":":
        print
        hand = deal_hand(n)
        play_hand(hand, n)
    if is_valid_word(word, hand, word_list) is False:
        print "Invalid word. See something else?"
        play_hand(hand, n, word_list)
    update_hand(hand, word)
    total += get_word_score(word, n)
    print '"' + word + '"', "earned", get_word_score(word, n), "points. Hand total:", total
    if calculate_handlen(hand) == 0:
        print "Cleared the hand! Nice!"
        print
        play_game(n, hand)
    print
    play_hand(hand, n, word_list)
     

## Problem #6C: Playing a game


def play_game(word_list, n = 6, hand = {}):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    if hand == {}:
        hand = deal_hand(n)
    cmd = raw_input("(N)ew hand, (r)epeat hand, or (e)xit? - ").lower()
    if cmd == 'e':
        assert False
    cmd_uc = raw_input("Who will play? (U)ser or (c)omputer? - ").lower()
    print
    if cmd == 'n':
        hand = deal_hand(n)
        if cmd_uc == 'u':
            play_hand(hand, n, word_list)
        else:
            comp_play_hand(hand, n, word_list)
    elif cmd == 'r':
        if calculate_handlen(hand) == 0:
            hand = deal_hand(n)
            print "The hand was empty, but it's okay I got you a new one. Sigh..."
        if cmd_uc == 'u':
            play_hand(hand, n, word_list)
        else:
            comp_play_hand(hand, n, word_list)
    elif cmd != 'n' and cmd != 'r' and cmd_uc != 'u' and cmd != 'c':
        print "Invalid command entered."
        print
        play_game(word_list, n, hand)
        
#
# Build data structures used for entire session and play game
#

##    play_game(word_list)



    
