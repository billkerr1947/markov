# markov
Markov chain generative poetry: Small Language Model

### USING NGRAMS AND MARKOV CHAINS TO GENERATE POETRY

> “What I cannot create, I do not understand”
Richard  Feynmann

This is an all purpose quote which does encapsulate most of my new learning, be it ngrams, markov chains or python

**My goal**: Starting with a corpus of known poetry or literature, my goal is to generate markov chain new “poetic” / interesting / close to grammatically sound / sort of (‘sorta’) meaningful sentences. ie. to make a small language model.

Achieving this goal helped me with a broader, more all purpose goal: to become more knowledgable and fluent in my python programming. Leaving to one side for now, the discussion: In the age of vibe coding is it still worthwhile to develop python expertise?

I’m always looking for inspirational exemplars. I need that for self motivation as well as something worth teaching, since I still regard my self as a wannabe educator. 

There is much online information about ngrams, markov chains and their uses. After some searching I discovered that they could be used to generate poetry. I liked Allison Parrish’s approach (see reference) in that she regards herself and exemplifies as a combination of **ARTIST + ENGINEER**. IMO she is a great teacher. 

However, I also discovered some very elegant and brief code from the somewhat cynical Mehrab Jamee, but which was also, I felt, limited in some respects. So, after much experimentation, I opted for improving Mehrab’s code as my way forward, whilst retaining Allison as a tutor.
https://medium.com/upperlinecode/making-a-markov-chain-poem-generator-in-python-4903d0586957

### DESIGN PROCESS

We are making a language model! What this means is that you input some words (eg. poetry) in some form and the model transforms those words so that the end result is a different string of words which are meaningful in some sense, not random nonsense. The model we are making can be called a Markov language model.

My design, which is the most important part of the whole process, initially took a wrong pathway, rather wrong pathways! On the internet you find code, good or not so good, and explanation of varying quality: absent, poor, wonderful. I wasn’t clear about the correct ways or good ways of using a markov chain to produce new sentences. 

Eventually this sentence from Allison Parish revealed a good way: 
*The easiest way to represent this model is with a dictionary whose keys are the n-grams and whose values are all of the possible "nexts."* 

### THE BIG PICTURE: NGRAMS AND MARKOV CHAINS

To illustrate I’ll apply it to this sentence: **“Ngrams are a successive list of the order in which words appear in a sentence.”** 

Ngrams may have a length of one (unigram), two (bigram), three (trigrams) or more. So for the above sentence an Ngram of size 2, aka a bigram, would look like:
[[‘Ngrams’, ‘are’], [‘are’, ‘a’], …. [‘a’, ‘sentence’]]

A Markov chain consists of an Ngram followed by a target or targets. It informs us of the probability that a given Ngram will be followed by a particular target. So, for the above sentence a unigram followed by a target would look like this dictionary:
{(‘Ngrams’): [‘are], (‘are’) : [‘a’]], (‘a’) : [‘successive’, ‘sentence’] … etc }

Other descriptors here are *context window* where the Ngram, which can vary in length, provides the context for the target. *“You can predict a word by the company it keeps”*. This famous saying encapsulates the statistical approach to language models in one short sentence.

Technical point: The dictionary keys are written as tuples not lists since dictionary keys have to be immutable and lists are mutable.

For this one sentence derived Markov chain the only time you get more than one dictionary value is that the word ‘a’ is followed by ‘successive’ half the time and ‘sentence’ the other half of the time. All the other instances have just one key and one value. 

But if you have a big corpus, a long text, then we will often have many values for the keys. In this way the probabilities can be built into the code implicitly. For example, in my final unigram dictionary I have these values for the unigram ‘come’:
('come',): ['to', 'up', 'near', 'nearest', 'out', 'back', 'with', 'out', 'to', 'alone', 'out', 'into', 'to', 'floating', 'with', 'out'],
Note that ‘to’ follows ‘come’ three times, ‘out’ follows ‘come’ four times and ‘floating’ follows come only once. So if we pick a random value for the key ‘come’ then some words are more likely to follow than others. Probabilistic or markov chain outcomes are achieved without calculating any probabilities. 

The python code can be split conceptually into the following parts:
- Uploading and preparing text files
- Making the markov dictionary, using for loops
- Explanation of the for loops
- Use the markov chains to generate a message with a while loop
- Refining, testing, debugging

### UPLOADING AND PREPARING TEXT FILES ###

For my main text I’ve copied Mehrab Jamee who used the poem *“Stray Birds”* by Rabindranath Tagore. Rabindranath Tagore was the first Asian Nobel Laureate. So we are starting with a text file, stray_birds.txt. 

There is quite a bit of text preparation required to get the text into a form where the words can be rearranged and still make sense:
    • remove all digits
    • replace line breaks, commas and some other characters with spaces
    • remove capitals

 ### MAKING THE MARKOV DICTIONARY, USING FOR LOOPS

Then the text was converted into lists of words inside lists of sentences: [[s1w1, s2w2, ..][s2w1, s2w2 …] etc … ]. The main reason for the nested lists was that I didn’t want the ngrams to overlap from the end of one sentence to the start of the next sentence since that sort of flow is different from the flow that occurs within a sentence.

Some other tidying up was required since some empty lists appeared in the process and they needed to be eliminated.

The Markov chain will be represented as a dictionary as described above:
The easiest way to represent this model is with a dictionary whose keys are the n-grams and whose values are all of the possible "nexts."

