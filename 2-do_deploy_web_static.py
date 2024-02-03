#!/usr/bin/python3
""" Fabric module """
from fabric.api import env, put, task, sudo, run
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
        put(archive_path, "/tmp/")

        folder = "/data/web_static/releases"
        file = archive_path.split("/")[-1].split(".")[0]

        run("mkdir -p {}/{}".format(folder, file))
        run("tar -xzf /tmp/{}.tgz -C {}/{}"
            format(file, folder, file))
        run('rm -rf /tmp/{}.tgz'.format(file))
        run('mv {}/{}/web_static/* {}/{}/'.
            format(folder, file, folder, file))
        run("rm -rf {}/{}/web_static".format(folder, file))

        run('rm -rf /data/web_static/current')

        run('ln -sf {}/{} /data/web_static/current'.sformat(folder, file))
        print("New version deployed!")
        return True
    except Exception:
        return False
