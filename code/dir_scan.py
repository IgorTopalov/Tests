"""
Scans all directories below the specified root
For tests
"""
import datetime
import logging
import os
from logging import Logger

logging.basicConfig(format='%(asctime)s - %(levelname)s %(message)s', level=logging.INFO)
log: Logger = logging.getLogger(__name__)

dir_root = r'D:\_From_Archives\_Books_NON-Fiction'
c_subs, c_files, c_size = 0, 0, 0
c_types = dict()
c_syn = {'jpg': 'jpeg', 'htm': 'html', 'xls': 'xlsx', 'doc': 'docx', 'djv': 'djvu', 'ppt': 'pptx'
    , 'jsp': 'web', 'css': 'web', 'js': 'web', 'php': 'web', 'jsonp': 'web', 'jspf': 'web'
    , 'war': 'web'}


def main(dir_scan: str):
    """
    Initiates directories traversing

    :param dir_scan:
    :return:
    """
    if not os.path.exists(os.path.abspath(dir_scan)):
        return 0  # ###

    walk_tree(dir_scan)

    return 1  # ###


def walk_tree(dir_2chk):
    """
    Traverses a specified directory and all sub-directories - recursively

    :param dir_2chk: str
    :return: int
    """
    global c_subs, c_files, c_size, c_types
    c_s, c_f, c_ss, c_sf, c_sb = 0, 0, 0, 0, 0

    for entry in os.scandir(dir_2chk):
        if entry.is_dir():
            c_ss += walk_tree(os.path.join(dir_2chk, entry))
            c_sb += 1
        elif entry.is_file():
            c_sf = os.path.getsize(entry)
            f_ext = os.path.splitext(entry)[1].lstrip('.').lower()
            if '_' in f_ext:
                f_ext = f_ext.split('_')[0]
            if not c_syn.get(f_ext, None) is None:
                f_ext = c_syn.get(f_ext)
            if len(f_ext) > 6 or len(f_ext) == 0:
                f_ext = 'non-comm'
            c_ext = c_types.get(f_ext, 0)
            c_types[f_ext] = c_ext + 1
            c_f += 1
        else:
            log.debug(f'Symbolic link {entry}')

    c_files += c_f
    c_size += c_sf
    c_subs += c_sb

    log.debug('Directory: %s Sub-dirs: %d Files: %d Size: %d', dir_2chk, c_sb, c_f, c_sf + c_ss)

    return c_ss + c_sf  # ##


if __name__ == "__main__":
    ts0 = datetime.datetime.now()
    if main(dir_root) == 0:
        print(f"Invalid directory: {dir_root}")
    else:
        print(f' Root: {dir_root} Sub_dirs: {c_subs}  Files: {c_files} Size: {c_size}')
        print('Statistic', c_types)
    ts1 = datetime.datetime.now()
    elapsed = ts1 - ts0
    print("Elapsed time (Sec.msec): {}.{:3.0f} ".format(elapsed.seconds, elapsed.microseconds / 1000))
