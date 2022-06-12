# MonogramMagic

This repository contains the source code and instructions for running
Monogram Magic. Monogram Magic is a free tool for generating
embroidery files from an embroidery or monogramming font.

Please file an issue on Github if anything is unclear or left underspecifed!

# Installation

- Clone this repository
  - ```git clone https://github.com/cvick32/MonogramMagic.git```
- Create a Python virtual environment in the MonogramMagic folder
  - ```python3 -m venv mono-mag```
    - this command creates a virtual environment named "mono-mag"
- Activate the venv
  - ```. /mono-mag/bin/activate```
- Install requirements
  - ```pip install -r requirements.txt```
- Run the GUI
  - ```python3 gui.py```

# Introductory Video


# How it Works

If we look in the `fonts/Gigi` directory, we will see 4 items:
- a folder named `1.5in`
- a folder named `2in`
- a folder named `4in`
- a file named `font_options.json`

Let's look at the `1.5in` folder first.

## A Folder Named 1.5in

The contents of ``1.5in/`` are pretty simple. There are 26 `pes` files
that each correspond to a different uppercase letter. If you have an
embroidery program that opens `pes` files you can inspect each file on
its own. If you don't have an embroidery program installed I highly
recommenced [Ink/Stitch](https://inkstitch.org/docs/install/) which
requires [InkScape](https://inkscape.org/release/inkscape-1.2/), both
are free and open-source.

The contents in `2in` and `4in` are the same as the files here except
for the change in sizing.

If the font had lowercase letters the names would be `aLower.pes`,
`bLower.pes`, et cetera.

## A File Named ```font_options.json```

This file contains information specific to the Gigi font. The only
fields that are used when running MonogramMagic are the `type` and
`sizes` field. The others are used when running the
`structure_font_dir.py` script. There are various scripts included in
the `scripts` directory that help with taking a font and forcing it
into the structure defined above.

## Typing with Gigi

Now that we know how the Gigi font files are stored, let's try to type
with them. If we run `gui.py`, input some initials, and click Create
File, MonogramMagic will add all of the character embroidery files
together and output the new embroidery pattern to the `Monograms/`
folder. Note that since we have no lowercase letters we cannot run
MonogramMagic with the initials "abc" (try it to see what happens).

## Under the Hood

Under the hood we use the fantastic `pyembroidery` library. This
project would be impossible without the hard work of the maintainers
of `pyembroiedery`, so we sincerely thank them.

# Your Turn!

Now that we've looked through the Gigi font and seen how it works,
take a look through the RoundCircleLinedAlpha font and try to spot the
differences. One hint is that RoundCircleLinedAlpha is a
`monogram`ming font while Gigi is a `spelling` font.


# Disclaimer

I've included two fonts, in the `fonts/` folder. These are just
example fonts, and I trust anyone who uses this software will abide by
the licensing of these fonts. If the creators of these fonts would
like me to take them down I am more than happy to.


