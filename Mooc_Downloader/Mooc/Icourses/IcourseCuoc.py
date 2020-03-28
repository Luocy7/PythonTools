"""
    www.icourses.cn/cuoc/ 下的视频公开课下载解析
"""

import os
import re
import json

from Mooc.Mooc_Config import *
from Mooc.Mooc_Request import *
from Mooc.Icourses.Icourse_Config import *
from Mooc.Icourses.IcourseBase import *

__all__ = [
    "IcourseCuoc"
]


class IcourseCuoc(IcourseBase):
    url_course = "http://www.icourses.cn/web/sword/portal/videoDetail?courseId="

    def __init__(self):
        super().__init__()

    def _get_cid(self, url):
        self.cid = None
        match = courses_re.get('icourse_cuoc').match(url)
        if match:
            self.cid = match.group(1)

    def _get_title(self):
        if self.cid is None:
            return
        self.title = None
        url = self.url_course + self.cid
        text = request_get(url)
        match_title = re.search(r"_courseTitle.*?=.*?'(.*?)';", text)
        match_school = re.search(r'<a +?class *?= *?"teacher-infor-from">(.*?)</a>', text)
        if match_title and match_school:
            title_name = match_title.group(1) + '__' + match_school.group(1)
            self.title = winre.sub('', title_name)[:WIN_LENGTH]

    def _get_infos(self):
        if self.cid is None:
            return
        self.infos = []
        url = self.url_course + self.cid
        text = request_get(url)
        match_courses = re.search(r'_sourceArrStr *?= *?(\[.*?\]);\s*?var +?_shareUrl', text)
        if match_courses:
            # !!! except json.decoder.JSONDecodeError
            courses = json.loads(match_courses.group(1))
            self.infos = [{'url': course['fullLinkUrl'], 'name': winre.sub('', course['title'])[:WIN_LENGTH]} for course
                          in courses]

    def _download(self):
        print('\n{:^{}s}'.format(self.title, LEN_S))
        self.rootdir = rootDir = os.path.join(PATH, self.title)
        course_dir = os.path.join(rootDir, COURSENAME)
        if not os.path.exists(course_dir):
            os.makedirs(course_dir)
        print(COURSENAME)
        IcourseBase.potplayer.init(rootDir)
        mp4_list = [(info['url'], info['name']) for info in self.infos]
        IcourseBase.potplayer.enable()
        self.download_video_list(course_dir, mp4_list)


def main():
    url = 'http://www.icourses.cn/web/sword/portal/videoDetail?courseId=9fe99900-1327-1000-9191-4876d02411f6#/?resId' \
          '=d0fff67d-1334-1000-8f6b-1d109e90c3cf '
    icourse_cuoc = IcourseCuoc()
    icourse_cuoc.prepare(url)
    icourse_cuoc.download()


if __name__ == '__main__':
    main()
