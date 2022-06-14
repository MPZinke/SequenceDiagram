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
import parse


TOKEN_TYPES = ["Identifier", "String", "Colon", "RightArrow", "LeftArrow", "WhiteSpace"]


# Because the function name is used to determine the token type, this wrapper is applied to ensure the function is named
#  appropriately.
def wrap_token_type(function: callable) -> callable:
	if(function.__name__ not in TOKEN_TYPES):
		raise Exception(f"Token Name: {function.__name__} not known")

	def inner(*args: list, **kwargs: dict) -> callable:
		return function(*args, **kwargs)

	inner.__name__ = function.__name__
	return inner


class Token:
	def __init__(self, line: int, length: int, column: int, string: str, type: str):
		self.line: int = line
		self.length: int = length
		self.column: int = column+1  # Adds 1 for human readablity
		self.string: str = string[column:column+length]
		self.type: str = type


	def __str__(self):
		return json.dumps(self.string)


class TokenException(Exception):
	def __new__(cls, message, token):
		fields = parse.compile(message)._named_fields
		message = message.format(**{field: getattr(token, field) for field in fields})
		return super(TokenException, cls).__new__(cls, message)


	def __init__(self, message):
		Exception.__init__(self, message)
