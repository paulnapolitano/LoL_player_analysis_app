import re

lines = [line.rstrip() for line in open('api_doc.txt').readlines()]

BUILTINS = ['int',
            'string',
            'boolean',
            'long', 
            'double']

newfile = open('transcribed.txt', 'w')

for line in lines:
    line_words = line.split()
    name = line_words[0]
    type = line_words[1]
    
    # Check for lowercase first word
    start = re.search(r'^([a-z0-9]*)', name)
    
    # Compile all Words
    mine = re.compile(r'([A-Z]+[a-z0-9]*)')
    words = mine.findall(name)
  
    # Convert name to all lowercase with _ from camelBack
    new_name = ''
    if start.group(1):
        new_name += start.group(1)
        new_name += '_'
    for word in words:
        new_name += '{}_'.format(word.lower())
    new_name = new_name[0:-1]
    
    newfile.write("\t{} = models.".format(new_name))
    if type == 'double':
        newfile.write("FloatField(blank=True)\n")
    
    else:
        newfile.write("\n")
    
