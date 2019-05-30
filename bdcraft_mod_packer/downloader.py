import os
import re
import time
from os import path
from sys import platform

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bdcraft_mod_packer.google_drive_downloader import GoogleDriveDownloader as gdd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36'
}

MATCHERS = [r".*file/d/(.*?)/.*", r".*\?id=(.*?)&*"]


def download_html(url: str):
    """
    Download html from url
    :param url:  The url str
    :return: True if download success, False if fail
    """
    print('Downloading html {}...'.format(url))

    r = requests.get(url, headers=HEADERS)
    content_type: str = r.headers['content-type']
    if 'text/html' in content_type:
        return r.text


def download_zip(url: str, zip_output_path='out'):
    """
    Download zip from url
    :param url: The given url of zip file
    :param zip_output_path: The destination dir of the zip goto, without leading /
    :return:
    """

    if len(url) == 0:
        return

    if re.match(r".*drive\.google\.com.*", url):
        file_id = None
        for matcher in MATCHERS:
            file_id_match = re.findall(matcher, url)
            if len(file_id_match) > 0:
                file_id = file_id_match[0]
                break
        if not file_id:
            return
        gdd.download_file_from_google_drive(file_id, os.path.join(zip_output_path, file_id + '.zip'), True)
    else:
        ua = UserAgent()
        header = {'User-Agent': str(ua.random)}
        r = requests.get(url, headers=header, stream=True)

        if r.status_code > 299:
            download_zip(re.sub(r'http://', 'https://', url), zip_output_path)
            return

        content_type: str = r.headers['content-type']

        if 'text/html' in content_type:
            soup = BeautifulSoup(r.text, 'lxml')
            download_zip(soup.find(lambda tag:
                                   tag.name == 'a' and
                                   tag.has_attr('aria-label') and
                                   tag['aria-label'] == 'Download file')['href'], zip_output_path)
            return

        if 'content-disposition' not in r.headers:
            match = {'filename': str(time.time_ns()) + '.zip'}
        else:
            match = re.search(r'filename="(?P<filename>.+)"', r.headers['Content-Disposition'])

        if platform == 'win32':
            # Make it Windows safe, stripping: \/<>:"|?*
            remove_characters = dict((ord(char), None) for char in '\\/<>:"|?*')
        else:
            # Make it macOS and linux safe, stripping: /
            remove_characters = dict((ord(char), None) for char in '/')
        file_name = match['filename'].translate(remove_characters)

        print('Downloading {} into {} ...'.format(file_name, path.join(zip_output_path, file_name)))

        if not path.exists(zip_output_path):
            os.mkdir(zip_output_path)
        create_zip(path.join(zip_output_path, file_name), r.content)


def create_zip(filename: str, content: bytes):
    with open(filename, 'wb') as f:
        f.write(content)
