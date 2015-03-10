import pyudev, os, re

def get_mtab_path():
    """stub: get the path of mtab file.

    :returns: path of mtab file.
    :rtype: 

    """
    return r'/etc/mtab'

def get_mtab_entries():
    """parse the whole mtab

    :returns: a dict of mounted devices, uses mount point as key
    :rtype: dict

    """
    path = get_mtab_path()
    if not os.access(path, os.R_OK):
        return None

    dict = {}
    with open(path) as f:
        for line in f:
            pair = parse_mtab_entry(line)
            dict[pair[1]] = pair[0]

    return dict

def parse_mtab_entry(line):
    patten = re.compile('\s')
    li = patten.split(line.strip())
    if len(li) > 1:
        return li[0], li[1]
    
