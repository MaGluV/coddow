#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from subprocess import Popen,PIPE
import shutil
import getpass
import os
from configparser import RawConfigParser as RCP

try:
	shutil.copy('coddow_run', '/usr/bin')
except Exception:
	os.remove('/usr/bin/coddow_run')
	shutil.copy('coddow_run', '/usr/bin')
ps = Popen('chmod -u=rwx /usr/bin/coddow_run', stdout=PIPE, stderr=PIPE, shell=True)
ps.communicate()
settings_path = os.getenv("HOME") + '/.local/share/coddow'
comics_data_path = os.getenv("HOME") + '/comics'

if not os.path.exists(settings_path):
	os.mkdir(settings_path)
	os.mkdir(settings_path + '/db')
	shutil.copytree('coddow/settings', settings_path + '/settings')
	cmd = 'chmod -R 777 %s' % settings_path
	ps = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	ps.communicate()
	config = RCP()
	config.read(settings_path + '/settings/general_settings.conf')
	config['General_Settings']['comics_main_dir'] = comics_data_path
	with open(settings_path + '/settings/general_settings.conf', 'w') as configfile:
		config.write(configfile)
	print("""Current directory for comic files storage is %s.
You can change default directory path in %s""" % (comics_data_path, settings_path+'general_settings.conf'))

setup(
    name='coddow',
    version="0.0.1",
    description="Program for parsing sites and downloading comics",
    author="Agent_K",
    author_email="sh345sqrt@gmail.com",
    maintainer='Agent_K',
    maintainer_email='sh345sqrt@gmail.com',
    url="https://MaximGlushkov93@bitbucket.org/polovincev/sensor-bluetooth-j2.git",
    packages=['coddow', 'coddow/models', 'coddow/services'],
    #package_data={'': ['*.sh'],},
)
