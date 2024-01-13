import os
import time
import urllib

from requests import Response

import util
from baidu import Baidu
from util import logger


def generate_archive_md(searches):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = item['url']
        return '1. [{}]({})'.format(word, url)
    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)

    return readme


def generate_readme(searches):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = item['url']
        return '1. [{}]({})'.format(word, url)
    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)


    return readme


def save_readme(md):
    logger.info('today md:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.info('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def save_raw_response(resp: Response, filename: str):
    """保存原始响应内容
    """
    if resp:
        content = resp.text
        filename = '{}.json'.format(filename)
        logger.info('save response:%s', filename)
        date = util.current_date()
        file = os.path.join('raw', date, filename)
        util.write_text(file, content)



def run():
    # 获取数据
    # 热搜
    searches, resp = Baidu.get_hot_search()
    save_raw_response(resp, 'hot-search')
    time.sleep(1)

    # 最新数据
    todayMd = generate_readme(searches)
    save_readme(todayMd)
    # 归档
    archiveMd = generate_archive_md(searches)
    save_archive_md(archiveMd)


if __name__ == "__main__":
    try:
        run()
    except:
        logger.exception('run failed')