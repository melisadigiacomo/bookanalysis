# -*- coding: utf-8 -*-
"""
@author: Melisa Di Giacomo
"""

# Book Analysis: Harry Potter and the Philosopher's Stone

#%%
## Modules ##

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

#%% 
## Book ##

text = open('HarryPotter.txt')
text = text.read()
#print(text)

#%%
## Tokenization  and cleaning text##

#Tokenize text: splitting an entire text into small units, known as tokens.

# Functions for removing punctuation and making lists of words, sentences, 
# paragraphs and chapters.

# Function to remove punctuation
def remove_punctuation(st,exception=''):
    'Remove punctuation.'
    punctuation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
    punctuation = punctuation.replace(exception,'')
    for c in st:
        if c in punctuation:
            st = st.replace(c,'')
    return st


# Function that takes in a book and returns a list of words
def create_word_list(st):
    'From a text, it returns a list of words.'
    st  = remove_punctuation(st)
    return word_tokenize(st)


# Function that takes in a book and returns a list of sentences
def create_sentence_list(st):
    'From a text, it returns a list of sentences.'
    st = remove_punctuation(st,'.')
    return sent_tokenize(st)


# Function that takes in a book and returns a list of paragraphs
def create_paragraph_list(st):
    'From a text, it returns a list of paragraphs.'
    ans = remove_punctuation(st)
    return ans.split('\n\n')


# Function that takes in a book and returns a list of chapters
def create_chapter_list(st):
    '''From a text, it returns a list of chapters if our 
    book include the word chapter'''
    ans = remove_punctuation(st,'-')
    ans = ans.replace('-',' ')
    return ans.split('CHAPTER')


# Create lists of words, sentences, paragraphs and chapters:

# Create a list of all the words in the book
words = create_word_list(text)
# Create a list of all the sentences in the book
sentences = create_sentence_list(text)
# Create a list of all the sentences in the book
paragraphs = create_paragraph_list(text)
# Create a list of all the chapters in the book
chapters = create_chapter_list(text)


#%%
# Create a frequency dictionary for all the words in Harry Potter:

# Use Frequency Distribution function from NLTK
freq_distribution = FreqDist(words)
# Convert into a dictionary
freq_d = dict(freq_distribution)
#print(freq_d)


# Create a ranked list of words.

# Use sorted() method
ranked_list = sorted(freq_d, key=freq_d.get, reverse = True)
# Remove anormalities observed
ranked_list.remove('Well')
ranked_list.remove('Oh')


# Stop words

stop_words = set(stopwords.words("english"))
words = set(words)


# Proper nouns

# Rank all proper nouns
tagged_text = pos_tag(text.split())
proper_nouns = [word for word,pos in tagged_text if pos == 'NNP']

filtered_d = {}
for word in ranked_list:
    if word in proper_nouns and word.istitle() and word.lower() not in stop_words:
        filtered_d[word] = freq_d[word]
        #print(word,':',freq_d[word])

# Remove any anomalies
del filtered_d['Professor']
del filtered_d['Uncle']

# DataFrame proper nouns

# Put the dictionary into a DataFrame
df = pd.DataFrame.from_dict(filtered_d, orient = 'index').iloc[0:10]
#print(df)

# Barplot
df.plot.bar(figsize = (20,10), fontsize = 20, legend = False, color='firebrick')
plt.title('Most mentioned Harry Potter Characters',fontsize = 30)
plt.ylabel("Number of mentions", fontsize = 20)
plt.show()

#%% 
## Sentiment Analysis ##


## Chapters ##


# Create a dictionary where chapter num is key and sentiment level is the value
chapter_sentiment = {}
chapter = 0 # change this to make chapters align
for c in chapters:
    chapter_sentiment[str(chapter)] = TextBlob(c).polarity
    chapter+=1

#print(chapter_sentiment)


# Put the dictionary into a DataFrame
df_sent = pd.DataFrame.from_dict(chapter_sentiment, orient = 'index').iloc[1:18]
#print(df_sent)

# Barplot
df_sent.plot.bar(figsize = (20,10), fontsize = 20, legend = False, color='goldenrod')
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Sentiment Analysis for chapters',fontsize = 30)
plt.xlabel("Chapter number", fontsize = 20)
plt.ylabel("Sentiment level", fontsize = 20)
plt.show()

#Lineplot
df_sent.plot.line(figsize = (20,10), fontsize = 20, legend = False, color='darkgreen')
plt.axhline(y=0, color='black', linestyle='--')
plt.title('Sentiment Analysis for chapters',fontsize = 30)
plt.xlabel("Chapter number", fontsize = 20)
plt.ylabel("Sentiment level", fontsize = 20)
plt.show()


# Sentiment level for sentences/paragraphs

# Each paragraph/sentence receives a sentiment level. 
# The candidate is then given the sentiment score based on their 
# average appearance in positive and negative paragraphs/sentences.


# Create a function that takes in a name and returns a positive/negative score
# for sentiment level (polarity):

