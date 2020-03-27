import os
import re
from pathlib import Path

despath = Path("C:/Users/y1297/Desktop/enml.txt")
soupath = Path("C:/Users/y1297/Desktop/zwml.txt")
outpath = Path("C:/Users/y1297/Desktop/out.txt")
output = []

patten = re.compile(r'\t(\d+)')

with open(soupath, encoding='utf-8') as f:
    souml = f.readlines()

middlefile = []

for line in souml:
    p = patten.search(line).group()
    newstr = '{}'.format(p)
    middlefile.append(newstr)

with open(despath, encoding='utf-8') as f:
    desml = f.readlines()

i = 0
for line in desml:
    p = patten.sub(middlefile[i], line)
    output.append(p)
    i += 1

with open(outpath, 'w', encoding='utf-8') as f:
    f.write(''.join(output))
print(output)