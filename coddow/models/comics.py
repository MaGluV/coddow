#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
# comics.py
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

class Comics_Data:
	def __init__(self):
		self.__name = ''
		self.__address = ''
		self.__rating = ''
		self.__pages_number = 0
		self.__link = ''
		self.__setting = ''
		self.__status = ''
		self.__date = ''
		
	def set_name(self, name):
		self.__name = name
		
	def get_name(self):
		return self.__name
		
	def set_address(self, address):
		self.__address = address
		
	def get_address(self):
		return self.__address
		
	def set_rating(self, rating):
		self.__rating = rating
	
	def get_rating(self):
		return self.__rating
	
	def set_pages_number(self, n):
		self.__pages_number = n
	
	def get_pages_number(self):
		return self.__pages_number
		
	def set_last_link(self, link):
		self.__link = link
		
	def get_last_link(self):
		return self.__link

	def set_status(self, status):
		self.__status = status
		
	def get_status(self):
		return self.__status

	def set_date(self, date):
		self.__date = date

	def get_date(self):
		return self.__date
		
	def print_data(self):
		print("""\t\t\tNAME : %s,
				 ADDRESS : %s,
				 RATING : %s,
				 PAGES : %s,
				 LAST LINK : %s
				 DATE : %s""" % (self.__name, self.__address, self.__rating, self.__pages_number, self.__link, self.__date))
