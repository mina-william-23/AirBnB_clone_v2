#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the"""
from fabric.api import sudo, env, put, local, task
from datetime import datetime
import os
env.hosts = ['18.207.112.242', '54.167.84.94']


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


@task
def do_deploy(archive_path):
    """Function To Deploy File"""
    """
    fab -f 2-do_deploy_web_static.py
    do_deploy:archive_path=versions/web_static_20231009012456.tgz
    -i ./alx -u root
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1].split(".")[0]
        put(archive_path, '/tmp/')
        sudo('mkdir -p /data/web_static/releases/{}'.format(file_name))
        sudo('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.
             format(file_name, file_name))
        sudo('mv /data/web_static/releases/{}/web_static/* \
             /data/web_static/releases/{}/'.
             format(file_name, file_name))
        sudo('rm -rf /data/web_static/releases/{}/web_static'.
             format(file_name))
        sudo('rm -rf /tmp/{}.tgz'.format(file_name))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -sf /data/web_static/releases/{}/ /data/web_static/current'.
             format(file_name))
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    """full deployment"""
    try:
        path = do_pack()
        if path is None:
            return False
        return do_deploy(path)
    except Exception:
        return False
