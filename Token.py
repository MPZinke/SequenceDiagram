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
	def __init__(self, line: int, length: int, column: int, string: str, type: str):
		self.line: int = line
		self.length: int = length
		self.column: int = column+1  # Adds 1 for human readablity
		self.string: str = string[column:column+length]
		self.type: str = type


	def __str__(self):
		return json.dumps(self.string)
