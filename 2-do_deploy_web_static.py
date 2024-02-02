#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the"""
from fabric.api import sudo, env, put, local, task
from datetime import datetime


@task
def do_pack():
    """Function To Compress File Using tar"""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_to_save = "versions"
        local("mkdir -p {}".fromat(folder_to_save))
        file_name_generated = "web_static_{}.tgz".format(current_time)
        local("tar -cvzf {}/{} web_static".
              fromat(folder_to_save, file_name_generated))
        return "{}/{}".fromat(folder_to_save, file_name_generated)
    except Exception:
        return None


@task
def get_ip_address(domain):
    """Function To Get IP Address"""
    import socket
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return False


env.hosts = [get_ip_address("web-01.minawilliam.tech"),
             get_ip_address("web-02.minawilliam.tech")]

# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/alx_server1'


@task
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
