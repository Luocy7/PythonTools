# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/29
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from pathlib import Path
from MdImg.QiNiu_Upload import qiniu_up

workpath = Path('D:\\Test')

for imgfile in workpath.glob("*.*"):
    imgname = imgfile.name
    upname = 'yblog-{}'.format(imgname)
    up = qiniu_up.upload_pic(imgfile, key=upname)
    print(upname)
