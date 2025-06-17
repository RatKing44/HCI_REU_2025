import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer
nltk.download('punkt_tab')
import sys
import pathlib
import re

debug = False

# used for debugging
def debugPrint(s):
    if debug:
        print(s)

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

'''
Calculates the readability of a text using the Dale-Chall readability score.
https://www.jstor.org/stable/1473169?seq=7

4.9 or lower	grades 4 and below
5.0-5.9     	grades 5 - 6
6.0-6.9	        grades 7 - 8
7.0-7.9     	grades 9 - 10
8.0-8.9	        grades 11 - 12
9.0-9.9	        grades 13 - 15 (college)
10.0 and above  grades 16+ (college graduate)
'''
def calculate_dale(text, easy_words):
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

    # find number of complex words according to dale-chall easy words list
    num_dale_complex = sum([1 for t in tokens if stemmer.stem(t.lower()) not in easy_words and not t.isnumeric()])

    # find average sentence length
    avg_sentence_len = num_words / num_sentences 

    # find percent of words not in dale-easy list
    percent_difficult_words = num_dale_complex / num_words * 100

    # dale-chall readability formula calculation
    score = (0.0496 * avg_sentence_len) + (0.1579 * percent_difficult_words) 
    if (percent_difficult_words > 5): # adjusted if percentage of difficult words is 5%
        score += 3.6365


    # # can ignore/delete later--debugging print statements
    # debugPrint(str(num_sentences) + " sentences, " + str(num_words) + " words")
    # debugPrint(str(num_dale_complex) + " / " + str(num_words) + " = " + str(round(percent_difficult_words)) + "% difficult words")
    # # for t in tokens:
    # #     if stemmer.stem(t.lower()) not in easy_words and not t.isnumeric():
    # #         debugPrint(t)

    return round(score) # final score rounded


def dale_chall(text):
    dale_path = "dale_easy.txt"
    with open(dale_path) as f:
        easy_words = set(line.strip() for line in f)

    return calculate_dale(text, easy_words)

def data():
    #with open("test.txt") as f:
    #    text = f.read() #sys.argv[1]
    score = dale_chall(text)

    return score

if __name__ == '__main__':
    from pathlib import Path
    for file in Path("EULAS_Danny").rglob('*.txt'):
        with open(file, encoding='utf-8') as f:
            clean_file(f.name)
            text = f.read()   
            fname = f.name.removeprefix('EULAS_Danny\\').removesuffix('.txt')
                                
            print(fname, data(), sep=' - Score: ')
