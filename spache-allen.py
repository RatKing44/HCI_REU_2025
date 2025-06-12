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

def spache(text, easy_words):
    stemmer = PorterStemmer()
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]

    num_words = len(tokens)
    if num_words == 0:
        return -1
    try:
        num_sentences = len(sent_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        num_sentences = len(sent_tokenize(text))
    num_spache_complex = sum([1 for t in tokens if stemmer.stem(t.lower()) not in easy_words])

    avg_sentence_len = num_words / num_sentences
    percent_difficult_words = num_spache_complex / num_words * 100

    return round((0.141 * avg_sentence_len) + (0.086 * percent_difficult_words) + 0.839)


def spache_allen(text):
    spache_path = "spache_easy.txt"
    with open(spache_path) as f:
        easy_words = set(line.strip() for line in f)

    return spache(text, easy_words)

def data():
    #with open("test.txt") as f:
    #    text = f.read() #sys.argv[1]
    score = spache_allen(text)

    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS").rglob('*.txt'):
        with open(file) as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS')
                              
            print(fname, data(), sep=' - Grade: ')
    


