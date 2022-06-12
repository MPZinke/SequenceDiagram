#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.10                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json


class Token:
	def __init__(self, line, length, column, string, type):
		self.line = line
		self.length = length
		self.column = column
		self.string = string[column:column+length]
		self.type = type


	def __str__(self):
		return json.dumps(self.string)
