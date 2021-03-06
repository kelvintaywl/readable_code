import json
from time import time

from redis import (
    ConnectionPool,
    StrictRedis
)


def timestamp():
    return int(time())

SEC = 1
MIN = 60 * SEC
HOUR = 60 * MIN
DAY = 24 * HOUR


class Storage:

    def __init__(self, redis_url):
        pool = ConnectionPool.from_url(redis_url)
        self.store = StrictRedis(connection_pool=pool, decode_responses=True)

    def get(self, source_code_repo, num_top_n_words, last_updated):
        document = self.store.get(source_code_repo)
        if not document:
            raise LookupError

        document = json.loads(document)
        if (int(document.get('num_top_n_words', 0)) >= num_top_n_words)\
                and (int(document.get('last_updated')) >= last_updated):

            return document['words'][:num_top_n_words]

        raise LookupError

    def set(self, source_code_repo, words, num_top_n_words):
        document = {
            'words': words,
            'num_top_n_words': num_top_n_words,
            'last_updated': timestamp()
        }

        self.store.set(source_code_repo, json.dumps(document))
