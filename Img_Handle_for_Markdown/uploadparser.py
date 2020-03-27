# -*- coding: utf-8 -*-

import re
import logging
import time
import random
from pathlib import Path

import requests

from configparser import ConfigParser

from qiniu import Auth, put_file
from qiniu import BucketManager


class MdImgHandle(object):

    def __init__(self, workpath, source='local', dest='qn', download_folder='images', change_name=True):
        logging.basicConfig(level=logging.INFO)

        # work path init
        self.workpath = Path(workpath)
        self.isfolder = self.workpath.is_dir()

        # method init
        self.source_from = source
        self.upload_method = dest

        self.randomstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # qn init
        self.qn_access_key = ''
        self.qn_secret_key = ''
        self.qn_bucket_name = ''
        self.qn_bucket_url = ''
        self.q = None
        self.bucket = None

        # file download init
        self.download_folder = Path(download_folder)
        self.download_filename_format = ''
        self.download_default_suffix = ''
        self.change_name = change_name

        self.imagehandle = None

    # document write
    @staticmethod
    def md_write(file_path, file_content):
        try:
            with open(file_path, 'w', encoding='utf-8') as md:
                md.write(file_content)
            logging.info("Job for --{}-- Done!".format(file_path))

        except BaseException as err:
            logging.error("Error in md_write\n{}".format(err))

    # format upload filename
    def format_key(self):
        return time.strftime('%Y%m%d%H%M%S') + '-' + random.choice(self.randomstring)

    # qn load config
    def loadconf(self):
        cfg = ConfigParser()
        try:
            cfg.read(r'UploadImg.ini')
            self.qn_access_key = cfg.get('qn', 'Access_Key')
            self.qn_secret_key = cfg.get('qn', 'Secret_Key')
            self.qn_bucket_name = cfg.get('qn', 'Bucket_Name')
            self.qn_bucket_url = cfg.get('qn', 'Bucket_Url')

            self.q = Auth(self.qn_access_key, self.qn_secret_key)

        except BaseException as err:
            logging.error("Error in loadconf\n{},please check your config file".format(err))

    # local upload to qn
    def local_2_qn(self, img_origin_url):
        try:
            key = self.format_key()
            token = self.q.upload_token(self.qn_bucket_name, key, 3600)
            localfile = img_origin_url
            ret, info = put_file(token, key, localfile)
            return self.qn_bucket_url + key
        except BaseException as err:
            logging.error("Error in Loacl Upload to qn\n{}".format(err))

    # url up load to qn
    def internet_2_qn(self, img_origin_url):
        try:
            key = self.format_key()
            ret, info = self.bucket.fetch(img_origin_url, self.qn_bucket_name, key)
            return self.qn_bucket_url + key
        except BaseException as err:
            logging.error("Error in Internet_url Upload to qn\n{}".format(err))

    def download_changed_filename(self, file: Path):
        file_suffix = file.suffix
        return self.format_key() + (file_suffix if file_suffix else self.download_default_suffix)

    # url download to local
    def url_2_local(self, img_origin_url: str):
        try:
            file = Path(img_origin_url)
            if self.change_name:
                filepath = self.download_folder / self.download_changed_filename(file)
            else:
                filepath = self.download_folder / file.name

            if filepath.exists():
                return str(filepath)

            r = requests.get(img_origin_url)

            with open(filepath, 'wb') as f:
                f.write(r.content)

            return str(filepath)
        except BaseException as err:
            logging.error("Error in Url Download to Local\n{}".format(err))

    # document handle
    def file_handle(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as md:
                file_content = md.read()

            img_block = re.findall(r'!\[.*?\)', file_content)

            for i in range(len(img_block)):
                img_origin_url = re.findall(r'\((.*?)\)', img_block[i])  # 获取插入图片时图片路径
                img_new_url = self.imagehandle(img_origin_url[0])
                file_content = file_content.replace(img_origin_url[0], img_new_url)

            self.md_write(filepath, file_content)
            return

        except BaseException as err:
            logging.error("Error in change_img_path\n{}".format(err))

    def handle(self):
        if self.source_from == 'local' and self.upload_method == 'qn':
            self.loadconf()
            self.imagehandle = self.local_2_qn
        elif self.source_from == 'internet' and self.upload_method == 'qn':
            self.loadconf()
            self.bucket = BucketManager(self.q)
            self.imagehandle = self.internet_2_qn
        elif self.source_from == 'internet' and self.upload_method == 'local':
            if self.isfolder:
                self.download_folder = self.workpath / self.download_folder
            else:
                self.download_folder = self.workpath.parent / self.download_folder
            try:
                self.download_folder.mkdir()
            except FileExistsError:
                logging.info("Download Folder {} is already exist !\nStill Use it!".format(self.download_folder))
            self.imagehandle = self.url_2_local
        else:
            pass

        if self.isfolder:
            try:
                for file in self.workpath.glob('*.md'):
                    self.file_handle(file)
            except BaseException as err:
                logging.error("Error in change_img_path\n{}".format(err))

        else:
            self.file_handle(self.workpath)


if __name__ == '__main__':
    path = "D:\\Fisher"

    for folder in Path(path).glob('*'):
        print(folder)
        foo = MdImgHandle(folder, source='internet')
        foo.handle()
    # print(foo.qn_upload('D:/nginx.png'))
