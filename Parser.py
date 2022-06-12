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


from ParseTree import ParseTree


# ————————————————————————————————————————————————————— WRAPPERS ————————————————————————————————————————————————————— #

def wrap_ParseTree(function: callable) -> ParseTree:
	def inner(token_list: list, index: int):
		if((results := function(token_list, index)) is None):
			return None

		return ParseTree(function.__name__, results[:-1]), results[-1]
	return inner


# —————————————————————————————————————————————————— NON-TERMINALS  —————————————————————————————————————————————————— #

@wrap_ParseTree
def Program(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Program -> Expression | ε
	"""
	if(index >= len(token_list)):
		return None

	if((expression := Expression(token_list, index)) is not None):
		return expression[0], expression[-1]

	return None


@wrap_ParseTree
def Expression(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Expression -> Declaration | Declaration Expression | Sequence | Sequence Expression
	"""
	if(index >= len(token_list)):
		return None

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


@wrap_ParseTree
def Declaration(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Declaration -> Identifier-Colon String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier-Colon String
	if((identifier := Identifier(token_list, index)) is not None):
		# String
		if((colon_string := Colon_String(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *colon_string[:-1], colon_string[-1]

	return None


@wrap_ParseTree
def Sequence(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Sequence -> LeftSequence | RightSequence
	"""
	if(index >= len(token_list)):
		return None

	if((left_sequence := LeftSequence(token_list, index)) is not None):
		return *left_sequence[:-1], left_sequence[-1]

	if((right_sequence := RightSequence(token_list, index)) is not None):
		return *right_sequence[:-1], right_sequence[-1]

	return None


@wrap_ParseTree
def LeftSequence(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftSequence -> Identifier LeftArrow-Identifier | Identifier LeftArrow--Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier LeftArrow--Identifier-String
	if((identifier := Identifier(token_list, index)) is not None):
		# LeftArrow--Identifier-String
		if((leftarrow__identifier_string := LeftArrow__Identifier_String(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *leftarrow__identifier_string[:-1], leftarrow__identifier_string[-1]

	# Identifier LeftArrow-Identifier
	if((identifier := Identifier(token_list, index)) is not None):
		# LeftArrow-Identifier
		if((leftarrow_identifier := LeftArrow_Identifier(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *leftarrow_identifier[:-1], leftarrow_identifier[-1]

	return None


@wrap_ParseTree
def RightSequence(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightSequence -> Identifier RightArrow-Identifier | Identifier RightArrow--Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier RightArrow-Identifier | Identifier RightArrow--Identifier-String
	if((identifier := Identifier(token_list, index)) is not None):
		# RightArrow--Identifier-String
		if((rightarrow__identifier_string := RightArrow__Identifier_String(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *rightarrow__identifier_string[:-1], rightarrow__identifier_string[-1]

		# RightArrow-Identifier
		if((rightarrow_identifier := RightArrow_Identifier(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *rightarrow_identifier[:-1], rightarrow_identifier[-1]

	return None



@wrap_ParseTree
def Colon_String(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Identifier-Colon -> Identifier Colon
	"""
	if(index >= len(token_list)):
		return None

	# Identifier Colon
	if((colon := Colon(token_list, index)) is not None):
		if((string := String(token_list, colon[-1])) is not None):
			return *colon[:-1], *string[:-1], string[-1]

	return None


@wrap_ParseTree
def LeftArrow__Identifier_String(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftArrow--Identifier-String -> LeftArrow Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# LeftArrow Identifier-String
	if((left_arrow := LeftArrow(token_list, index)) is not None):
		if((identifier_string := Identifier_String(token_list, left_arrow[-1])) is not None):
			return *left_arrow[:-1], *identifier_string[:-1], identifier_string[-1]

	return None


@wrap_ParseTree
def LeftArrow_Identifier(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftArrow-Identifier -> LeftArrow Identifier
	"""
	if(index >= len(token_list)):
		return None

	# LeftArrow Identifier
	if((left_arrow := LeftArrow(token_list, index)) is not None):
		if((identifier := Identifier(token_list, left_arrow[-1])) is not None):
			return *left_arrow[:-1], *identifier[:-1], identifier[-1]

	return None


@wrap_ParseTree
def RightArrow__Identifier_String(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightArrow--Identifier-String -> RightArrow Identifier-String
	"""
	if(index >= len(token_list)):
		return None

	# RightArrow Identifier-String
	if((right_arrow := RightArrow(token_list, index)) is not None):
		if((identifier_string := Identifier_String(token_list, right_arrow[-1])) is not None):
			return *right_arrow[:-1], *identifier_string[:-1], identifier_string[-1]

	return None


@wrap_ParseTree
def RightArrow_Identifier(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightArrow-Identifier -> RightArrow Identifier
	"""
	if(index >= len(token_list)):
		return None

	# RightArrow Identifier
	if((right_arrow := RightArrow(token_list, index)) is not None):
		if((identifier := Identifier(token_list, right_arrow[-1])) is not None):
			return *right_arrow[:-1], *identifier[:-1], identifier[-1]

	return None


@wrap_ParseTree
def Identifier_String(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Identifier-String -> Identifier String
	"""
	if(index >= len(token_list)):
		return None

	# Identifier String
	if((identifier := Identifier(token_list, index)) is not None):
		if((string := String(token_list, identifier[-1])) is not None):
			return *identifier[:-1], *string[:-1], string[-1]

	return None


# ———————————————————————————————————————————————————— TERMINALS  ———————————————————————————————————————————————————— #

@wrap_ParseTree
def Identifier(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Identifier -> "[_a-zA-Z][_a-zA-Z0-9]*"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "identifier"):
		return token_list[index], index+1

	return None


@wrap_ParseTree
def String(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	String -> "\"([^\\\"]|\\.)*\""
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "string"):
		return token_list[index], index+1

	return None


@wrap_ParseTree
def Colon(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	Colon -> ":"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "colon"):
		return token_list[index], index+1

	return None


@wrap_ParseTree
def RightArrow(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	RightArrow -> "->"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "right_arrow"):
		return token_list[index], index+1

	return None


@wrap_ParseTree
def LeftArrow(token_list: list, index: int) -> Union[Tuple[ParseTree, int], None]:
	"""
	LeftArrow -> "<-"
	"""
	if(index >= len(token_list)):
		return None

	if(token_list[index].type == "left_arrow"):
		return token_list[index], index+1

	return None


# —————————————————————————————————————————————————————— PARSE  —————————————————————————————————————————————————————— #

def parse(token_list: list) -> Union[ParseTree, None]:
	abstract_syntax_tree, last_consumed_index = Program(token_list, 0)
	if(last_consumed_index != len(token_list)):
		token = token_list[last_consumed_index]
		error = f"Parsing Failed: Last consumed token: '{token.string}' at Line: {token.line}, Column: {token.column}"
		raise Exception(error)

	return abstract_syntax_tree
