
#!pip install PyDictionary
import inflect
p = inflect.engine()
from PyDictionary import PyDictionary
import re
import numpy
import nltk

#nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import requests
import ast
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
import sys
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


dictionary = PyDictionary()
def findWords(stri):
    result = []
    data = re.split(', |_|-|!| ', stri)
    for words in data:
        blockPrint()
        synonym = dictionary.synonym(words)
        antonym = dictionary.antonym(words)
        enablePrint()
        if not antonym and not synonym:
            temp = []
        elif not synonym and antonym:
            temp = antonym
        elif not antonym and synonym:
            temp = synonym
        else:
            temp = numpy.concatenate([synonym, antonym])
        result = numpy.concatenate([result, temp])

    return result

def wikipedia_solution(wikipedia_clues):
    WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?action=query&utf8=&format=json&list=search&srlimit=50&srsearch="
    stop = stopwords.words('english') + list(string.punctuation)
    #clue_mapping = dict()
    #print("wikipedia fetching word for " + wikipedia_clues)
    if '#' in wikipedia_clues:
        wikipedia_clues = wikipedia_clues.replace("#", "")

    
    for sentence in wikipedia_clues:
        req = requests.get(WIKIPEDIA_API + sentence)
        wiki_json = ast.literal_eval(req.text)
        #print(wiki_json["query"])
        solutions = list(set([word for word in [[word for word in word_tokenize(info["title"].lower()) if word not in stop] for info in wiki_json["query"]["search"]] for word in word]))
    return solutions

def wikipedia_sentence_solution(wikipedia_clues):
    WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?action=query&utf8=&format=json&list=search&srlimit=50&srsearch="
    stop = stopwords.words('english') + list(string.punctuation)
    #clue_mapping = dict()
    #print(">>> STARTING WIKI FETCH sentence.....")
    if '#' in wikipedia_clues:
        wikipedia_clues = wikipedia_clues.replace("#", "")
    req = requests.get(WIKIPEDIA_API + wikipedia_clues)
    wiki_json = ast.literal_eval(req.text)
    solutions = list(set([word for word in [[word for word in word_tokenize(info["title"].lower()) if word not in stop] for info in wiki_json["query"]["search"]] for word in word]))
    return solutions
  
  
def possible_answers(clues, length):
    myarr = wikipedia_solution(clues)
    myarr = numpy.array(myarr)
    myarr = numpy.concatenate([myarr, findWords(clues)])
    myarr = numpy.concatenate([myarr, wikipedia_sentence_solution(clues)])
    finalResult = []
    returnResult = []
    for i in myarr:
    #if len(i) <= length:
       if i not in finalResult:
        finalResult.append(i.upper())
        if p.plural(i.upper()):
            finalResult.append(p.plural(i.upper()))
            
        if p.singular_noun(i.upper()):
            finalResult.append(p.singular_noun(i.upper()))

    for j in finalResult:
        #sorting based on length
        if len(j) == length:
            if j not in returnResult:
                returnResult.append(j)

    return returnResult