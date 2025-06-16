import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer
nltk.download('punkt_tab')
import sys
import pathlib
import re

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove multiple spaces and newlines
    #text = re.sub(r'\s+', ' ', text).strip()

    # Replace tabs with spaces
    #text = text.replace('\t', ' ')

    # Remove any remaining non-alphanumeric characters except spaces
    #text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return text


#https://stackoverflow.com/questions/46759492/syllable-count-in-python
def count_syllables(word):
    word = word.lower()
    count = 0 # number of syllables in word
    vowels = "aeiouy"

    if word[0] in vowels: # if the first letter is a vowel count 1 syllable
        count += 1
    for index in range(1, len(word)): # count each occurrence of a vowel followed by a consonant
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"): # special case
        count -= 1
    if count == 0:
        count += 1
    return count

# return readability score using gunning-fog index
def gunning_fog(text):
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t.isalnum()] # extract every alphanumeric word as a "word" for our purposes

    # number of letters in the text (in actual words)
    num_letters = 0
    for t in tokens:
        num_letters += len(t)

    # number of actual words in the text
    num_words = len(tokens)
    if num_words == 0:
        return -1
    try:
        # number of sentences using nlkt sentence tokenizer
        num_sentences = len(sent_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        num_sentences = len(sent_tokenize(text))

    # find average sentence length
    avg_sentence_len = num_words / num_sentences

    num_complex = 0 # number of words with more than 3 syllables
    for token in tokens:
        if count_syllables(token) > 3:
            num_complex+=1

    # final gunning fog index calculation, rounded
    return round(0.4 * (avg_sentence_len + 100*(num_complex/num_words)))

def data():
    #with open("test.txt") as f:
    #    text = f.read() #sys.argv[1]
    score = gunning_fog(text)
    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS").rglob('*.txt'):
        with open(file) as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS')
                              
            print(fname, data(), sep=' - Grade: ')
    
    # print(count_syllables("Supercalifragilisticexpialidocious"))