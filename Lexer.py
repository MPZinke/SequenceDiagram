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


import re
from typing import Union


from Token import Token


def list_diff(int_diff: list) -> int:
	return int_diff[1] - int_diff[0]


def match_regex(regex: str, string: str) -> int:
	match: Union[re.Match, None] = re.match(regex, string)
	return list_diff(match.span()) if(match) else 0




def identifier(string: str) -> int:
	return match_regex(r"[_a-zA-Z][_a-zA-Z0-9]*", string)


def string(string: str) -> int:
	return match_regex(r"\"([^\\\"]|\\.)*\"", string)


def colon(string: str) -> int:
	return match_regex(r":", string)


def right_arrow(string: str) -> int:
	return match_regex(r"->", string)


def left_arrow(string: str) -> int:
	return match_regex(r"<-", string)


def white_space(string: str) -> int:
	return match_regex(r"[ \t\r]+", string)



def token_type(line_num: int,  line: str, column: int) -> Token:
	token = Token(0, 0, column, "", "")
	for function in [identifier, string, colon, right_arrow, left_arrow, white_space]:
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

			if(token.type != "white_space"):
				tokens.append(token)
			position += token.length

	return tokens
