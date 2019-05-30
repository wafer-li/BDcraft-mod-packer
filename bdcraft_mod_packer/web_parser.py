import re
from typing import *

from bs4 import BeautifulSoup

from bdcraft_mod_packer import downloader


def parse(html: str, mc_version: str = '1.12', resolution='128x') -> List[str]:
    """
    Parse the given HTML str using lxml
    Please notice that you need to install 'lxml' as dependency
    :param resolution: The resolution you need
    :param mc_version: MC Version string, such as '1.12'
    :param html: The HTML str
    :return: The List containing the zip urls
    """

    soup = BeautifulSoup(html, 'lxml')
    remain_page_urls = parse_remain_page_urls(soup)
    current_page_posts_urls = parse_current_page_posts_urls(soup, mc_version)

    for page_url in remain_page_urls:
        page_html = downloader.download_html(page_url)
        print('Parsing page {}'.format(page_url))
        current_page_posts_urls += parse_current_page_posts_urls(BeautifulSoup(page_html, 'lxml'), mc_version)

    result = []
    for post_url in current_page_posts_urls:
        post_html = downloader.download_html(post_url)
        print('Parsing post {}'.format(post_url))
        result += parse_current_post_zip_url(BeautifulSoup(post_html, 'lxml'), mc_version, resolution)

    return result


def parse_current_post_zip_url(soup, mc_version, resolution) -> List[str]:
    return [it['href'] for it in
            sorted(soup.find(lambda tag:
                             tag.has_attr('class') and
                             tag['class'] == ['text-strong'] and
                             mc_version in tag.string
                             ).find_next_sibling(lambda tag:
                                                 tag.has_attr('class') and tag['class'] == ['spoiler']
                                                 )
                   .find_all(lambda tag:
                             tag.name == 'a' and
                             tag.has_attr('href') and
                             len(find_number_in_str_sorted(tag.string)) > 0 and
                             ((resolution in tag.string) or
                              (int(resolution[:-1]) < find_number_in_str_sorted(tag.string)[-1]))
                             ), key=lambda tag: tag.string) if it != '\n'][:1]


def find_number_in_str_sorted(text):
    return sorted([int(it) for it in re.findall(r'(\d+)', text)])


def parse_remain_page_urls(soup) -> List[str]:
    li_with_active = [it for it in
                      soup.find(lambda tag:
                                tag.name == 'div' and tag.has_attr('class') and
                                tag['class'] == ['pagination']).ul.children
                      if (it != '\n') and ((it.has_attr('class') and it['class'] == ['active']) or
                                           (not it.has_attr('class') and it.find('a')))]
    index = 0
    for i, j in enumerate(li_with_active):
        if j.has_attr('class'):
            index = i
    return [it.a['href'] for it in li_with_active[index + 1:]]


def parse_current_page_posts_urls(soup: BeautifulSoup, mc_version: str) -> List[str]:
    """
    Get all the post with given mc version in the current page
    :param soup: BeautifulSoup Object
    :param mc_version: MC Version string, such as '1.12'
    :return:
    """
    mc_version = check_mc_version(mc_version)
    return [it.a['href'] for it in soup.find_all(lambda tag:
                                                 tag.name == 'div' and
                                                 tag.has_attr('class') and
                                                 tag['class'] == ['row'])
            if mc_version in it.find('div', {'class', 'topic-title'}).string]


def check_mc_version(mc_version: str):
    if re.match(r"[1]\.\d{1,2}", mc_version):
        return mc_version
    else:
        return '1.12'
