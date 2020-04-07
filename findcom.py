#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
# findcom.py
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

from readconf import ReadConfig
from comics import Comics_Data
from downcom import Download
import datetime 
import re
import requests
import json


class FindComics:

	def __init__(self, setting_name):
		self.__rc = ReadConfig("settings.conf")
		self.__setting = setting_name
		self.__parameters = self.__rc.read(setting_name)
		
	def __data_parse(self, text):
		
		address = re.findall(self.__parameters["address_match"], text)
		name = re.findall(self.__parameters["name_match"], text)
		if self.__parameters["rating_match"] != 'NONE':
			rating = re.findall(self.__parameters["rating_match"], text)
		else:
			rating = ['NONE' for i in range(len(name))]
		pages = re.findall(self.__parameters["pages_match"], text)
		description = re.findall(self.__parameters["description_match"], text)
			
		return name, address, rating, pages, description
		
	def __make_json(self, text):
		try:
			return json.loads(text)
		except Exception:
			return text 

	def find(self, name):
		skip = int(self.__parameters["start_skip"])
		url = self.__parameters["main_url"] + self.__parameters["skip_message"] % str(skip) if skip > 0 else self.__parameters["main_url"]
		
		while True:
		
			r = Download(url, self.__parameters["request_type"])
			founded = self.__data_parse(r.read_page(self.__make_json(self.__parameters["parameters"])).text)
			
			ind = -1
			for word in founded[0]:
				if word.count(name) > 0:
					ind = founded[0].index(word)
			
			if ind >= 0:
				break
			else:
				skip += int(self.__parameters["skip"])
				url = self.__parameters["main_url"] + self.__parameters["skip_message"] % str(skip)
				
		comics = Comics_Data()
		comics.set_name(founded[0][ind]) 
		comics.set_address(founded[1][ind])
		comics.set_rating(founded[2][ind])
		comics.set_last_link(self.__parameters["start_page"])
		comics.set_status("exists")
		comics.set_pages_number(0)
		cls_date = datetime.datetime.now()
		curr_date = "%s:%s %s/%s/%s" % (cls_date.hour,
										cls_date.minute,
										cls_date.day,
										cls_date.month,
										cls_date.year)
		comics.set_date(curr_date)
		
		return comics
		
	def list(self):
	
		skip = int(self.__parameters["start_skip"])
		
		while True:
			skip_pages = input("Print %s pages? [yYnN]" % self.__parameters["skip"])
			
			if skip_pages in 'yY':
				url = self.__parameters["main_url"] + self.__parameters["skip_message"] % str(skip) if skip > 0 else self.__parameters["main_url"]
				r = Download(url, self.__parameters["request_type"])
				name, address, rating, pages, description = self.__data_parse(r.read_page(self.__make_json(self.__parameters["parameters"])).text)
				
				for n,a,r,p,d in zip(name, address, rating, pages, description):
					if d[0:2] == self.__parameters["ignore_text"]:
						d = ''
					print("""name = %s\naddress = %s\nrating = %s\npages = %s\ndescription = %s\n\n""" % (n,a,r,p,d))
					
				skip += int(self.__parameters["skip"])
				
			elif skip_pages in 'nN':
				break
				
			else:
				print("Incorrect input")
		
if __name__ == '__main__':
	find = FindComics("Settings1")
	print(find.find('Пески Богов'))
	find.list()
