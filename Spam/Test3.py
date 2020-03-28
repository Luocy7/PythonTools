import re

img_origin_url = " "

if re.match(r'([C-Z]:\\.*)|(\\.*)', img_origin_url):
    print(1)

