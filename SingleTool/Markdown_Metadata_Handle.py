from pathlib import Path

meta_template = ['', '', "created: '2020-01-05T06:13:22.217Z'", "modified: '2020-01-07T09:33:40.536Z'"]

meta_tags_template = 'tags: [{}]'
meta_title_template = 'title: {}'


class Metaprocessor(object):
    def __init__(self, filepath, meta_new_tags='', meta_new_title=''):
        self.filepath = Path(filepath)
        self.filename = self.filepath.stem

        with open(filepath, 'r', encoding='utf-8') as md:
            self.markdown = md.read()
            # print(self.markdown)

        self.has_meta = True
        self.markdown_meta = []

        self.meta_pre_tags = ''
        self.meta_pre_title = ''

        self.meta_new_tags = meta_new_tags
        self.meta_new_title = meta_new_title if meta_new_title else self.filename

        self.meta_format_new_tags = meta_tags_template.format(meta_new_tags)
        self.meta_format_new_title = meta_title_template.format(self.meta_new_title)

    def parse_meta(self):
        """ Parse MetaData and store in Markdown.Meta. """
        lines = self.markdown.split('\n')
        metadata_block = []
        line = lines.pop(0)
        if line == "---":
            while lines:
                line = lines.pop(0)
                if line == "---":
                    break
                metadata_block.append(line)
        else:
            lines.insert(0, line)
        if metadata_block:
            self.markdown_meta = metadata_block
            self.meta_pre_tags = self.markdown_meta[0]
            self.meta_pre_title = self.markdown_meta[1]
        else:
            self.has_meta = False
        return

    def write_meta_back(self):
        lines = self.markdown.split('\n')
        lines[1:5] = self.markdown_meta

        with open(self.filepath, 'w', encoding='utf-8') as md:
            for line in lines:
                md.write(line + '\n')

    def add_meta(self):
        lines = self.markdown.split('\n')
        lines = ['---'] + self.markdown_meta + ['---', ''] + lines

        with open(self.filepath, 'w', encoding='utf-8') as md:
            for line in lines:
                md.write(line + '\n')

    def main(self):
        self.parse_meta()
        if self.has_meta:
            self.markdown_meta[0] = self.meta_format_new_tags if self.meta_new_tags else self.meta_pre_tags
            self.markdown_meta[1] = self.meta_format_new_title if self.meta_new_title else self.meta_pre_title
            self.write_meta_back()
        else:
            meta_template[0] = self.meta_format_new_tags
            meta_template[1] = self.meta_format_new_title
            self.markdown_meta = meta_template
            self.add_meta()

            print("{} Handle Done!".format(self.filename))


if __name__ == '__main__':
    path = Path("D:/command")
    for i in path.glob("*.md"):
        Metaprocessor(i, meta_new_tags='Linux/Command').main()
