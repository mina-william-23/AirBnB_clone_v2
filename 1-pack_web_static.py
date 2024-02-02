#!/usr/bin/python3
'''Fabric script that generates a .tgz archive'''
from datetime import datetime
from fabric.api import local
from fabric import task


@task
def do_pack():
    '''Function that converts a .tgz archive'''

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    try:
        # compress the file in path to web_static
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except Exception as e:
        return None
