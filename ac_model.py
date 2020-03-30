#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from downcom import Download 
from readconf import ReadConfig
from comdb import DB_Comics
import re
import os
import datetime

class AC_Model:
	
	def __init__(self, setting):
		self.__image = []
		self.__setting = setting
		conf = ReadConfig("settings.conf")
		self.__conf = conf.read(setting)
		self.__db = DB_Comics()
		self.__last_link = ''
		
	def find_images(self, comics_address, data='', header='', last_link=''):
	
		address = "/".join((comics_address, last_link))
		page = Download(address, self.__conf["request_type"])
		read = page.read_page(header, data)
		if read.text.count(self.__conf["error"]) > 0:
			print("My program : Only try to realyze the truth.\nYou : What truth?\nMy program : There is no comics...")
			self.__db.update_status(self.__setting, comics_address, 'deleted')
			return None
		
		while True:
			page = Download(address, self.__conf["request_type"])
			read = page.read_page(header, data)
				
			if read.status_code != 200:
				print("YOU! SHALL NOT! PASSED!! HTTP status code : %s" % read.status_code)
				self.__image = []
				return None
			self.__image.append(re.findall(self.__conf["image_match"], read.text)[0])
			self.__last_link = address.split('/')[-1]
			try:
				address = re.findall(self.__conf["next_match"] , read.text)[0]
				#print(address)
			except IndexError:
				break
				
		return True
				
	def get_image_list(self):
		return self.__image
		
	def clean_image_list(self):
		self.__image = []
		
	def download_images(self, name, num, data='', header=''):
		
		if not os.path.exists(name):
			os.mkdir(name)
		os.chdir(name)
		
		for link in self.__image:
			image_name = link.split('/')[-1]
			page = Download(self.__conf['pic_address'] + link, self.__conf["request_type"])
			read = page.read_page(header, data)
			with open(image_name, 'wb') as wt:
				wt.write(read.content)
		
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
									 self.__last_link, 
									 "exists")
				
		os.chdir('../')
		
	def rescan(self, name, num, address, data='', header=''):
		
		os.chdir(name)
		if self.find_images(address, data, header, self.__conf['start_page']) is not None:
			images_list = sorted(os.listdir('./'))
			for link in self.__image:
				image_name = link.split('/')[-1]
				if images_list.count(image_name) == 0:
					images_list.append(image_name)
					images_list.sort()
					page = Download(self.__conf['pic_address'] + link, self.__conf["request_type"])
					read = page.read_page(header, data)
					with open(image_name, 'wb') as wt:
						wt.write(read.content)
						
			removing_images = []
			image_copy = sorted(self.__image.copy())
			while len(images_list) > 0:
				if image_copy[0].count(images_list[0]) > 0:
					images_list.pop(0)
					image_copy.pop(0)
				else:
					removing_images.append(images_list[0])
					images_list.pop(0)
			
			for image in removing_images:
				os.remove(image)
				
			cls_date = datetime.datetime.now()
			curr_date = "%s:%s %s/%s/%s" % (cls_date.hour,
											cls_date.minute,
											cls_date.day,
											cls_date.month,
											cls_date.year)
			self.__db.update_comics_info(self.__setting,
										 name, 
										 len(self.__image), 
										 curr_date, 
										 self.__last_link, 
										 "exists")
				
		os.chdir('../')
		
if __name__ == '__main__':
	a = AC_Model("Settings1")
	if a.find_images("https://acomics.ru/~iddqd/1") is not None:
		print(a.get_image_list())
