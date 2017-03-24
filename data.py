from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import Stemmer
import io


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


def get_data(file):
    to_return = []
    f = open(file, "r")
    i = 0
    file_len = _file_len(file)
    while i < file_len:
        line = f.readline()
        sentences = line.split(". ")
        for sentence in sentences:
            if sentence != "\n" and sentence != '':
                if sentence.startswith(" "):
                    sentence.replace(" ", "")
                if sentence.endswith("\n"):
                    sentence = sentence.replace("\n", "")
                to_return.append(sentence)
        i += 1
    f.close()
    return to_return


def remove_doc(text):
    to_return = []
    for sentence in text:
        if not sentence.startswith("doc"):
            to_return.append(sentence)
    return to_return


def _file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def add_points(data):
    to_return = []
    for sentence in data:
        if sentence.endswith("\n"):
            sentence = sentence.replace("\n", "")
        if not sentence.endswith("."):
            sentence += "."
        to_return.append(sentence)
    return to_return


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
    out.close()


def export_summary(output_dir_path, filename, text):
    # create directory if does not exist
    import os
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    out = open(output_dir_path + '/' + filename, "w")
    out.write(text)
    out.close()
