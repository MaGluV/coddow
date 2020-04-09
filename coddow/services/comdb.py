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

from services.db import DB 
import os
from glob import glob
from time import localtime,asctime

class DB_Comics:

	def __init__(self):
		self.__DBNAME = os.path.join(os.getenv("HOME") + '/.local/share/coddow/db', "Comics.db")

	def db_create(self, table_name):
	
		db = DB(self.__DBNAME)
		keys = """ID INTEGER PRIMARY KEY NOT NULL,
				  NAME TEXT UNIQUE NOT NULL,
				  ADDRESS TEXT UNIQUE NOT NULL,
				  RATING TEXT NOT NULL,
				  PAGES_NUMBER INTEGER NOT NULL,
				  LAST_LINK TEXT NOT NULL,
				  STATUS TEXT NOT NULL,
				  UPDATE_DATE TEXT NOT NULL"""
				   
		db.create_table(table_name,keys)
		db.close()
		
	def add_comics(self, table_name, data):
		
		db = DB(self.__DBNAME)		
		try:
			row_id = max(db.get_data(table_name,"ID"))[0] + 1 
		except Exception:
			row_id = 1
		data_list = [row_id,
					 data.get_name(), 
					 data.get_address(), 
					 data.get_rating(), 
					 data.get_pages_number(), 
					 data.get_last_link(),
					 data.get_status(),
					 data.get_date()]
		data.print_data()
		db.row_add(table_name, data_list)
		db.close()
		
	def delete_by_name(self, table_name, name):
	
		db = DB(self.__DBNAME)
		data = db.delete_row(table_name, "NAME = '%s'" % name)
		db.close()
		
	def update_comics_info(self, table_name, name, num, date, link, status):
		
		db = DB(self.__DBNAME)
		set_columns = """PAGES_NUMBER = %s, 
						 UPDATE_DATE = '%s', 
						 LAST_LINK = '%s', 
						 STATUS = '%s'""" % (num, date, link, status)
		filter_by_name = "NAME = '%s'" % name
		db.update_row(table_name, set_columns, filter_by_name)
		db.close()
		
	def update_status(self, table_name, address, status):
		
		db = DB(self.__DBNAME)
		set_columns = "STATUS = %s" % status
		filter_by_address = "ADDRESS = '%s'" % address
		db.update_row(table_name, set_columns, filter_by_address)
		db.close()
		
	def get_sorted_by_date(self, table_name):
		
		db = DB(self.__DBNAME)
		data = db.get_data(table_name, "*", "ORDER BY UPDATE_DATE")
		db.close()
		return data
		
	def get_not_deleted(self, table_name):
		
		db = DB(self.__DBNAME)
		data = db.get_data(table_name, "*", "WHERE STATUS != 'deleted'")
		db.close()
		return data
	
	def get_column(self, table_name, column):
		
		db = DB(self.__DBNAME)
		data = db.get_data(table_name, column)
		db.close()
		return data
