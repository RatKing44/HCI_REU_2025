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


# return readability score using coleman_liau method
def coleman_liau(text):
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

    # number of sentences per 100 words
    avg_sentence_len = num_sentences * 100 / num_words

    # number of letters per 100 words
    avg_word_length = num_letters * 100 / num_words

    # percentage of deletions that can be filled in by college undergrad (according to coleman-liau paper)
    cloze_perc = 141.8401 - .214590 * avg_word_length + 1.079812 * avg_sentence_len

    # grade level conversion from cloze percentage
    return round(-27.4004 * (cloze_perc/100) + 23.06395)

def data():
    #with open("test.txt") as f:
    #    text = f.read() #sys.argv[1]
    score = coleman_liau(text)
    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS").rglob('*.txt'):
        with open(file) as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS')
                              
            print(fname, data(), sep=' - Grade: ')
    
