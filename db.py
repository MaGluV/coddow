#!/usr/bin/env python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 

# db.py
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

import sqlite3

class DB():
	
	def __init__(self, dbname):
		self.__CON = sqlite3.connect(dbname) 
			
	def close(self):
		self.__CON.close()
		
	def create_table(self, table_name, columns):
	
		if table_name == "backup":
			print("Create_Error: table cannot be called backup")
			return None
		create_message = """ CREATE TABLE IF NOT EXISTS %s (%s) """ % (table_name, columns)
		db = self.__CON.cursor()
		try:
			db.execute(create_message)
		except sqlite3.Error as e:
			print("Create_Error:",e.args[0])
		db.close()
		
	def add_column(self, table_name, column):
		
		db = self.__CON.cursor()
		create_message = """ALTER TABLE %s ADD COLUMN %s""" % (table_name, column)
		try:
			db.execute(create_message)
		except sqlite3.Error as e:
			print("Add_Error:",e.args[0])
		db.close()
		
	def rename_table(self, table_name, new_name):
		
		create_message = """ALTER TABLE %s RENAME TO %s""" % (table_name, new_name)
		db = self.__CON.cursor()
		try:
			db.execute(create_message)
		except sqlite3.Error as e:
			print("Rename_Error:",e.args[0])
		db.close()
		
	def remove_table(self, table_name):
		
		create_message = """ DROP TABLE %s """ % table_name
		db = self.__CON.cursor()
		try:
			db.execute(create_message)
		except sqlite3.Error as e:
			print("Remove_Error:",e.args[0])
		db.close()
		
	def column_list(self, table_name):
		
		self.__CON.row_factory = sqlite3.Row
		try:
			command = 'select * from %s' % table_name
			db = self.__CON.execute(command)
			row = db.fetchone()
			keys = row.keys()
		except sqlite3.Error as e:
			print("Column_List_Error:",e.args[0])
			return []
		return keys
		
	def remove_column(self, table_name, column):
		
		keys = ""
		for key in self.column_list(table_name):
			if key != column:
				keys += key + ", "
		if len(keys) == 0:
			return None
		keys = keys.rstrip(", ")
		db = self.__CON.cursor()
		command = """CREATE TABLE backup AS SELECT %s FROM %s""" % (keys, table_name)
		try:
			db.execute(command)
		except sqlite3.Error as e:
			print("Remove_Column_Error:",e.args[0])
			return None
		db.close()
		self.remove_table(table_name)
		self.rename_table("backup", table_name)
	
	def row_add(self, table_name, data):
		
		db = self.__CON.cursor()
		command = """ INSERT INTO %s VALUES (%s) """ % (table_name, ("?,"*len(data))[:-1])
		try:
			db.execute(command, tuple(data))	
			self.__CON.commit()
		except sqlite3.Error as e:
			print("Row_Add_Error:",e.args[0])
		db.close()
		
	def delete_row(self, table_name, row_filter):
	
		db = self.__CON.cursor()
		try:
			command = """DELETE FROM %s WHERE %s""" % (table_name, row_filter)
			db.execute(command)	
			self.__CON.commit()
		except sqlite3.Error as e:
			print("Delete_Row_Error:",e.args[0])
		db.close()
	
	def get_data(self, table_name, col, row_filter=''):
	
		db = self.__CON.cursor()
		command = """SELECT %s FROM %s %s""" % (col, table_name, row_filter)
		data = []
		try:
			fet = db.execute(command)
			data = fet.fetchall()	
		except sqlite3.Error as e:
			print("Get_Data_Error:",e.args[0])
		db.close()
		return data
		
	def update_row(self, table_name, columns, row_filter):
		
		db = self.__CON.cursor()
		try:
			command = """UPDATE %s SET %s WHERE %s""" % (table_name, columns, row_filter)
			db.execute(command)
			self.__CON.commit()	
		except sqlite3.Error as e:
			print("Update_Row_Error:",e.args[0])
		db.close()
