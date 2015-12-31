import re

newfile = open('if_in_written.txt', 'w')

for line in open('if_in.txt').readlines():
    my_search = re.search(r"'([^']+)", line)
    my_attr = my_search.group(1)
    string = "\t\tif '{}' in dict:\n\t{}".format(my_attr, line)
    newfile.write(string)
    
