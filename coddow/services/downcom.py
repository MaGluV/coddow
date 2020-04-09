#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
# downcom.py
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

import requests
import time

class Download:
	
	def __init__(self, url, request_type):
		self.__url = url
		self.__request_type = request_type
				
	def read_page(self, params='', data=''):
		
		client = requests.session()

		while True:		
		
			try:	
				if self.__request_type == "GET":
					page = client.get(url=self.__url, data=data, params=params)
					break
					
				if self.__request_type == "POST":
					page = client.post(url=self.__url, data=data, params=params)
					break
				
				if self.__request_type == "PUT":
					page = client.put(url=self.__url, data=data, params=params)
					break
					
			except Exception as e:
				print("Error: %s" % e)
				time.sleep(10)
		
		return page

