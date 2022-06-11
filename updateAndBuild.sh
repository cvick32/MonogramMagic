#!/bin/bash
git pull
pyinstaller -y --noconsole --hidden-import=babel.numbers $1
