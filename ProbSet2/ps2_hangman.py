# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
##    print "Loading word list..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
##    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code beginshere!

def check_letter(char, word):
    """
    Scans word for the letter char.
    """
    ticker = 0
    for c in word:
        if char == c:
            ticker += 1
    if ticker > 0:
        guess = 1
    else:
        guess = 0
    return guess

def hidden_show(solution, lets_used):
    display = ''
    for c in solution:
        if c in lets_used:
            display = display + c
        else:
            display = display + '_'
    return display

##def hangman_data(guesses_correct, guesses_false):
##    global_correct, global_false += guesses_correct
##    local_total = guesses_correct + guesses_false
##    print guesses_correct, "correct guesses to", guesses_false, "incorrect out of", \
##            total, "total guesses."
##    print 

def hangman(lives):
    """
    Play hangman!
    Enter how many lives you would like in digits.
    """
    print "Let's play some Hangman, bro!"
    solution = choose_word(wordlist)
    print "Your word has", len(solution), "letters. Let's get guessing!"
    print '(HINT: Type "help" for some helpful hidden features.)'
    print ''
    lets_avail = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                  'n','o','p','q','r','s','t','u','v','w','x','y','z']
    lets_used = []
    guesses_correct, guesses_false = 0, 0
    victory = False
    if lives >= 26:
        print "Hold on a second, bro. You've got more lives than there are letters in alphabet."
        lives = int(raw_input("Let's pick a new number of lives that's less than 26: "))
        print ""
        if lives >= 26:
            lives = int(raw_input("This isn't funny. One more chance or you're out of here: "))
            print ""
            if lives >= 26:
                "That's it. I'm going home."
                assert False
    while lives >= 0 and not victory:
        print "Your word:", hidden_show(solution, lets_used), "Incorrect guesses left:", lives
        letter = raw_input("Your next guess? - ")
        if letter == 'guessed':
            print "Letters guessed: " + "".join(lets_used)
        elif letter == 'not guessed':
            print "Letters not guessed: " + "".join(lets_avail)
        elif letter == 'length':
            print "The word is", len(solution), "letters long."
        elif letter == 'help':
            print 'To see what letters you have already guessed, type "guessed".'
            print 'To see what letters you have NOT guessed, type "not guessed".'
            print 'To see the length of the word, type "length".'
        elif letter in lets_used:
            print "You've already guessed that letter, silly!"
        elif letter not in solution:
            lives -= 1
            lets_avail.remove(letter)
            lets_used += [str(letter)]
            guesses_false += 1
            print "Sorry bro, that's not in the word."
        else:
            lets_avail.remove(letter)
            lets_used += [str(letter)]
            guesses_correct += 1
            print "Yeah buddy! That one's in the word."
        print ''
        if solution == hidden_show(solution, lets_used):
            victory = True
    if lives < 0:
        print "Bro, you died!"
        print "The word was", str(solution).upper()
    else:
        print "Congratulations, bro! Your word was", str(solution).upper() + "."
