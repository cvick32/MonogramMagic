import os
import shutil

#font_dir = 'C:/Users/initi/Documents/embroidery/pes/Bean/'
font_dir = '/Users/colevick/Documents/cs/projects/embroidery/pes/Maxwell/'


sizes = ['1.5in', '2.5in', '3.5in']

for size in sizes:
#    for position in ["center"]:
    path = os.path.join(font_dir, size)#, position)
    files = [f for f in os.listdir(path)]
    for letter_file in files:
        old_letter_file = os.path.join(path, letter_file)
        letter = letter_file.split(".")[0]
        new_letter_file = letter.upper() + "Upper.pes"
        os.rename(old_letter_file, os.path.join(path, new_letter_file))


