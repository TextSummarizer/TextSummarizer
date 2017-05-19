from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import Stemmer
import re


def stemming(data):
    to_return = []
    stemmer = Stemmer.Stemmer('english')
    for sentence in data:
        string = ""
        temp = sentence.lower().split(" ")
        for word in temp:
            new_word = stemmer.stemWord(word)
            string += new_word
            string += " "
        to_return.append(string)
    return to_return


def remove_punctuation_regex(data):
    to_return = []
    p = re.compile(r'\W+')
    for sentence in data:
        temp = ""
        tokenized = p.split(sentence.lower())
        for word in tokenized:
            temp += word
            temp += " "
        to_return.append(temp)
    return to_return


def remove_punctuation_nltk(data):
    to_return = []
    for sentence in data:
        temp = ""
        tokenized = TreebankWordTokenizer().tokenize(sentence.lower())
        for word in tokenized:
            temp += word
            temp += " "
        to_return.append(temp[:-1])
    return to_return


def remove_stopwords(data):
    to_return = []
    stop = set(stopwords.words('english'))
    for sentence in data:
        stopped = ""
        sentence = sentence.lower().split(" ")
        temp = [i for i in sentence if i not in stop]
        for word in temp:
            stopped += word
            stopped += " "
        to_return.append(stopped)
    return to_return


def get_data(text):
    to_return = []
    sentences = text.split(". ")
    for sentence in sentences:
        if sentence != "\n" and sentence != '':
            if sentence.startswith(" "):
                sentence.replace(" ", "")
            if sentence.endswith("\n"):
                sentence = sentence.replace("\n", "")
            to_return.append(sentence)
    return to_return


def add_points(data):
    to_return = []
    for sentence in data:
        if sentence.endswith("\n"):
            sentence = sentence.replace("\n", "")
        if not sentence.endswith("."):
            sentence += "."
        to_return.append(sentence)
    return to_return


def export_summary(output_dir_path, filename, text):
    # create directory if does not exist
    import os
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    out = open(output_dir_path + '/' + filename, "w")
    out.write(text.encode('utf-8'))
    out.close()
