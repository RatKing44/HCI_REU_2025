import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer
nltk.download('punkt_tab')
import sys
import pathlib
import re

def strip_ascii(text):

    text = "".join(
        char for char in text
        if 31 < ord(char) < 127 and ord(char) not in (40, 41) or ord(char) == 10
    )

    return text

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    text = strip_ascii(text)
    text = re.sub(r'\n+', '\n', text)
            
    return text

# return readability score using coleman_liau method
def coleman_liau(text):
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

    # Extract all the word tokens, remove any that aren't alphanumeric
    tokens = []
    for s in sentences:
        tokens += tokenizer.tokenize(s)

    tokens = [t for t in tokens if t.isalnum()]

    num_words = len(tokens)
    if num_words == 0:
        return -1

    # number of letters in the text (in actual words)
    num_letters = 0
    for t in tokens:
        num_letters += len(t)

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
    for file in Path("EULAS_Danny").rglob('*.txt'):
        with open(file, encoding='utf-8') as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS_Danny')
                              
            print(fname, data(), sep=' - Grade: ')
    
