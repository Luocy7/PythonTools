"""
    定义一个爱课程 Icourse 的虚基类
    用于派生 IcourseCuoc 和 IcourseMooc
"""

from abc import abstractmethod

from Mooc.Mooc_Config import *
from Mooc.MoocBase import *
from Mooc.MoocPotplayer import *

__all__ = [
    "IcourseBase"
]


class IcourseBase(MoocBase):
    potplayer = MoocPotplayer()

    def __init__(self):
        super().__init__()
        self.__infos = []
        self.__cid = None

    def prepare(self, url):
        getattr(self, "_get_cid")(url)
        getattr(self, "_get_title")()
        getattr(self, "_get_infos")()

    def download(self):
        if self.cid and self.title and self.infos:
            getattr(self, "_download")()
            return True
        return False

    @property
    def cid(self):
        return self.__cid

    @cid.setter
    def cid(self, cid):
        self.__cid = cid

    @abstractmethod
    def _get_cid(self, url):
        pass

    def set_mode(self):
        return True

    @classmethod
    @potplayer
    def download_video(cls, video_url, video_name, video_dir):
        return super().download_video(video_url, video_name, video_dir)

    @classmethod
    def download_video_list(cls, dirpath, mp4list, prefix=''):
        for cnt, videos in enumerate(mp4list, 1):
            mp4_url, mp4_name = videos
            mp4_name = winre.sub('', '[' + prefix + str(cnt) + ']--' + mp4_name).rstrip('.mp4')[:WIN_LENGTH]
            cls.download_video(video_url=mp4_url, video_name=mp4_name, video_dir=dirpath)

    @classmethod
    def download_pdf_list(cls, dirpath, pdflist, prefix=''):
        for cnt, pdfs in enumerate(pdflist, 1):
            pdf_url, pdf_name = pdfs
            pdf_name = winre.sub('', '(' + prefix + str(cnt) + ')--' + pdf_name).rstrip('.pdf')[:WIN_LENGTH]
            cls.download_pdf(pdf_url, pdf_name, dirpath)
