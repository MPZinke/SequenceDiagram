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


from Token import TOKEN_TYPES


NON_TERMINALS = ["Program", "Expression", "Declaration", "Sequence", "LeftSequence", "RightSequence"]
TERMINALS = TOKEN_TYPES

SYMBOLS = NON_TERMINALS + TERMINALS


# Because the function name is used to determine the token type, this wrapper is applied to ensure the function is named
#  appropriately.
def wrap_parse_type(function: callable) -> callable:
	if(function.__name__ not in SYMBOLS):
		raise Exception(f"Token Name: {function.__name__} not known")

	def inner(*args: list, **kwargs: dict) -> callable:
		return function(*args, **kwargs)

	inner.__name__ = function.__name__
	return inner


class ParseTree:
	def __init__(self, type: str, tokens: list):
		self.type: str = type
		self.tokens: list = tokens


	def __str__(self):
		return self.type + "".join(["\n    " + "\n    ".join(str(token).split("\n")) for token in self.tokens])


	def __getitem__(self, right: int):
		return self.tokens[right]


	def __iter__(self):
		return iter(self.tokens)
