#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the"""
# from fabric.api import sudo, env, put, local, task
from fabric.api import *
from fabric.operations import put, sudo


env.hosts = ['18.207.112.242', '54.167.84.94']


def do_deploy(archive_path):
    """Function To Deploy File"""
    """
    fab -f 2-do_deploy_web_static.py
    do_deploy:archive_path=versions/web_static_20231009012456.tgz
    -i ./alx -u root
    """
    import os
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")

        folder_to_save = "/data/web_static/releases"
        file_name_generated = archive_path.split(".")[0]
        file_name_generated = file_name_generated.split("/")[-1]

        server_archive_path = "/tmp/{}.tgz".format(file_name_generated)
        sudo("mkdir -p {}/{}")
        sudo("tar -xzf /tmp/{}.tgz -C {}/{}".
             format(file_name_generated, folder_to_save, file_name_generated))

        sudo("rm {}".format(server_archive_path))
        sudo("mv {}/{}/web_static/* {}/{}/".
             format(folder_to_save, file_name_generated,
                    folder_to_save, file_name_generated))
        sudo("rm -rf {}/{}/web_static".
             format(folder_to_save, file_name_generated))

        try:
            sudo('rm -rf /data/web_static/current')
        except BaseException:
            pass
        sudo("ln -s {}/{} /data/web_static/current".
             format(folder_to_save, file_name_generated))
        print("New version deployed!")
        return True
    except Exception:
        return False
