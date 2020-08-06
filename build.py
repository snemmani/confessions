#!/usr/bin/python

import sys
import os
import shutil
from pynt import task

client_dir_name = 'confessions-client'
rest_dir_name = 'confessions-rest'
root_dir = os.path.abspath(os.path.dirname(__file__))
client_dir = os.path.join(root_dir, client_dir_name)
rest_dir = os.path.join(root_dir, rest_dir_name)


def system_command(command):
    returncode = os.system(' '.join(command))
    if returncode:
        raise Exception()

@task()
def build_client():
    """Build the client code"""
    os.chdir(client_dir)
    command = [
        'ng', 'build', '--prod', '--output-path', os.path.join(rest_dir, 'static', 'ang'), '--output-hashing', 'none'
    ]
    system_command(command)


@task()
def clean():
    """Clean the client node_modules installation"""
    os.chdir(client_dir)
    node_modules = os.path.join(client_dir, 'node_modules')
    if os.path.isdir(node_modules):
        shutil.rmtree(node_modules)


@task()
def _install():
    """Install node dependencies"""
    os.chdir(client_dir)
    command = ['npm', 'install']
    system_command(command)


@task(clean, _install)
def clean_install():
    """Clean install node modules"""
    pass


@task()
def run_client():
    """Run client service"""
    os.chdir(client_dir)
    command = ['ng', 'serve']
    system_command(command)


@task()
def run_rest_service():
    """Run rest service"""
    os.chdir(rest_dir)
    command = [sys.executable, 'manage.py', 'runserver']
    system_command(command)


@task(clean_install, build_client, run_rest_service)
def run():
    """Run the application"""
    pass
