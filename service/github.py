import calendar
from datetime import datetime
import io
import logging
import shutil
import tempfile
from time import time
import zipfile

import requests

from service.code_language import CodeLanguageFactory


class RepoInfo:

    API_ENDPOINT_BASE = 'https://api.github.com/repos'
    API_ENDPOINT_REPO_INFO = '/'.join([API_ENDPOINT_BASE, '{owner}/{repo}'])

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.code_language, self.last_updated = self.get_repo_info()

    def get_repo_info(self):
        url = self.API_ENDPOINT_REPO_INFO.format(owner=self.owner, repo=self.repo)
        resp = requests.get(url).json()
        if not resp:
            raise ValueError

        code_language = CodeLanguageFactory.create(resp['language'].lower())
        try:
            last_updated_str = max(resp['pushed_at'], resp['updated_at'])
            last_updated = calendar.timegm(
                datetime.strptime(last_updated_str, '%Y-%m-%dT%H:%M:%SZ').timetuple()
            )

        except (KeyError, ValueError):
            last_updated = int(time())

        return code_language, last_updated


class SourceCode:

    ENDPOINT_BASE = 'https://github.com'
    API_ENDPOINT_SOURCE_ZIP = '/'.join([ENDPOINT_BASE, '{owner}/{repo}', 'archive/master.zip'])

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.tmp_folder, self.code_dirpath = self.fetch_source_code()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            shutil.rmtree(self.tmp_folder)
        except Exception as e:
            logging.exception(e)
            pass

    def fetch_source_code(self):
        url = self.API_ENDPOINT_SOURCE_ZIP.format(owner=self.owner, repo=self.repo)
        resp = requests.get(url, stream=True)
        if not resp.ok:
            raise ValueError

        zfile = zipfile.ZipFile(io.BytesIO(resp.content), mode='r')
        tmp_dir_name = tempfile.mkdtemp()

        zfile.extractall(tmp_dir_name)

        return (
            tmp_dir_name,
            '{tmp_folder}/{repo_name}-master'.format(tmp_folder=tmp_dir_name, repo_name=self.repo)
        )
