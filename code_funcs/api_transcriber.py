import re

lines = [line.rstrip() for line in open('api_doc.txt').readlines()]

BUILTINS = ['int',
            'string',
            'boolean',
            'long', 
            'double']

newfile = open('transcribed.txt', 'w')
newfile.write('\tdef __init__(self, dict):\n')

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
  
    string = "\t\tif '{}' in dict:\n\t\t\tself.{}".format(name, new_name)
    
    if type in BUILTINS:
        string += " = dict['{}']".format(name)
    elif 'List[' in type:
        type = type[5:-1]
        if type in BUILTINS:
            string += " = dict['{}']".format(name)
        else: 
            string += " = [{}(el) for el in dict['{}']]".format(type, name)
    elif 'Map[' in type:
        type = ''
        for word in line_words[1:3]:
            type += word
        type = type[4:-1]
        type = type.split(',')
        
        if type[0] in BUILTINS and type[1] in BUILTINS:
            string += " = dict['{}']".format(name)
        else:
            string += " = {}\n\t\t"
            string += "for key in dict['{}']:\n\t\t\t".format(name)
            string += "self.{}[key] = {}(dict['{}'][key])".format(new_name, type[1], name)
    else:
        string += " = {}(dict['{}'])".format(type, name)
    string += '\n' 
    newfile.write(string)
    
