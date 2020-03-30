#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from downcom import Download 
from readconf import ReadConfig
from comdb import DB_Comics
import re
import os
import datetime
from shutil import rmtree

class MK_Model:
	
	def __init__(self, setting):
	
		self.__images = {}
		conf = ReadConfig("settings.conf")
		self.__conf = conf.read(setting)
		
	def find_images(self, address, data='', header='', last_link=''):
	
		links = ['']
		page = Download(address, self.__conf["request_type"])
		read = page.read_page(header, data)
		if read.text.count(self.__conf["error"]) > 0:
			print("My program : Only try to realyze the truth.\nYou : What truth?\nMy program : There is no comics...")
			return None	
		elif read.status_code != 200:
			print("YOU! SHALL NOT! PASSED!! HTTP status code : %s" % read.status_code)
			return None
			
		links.extend(re.findall(self.__conf["links_match"], read.text))	
		for i in range(links.index(last_link)+1, len(self.__links)-1):
			chapter = Download(links[i], self.__conf["request_type"])
			chread = chapter.read_page(header, data)
			self.__images[links[i].split('/')[-1]] = re.findall(self.__conf["image_match"], read.text)
			
				
	def get_image_list(self):
		return self.__images
			
	
	def clean_image_list(self):
		self.__images= {}
		
	def download_images(self, name, num, data='', header=''):
		
		if not os.path.exists(name):
			os.mkdir(name)
		os.chdir(name)
		
		for key in self.__images.keys():
			os.mkdir(key)
			os.chdir(key)
			for link in self.__images[key]:
				image_name = link.split('/')[-1]
				page = Download(self.__conf['pic_address'] + link, self.__conf["request_type"])
				read = page.read_page(header, data)
				with open(image_name, 'wb') as wt:
					wt.write(read.content)
			os.chdir('../')	
		
		pages_number = int(num) + len(self.__image) - 1 if num > 0 else len(self.__image)
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
									 self.__images[-1], 
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
						page = Download(self.__conf['pic_address'] + link, self.__conf["request_type"])
						read = page.read_page(header, data)
						with open(image_name, 'wb') as wt:
							wt.write(read.content)
							
			removing_chapters = []
			chapters_copy = sorted(list(self.__image.keys()))
			while len(chapters_list) > 0:
				if chapters_copy[0].count(chapters_list[0]) > 0:
					chapters_list.pop(0)
					chapters_copy.pop(0)
				else:
					removing_chapters.append(chapters_list[0])
					chapters_list.pop(0)
			
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
										 self.__images[-1], 
										 "exists")
				
		os.chdir('../')
