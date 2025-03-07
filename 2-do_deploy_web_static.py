#!/usr/bin/python3
""" Fabric module """
from fabric.api import env, put, task, sudo
import os
env.hosts = ['18.207.112.242', '54.167.84.94']


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
