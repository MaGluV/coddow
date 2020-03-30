#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2020 max <max@max-HP-Notebook>
# 
# acrylic is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# acrylic is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from readconf import ReadConfig
from comics import Comics_Data
from comdb import DB_Comics
from findcom import FindComics
from ac_model import AC_Model
from mk_model import MK_Model
import requests
import os
import glob
import shutil
import time
import shutil

class Acrylic:
	
	def __init__(self):
		self.__db = DB_Comics()
	
	def start(self):
		
		general_conf = ReadConfig("general_settings.conf")
		general = general_conf.read("General_Settings")
		models = {'ac' : AC_Model, 'mk' : MK_Model}
		os.chdir(general["comics_main_dir"])
		read_conf = ReadConfig("settings.conf")
		settings = read_conf.settings()
			
		while True:
			for config in settings:
				print(config)

				self.__db.db_create(config)	
				search = FindComics(config)
				config_data = read_conf.read(config)
				print("Current site : %s" % config_data["main_url"])

				scan = input("Scan data?[yYnN]")
				if scan in 'yY':
					search.list()
				elif not scan in 'yYnN':
					print("Incorrect Input")
				
				add = input("Add comics?[yYnN]")
				if add in 'yY':
					names = input("Input names[name1|name2...]: ")
					name_list = names.split('|') if names.count('|') > 0 else [names] 
					for name in name_list:
						add_data = search.find(name)
						self.__db.add_comics(config, add_data)
						if not os.path.exists(add_data.get_name()):
							os.mkdir(add_data.get_name())
				elif not add in 'yYnN':
					print("Incorrect Input")
				
				delete = input("Delete comics?[yYnN]")
				if delete in 'yY':
					name = input("Input names[name1|name2...]: ")
					name_list = names.split('|') if names.count('|') > 0 else [names] 
					for name in name_list:
						del_data = self.__db.get_sorted_by_date(config)
						del_func = lambda name: lambda x: name in x[1]
						deleted = list(filter(del_func(name), del_data))
						if len(deleted[0][1]) > 0: 
							self.__db.delete_by_name(config, deleted[0][1])
							try:	
								shutil.rmtree(deleted[0][1])
							except Exception as e:
								print("Error : %s" % e)
						else:
							print("Not found")
				elif not delete in 'yYnN':
					print("Incorrect Input")
					
				update = input("Update comics?[yYnN]")
				if update in 'yY':
					comics_data_list = self.__db.get_not_deleted(config)
					model = models[config_data["model"]](config)
					for comics_data in comics_data_list:
						model.find_images(comics_data[2], 
										  config_data["access_data"], 
										  config_data["access_params"], 
										  comics_data[5])
						print(model.get_image_list())
						model.download_images(comics_data[1], 
											  comics_data[4],
											  config_data["access_data"], 
											  config_data["access_params"])
						model.clean_image_list()
				
				elif not update in 'yYnN':
					print("Incorrect Input")
						
				rescan = input("Rescan comics[yYnN]?")
				if rescan in 'yY':
					comics_data_list = self.__db.get_not_deleted(config)
					name_from_db = [data[1] for data in comics_data_list]
					print(name_from_db)
					model = models[config_data["model"]](config)
					names = input("Comics names[name1|name2...]:")
					name_list = names.split('|') if names.count('|') > 0 else [names] 
					try:
						for name in name_list:
							print(name)
							comics_data = comics_data_list[name_from_db.index(name)]
							model.rescan(comics_data[1], 
										 comics_data[4],
										 comics_data[2], 
										 config_data["access_data"], 
										 config_data["access_params"])
							print(model.get_image_list())
							model.clean_image_list()
					except Exception as e:
						print("Incorrect input! Error - %s" % e)
						
				elif not rescan in 'yYnN':
					print("Incorrect Input")		
					
				stop = input("Exit?[yYnN]:")
				if stop in 'yY':
					exit(0)
				elif not stop in 'yYnN':
					print("Incorrect Input")
				
if __name__ == '__main__':
	acr = Acrylic()
	acr.start()
