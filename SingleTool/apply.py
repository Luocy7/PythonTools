import SingleTool.Spoken_word2number as Swn

from pathlib import Path


def file_spoken_word2number():
    sw = Swn.spoken_word_to_number
    path = Path('D:\\Download\\Python-Offer-master\\Python-Offer-master')

    filelist = path.glob('*.py')
    file_suffix = '.py'

    for file in filelist:
        filename = file.stem
        _ = sw(filename)

        if isinstance(_, int):
            _ = str(_).zfill(2)
        newname = str(_) + file_suffix
        newfile = path / newname

        print(file, newfile)
        file.rename(newfile)


if __name__ == '__main__':
    file_spoken_word2number()
