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

        folder_to_save = "/data/web_static/releases"
        file_name = archive_path.split("/")[-1].split(".")[0]
        server_archive_path = f"/tmp/{file_name}.tgz"

        run("mkdir -p {}/{}".format(folder_to_save, file_name))
        run("tar -xzf /tmp/{}.tgz -C {}/{}".
            format(file_name, folder_to_save, file_name))

        run("rm {}".format(server_archive_path))
        run('mv {}/{}/web_static/* {}/{}/'.
            format(folder_to_save, file_name, folder_to_save, file_name))
        run("rm -rf {}/{}/web_static".format(folder_to_save, file_name))

        try:
            run('rm -rf /data/web_static/current')
        except BaseException:
            pass
        run('ln -sf {}/{} /data/web_static/current'.
            format(folder_to_save, file_name))
        print("New version deployed!")
        return True
    except Exception:
        return False
