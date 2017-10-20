import io
import logging
import shutil
import tempfile
import zipfile

import requests

from service.code_language import CodeLanguageFactory


class Github:

    API_ENDPOINT_BASE = 'https://api.github.com/repos'
    ENDPOINT_BASE = 'https://github.com'
    API_ENDPOINT_REPO_LANGUAGES = '/'.join([API_ENDPOINT_BASE, '{owner}/{repo}/languages'])
    API_ENDPOINT_SOURCE_ZIP = '/'.join([ENDPOINT_BASE, '{owner}/{repo}', 'archive/master.zip'])

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.code_language = CodeLanguageFactory.create(self.fetch_language())
        self.tmp_folder, self.code_dirpath = self.fetch_source_code()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            shutil.rmtree(self.tmp_folder)
        except Exception as e:
            logging.exception(e)
            pass

    def fetch_language(self):
        url = self.API_ENDPOINT_REPO_LANGUAGES.format(owner=self.owner, repo=self.repo)
        lang_dict = requests.get(url).json()
        if not lang_dict:
            raise ValueError
        # only return main / top language
        langs_by_most_code = sorted(tuple(lang_dict), key=lambda x: -1 * x[1])
        return langs_by_most_code[0]

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
