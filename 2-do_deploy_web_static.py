#!/usr/bin/python3
""" Fabric module """
from fabric.api import env, put, run, task
import os
env.hosts = ['18.207.112.242', '54.167.84.94']


@task
def do_deploy(archive_path):
    """Distribute an Archive to servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1].split(".")[0]
        put(archive_path, '/tmp/')
        run('mkdir /data/web_static/releases/{}'.format(file_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.
            format(file_name, file_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.
            format(file_name, file_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name))
        run('rm -rf /tmp/{}.tgz'.format(file_name))
        run('rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'.
            format(file_name))
        print("New version deployed!")
        return True
    except Exception as e:
        return False
