#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.11                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Tuple, Union


class ParseToken:
	def __init__(self, type, tokens):
		self.type = type
		self.tokens = tokens


	def __str__(self):
		return self.type + "".join(["\n    " + "\n    ".join(str(token).split("\n")) for token in self.tokens])


# ————————————————————————————————————————————————————— WRAPPERS ————————————————————————————————————————————————————— #

def wrap_ParseToken(function: callable) -> ParseToken:
	def inner(token_list: list, index: int):
		if((results := function(token_list, index)) is None):
			return None

		return ParseToken(function.__name__, results[:-1]), results[-1]
	return inner


# —————————————————————————————————————————————————— NON-TERMINALS  —————————————————————————————————————————————————— #

@wrap_ParseToken
def Program(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Program -> Expression | ε
	"""
	if(index >= len(token_list)):
		return None

	if((expression := Expression(token_list, index)) is not None):
		return expression[0], expression[1]

	return None


@wrap_ParseToken
def Expression(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Expression -> Declaration | Declaration Expression | Sequence | Sequence Expression
	"""
	if(index >= len(token_list)):
		return None

	# Declaration | Declaration Expression
	if((declaration := Declaration(token_list, index)) is not None):
		# Declaration Expression
		if((expression := Expression(token_list, declaration[1])) is not None):
			return declaration[0], expression[0], expression[1]

		# Declaration
		return declaration[0], declaration[1]

	# Sequence | Sequence Expression
	if((sequence := Sequence(token_list, index)) is not None):
		# Sequence Expression
		if((expression := Expression(token_list, sequence[1])) is not None):
			return sequence[0], expression[0], expression[1]

		# Sequence
		return sequence[0], sequence[1]

	return None


@wrap_ParseToken
def Declaration(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Declaration -> Identifier-Colon String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier-Colon String
	if((identifier_colon := Identifier_Colon(token_list, index)) is not None):
		# String
		if((string := String(token_list, identifier_colon[1])) is not None):
			return identifier_colon[0], string[0], string[1]

	return None


@wrap_ParseToken
def Sequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Sequence -> LeftSequence | RightSequence
	"""
	if(index >= len(token_list)):
		return None

	if((left_sequence := LeftSequence(token_list, index)) is not None):
		return left_sequence[0], left_sequence[1]

	if((right_sequence := RightSequence(token_list, index)) is not None):
		return right_sequence[0], right_sequence[1]

	return None


@wrap_ParseToken
def LeftSequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	LeftSequence -> Identifier-LeftArrow Identifier | Identifier-LeftArrow Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier-LeftArrow Identifier-String
	if((identifier_leftarrow := Identifier_LeftArrow(token_list, index)) is not None):
		# Identifier-String
		if((identifier_string := Identifier_String(token_list, identifier_leftarrow[1])) is not None):
			return identifier_leftarrow[0], identifier_string[0], identifier_string[1]

	# Identifier-LeftArrow Identifier
	if((identifier_leftarrow := Identifier_LeftArrow(token_list, index)) is not None):
		# Identifier
		if((identifier := Identifier(token_list, identifier_leftarrow[1])) is not None):
			return identifier_leftarrow[0], identifier[0], identifier[1]

	return None


@wrap_ParseToken
def RightSequence(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	RightSequence -> Identifier-RightArrow Identifier | Identifier-RightArrow Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier-RightArrow Identifier-String
	if((identifier_rightarrow := Identifier_RightArrow(token_list, index)) is not None):
		# Identifier-String
		if((identifier_string := Identifier_String(token_list, identifier_rightarrow[1])) is not None):
			return identifier_rightarrow[0], identifier_string[0], identifier_string[1]

	# Identifier-RightArrow Identifier
	if((identifier_rightarrow := Identifier_RightArrow(token_list, index)) is not None):
		# Identifier
		if((identifier := Identifier(token_list, identifier_rightarrow[1])) is not None):
			return identifier_rightarrow[0], identifier[0], identifier[1]

	return None



@wrap_ParseToken
def Identifier_Colon(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-Colon -> Identifier Colon
	"""
	if(index >= len(token_list)):
		return None

	# Identifier Colon
	if((identifier := Identifier(token_list, index)) is not None):
		if((colon := Colon(token_list, identifier[1])) is not None):
			return identifier[0], colon[0], colon[1]

	return None


@wrap_ParseToken
def Identifier_LeftArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-LeftArrow -> Identifier LeftArrow
	"""
	if(index >= len(token_list)):
		return None

	# Identifier LeftArrow
	if((identifier := Identifier(token_list, index)) is not None):
		if((left_arrow := LeftArrow(token_list, identifier[1])) is not None):
			return identifier[0], left_arrow[0], left_arrow[1]

	return None


@wrap_ParseToken
def Identifier_RightArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-RightArrow -> Identifier RightArrow
	"""
	if(index >= len(token_list)):
		return None

	# Identifier RightArrow
	if((identifier := Identifier(token_list, index)) is not None):
		if((right_arrow := RightArrow(token_list, identifier[1])) is not None):
			return identifier[0], right_arrow[0], right_arrow[1]

	return None


@wrap_ParseToken
def Identifier_String(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier-String -> Identifier String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier String
	if((identifier := Identifier(token_list, index)) is not None):
		if((string := String(token_list, identifier[1])) is not None):
			return identifier[0], string[0], string[1]

	return None


# ———————————————————————————————————————————————————— TERMINALS  ———————————————————————————————————————————————————— #

@wrap_ParseToken
def Identifier(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Identifier -> "[_a-zA-Z][_a-zA-Z0-9]*"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "identifier"):
		return token_list[index], index+1

	return None


@wrap_ParseToken
def String(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	String -> "\"([^\\\"]|\\.)*\""
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "string"):
		return token_list[index], index+1

	return None


@wrap_ParseToken
def Colon(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	Colon -> ":"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "colon"):
		return token_list[index], index+1

	return None


@wrap_ParseToken
def RightArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	RightArrow -> "->"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "right_arrow"):
		return token_list[index], index+1

	return None


@wrap_ParseToken
def LeftArrow(token_list: list, index: int) -> Tuple[Union[ParseToken, None], int]:
	"""
	LeftArrow -> "<-"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "left_arrow"):
		return token_list[index], index+1

	return None


# —————————————————————————————————————————————————————— PARSE  —————————————————————————————————————————————————————— #

def parse(token_list: list) -> Union[ParseToken, None]:
	return Program(token_list, 0)[0]
