#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.12                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Classes.Token import TOKEN_TYPES


NON_TERMINALS = ["Program", "Expression", "Declaration", "StringDeclaration", "TitleDeclaration", "LifelineDeclaration",
  "Sequence", "LeftSequence", "RightSequence"]
TERMINALS = TOKEN_TYPES

SYMBOLS = NON_TERMINALS + TERMINALS


class ParseTree:
	def __init__(self, type: str, tokens: list):
		self.type: str = type
		self.tokens: list = tokens


	def __str__(self):
		token_strings = ["\n    " + "\n    ".join(str(token).split("\n")) for token in self.tokens]
		return self.type + "".join(token_strings)


	def __reduce__(self):
		return str(self)


	def __getitem__(self, right: int):
		# if(isinstance())
		return self.tokens[right]


	def __iter__(self):
		return iter(self.tokens)


	def __len__(self) -> int:
		return len(self.tokens)


# ————————————————————————————————————————————————————— WRAPPERS ————————————————————————————————————————————————————— #

# Because the function name is used to determine the token type, this wrapper is applied to ensure the function is named
#  appropriately.
def check_parse_type(function: callable) -> callable:
	if(function.__name__ not in SYMBOLS):
		raise Exception(f"Token Name: {function.__name__} not known")

	def inner(*args: list) -> callable:
		return function(*args)

	inner.__name__ = function.__name__
	return inner


def add_parse_type(function: callable) -> callable:
	if(function.__name__ not in SYMBOLS):
		raise Exception(f"Token Name: {function.__name__} not known")

	def inner(*args: list) -> callable:
		return function(*args, function.__name__)

	inner.__name__ = function.__name__
	return inner


def to_ParseTree(function: callable) -> callable:
	if(function.__name__ not in SYMBOLS):
		raise Exception(f"Token Name: {function.__name__} not known")

	def inner(token_list: list, index: int) -> ParseTree:
		if((results := function(token_list, index, function.__name__)) is None):
			return None

		return ParseTree(function.__name__, results[:-1]), results[-1]

	inner.__name__ = function.__name__
	return inner
