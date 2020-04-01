"""
Scans and makes a copy of the quite simple web-site layout
For tests and improvements
GIT rules!
"""
import datetime
import logging
import os
import re
import shutil
import sys

import requests
from bs4 import BeautifulSoup

from itutl import itu_properties

PRJ_PROP = itu_properties.get_properties(r'D:\DEV\Python\_CONFIG', 'projects.properties')
logging.basicConfig(format='%(asctime)s - %(levelname)s %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# define file handler and formatter
log_file = logging.getLogger('file')
file_handler = logging.FileHandler(os.path.join(PRJ_PROP.get('dir_log'), 'log-web.log'))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
log_file.addHandler(file_handler)

chk_4htm = re.compile(r'.htm|.HTM')

url_2chk = "http://vivovoco.ibmh.msk.su/VV/"
b_skip = True
url_thr = "/VV/WALK/"
cnt_subs, cnt_files_t, cnt_files_b, cnt_size = 0, 0, 0, 0


def reset_data_dir():
    global PRJ_PROP
    data_root = PRJ_PROP.get('dir_data_out', None)

    if data_root is None:
        raise ValueError("Data root is not defined in the project's properties")

    data_root = os.path.abspath(data_root)

    dir_data = os.path.join(data_root, 'site-get')

    if os.path.exists(dir_data):
        try:
            log.debug("Purging directory %s", dir_data)
            shutil.rmtree(dir_data)
        except OSError as e:
            log.debug("Failed purge %s due to %s", dir_data, e.strerror)

    os.mkdir(dir_data)
    log.debug("Created directory %s", dir_data)

    return  # ##


# noinspection PyBroadException
def walk_tree(url_2scan, dir_data):
    page_full = requests.get(url_2scan)
    page_html = page_full.content

    global b_skip

    log.debug("Root: %s Page: ", url_2scan, page_html)

    if not os.path.exists(dir_data):
        os.mkdir(dir_data)
        log.debug("Directory %s create", dir_data)

    log.debug("Encoding:  %s  Apparent %s ", page_full.encoding, page_full.apparent_encoding)

    soup = BeautifulSoup(page_html, "html.parser")
    file_abs_path = ''

    c_subs, c_ft, c_fb, c_size = 0, 0, 0, 0

    for href_link in soup.findAll('a', href=True):
        attr_link = href_link['href']
        attr_text = href_link.text
        if attr_link != attr_text: continue  # =>>
        url_source = url_2scan + attr_link

        if b_skip and url_thr not in url_source:
            log.debug("Skipped %s", url_source)
            continue  # =>>
        else:
            b_skip = False

        # log.debug("Link %s text %s ", attr_link, attr_text)
        if attr_text.endswith("/"):
            c_subs += 1
            log.debug("Sub-dir: %s", attr_link)
            walk_tree(url_source, os.path.join(dir_data, attr_link.rstrip('/')))
        else:
            # Process files here
            try:
                file_abs_path = os.path.join(dir_data, attr_text)
                file_web = requests.get(url_source, timeout=10, allow_redirects=True)
                if chk_4htm.search(attr_text):
                    log.debug("Source: %s TextFile: %s", url_source, file_abs_path)
                    c_ft += 1
                    file_text = file_web.content.decode(file_web.encoding, errors="ignore")
                    with open(file_abs_path, 'w', encoding=file_web.encoding) as file:
                        file.write(file_text)
                else:
                    log.debug("Source: %s BinaryFile: %s", url_source, file_abs_path)
                    c_fb += 1
                    with open(file_abs_path, 'wb') as file:
                        file.write(file_web.content)
            except:
                log.critical("Failed retrieve: %s due to: %s ", file_abs_path, sys.exc_info()[0])

    return  # ##


def main(url_2chk):
    dir_data = reset_data_dir()
    log_file.info('Site will be retrieved into: %s', dir_data)

    # walk_tree(url_2chk, dir_data)

    return  # ##


if __name__ == "__main__":
    ts0 = datetime.datetime.now()
    main(url_2chk)
    ts1 = datetime.datetime.now()
    elapsed = ts1 - ts0
    print("Elapsed time (Sec.msec): {}.{:3.0f} ".format(elapsed.seconds, elapsed.microseconds / 1000))
