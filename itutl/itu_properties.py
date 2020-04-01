"""
Properties Handler
"""

import logging
import os

log = logging.getLogger(__name__)


def get_properties(dir_root, file_prop):
    file_prop_full = None

    if not file_prop is None and dir_root is None:
        file_prop_full = file_prop
        dir_root = os.path.split(file_prop_full)[0]
        file_prop = os.path.split(file_prop_full)[1]

    if dir_root is None or file_prop is None:
        raise ValueError("Dir_Root and/or properties file are empty")  # !!

    dir_root = os.path.abspath(dir_root)

    if file_prop_full is None:
        file_prop_full = os.path.join(dir_root, file_prop)

    if not os.path.exists(file_prop_full):
        raise OSError(f"File {file_prop_full} doe not exists")  # !!

    log.debug("Retrieving properties from %s ", file_prop_full)
    with open(file_prop_full, "r") as file:
        propFile = file.readlines()
        propDict = dict()
        for propLine in propFile:
            propDef = propLine.strip()
            if len(propDef) == 0:
                continue  # =>>
            if propDef[0] in ('!', '#'):
                continue  # =>>
            punctuation = [propDef.find(c) for c in ':= '] + [len(propDef)]
            found = min([pos for pos in punctuation if pos != -1])
            name = propDef[:found].rstrip()
            value = propDef[found:].lstrip(":= ").rstrip()
            propDict[name] = value

    return propDict  # ###


if __name__ == '__main__':
    prop = get_properties(r'D:\DEV\Python\_CONFIG', 'projects.properties')
    print(prop)
