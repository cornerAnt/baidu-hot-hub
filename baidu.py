import contextlib
import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from util import logger

HOT_SEARCH_URL = 'https://top.baidu.com/api/board'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}
QUERIES = {
    'platform': 'web',
    'tab': 'realtime',
    'tag': '%7B%7D'
}
RETRIES = Retry(total=3,
                backoff_factor=1,
                status_forcelist=[k for k in range(400, 600)])


@contextlib.contextmanager
def request_session():
    session = requests.session()
    try:
        session.headers.update(HEADERS)
        session.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield session
    finally:
        session.close()


class Baidu:

    @staticmethod
    def get_hot_search():
        try:
            with request_session() as session:
                response = session.get(HOT_SEARCH_URL, params=QUERIES)
                raw_data = json.loads(response.text)
                word_list = raw_data['data']['cards'][0]['content']
                items = [item for item in word_list]
                return (items, response)
        except:
            logger.exception('get hot search failed')
            return None


if __name__ == "__main__":

    items, text = Baidu.get_hot_search()
    for item in items:
        logger.info('item:%s', item)
