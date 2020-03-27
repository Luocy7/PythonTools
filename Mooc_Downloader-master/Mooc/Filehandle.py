#!/usr/bin/python3

import os
import re
import shutil
from pathlib import Path

cwd = os.getcwd()
folder = Path(cwd) / 'Java'

for i in folder.glob('*/*.mp4'):
    filename = i.name
    filename = re.sub(r'\[(.*)\]--(\w(\.\w)+)', r'\1-', filename)
    filename = re.sub(r'\[(.*)\]--', r'\1-', filename)

    newfloder = i.parent
    newfile = newfloder / filename

    shutil.move(i, newfile)

    print(i, newfile)