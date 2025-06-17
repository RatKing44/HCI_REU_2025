import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer
nltk.download('punkt_tab')
import sys
import pathlib
import re

debug = False

def debugPrint(s):
    if debug:
        print(s)


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

def dale(text, easy_words):
    stemmer = PorterStemmer()
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]

    # find number of words in text
    num_words = len(tokens)
    if num_words == 0:
        return -1
    try: # find number of sentences in text
        num_sentences = len(sent_tokenize(text))
    except LookupError:
        nltk.download('punkt')
        num_sentences = len(sent_tokenize(text))

    num_dale_complex = sum([1 for t in tokens if stemmer.stem(t.lower()) not in easy_words and not t.isnumeric()])     # find number of complex words according to dale-chall easy words list

    avg_sentence_len = num_words / num_sentences 
    percent_difficult_words = num_dale_complex / num_words * 100

    # can ignore/delete later--debugging print statements
    debugPrint(str(num_sentences) + " sentences, " + str(num_words) + " words")
    debugPrint(str(num_dale_complex) + " / " + str(num_words) + " = " + str(round(percent_difficult_words)) + "% difficult words")
    # for t in tokens:
    #     if stemmer.stem(t.lower()) not in easy_words and not t.isnumeric():
    #         debugPrint(t)

    return round((0.0496 * avg_sentence_len) + (0.1579 * percent_difficult_words))


def dale_chall(text):
    dale_path = "dale_easy.txt"
    with open(dale_path) as f:
        easy_words = set(line.strip() for line in f)

    return dale(text, easy_words)

def data():
    #with open("test.txt") as f:
    #    text = f.read() #sys.argv[1]
    score = dale_chall(text)

    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS").rglob('*.txt'):
        with open(file) as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS')
                                
            print(fname, data(), sep=' - Score: ')
