# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:01:02 2026
https://medium.com/upperlinecode/making-a-markov-chain-poem-generator-in-python-4903d0586957
@author: billk
concise and very clever code by Mehrab Jamee
modify this for variable context window
"""

# modified from
# Mehrab Jamee
# Markov Chain Poetry
# Generated from Stray Birds by Rabindranath Tagore

import random
import re

# open and read the file    
# works well for stray_birds
# not so good for other texts: punctuation varies
poem1 = open("stray_birds.txt", "r").read()
#other texts
poem2 = open("genesis.txt", "r").read()
poem3 = open("frankenstein.txt", "r").read()

# tidy characters 
def setup(poems):
    # use regular expressions to remove all digits
    # \d+ is one of more digits, replace with '' (nothing)
    poems = re.sub(r'\d+', '', poems) 
    
    # tidying punctuation is messy
    # replace \n with a space, ' ' 
    # need a space for CR on long lines
    # "quotes", ?, commas, -- and ? don't work in mixed up output
    # so replace with nothing and -- and commas with a space
    # ; and ' kept, do no harm
    replacements = {"\n": " ", ",": " ", '"': '', "--":" ", '?':''}
    for old, new in replacements.items():
        poems = poems.replace(old, new)
    
    # remove all caps
    poems = poems.lower()
    
    return poems

poems = setup(poem1)
length = len(poems.split())
# print(length) # poem1 5562 words long!

N = 2 #ngram size
# This function inputs a poem creates and returns a dictionary called "chain". 
# Convert text into lists of words inside lists of sentences
# Each key is a ngram tuple, and the value of each key is a list of the words that immediately followed it. 
def markov (poems, N):
    # split into one list of sentences
    poems = poems.split('.') 
    
    # remove any empty strings (eg. at end) using a list comprehension
    poems = [notEmpty for notEmpty in poems if notEmpty.strip()] 
    # notEmpty.strip() True for non empty strings!!!
    
    # make lists of words inside lists of sentences
    # remove unwanted spaces
    sentences = []
    for i in range(len(poems)):
        # split at white spaces, also eliminates excess white spaces
        sentences.append(poems[i].split())

    index = 1 # dictionary offset value
    chain = {} # initialise dictionary

    for sentence in sentences:
        index = 1 # reset for next sentence
        # adjust word offset for ngram size
        # word follows the ngram
        for word in sentence[(index+N-1):]:
        # get dictionary key ngrams
        # key starts at 0 (index - 1), then jumps to ngram length
            key = tuple(sentence[index - 1 : index - 1 + N])
            if key in chain:
                # add another word to the dictionary value
                chain[key].append(word) 
            else:
                chain[key] = [word] # add initial key:value to dictionary
            index += 1 # iterate to next word in the sentence
    return chain

chain = markov(poems, 2)
# {(word1, word2) : [value1, value2, value3 ...], etc}
# ie. all the values that follow each word
# print(len(chain)) # 3504 dictionary items for N=2

def message(chain):
    #count = input("Enter the number of output words you want: ")
    #count = int(count)
    count = 20 # Desired maximum word count of output
    
    # start message with random key ngram
    ngram1 = random.choice(list(chain.keys()))
    message = " ".join(ngram1)
    
    # Pick the next word over and over until word count achieved
    while len(message.split(' ')) < count:
        # get random value word2 from ngram1 in chain
        word2 = random.choice(chain[ngram1]) 
        message += ' ' + word2 # add value word to message
        # get next ngram from end of message
        ngram2 = tuple(message.split()[-N:]) 
        if ngram2 not in chain:
            print("key not found")
            break
        ngram1 = ngram2 # new ngram loops back to start
    
    return(message)

message = message(chain)

# make the final word of the message at least 5 letters where possible
# use markov process to find suitable final word
def final(message):
    #turn message string back into list
    msgList = message.split()
    # if the final word length >= 5 we have finished
    if len(msgList[-1]) >= 5:
        return(message)
    else:
        # turn short final word into a tuple
        short = tuple(msgList[-1].split())
        #make a new chain, this time {unigram: values}  
        chain = markov(poems, 1) 
        # print(len(chain)) # 1183 for unigram! how possible?
        # is the short word in the dictionary?
        # is a dictionary value of the short final word, chain[short] > 5?
        if short in chain:
            print(f"{short} in chain")
            for item in chain[short]:
                # get the longer final word, add to message
                if len(item) > 5:
                    final = item
                    print(final)
                    return (message + ' ' + final)
    
        return (message) # if longer word not found
        
message = final(message)
message = message.capitalize() # capitalize first word
message = message.replace(" i ", " I ") # replace ' i ' with ' I '
message = message + '.' # add full stop
print(message)
 

