import re

attrs = [line.rstrip().lstrip().split()[0].split('.')[1] 
         for line in open('attributes.txt').readlines()]

newfile = open('get_funcs.txt', 'w')

for attr in attrs:
    string = "\tdef get_{}(self):\n\t\treturn self.{}\n".format(attr,attr)
    newfile.write(string)
    
