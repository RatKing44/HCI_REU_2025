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

def spache(text, easy_words):
    stemmer = PorterStemmer()
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

    if num_sentences == 0:
        return -1

    # Extract all the word tokens, remove any that aren't alphanumeric
    tokens = []
    for s in sentences:
        tokens += tokenizer.tokenize(s)

    tokens = [t for t in tokens if t.isalnum()]

    num_words = len(tokens)
    if num_words == 0:
        return -1

    # Find number of words not in the easy word list
    num_spache_complex = sum([1 for t in tokens if stemmer.stem(t.lower()) not in easy_words])

    # Determine average length of sentence
    avg_sentence_len = num_words / num_sentences

    # Determine percentage of words that are "difficult"
    percent_difficult_words = num_spache_complex / num_words * 100

    # Apply Spache-Allen formula
    return round((0.141 * avg_sentence_len) + (0.086 * percent_difficult_words) + 0.839)


def spache_allen(text):
    word_list = "f"
    if word_list == "8grade":
        spache_path = "spache_easy_8th_grade.txt"
    elif word_list == "13yo":
        spache_path = "spache_easy_13.txt"
    elif word_list == "agspache":
        spache_path = "ag-spache-allen.txt"
    else:
        spache_path = "spache_easy.txt"
    with open(spache_path) as f:
        easy_words = set(line.strip() for line in f)

    #print("Using word list:", spache_path)
    return spache(text, easy_words)

def data():
    score = spache_allen(text)

    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS_Danny").rglob('*.txt'):
        with open(file, encoding='utf-8') as f:
            text = clean_file(f.name)
            fname = f.name.removeprefix('EULAS_Danny\\').removesuffix('.txt')
                              
            print(fname, data(), sep=' - Grade: ')
