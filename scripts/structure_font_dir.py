import json, os, re
from shutil import copyfile

#main_font_dir = 'C:/Users/initi/Documents/embroidery/pes/Diamond5/'
main_font_dir = '/Users/colevick/Documents/cs/projects/embroidery/pes/VintageVine/'

def read_font_settings_json(dir):
        font_settings_file = os.path.join(dir, 'font_options.json')
        with open(font_settings_file) as f:
                return json.load(f)

def create_size_dir(dir, size_name):
        new_size_dir = os.path.join(dir, size_name)
        try:
                os.mkdir(new_size_dir)
        except:
                pass
def create_position_dirs(dir, size_name):
        for pos in ["left", "right", "center"]:
                new_dir = os.path.join(dir, size_name, pos)
                try:
                        os.mkdir(new_dir)
                except:
                        pass

def get_letter(filename, case_dict):
        try:
                a = re.sub(case_dict['postfix'], '', re.sub(case_dict['prefix'], '', filename))
                if len(a) == 2:
                        return a[0]
                else:
                        return a
        except:
                print(filename)

def get_size_key(filename, sizes):
        '''
        Returns the longest size that the current filename
        contains.
        '''
        sizes_contained = list()
        for size in sizes:
                if size in filename:
                        sizes_contained.append((size, len(size)))
        return sorted(sizes_contained, key=lambda size: size[1], reverse=True)[0][0]

def get_dir_and_file_by_size(dir, filename, settings):
        if settings['sizes']:
                size_key = get_size_key(filename, settings['sizes'].keys())
                size = settings['sizes'][size_key]
                filename = filename.replace(size_key, '')
                cur_copy_dir = os.path.join(dir, size)
                return (cur_copy_dir, filename)
        else:
                print('here')
                return (dir, filename)


def is_in_group(filename, group):
        if group:
                if group['prefix'] in filename and group['postfix'] in filename:
                        return True
                else:
                        return False
        else:
                return False
        '''
        if group:
                group_regex = re.compile(group['regex'])
                return group_regex.match(filename)
        else:
                return False
        '''

def get_checks(settings):
        if settings['type'] == 'spelling':
                return [(settings['numbers'], "", ".pes"),
                        (settings['uppers'], "", "Upper.pes"),
                        (settings['lowers'], "", "Lower.pes"),
                        (settings['punctuation'], "",  ".pes")]
        else:
                return [(settings['right'], "right", "Upper.pes"),
                        (settings['left'], "left", "Upper.pes"),
                        (settings['center'], "center", "Upper.pes")]

def copy_letters_to_dir(font_dir, settings_json):
        cur_copy_dir = font_dir
        files = [f for f in os.listdir(font_dir) if ".pes" in f or ".PES" in f]
        for font_file in files:
                new_dir_name, new_filename = get_dir_and_file_by_size(font_dir, font_file, settings_json)
                checks = get_checks(settings_json)
                for check in checks:
                        if is_in_group(new_filename, check[0]):
                                letter_name = get_letter(new_filename, check[0])
                                if "Upper" in check[2]:
                                        letter_name = letter_name.upper()
                                elif "Lower" in check[2]:
                                        letter_name = letter_name.lower()
                                if len(check) == 4:
                                        copyfile(os.path.join(font_dir, font_file), os.path.join(new_dir_name, check[1], letter_name + check[3]))
                                        os.rename(os.path.join(font_dir, font_file), os.path.join(new_dir_name, check[2], letter_name + check[3]))
                                else:
                                        os.rename(os.path.join(font_dir, font_file), os.path.join(new_dir_name, check[1], letter_name + check[2]))

def structure_font_dir(dir):
        settings = read_font_settings_json(dir)
        if settings['sizes'].keys():
                for size in settings['sizes'].values():
                        create_size_dir(dir, size)
                        if settings['type'] == 'monogram':
                                create_position_dirs(dir, size)
        copy_letters_to_dir(dir, settings)

structure_font_dir(main_font_dir)
