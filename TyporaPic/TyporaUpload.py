# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/05/28
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import os
import re
import sys
import time
import imghdr
import random

from pathlib import Path
from dotenv import load_dotenv

from qiniu import Auth, put_file, etag

dotenv_path = Path(__file__).parent.absolute() / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


class QnUpload(object):

    def __init__(self):

        try:
            self.qn_access_key = os.getenv('QN_ACCESS_KEY')
            self.qn_secret_key = os.getenv('QN_SECRET_KEY')
            self.qn_bucket_name = os.getenv('QN_BUCKET_NAME')
            self.qn_bucket_url = os.getenv('QN_BUCKET_URL')
            self.q = Auth(self.qn_access_key, self.qn_secret_key)
        except BaseException as err:
            print("Error in loadconf! \n{}\nPlease check your config file".format(err))

        self.token = self.geneate_token(expires=600)

    def geneate_token(self, expires=15552000):
        return self.q.upload_token(self.qn_bucket_name, expires=expires)

    def upload(self, img_file: Path, key=None) -> str:
        try:
            if not key:
                key = img_file.name
            ret, info = put_file(self.token, key, img_file)
            assert ret['key'] == key
            assert ret['hash'] == etag(img_file)
            return self.qn_bucket_url + key
        except BaseException as err:
            print("Error in Uploading {} \n{}".format(img_file, err))


qn = QnUpload()

randomstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_suffix(path) -> str:
    return imghdr.what(path, h=None)


def get_key():
    ct = time.time()
    data_head = time.strftime("%Y%m%d%H%M%S")
    data_secs = (ct - int(ct)) * 1000
    return "%s%03d%s" % (data_head, data_secs, random.choice(randomstring))


def img_handle(img):
    if re.match('([C-Z]:\\.*)|(\\.*)', img):
        suffix = get_suffix(img)
        img = Path(img)
        if img.exists():
            keyname = get_key()
            key = "{}.{}".format(keyname, suffix) if suffix else keyname
            return qn.upload(img, key=key)


def upload(*files):
    imgs = sys.argv[1:] if not files else files
    result = []
    if imgs:
        for img in imgs:
            new_url = img_handle(img)
            result.append(new_url)
    if result and result[0]:
        print('Upload Success:')
        for url in result:
            print(url)


if len(sys.argv) > 1:
    upload()
