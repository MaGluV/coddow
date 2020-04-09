#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 

# comdb.py
#
# Copyright (C) 2020 - max
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from services.downcom import Download 
from services.readconf import ReadConfig
from services.comdb import DB_Comics
import re
import os
import datetime
from shutil import rmtree

class MK_Model:
	
	def __init__(self, setting):
	
		self.__images = {}
		self.__setting = setting
		conf = ReadConfig("settings.conf")
		self.__conf = conf.read(setting)
		self.__db = DB_Comics()
		self.__last_link = ''
		
	def find_images(self, address, data='', header='', last_link=''):
	
		links = []
		page = Download(address, self.__conf["image_request_type"])
		read = page.read_page(header, data)
		if read.text.count(self.__conf["error"]) > 0:
			print("My program : Only try to realyze the truth.\nYou : What truth?\nMy program : There is no comics...")
			return None	
		elif read.status_code != 200:
			print("YOU! SHALL NOT! PASSED!! HTTP status code : %s" % read.status_code)
			return None
			
		links.extend(re.findall(self.__conf["links_match"], read.text))	
		self.__last_link = links[0] 
		index = links.index(last_link) if last_link != '' else len(links) 
		for i in range(0, index):
			chapter = Download(links[i], self.__conf["image_request_type"])
			chread = chapter.read_page(header, data)
			self.__images[links[i].split('/')[-1]] = re.findall(self.__conf["image_match"], chread.text)
		return True
			
				
	def get_image_list(self):
		images_list = [[chapter, len(self.__images[chapter])] for chapter in sorted(self.__images)]
		return images_list
			
	
	def clean_image_list(self):
		self.__images= {}
		self.__last_link = ''
		
	def download_images(self, name, num, data='', header=''):
		
		if not os.path.exists(name):
			os.mkdir(name)
		os.chdir(name)
		
		for key in list(self.__images.keys()):
			os.mkdir(key)
			os.chdir(key)
			for link in self.__images[key]:
				image_name = link.split('/')[-1]
				page = Download(self.__conf['pic_address'] + link, self.__conf["image_request_type"])
				read = page.read_page(header, data)
				with open(image_name, 'wb') as wt:
					wt.write(read.content)
			os.chdir('../')	
		
		pages_number = int(num) + len(self.__images) if num > 0 else len(self.__images)
		cls_date = datetime.datetime.now()
		curr_date = "%s:%s %s/%s/%s" % (cls_date.hour,
										cls_date.minute,
										cls_date.day,
										cls_date.month,
										cls_date.year)
		self.__db.update_comics_info(self.__setting,
									 name, 
									 pages_number, 
									 curr_date, 
									 self.__last_link, 
									 "exists")
				
		os.chdir('../')
		
	def rescan(self, name, num, address, data='', header=''):
		
		os.chdir(name)
		if self.find_images(address, data, header, self.__conf['start_page']) is not None:
			chapters_list = sorted(os.listdir('./'))
			for key in self.__images.keys():
				if chapters_list.count(key) == 0:
					os.mkdir(key)
					os.chdir(key)
					chapters_list.append(key)
					chapters_list.sort()
					for image in self.__images[key]:
						image_name = image.split('/')[-1]
						page = Download(self.__conf['pic_address'] + image, self.__conf["image_request_type"])
						read = page.read_page(header, data)
						with open(image_name, 'wb') as wt:
							wt.write(read.content)
					os.chdir('../')
							
			removing_chapters = []
			chapters_copy = sorted(list(self.__images.keys()))
			while len(chapters_list) > 0:
				if len(chapters_copy) == 0:
					removing_chapters.extend(chapters_list)
					chapters_list.clear()
					break
				if chapters_copy[0].count(chapters_list[0]) > 0 :
					chapters_list.pop(0)
					chapters_copy.pop(0)
				else:
					removing_chapters.append(chapters_list[0])
					chapters_list.pop(0)
			
			print("Removed_chapters =", removing_chapters)
			for chapter in removing_chapters:
				rmtree(chapter)
		
			cls_date = datetime.datetime.now()
			curr_date = "%s:%s %s/%s/%s" % (cls_date.hour,
											cls_date.minute,
											cls_date.day,
											cls_date.month,
											cls_date.year)
			self.__db.update_comics_info(self.__setting,
										 name, 
										 len(self.__images), 
										 curr_date, 
										 self.__last_link, 
										 "exists")
		else:
			print("Something wrong...")
				
		os.chdir('../')
