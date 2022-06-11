import os
import shutil
from pyembroidery import *

#font_dir = 'C:/Users/initi/Documents/embroidery/pes/Bean/'
font_dir = '/Users/colevick/Documents/cs/projects/embroidery/pes/MonogramChic/'


sizes = ['4in']

for size in sizes:
#    for position in ["center"]:
    path = os.path.join(font_dir, size)#, position)
    files = [f for f in os.listdir(path)]
    for letter_file in files:
        print(letter_file)
        old_letter_file = os.path.join(path, letter_file)
        letter = letter_file.split('.')[0]
        letter = letter.split(' ')[0]
        pattern = EmbPattern(old_letter_file)
        pattern.write(os.path.join(path, letter + '.pes'))
        print(os.path.join(path, letter + '.pes'))