Dictionary keys have to be immutable so the ngram keys are converted to tuples.

I was impressed by Mehrab Jamee’s clever coding, especially by the way he iterates so as to offset the context word from the target word. His design follows the Allison Parrish quote, as well. The probabilities are built in: if a word appears more often in the target then it will appear more often in generated messages.

But IMO some things in Mehrab’s code need improving. The ability to modify ngram size is a necessary feature to experiment to see which ngram size achieves the most realistic new sentences. He also is  pairing the last word of a sentence to the first word of the next sentence which I think introduces unrealistic markov chains.

Mehrab Jamee design: Each key is a single word from the poem, and the value of each key is a list of the words that immediately followed it.
My modified design: Each key is a ngram tuple taken from each sentence of the poem, and the value of each key is a list of the words that immediately followed it. 

### EXPLANATION OF THE FOR LOOPS
Extract from the markov function:

    N = 2 #ngram size
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

The inner loop is iterating over the words. The index starts at 1, whereas the loop counting starts at 0. We need to increment index at the bottom of the loop to keep up with jumping to the next word.

Indexing the sentence in the inner loop: if ngram size = 1 then the dictionary key word will be at index – 1 and the target (dictionary value) word will be the following word, where the index value is set. If the ngram size = 2 then the index has to jump to the ngram length

The key has to be a tuple, since lists are mutable. Some in depth knowledge of python is  required here.

The else: statement is activated first since that adds the key: value pairs to the dictionary if they are not there. Then once the key: value pair is in the chain further target words are appended.

The outer loop iterates over the sentences. The index needs to be reset to 1 for each sentence.

### USE THE MARKOV CHAINS TO GENERATE A MESSAGE WITH A WHILE LOOP

This code generates a message. It starts with a random ngram from the dictionary chain. Then the while loop iterates over the dictionary getting a random value from each ngram key, then sliding to the next ngram and repeating, until the message word count is achieved. However, if the next ngram is not found in the dictionary keys then break the loop. So, some messages will be shorter than the count length. This raises the issue of data sparsity.

*Some theory:*
One of the key limitations of n-gram models is data sparsity. Even in large corpora, there are many valid word sequences that simply don’t occur. When a model encounters an unseen n-gram, it assigns it a probability of zero, which can lead to significant performance issues.

This is where smoothing techniques come into play. These methods assign small probabilities to unseen n-grams to ensure the model remains robust. 

These smoothing techniques are not utilised here. My goal is to achieve sorta meaningful sentences so it’s not an issue if they are shorter. I have kept a "key not found" print message in the code as a reminder.

### REFINING, TESTING, DEBUGGING

I encountered a problem with the final word of the message. Finishing a sentence with words like : (the, of, in, it, here, your) is a bad look. If the final word is short (<5 letters) and common then the sentence looks and feels weird. To improve this I made a new markov chain with ngram = 1 and then, if the final word was short, I added another longer word from the values of the short word. This is not a perfect solution but it did improve the generated messages significantly. 

### SAMPLE OUTPUT

I’ve now run the program many times and am pleased with the results. I found that a main ngram = 2 created interesting sentences. I’ve kept the “key not found” message there as a reminder of why some sentences are shorter. I’ve included other messages to indicate the outcome if the initial final word of the sentence was 4 characters or less. Sometimes there is no longer new word to be added to the short end word.

key not found  
The burden of its tail.

key not found  
'('sun',)' in chain  
Asked the setting sun.

key not found  
Its bud and cries this is my flower my death.

The silent night has the earth and the glass lamp rebukes the earthen for calling it cousin the moon rises.

key not found  
Lands of barren years to reach the moment scoffs at the burden of their wings.

key not found  
Me asking me their own names.

key not found  
('thee',) in chain  
mother  
Prove she is the day with the words I love thee mother.

('it',) in chain  
becomes  
Thy words in their own lamps and sing their own hissing world of mine and am afraid to make it becomes.

key not found  
('fire',) in chain  
Chastity is a bag that bursts with the light of the sky and ashes to the fire.

('my',) in chain  
window  
Trees like the cry of some early dawn comes to me from my water jar as I walk on my window.

### REFERENCE / FURTHER LINKS

Mehrab Jamee, Markov Chain Poetry, Generated from Stray Birds by Rabindranath Tagore  
https://medium.com/upperlinecode/making-a-markov-chain-poem-generator-in-python-4903d0586957

Allison Parrish is a great teacher. Check out her github for a series of well explained python tutorials. These links are about her markov chain developments:  
https://www.decontextualize.com/teaching/dwwp/topics-n-grams-and-markov-chains/  
She makes a class here but not on her longer github explanation  
https://github.com/aparrish/rwet/blob/master/ngrams-and-markov-chains.ipynb

This one has an idea which could be an extension of mine: style the poem at the end, control line length (no caps or full stops)  
https://github.com/abdullah1772/poetry-generator-with-markov-models/blob/main/poetry-generator-with-markov-models.ipynb

This next one has more sophisticated coding features, the main one being a Ngram model class. The first link is the article and the other links lead to the code on github  
https://towardsdatascience.com/text-generation-using-n-gram-model-8d12d9802aa0/  
136 lines  
Frankenstein text  
https://github.com/olegborisovv/NGram_LanguageModel  
https://github.com/olegborisovv/NGram_LanguageModel/blob/main/text_generator_ngram.py


