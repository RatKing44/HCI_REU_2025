import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer
nltk.download('punkt_tab')
import sys
import pathlib
import re
import random
import math

# count syllables in a word.
# sylco from https://stackoverflow.com/questions/46759492/syllable-count-in-python
def sylco(word) :
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']

    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']

    pre_one = ['preach']

    syls = 0 #added syllable number
    disc = 0 #discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        return syls

    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                disc+=1

    #3) discard trailing "e", except where ending is "le"  

    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']

    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass

        else :
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
    disc+=doubleAndtripple + tripple

    #5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian" : 
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui' :

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]

    if word[-3:] == "n't" :
        if word in negative :
            syls+=1
        else :
            pass   

    #14) Handling the exceptional words.

    if word in exception_del :
        disc+=1

    if word in exception_add :
        syls+=1     

    # calculate the output
    return numVowels - disc + syls

# Remove unwanted ASCII characters from the text
def strip_ascii(text):

    text = "".join(
        char for char in text
        if 31 < ord(char) < 127 and ord(char) not in (40, 41) or ord(char) == 10
    )

    return text

# Clean the file to be readable for the algorithm
def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    text = strip_ascii(text)
    text = re.sub(r'\n+', '\n', text)
            
    return text


# return readability score using smog grading method
def smog(text):
    tokenizer = TweetTokenizer()

    # Split on sentence-ending punctuation followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # Filter out empty strings
    sentences = [s for s in sentences if s.strip()]

    # Filter out captions
    for i in range(len(sentences)):
        if '\n' in sentences[i]:
            sentences[i] = sentences[i].rsplit('\n', 1)[1].strip()

    num_sentences = len(sentences)

    # If not enough sentences for somewhat accurate scoring, break
    if num_sentences < 30:
        return -1

    # beginning of sentence: 0 to .2 * num_sentences
    beginning_sents_range_end = round(0.2 * num_sentences)
    beginning_sents_start = random.randint(0, beginning_sents_range_end)
    beginning_sents = sentences[beginning_sents_start: beginning_sents_start + 10]

    # middle of sentence: .4 * num_sentences to .6 * num_sentences
    middle_sents_range_start = round(0.4 * num_sentences)
    middle_sents_range_end = round(0.6 * num_sentences)
    middle_sents_start = random.randint(middle_sents_range_start, middle_sents_range_end)
    middle_sents = sentences[middle_sents_start: middle_sents_start + 10]

    # end of sentence: .8 * num_sentences to num_sentences - 1
    final_sents_range_start = round(0.7 * num_sentences)
    final_sents_start = random.randint(final_sents_range_start, num_sentences - 10)
    final_sents = sentences[final_sents_start: final_sents_start + 10]
    
    # find how many words in selected sentences have 3 or more syllables
    polysyls = 0
    sents = beginning_sents + middle_sents + final_sents
    for s in sents:
        s_words = tokenizer.tokenize(s) # split each sentence into words
        for w in s_words: # check if each word is polysyllabic
            if sylco(w) >= 3:
                polysyls += 1


    # grade level conversion from cloze percentage
    return round(math.sqrt(polysyls)) + 3

def data():
    score = smog(text)
    return score

# Execute smog grading on every file in folder
if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS_Danny").rglob('*.txt'):
        with open(file, encoding='utf-8') as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS_Danny\\').removesuffix('.txt')

            # number of runs for each document to get an average result
            trials = 10

            # run smog grading [trials] number of times, then average
            dataset = []
            for i in range(trials):
                dataset.append(data())

            result = sum(dataset)/trials
                              
            print(fname, round(result), sep=' - Grade: ')
    