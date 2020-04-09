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

from configparser import RawConfigParser as RCP
import os

class ReadConfig:
	
	def __init__(self, file_name):
	
		self.__CONF_NAME = os.path.join(os.getenv("HOME") + '/.local/share/coddow/settings', file_name)
		self.__config = RCP()
		
	def settings(self):
		while True:
			try:
				self.__config.read(self.__CONF_NAME)
				values = self.__config.sections()
				break
			except Exception as e:
				print("Configurations Reading Error: %s" % e)
				
		return values
		
	def read(self, setting):
	
		while True:
			try:
				self.__config.read(self.__CONF_NAME)
				values = self.__config[setting]
				break
			except Exception as e:
				print("Configurations Reading Error: %s" % e)	
				
		return values
		
if __name__ == '__main__':
	stgs = ReadConfig()
	print(stgs.settings())
