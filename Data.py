class Data:
  def __init__(self):
    pass

  def stemming(self):
    pass

  def deleteStopwords(self):
    pass

  def getData(self, data):
    to_return = []
    f = open(data, "r")
    i = 0
    while i < len(data):
      line = f.readline()
      line.lower()  # non funziona, cribbio
      sentences = line.split(".")
      for sentence in sentences:
        to_return.append(sentence)
      i += 1
    f.close()
    return to_return

  def print_file(self, data, out):
    f = open(out, "w")
    for string in data:
      f.write(string)
    f.close()

  def print_and_format(self, data): # può diventare solo di format
    for row in data:
      line = ""
      for i in row:
        line += i
      print line

  def writeon(self, data, out):
    out = open(out, "w")
    for row in data:
      line = ""
      for i in row:
        line += i
      out.write(line)


d = Data()
data = d.getData("doc.txt")
d.print_and_format(data)
