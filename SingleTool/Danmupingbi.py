from pathlib import Path
import re

# common block words list
com_bwl = ['爱情', '备胎', '选择', 'bgm', 'BGM', '主题曲', '喜欢', '弹幕', '馋身子', '阴影', '原创',
           '魔改', '加戏', '小三', '贱', '婊', '白莲', '圣母', '引战', '招黑', '女人', '撕', '素质',
           '逼', '去死', '真丑', '党', '站', '青春', '小学', '童年', '高能', '温柔', '男孩', '护眼',
           '配音', '前女友', '愧疚', '啊啊啊', '再来亿集', '肝', '我爱', '都爱', '最爱', '扎心',
           '都要', '吃瓜', '看戏', '片头曲', 'biss', '开虐', '老婆', 'BGM', '尼玛', '特别虐', '裂开',
           '媳妇', '馋她', '跳集', '结婚', '太美', '心疼', '可爱', '可怜', '善良', '女主', '男主',
           '穆斯林', '手动', '立场', '各有所爱', '00后', '90后', '哎', '没有错', '呵呵', '屏蔽词',
           '理智', '路人', '666', '实话', '？？', '别再争了', '我有点', '口吐', '狗血', '狗男人',
           '脏话', '美哭了', '好美啊', '前面', '百合', '屁话', '大家', '哈哈哈', '233', '女生', '粉丝',
           '争个', '一个人', '肝', '渣男', '标题', '争来争去', '我家', '前方', '狗男女', '修罗场', '绿茶',
           '口区', '三观', '气死我', '卧槽', '吐了', '刀片', '气哭', '好气', '女孩', '真爱', '舒服', '爽爽',
           '舒适', '啧啧', '出轨', '直男', '天朝', 'pos(0,-999)', '反派']


class Danmu:

    def __init__(self, path, bwl: list):
        self.path = Path(path)
        self.isfolder = self.path.is_dir()
        self.bwl = bwl + com_bwl
        self.patterns = {
            'dialogue': re.compile(r'Dialogue:'),
            'move': re.compile(r'move\((.+,(\d+))\)'),
            'pos': re.compile(r'pos\((.+,(\d+))\)'),
            'style': re.compile(r'(Style: .*,黑体,)(\d+)')
        }

    def pb(self):

        with open(self.path, 'r', encoding='utf-8') as dmfile:
            dm = dmfile.readlines()

        blocked_dml = []
        for line in dm:
            flag = False  # block word in line?
            for bw in self.bwl:
                if bw in line:
                    flag = True

            if not flag:
                blocked_dml.append(self.dm_parse(line))
        self.save2file(''.join(blocked_dml))

    def handle(self):
        if self.isfolder:
            folerpath = self.path
            for file in folerpath.glob('*.ass'):
                self.path = file
                self.pb()
        else:
            self.pb()

    def save2file(self, blocked_dm):
        if self.isfolder:
            name = self.path.name
            parent = self.path.parent / 'Blocked'
            parent.mkdir(exist_ok=True)
        else:
            stem = self.path.stem
            suffix = self.path.suffix
            name = '{}_blocked{}'.format(stem, suffix)
            parent = self.path.parent

        newfile = parent / name
        with open(newfile, 'w', encoding='utf-8') as f:
            f.write(blocked_dm)
        print(newfile)

    # danmu parse
    def dm_parse(self, text):
        if self.patterns['dialogue'].match(text):
            move = self.patterns['move'].search(text)
            pos = self.patterns['pos'].search(text)

            if move:
                old = move.group(1)
                tmp = old.split(',')
                tmp[1] = tmp[3] = posfunc(tmp[1])
                new = ','.join(tmp)
                return text.replace(old, new)
            elif pos:
                old = pos.group(1)
                tmp = old.split(',')
                tmp[1] = posfunc(tmp[1])
                new = ','.join(tmp)
                return text.replace(old, new)
            else:
                return text
        elif self.patterns['style'].search(text):
            return self.patterns['style'].sub(stylefunc, text)
        else:
            return text

    def test(self):
        with open(self.path, 'r', encoding='utf-8') as dm:
            dm = dm.readlines()

        for line in dm:
            print(self.dm_parse(line))


def getpbc(path):
    with open(path, encoding='utf-8') as fl:
        pp = fl.readlines()
    oo = []
    for i in pp:
        oo.append(i.strip())
    print(oo)


def posfunc(x: str) -> str:
    return str(int(x) // 30 * 22)


def stylefunc(m):
    return m.group(1) + str(int(m.group(2)) // 1.5)


if __name__ == '__main__':
    qycpbc = ['犬夜叉', '杀生丸', '桔梗', '戈薇', '阿篱', '阿离', '老婆', '护妻狂魔', '杀殿', '桔粉',
              '犬薇', '犬微', '犬桔', '桔薇', '戈桔之争', '狗子', '玲', '铃', '北条', '钢牙', '奈落', '渣狗',
              '珊瑚', '弥勒', '神乐', '杀乐']
    d = Danmu('D:\\Download\\犬夜叉弹幕', qycpbc)
    d.handle()
