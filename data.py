from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import Stemmer


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


def remove_punctuation(data):
    to_return = []
    tokenizer = RegexpTokenizer(r'\w+')
    for sentence in data:
        temp = ""
        tokenized = tokenizer.tokenize(sentence.lower())
        for word in tokenized:
            temp += word
            temp += " "
        to_return.append(temp)
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


def get_data(data):
    to_return = []
    f = open(data, "r")
    i = 0
    while i < len(
            data):  # scandisce fino alla fine dei giorni. per risolvere non ho salvato nell'array da ritornare le frasi(stringhe) vuote
        line = f.readline()
        sentences = line.split(". ")
        for sentence in sentences:
            if sentence != "\n" and sentence != '':
                if sentence.startswith(" "):
                    sentence.replace(" ", "")
                to_return.append(sentence)
        i += 1
    f.close()
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


def print_file(data, out):
    f = open(out, "w")
    for string in data:
        f.write(string)
    f.close()


def print_data(data):
    for row in data:
        print row


def write_on(data, out):
    out = open(out, "w")
    for row in data:
        line = ""
        for i in row:
            line += i
        out.write(line)