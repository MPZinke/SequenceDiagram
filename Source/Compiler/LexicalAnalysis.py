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


from functools import wraps
import re
from typing import Union


from Classes.Compiling.Token import Token, wrap_token_type


# ————————————————————————————————————————————————————— WRAPPERS ————————————————————————————————————————————————————— #

def match_regex(function: callable) -> int:
	def list_diff(int_diff: list) -> int:
		return int_diff[1] - int_diff[0]

	@wraps(function)
	def inner(string: str) -> str:
		regex = function()
		match: Union[re.Match, None] = re.match(regex, string)
		return list_diff(match.span()) if(match) else 0

	return inner


@wrap_token_type
@match_regex
def StringKeyword() -> int:
	return "String"


@wrap_token_type
@match_regex
def TitleKeyword() -> int:
	return "Title"


@wrap_token_type
@match_regex
def LifelineKeyword() -> int:
	return "Lifeline"


@wrap_token_type
@match_regex
def Identifier() -> int:
	return r"[_a-zA-Z][_a-zA-Z0-9]*"


@wrap_token_type
@match_regex
def String() -> int:
	return r"\"([^\\\"]|\\.)*\""


@wrap_token_type
@match_regex
def Colon() -> int:
	return r":"


@wrap_token_type
@match_regex
def RightArrow() -> int:
	return r"->"


@wrap_token_type
@match_regex
def LeftArrow() -> int:
	return r"<-"


@wrap_token_type
@match_regex
def WhiteSpace() -> int:
	return r"[ \t\r]+"


# ———————————————————————————————————————————————— TOKEN  IDENTIFYING ———————————————————————————————————————————————— #

def token_type(line_num: int,  line: str, column: int) -> Token:
	token = Token(0, 0, column, "", "")
	for function in [StringKeyword, TitleKeyword, LifelineKeyword, Identifier, String, Colon, RightArrow, LeftArrow,
	  WhiteSpace]:
		if((temp := Token(line_num+1, function(line[column:]), column, line, function.__name__)).length > token.length):
			token = temp

	if(token.length == 0):
		raise Exception(f"Token at pos: {token.column} failed")

	return token


def parse(lines: list) -> list:
	tokens = []

	for line_num, line in enumerate(lines):
		if(line.strip() == ""):
			continue

		position = 0
		while position < len(line):
			token = token_type(line_num, line, position)

			if(token.type != WhiteSpace.__name__):
				tokens.append(token)
			position += token.length

	return tokens
