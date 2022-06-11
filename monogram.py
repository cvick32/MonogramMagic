import glob, os, json
from pyembroidery import *

punctuation = {
    "!": "exclamation.pes",
    "?": "question.pes",
    ".": "period.pes",
    ",": "comma.pes",
    ">": "bracket.pes",
    "<": "bracket.pes"
}

def get_letter_file(letter, font_dir):
    letter_file = None
    if letter.isupper():
        letter_file = os.path.join(font_dir, letter + "Upper.pes")
    elif letter.islower():
        letter_file = os.path.join(font_dir, letter + "Lower.pes")
    elif letter.isnumeric():
        letter_file = os.path.join(font_dir, letter + ".pes")
    elif letter in punctuation.keys():
        letter_file = os.path.join(font_dir, punctuation[letter])
    if os.path.exists(letter_file):
        return letter_file
    else:
        raise ValueError(f"Could not find \"{letter}\" in selected font and size." + f"\n{font_dir}")

def remove_stitches_from_pattern(pat, del_list):
    for idx, stitch_idx in enumerate(del_list):
        stitch_idx -= (2 * idx)
        del pat.stitches[(stitch_idx - 2):stitch_idx]
        pat.add_command(JUMP)
    del pat.stitches[len(pat.stitches) - 1]
    return pat

def calculate_dx(cur_width, last_width):
    BUFFER = 50
    scale = last_width / cur_width
    if last_width > cur_width:
        if scale > 1:
            scale = (1 / scale)
        dx = ((last_width / 2)  + (cur_width / 2)) + (scale * BUFFER)
    else:
        dx = ((last_width / 2) + (cur_width / 2)) + (scale * BUFFER)
    return BUFFER + dx

def normalize_letter_pat_to_tallest_letter(letter_pat, least_min_y):
    min_y = letter_pat.bounds()[1]
    if min_y != least_min_y:
        dy = least_min_y + abs(min_y)
        letter_pat.translate(dx=0,dy=abs(dy))
    return letter_pat

def normalize_letter_pat_to_origin(letter_pat):
    bounds = letter_pat.bounds()
    min_x, min_y, max_x, max_y = bounds[0], bounds[1], bounds[2], bounds[3]
    dx, dy = 0, 0
    if min_x + max_x != 0:
        width = abs(max_x) + abs(min_x)
        dx = (width // 2) - max_x
    if min_y + max_y != 0:
        height = abs(max_y) + abs(min_y)
        dy = (height // 2) - max_y
    letter_pat.translate(dx, dy)
    return letter_pat

def normalize_all_letter_pats_to_origin(letters, font_dir):
    letter_pats = []
    least_min_y = 1000
    for letter in letters:
        position = letter[1]
        letter = letter[0]
        cur_font_dir = os.path.join(font_dir, position)
        letter_path = get_letter_file(letter, cur_font_dir)
        letter_pat = normalize_letter_pat_to_origin(EmbPattern(letter_path))
        if letter_pat.bounds()[1] < least_min_y:
            least_min_y = letter_pat.bounds()[1]
        letter_pats.append(letter_pat)
    return [normalize_letter_pat_to_tallest_letter(lp, least_min_y) for lp in letter_pats]

def combine_font_files(initials, font_dir, monogram_position):
    pattern = EmbPattern()
    pattern.add_block([0,0],[0,0])
    stitches_to_delete = [3]
    initials = zip(initials, monogram_position)
    letter_widths = []
    normalized_letter_pats = normalize_all_letter_pats_to_origin(initials, font_dir)
    for idx, letter_pat in enumerate(normalized_letter_pats):
        letter_pat.threadlist = [pattern.threadlist[0]]
        bounds = letter_pat.bounds()
        width = abs(bounds[2]) + abs(bounds[0])
        letter_widths.append(width)
        dx = 0
        if idx != 0:
            i = idx - 1
            dx = calculate_dx(width, letter_widths[i])
        pattern.add_pattern(letter_pat, dx=dx)
        p = EmbPattern()
        p.add_block([(0,0), (0,0)], pattern.threadlist[0])
        pattern += p
        stitches_to_delete.append(len(pattern.stitches) - 1)
    return remove_stitches_from_pattern(pattern, stitches_to_delete)

def get_double_letter_file(letters, font_dir, font_name):
    if len(letters) != 2:
        raise Exception(f"Font {font_name} only handles initials of exactly length 2. Initials '{letters}' does not satisfy this requirement.")
    else:
        letters = [l for l in letters]
        if letters[0] <= letters[1]:
            filename = f"{letters[0]}-{letters[1]}.pes"
        else:
            filename = f"{letters[1]}-{letters[0]}.pes"
        double_letter_file = os.path.join(font_dir, filename)
        return EmbPattern(double_letter_file)

def get_type(font_dir):
    with open(os.path.join(font_dir, 'font_options.json')) as f:
        opt = json.load(f)
        return opt["type"]

def split_letters_and_symbols(initials):
    letters = ""
    symbols = ""
    for init in initials:
        if init.isalnum():
            letters += init
        else:
            symbols += init
    return letters, symbols

def monogram(font_name, monogram_initials, size, platform):
    platform_font_dir, platform_write_dir = platform
    font_dir = os.path.join(platform_font_dir, font_name, size)
    filename = f"{monogram_initials}-{font_name}-{size}.pes"
    full_filename = os.path.join(platform_write_dir, filename)
    if os.path.isfile(full_filename):
        with open(full_filename, 'a') as f:
            f.write(" ") # just make it so we save the file in the current time
        return "exists"
    type = get_type(os.path.join(platform_font_dir, font_name))
    if type == "monogram":
        monogram_initials, monogram_symbols = split_letters_and_symbols(monogram_initials)
        if len(monogram_initials) == 1:
            new_pattern = combine_font_files(monogram_initials, font_dir, ["center"])
        elif len(monogram_initials) == 2:
            new_pattern = combine_font_files(monogram_initials, font_dir, ["left", "right"])
        elif len(monogram_initials) == 3:
            new_pattern = combine_font_files(monogram_initials, font_dir, ["left", "center", "right"])
        else:
            new_pattern = combine_font_files(monogram_initials, font_dir, ["left" for i in monogram_initials])
        if monogram_symbols:
            new_pattern = combine_font_files(monogram_symbols, font_dir, ["" for i in monogram_symbols], pattern=new_pattern)
    elif type == "double":
        new_pattern = get_double_letter_file(monogram_initials, font_dir, font_name)

    else:
        new_pattern = combine_font_files(monogram_initials, font_dir, ["" for i in monogram_initials])
    return "created", new_pattern, full_filename

def print_png(pattern, out):
    '''
    must add .png to work
    '''
    pattern.write(out + ".png")
