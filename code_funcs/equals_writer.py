newfile = open('equals_written.txt', 'w')

for line in open('oneequalsone.txt').readlines():
    word = line.split()[0]
    string = "{}={},\n".format(word,word)
    newfile.write(string)
    