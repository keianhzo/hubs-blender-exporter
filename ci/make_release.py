import sys
from os import path, walk, chdir
from zipfile import ZipFile, ZIP_DEFLATED

CWD = path.dirname(__file__)
SCRIPT_DIR = path.join(path.abspath(path.join(CWD, '..', 'addons')), '')
sys.path.append(SCRIPT_DIR)

from io_hubs_addon import bl_info

chdir(SCRIPT_DIR)

version = '.'.join(map(str, bl_info['version']))

FILE_NAME = 'io_hubs_addon_{}_'.format(
    ('.'.join(map(str, bl_info['version'])))) + '.zip'
with ZipFile(path.join(CWD, FILE_NAME), 'w') as z:
    for root, _, files in walk('io_hubs_addon'):
        for file in files:
            z.write(path.join(root, file), compress_type=ZIP_DEFLATED)

chdir("..")

print(version)
