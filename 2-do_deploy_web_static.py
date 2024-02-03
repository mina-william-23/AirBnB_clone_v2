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
        put(archive_path, "/tmp/")

        folder_to_save = "/data/web_static/releases"
        file_name = archive_path.split("/")[-1].split(".")[0]
        server_archive_path = f"/tmp/{file_name}.tgz"
        sudo(f"mkdir -p {folder_to_save}/{file_name}")
        sudo(f"tar -xzf /tmp/{file_name}.tgz "
             f"-C {folder_to_save}/{file_name}")

        sudo(f"rm {server_archive_path}")
        sudo(f"mv {folder_to_save}/{file_name}/web_static/*"
             f" {folder_to_save}/{file_name}/")
        sudo(f"rm -rf {folder_to_save}/{file_name}/web_static")

        try:
            sudo('rm -rf /data/web_static/current')
        except BaseException:
            pass
        sudo(f"ln -s {folder_to_save}/{file_name}"
             f" /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
