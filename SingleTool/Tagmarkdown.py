from pathlib import Path
import re
import shutil


class TagMarkdown:

    def __init__(self, file):
        self.path = Path(file)
        self.tags = []
        self.title = ''

    def gettag(self):
        self.tags, self.title = self.format_heads()

    def searchtag(self, stags):
        result = None
        etags = self.tags
        flag = True
        for stag in stags:
            if stag not in etags:
                flag = False
        if flag:
            result = self.path
        return result

    def searchtaginfolder(self, *stags):
        if self.path.is_dir():
            results = []
            print('Search Result for {}:'.format(stags))
            for file in self.path.glob('*.md'):
                self.path = file
                self.gettag()
                stags = list(stags)
                result = self.searchtag(stags)
                if result:
                    results.append(result)
                    print(result)
            return results

    def addtag(self):
        pass

    def read_some_lines(self, start=0, end=6):
        with open(self.path, 'r', encoding='utf-8') as file:
            return file.readlines()[start:end]

    def writefile(self, content):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(content)

    def format_heads(self):
        try:
            heads = self.read_some_lines()
            tags = re.search(r'\[(.*)\]', heads[1]).group(1).split(',')
            title = heads[2].replace('title: ', '')
            return tags, title
        except AttributeError as e:
            print(self.path)
            return [], ''


def move2folder(file: Path, folder='Command'):
    name = file.name
    parent = file.parent / folder
    parent.mkdir(exist_ok=True)
    newfile = parent / name
    # shutil.move(file, newfile
    print(file, '--->', newfile)


if __name__ == '__main__':
    # path = 'D:\\Notable\\notes\\ab.md'
    path = 'D:\\Notable\\notes'
    t = TagMarkdown(path)
    t.searchtaginfolder('Linux/Command')
