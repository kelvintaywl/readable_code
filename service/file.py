import os


class File:
    """ Collection of file-related helper functions """
    @staticmethod
    def get_filepaths(dirpath='.'):
        for dpath, dirs, files in os.walk(dirpath):
            for name in files:
                filename = os.path.join(dpath, name)
                yield filename
            if not dirs:
                continue
            else:
                for d in dirs:
                    File.get_filepaths(os.path.join(dpath, d))
