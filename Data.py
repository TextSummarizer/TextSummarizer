from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class Data:
  def __init__(self):
    pass

  def stemming(self):
    pass

  def remove_punctuation(self, data):
    to_return = []
    tokenizer = RegexpTokenizer(r'\w+')
    for sentence in data:
      temp = ""
      tokenized = tokenizer.tokenize(sentence)
      for word in tokenized:
        temp += word
        temp += " "
      to_return.append(temp)
    return to_return

  def delete_stopwords(self, data):
    to_return = []
    stop = set(stopwords.words('english'))
    for sentence in data:
      stopped = ""
      sentence = sentence.split(" ")
      temp = [i for i in sentence if i not in stop]
      for word in temp:
        stopped += word
        stopped += " "
      to_return.append(stopped)
    return to_return

  def get_data(self, data):
    to_return = []
    f = open(data, "r")
    i = 0
    while i < len(
      data):  # scandisce fino alla fine dei giorni. per risolvere non ho salvato nell'array da ritornare le frasi(stringhe) vuote
      line = f.readline()
      sentences = line.lower().split(". ")
      for sentence in sentences:
        if sentence != "\n" and sentence != '':
          if sentence.startswith(" "):
            sentence.replace(" ", "")
          to_return.append(sentence)
      i += 1
    f.close()
    return to_return

  def print_file(self, data, out):
    f = open(out, "w")
    for string in data:
      f.write(string)
    f.close()

  def print_data(self, data):
    for row in data:
      print row

  def write_on(self, data, out):
    out = open(out, "w")
    for row in data:
      line = ""
      for i in row:
        line += i
      out.write(line)


d = Data()
data = d.get_data("testo.txt")
# d.print_data(data)
stopped = d.delete_stopwords(data)
# d.print_data(stopped)
no_points = d.remove_punctuation(data)
# d.print_data(no_points)
