# -*- coding: utf-8 -*-

import re
import logging
import time
import random

from pathlib import Path
from SingleTool.Download import download_pic
from MdImg.QiNiu_Upload import qiniu_up

randomstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def format_key():
    ct = time.time()
    data_head = time.strftime("%Y%m%d%H%M%S")
    data_secs = (ct - int(ct)) * 1000
    return "%s%03d%s" % (data_head, data_secs, random.choice(randomstring))


def dl_pic(url: str, dl_folder: Path) -> Path:
    pic_name = format_key()
    pic_file = dl_folder / pic_name
    dl_file = download_pic(url, pic_file)
    return dl_file


class MdImgHandle(object):

    def __init__(self, workpath, download_folder='images', to_local=False, to_qiniu=False):
        logging.basicConfig(level=logging.INFO)

        # work path init
        self.workpath = Path(workpath)
        self.isfolder = self.workpath.is_dir()

        self.to_local = to_local
        self.to_qiniu = to_qiniu

        # file download init
        self.dl_folder = (self.workpath / download_folder) if self.isfolder \
            else (self.workpath.parent / download_folder)
        self.dl_folder.mkdir(exist_ok=True)

    # document write
    @staticmethod
    def md_write(file_path, file_content):
        try:
            file_path.write_text(file_content, encoding='utf-8')
            logging.info("Job for --{}-- Done!".format(file_path))
        except BaseException as err:
            logging.error("Error in md_write\n{}".format(err))

    def dlto_local(self, filepath):
        file_content = filepath.read_text(encoding="utf-8")
        img_block = re.findall(r'!\[.*?\)', file_content)
        if img_block:
            file_change = False
            for i in range(len(img_block)):
                img_origin_url = re.findall(r'\((.*?)\)', img_block[i])[0]
                try:
                    # Origin: Internet
                    if re.match('((http(s?))|(ftp))://.*', img_origin_url):
                        img_new_url = dl_pic(img_origin_url, self.dl_folder)
                        file_content = file_content.replace(img_origin_url, str(img_new_url))
                        file_change = True
                    # Origin: Local
                    elif re.match('([C-Z]:\\.*)|(\\.*)', img_origin_url):
                        if Path(img_origin_url).exists():
                            print(img_origin_url)
                    else:
                        pass
                except BaseException as e:
                    logging.error("Error in handle_img: {}\n-->{}".format(img_origin_url, e))
            if file_change:
                self.md_write(filepath, file_content)
        return

    def upto_qiniu(self, filepath):
        """

        @param filepath:
        @return:
        """
        file_content = filepath.read_text(encoding="utf-8")
        img_block = re.findall(r'!\[.*?\)', file_content)
        if img_block:
            file_change = False
            for i in range(len(img_block)):
                img_origin_url = re.findall(r'\((.*?)\)', img_block[i])[0]
                try:
                    # Origin: Internet
                    if re.match(r'((http(s?))|(ftp))://.*', img_origin_url):
                        print('Internet: ' + img_origin_url)
                        img_new_url = qiniu_up.crawling_pic(img_origin_url)
                        file_content = file_content.replace(img_origin_url, str(img_new_url))
                        file_change = True
                    # Origin: Local
                    elif re.match(r'([C-Z]:\\.*)|(\\.*)', img_origin_url):
                        print('Local: ' + img_origin_url)
                        img_new_url = qiniu_up.upload_pic(Path(img_origin_url))
                        file_content = file_content.replace(img_origin_url, str(img_new_url))
                        file_change = True
                    else:
                        pass
                except BaseException as e:
                    logging.error("Error in handle_img: {}\n-->{}".format(img_origin_url, e))
            if file_change:
                self.md_write(filepath, file_content)
        return

    def handle(self, filepath):
        if self.to_local and self.to_qiniu:
            logging.error("You can only set one from to_loacl and to_qiniu")
            return
        elif self.to_qiniu:
            self.upto_qiniu(filepath)
        elif self.to_local:
            self.dlto_local(filepath)
        else:
            return

    def start(self):
        if self.isfolder:
            try:
                for file in self.workpath.glob('*.md'):
                    print("Handle file {}".format(file))
                    self.handle(file)
            except BaseException as err:
                logging.error("Error in Handling folder: {}\n{}".format(self.workpath, err))
        else:
            print("Handle file {}".format(self.workpath))
            self.handle(self.workpath)


if __name__ == '__main__':
    foo = MdImgHandle("D:\\Test", to_qiniu=True)
    foo.start()
