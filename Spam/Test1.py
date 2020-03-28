import re

text1 = 'Dialogue: 0,0:00:01.40,0:00:13.40,Medium,,0,0,0,,{\\move(2258.999,150,-338,150,0,12000)\\c&H1200e7&}I want' \
        ' to change the world'
text2 = 'Dialogue: 0,0:00:05.14,0:00:09.14,Medium,,0,0,0,,{\\pos(959.9999999999999,150)}全剧终'

text3 = 'Style: Small,黑体,20,&H64FFFFFF,&H64FFFFFF,&H64000000,&H64000000,1,0,0,0,100,100,0,0,1,1.2,0,5,0,0,0,0'

patterns = {
    'dialogue': re.compile(r'Dialogue:'),
    'move': re.compile(r'move\((.+,(\d+))\)'),
    'pos': re.compile(r'pos\((.+,(\d+))\)'),
    'style': re.compile(r'(Style: .*,黑体,)(\d+)')
}

def stylefunc(m):
    # return str(int(x) / 2)
    return m.group(1) + str(int(m.group(2)) // 2)


t = patterns['style'].sub(stylefunc, text3)

print(t)