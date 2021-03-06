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


from Classes.ParseTree import ParseTree, add_parse_type, check_parse_type, to_ParseTree
from Classes.Token import UnexpectedEOF, UnexpectedToken


def wrap_index(function: callable) -> callable:
	def inner(token_list: list, index: int) -> callable:
		if(index >= len(token_list)):
			return None

		return function(token_list, index)
	inner.__name__ = function.__name__
	return inner


# —————————————————————————————————————————————————— NON-TERMINALS  —————————————————————————————————————————————————— #

@wrap_index
@to_ParseTree
def Program(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Program -> Expression | ε
	"""
	if((expression := Expression(token_list, index)) is not None):
		return expression[0], expression[-1]

	return None


@wrap_index
@to_ParseTree
def Expression(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Expression -> Declaration | Declaration Expression | Sequence | Sequence Expression
	"""
	# Declaration | Declaration Expression
	if((declaration := Declaration(token_list, index)) is not None):
		# Declaration Expression
		if((expression := Expression(token_list, declaration[-1])) is not None):
			return *declaration[:-1], *expression[:-1], expression[-1]

		# Declaration
		return *declaration[:-1], declaration[-1]

	# Sequence | Sequence Expression
	if((sequence := Sequence(token_list, index)) is not None):
		# Sequence Expression
		if((expression := Expression(token_list, sequence[-1])) is not None):
			return *sequence[:-1], *expression[:-1], expression[-1]

		# Sequence
		return *sequence[:-1], sequence[-1]

	return None


@wrap_index
@to_ParseTree
def Declaration(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Declaration -> Identifier Colon String
	"""
	# Identifier Colon String
	if((identifier := Identifier(token_list, index)) is not None
	  and (colon := Colon(token_list, identifier[-1])) is not None
	):
		if((string := String(token_list, colon[-1])) is not None):
			return identifier[0], colon[0], string[0], string[-1]

		if(len(token_list) <= colon[-1]):
			raise UnexpectedEOF(String.__name__, token_list[identifier[-1]])
		raise UnexpectedToken(String.__name__, token_list[colon[-1]])

	return None


@wrap_index
@to_ParseTree
def Sequence(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Sequence -> LeftSequence | RightSequence
	"""
	if((left_sequence := LeftSequence(token_list, index)) is not None):
		return *left_sequence[:-1], left_sequence[-1]

	if((right_sequence := RightSequence(token_list, index)) is not None):
		return *right_sequence[:-1], right_sequence[-1]

	return None


@wrap_index
@to_ParseTree
def LeftSequence(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftSequence -> Identifier LeftArrow Identifier | Identifier LeftArrow Identifier String
	"""
	# Identifier LeftArrow Identifier String
	if((identifier1 := Identifier(token_list, index)) is not None
	  and (left_arrow := LeftArrow(token_list, identifier1[-1])) is not None
	):
		if((identifier2 := Identifier(token_list, left_arrow[-1])) is not None):
			# Identifier LeftArrow Identifier String
			if((string := String(token_list, identifier2[-1])) is not None):
				return identifier1[0], left_arrow[0], identifier2[0], string[0], string[-1]

			# Identifier LeftArrow Identifier
			return identifier1[0], left_arrow[0], identifier2[0], identifier2[-1]

		if(len(token_list) <= left_arrow[-1]):
			raise UnexpectedEOF(Identifier.__name__, token_list[identifier1[-1]])
		raise UnexpectedToken(Identifier.__name__, token_list[left_arrow[-1]])  # Identifier LeftArrow ??

	return None


@wrap_index
@to_ParseTree
def RightSequence(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightSequence -> Identifier RightArrow-Identifier | Identifier RightArrow Identifier String
	"""
	# Identifier RightArrow Identifier | Identifier RightArrow Identifier String
	if((identifier1 := Identifier(token_list, index)) is not None
	  and (right_arrow := RightArrow(token_list, identifier1[-1])) is not None
	):
		if((identifier2 := Identifier(token_list, right_arrow[-1])) is not None):
			# Identifier RightArrow Identifier String
			if((string := String(token_list, identifier2[-1])) is not None):
				return identifier1[0], right_arrow[0], identifier2[0], string[0], string[-1]

			# Identifier RightArrow Identifier
			return identifier1[0], right_arrow[0], identifier2[0], identifier2[-1]

		if(len(token_list) <= right_arrow[-1]):
			raise UnexpectedEOF(Identifier.__name__, token_list[identifier1[-1]])
		raise UnexpectedToken(Identifier.__name__, token_list[right_arrow[-1]])  # Identifier LeftArrow ??

	return None


# ———————————————————————————————————————————————————— TERMINALS  ———————————————————————————————————————————————————— #

@wrap_index
@add_parse_type
def Identifier(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Identifier -> "[_a-zA-Z][_a-zA-Z0-9]*"
	"""
	if(token_list[index].type == function_name):
		return token_list[index], index+1

	return None


@wrap_index
@add_parse_type
def String(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	String -> "\"([^\\\"]|\\.)*\""
	"""
	if(token_list[index].type == function_name):
		return token_list[index], index+1

	return None


@wrap_index
@add_parse_type
def Colon(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	Colon -> ":"
	"""
	if(token_list[index].type == function_name):
		return token_list[index], index+1

	return None


@wrap_index
@add_parse_type
def RightArrow(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightArrow -> "->"
	"""
	if(token_list[index].type == function_name):
		return token_list[index], index+1

	return None


@wrap_index
@add_parse_type
def LeftArrow(token_list: list, index: int, function_name: str) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftArrow -> "<-"
	"""
	if(token_list[index].type == function_name):
		return token_list[index], index+1

	return None


# —————————————————————————————————————————————————————— PARSE  —————————————————————————————————————————————————————— #

def parse(token_list: list) -> Union[ParseTree, None]:
	abstract_syntax_tree, last_consumed_index = Program(token_list, 0)
	if(last_consumed_index != len(token_list)):
		token = token_list[last_consumed_index]
		error = f"Parsing Failed: Last consumed token: '{token.str}' at Line: {token.line}, Column: {token.column}"
		raise Exception(error)

	return abstract_syntax_tree
