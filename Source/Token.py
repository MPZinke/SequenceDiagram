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
		self.str: str = string[column+1:column+length-1] if(type == TOKEN_TYPES[1]) else string[column:column+length]
		self.type: str = type


	def __str__(self):
		return json.dumps(self.str)



class TokenErr(Exception):
	def __init__(self, message_format: str, token: Token, additional_values: dict={}):
		Exception.__init__(self, TokenErr.format_message(message_format, token, additional_values))


	@staticmethod
	def format_message(message_format: str, token: Token, additional_values: dict) -> str:
		message_prefix = f"LN: {token.line}, COL: {token.column}::"

		fields = parse.compile(message_format)._named_fields
		values = {field: getattr(token, field) for field in fields if(field not in additional_values)}
		return message_prefix + message_format.format(**{**values, **additional_values})


class UnexpectedEOF(TokenErr):
	def __init__(self, expected: str, token: Token):
		TokenErr.__init__(self, "Unexpected EOF after '{str}'. Expected: {expected}", token, {"expected": expected})


class UnexpectedToken(TokenErr):
	def __init__(self, expected: str, token: Token):
		TokenErr.__init__(self, "Expected '{expected}'; found '{type}'\n", token, {"expected": expected})