def protagonist_score(candidate,paragraph_list):
    '''Takes a name (candidate) and a list of paragraphs/sentences 
    and returns a positive/negative score for sentiment level (polarity)'''
    score = 0
    for entity in paragraph_list:
        blob = TextBlob(entity)
        if candidate in entity:
            score += blob.polarity
    return score

print('Sentiment level of Harry Potter based on sentences:', round(protagonist_score('Harry',sentences),2))
print('Sentiment level of Harry Potter based on paragraphs:', round(protagonist_score('Harry',paragraphs),2))


## Hogwarts houses ##


# Sentiment level for Harry Potter and the four Hogwarts houses based of 
# appareances in senteces:
print('Harry Potter:', protagonist_score('Harry',sentences))
print('Gryffindor: ', protagonist_score('Gryffindor',sentences))
print('Slytherin: ', protagonist_score('Slytherin',sentences))
print('Hufflepuff: ', protagonist_score('Hufflepuff',sentences))
print('Ravenclaw: ', protagonist_score('Ravenclaw',sentences))

# Dictionary of houses and their sentiment level:
houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
houses_sent = {}
for house in houses:
    houses_sent[house] = protagonist_score(house,sentences)

# Put the dictionary into a DataFrame
df_houses = pd.DataFrame.from_dict(houses_sent, orient = 'index')

# Barplot
df_houses.plot.bar(figsize = (20,10), fontsize = 20, legend = False, 
                   color=('firebrick', 'darkgreen', 'goldenrod', 'navy'))
plt.title('Sentiment Analysis for Hogwarts Houses',fontsize = 30)
plt.ylabel("Sentiment level", fontsize = 20)
plt.show()


## Key Characters ##


# List of key characters:
protagonists = list(filtered_d.keys())
protagonists10 = protagonists[0:10]

# Dictionary of key characters and their sentiment level:
protagonist_index = {}
for candidate in protagonists10:
    protagonist_index[candidate] = protagonist_score(candidate,paragraphs)


# Put the dictionary into a DataFrame
df_prot = pd.DataFrame.from_dict(protagonist_index, orient = 'index')

# Barplot
df_prot.plot.bar(figsize = (20,10), fontsize = 20, legend = False, color='navy')
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Sentiment Analysis for key characters',fontsize = 30)
plt.ylabel("Sentiment level", fontsize = 20)
plt.show()



## Character's sentiment journey across the book ##

protag = "Snape"

# Functions
def character_sentences(character):
    "Returns a list of sentences containing the character's name."
    character_sents = []
    for sent in sentences:
        if character in sent:
            character_sents.append(sent)
    return character_sents

def character_journey(character, sample_size):
    '''Takes in a character and a sample size of choice 
    and returns a dictinary with a chronological counter and polarity.'''
    sentences = character_sentences(character)
    character_journey = {}
    counter = 0
    upper_slice = sample_size
    lower_slice = 0
    while upper_slice < len(sentences):
        sample = sentences[lower_slice : upper_slice]
        sample = ' '.join(sample)
        character_journey[str(counter)] = TextBlob(sample).polarity
        counter += 1
        upper_slice += sample_size
        lower_slice += sample_size
    return character_journey

def character_journey_cumulative(character, sample_size):
    '''Takes in a character and a sample size of choice 
    and returns a dictinary with a chronological counter and cumulative polarity.'''
    sentences = character_sentences(character)
    character_journey = {}
    counter = 0
    upper_slice = sample_size
    lower_slice = 0
    overall_polarity = 0
    while upper_slice < len(sentences):
        sample = sentences[lower_slice : upper_slice]
        sample = ' '.join(sample)
        overall_polarity += TextBlob(sample).polarity
        character_journey[str(counter)] = overall_polarity
        counter += 1
        upper_slice += sample_size
        lower_slice += sample_size
    return character_journey


# Number of sentences of Snape
protag_sent = character_sentences(protag)
print('Number of sentences where', protag, 'appears:', len(protag_sent))


# Protagonist Journey
character_j = character_journey(protag,10)
df_j = pd.DataFrame.from_dict(character_j, orient = 'index')

#Lineplot
df_j.plot.line(figsize = (20,10), fontsize = 20, legend = False, color='darkgreen')
plt.axhline(y=0, color='black', linestyle='--')
plt.title('Sentiment Analysis for the journey of ' + protag ,fontsize = 30)
plt.xlabel("Journey", fontsize = 20)
plt.ylabel("Sentiment level", fontsize = 20)
plt.show()


# Protagonist Journey cumulative
character_jc = character_journey_cumulative(protag,10)
df_jc = pd.DataFrame.from_dict(character_jc, orient = 'index')

#Lineplot
df_jc.plot.line(figsize = (20,10), fontsize = 20, legend = False, color='darkgreen')
plt.axhline(y=0, color='black', linestyle='--')
plt.title('Sentiment Analysis for the journey of ' + protag ,fontsize = 30)
plt.xlabel("Journey", fontsize = 20)
plt.ylabel("Cumulative sentiment level", fontsize = 20)
plt.show()
