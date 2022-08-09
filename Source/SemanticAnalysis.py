#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.13                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import List


import Diagram
from Classes.ParseTree import ParseTree, check_parse_type
from Classes.SymbolTable import SymbolTable
from Classes.Token import TokenErr


SYMBOL_TABLE = SymbolTable()


# —————————————————————————————————————————————————— NON-TERMINALS  —————————————————————————————————————————————————— #
# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————————— #

@check_parse_type
def Program(program: ParseTree) -> List[callable]:
	if(program.tokens == 0):
		return []

	else:
		return Expression(program.tokens[0])


@check_parse_type
def Expression(expression: ParseTree) -> List[callable]:
	execution: List[callable] = []
	for symbol in expression:
		execution += globals()[symbol.type](symbol)

	return execution


# ——————————————————————————————————————————— NON-TERMINALS::DECLARATIONS  ——————————————————————————————————————————— #

@check_parse_type
def Declaration(declaration: ParseTree) -> List[callable]:
	name, type, value = globals()[declaration[0].type](declaration[0])
	SYMBOL_TABLE.append(name, type, value)

	return []


def StringDeclaration(string_declaration: ParseTree) -> List[str]:
	identifier = string_declaration[1]

	if(identifier.str in SYMBOL_TABLE):
		raise TokenErr("Redefinition of declaration '{str}'", identifier)

	if(string_declaration[3].type == "String"):
		string = string_declaration[3].str
	else:
		if(all(string_declaration[3].str != symbol.name for symbol in SYMBOL_TABLE)):
			raise TokenErr("{{str}} is not declared", string_declaration[3])
		string = [symbol for symbol in SYMBOL_TABLE if(symbol.name == string_declaration[3].str)][0].value

	return identifier.str, string_declaration.type, string


def TitleDeclaration(title_declaration: ParseTree) -> List[str]:
	identifier = title_declaration[1]

	if(identifier.str in SYMBOL_TABLE):
		raise TokenErr("Redefinition of declaration '{str}'", identifier)

	if(any(symbol.type == title_declaration.type for symbol in SYMBOL_TABLE)):
		raise TokenErr("{{type}} already declared", title_declaration)

	if(title_declaration[3].type == "String"):
		string = title_declaration[3].str
	else:
		if(all(title_declaration[3].str != symbol.name for symbol in SYMBOL_TABLE)):
			raise TokenErr("{{str}} is not declared", title_declaration[3])
		string = [symbol for symbol in SYMBOL_TABLE if(symbol.name == title_declaration[3].str)][0].value

	return identifier.str, title_declaration.type, string


def LifelineDeclaration(title_declaration: ParseTree) -> List[str]:
	identifier = title_declaration[1]

	if(identifier.str in SYMBOL_TABLE):
		raise TokenErr("Redefinition of declaration '{str}'", identifier)

	if(title_declaration[3].type == "String"):
		string = title_declaration[3].str
	else:
		if(all(title_declaration[3].str != symbol.name for symbol in SYMBOL_TABLE)):
			raise TokenErr("{{str}} is not declared", title_declaration[3])
		string = [symbol for symbol in SYMBOL_TABLE if(symbol.name == title_declaration[3].str)][0].value

	return identifier.str, title_declaration.type, string



# ————————————————————————————————————————————— NON-TERMINALS::SEQUENCES ————————————————————————————————————————————— #

@check_parse_type
def Sequence(sequence: ParseTree) -> List[callable]:
	return globals()[sequence[0].type](sequence[0])


def LeftSequence(left_sequence: ParseTree) -> List[callable]:
	if((identifier1 := left_sequence[0]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier1)

	if((identifier2 := left_sequence[2]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier2)

	if(SYMBOL_TABLE.order(identifier2) < SYMBOL_TABLE.order(identifier1)):
		raise TokenErr(f"{{str}} declared before {identifier2.str}, but listed as sequenced after", identifier1)

	if(len(left_sequence) == 4):
		if(identifier1.str == identifier2.str):
			return [Diagram.labeled_circular_sequence(identifier1.str, left_sequence[3].str)]
		else:
			return [Diagram.labeled_backward_sequence(identifier1.str, identifier2.str, left_sequence[3].str)]
	else:
		if(identifier1.str == identifier2.str):
			return [Diagram.unlabeled_circular_sequence(identifier1.str)]
		else:
			return [Diagram.unlabeled_backward_sequence(identifier1.str, identifier2.str)]



def RightSequence(right_sequence: ParseTree) -> List[callable]:
	if((identifier1 := right_sequence[0]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier1)

	if((identifier2 := right_sequence[2]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier2)

	if(SYMBOL_TABLE.order(identifier2) < SYMBOL_TABLE.order(identifier1)):
		raise TokenErr(f"{{str}} declared before {identifier2.str}, but listed as sequenced after", identifier1)

	if(len(right_sequence) == 4):
		if(identifier1.str == identifier2.str):
			return [Diagram.labeled_circular_sequence(identifier1.str, right_sequence[3].str)]
		else:
			return [Diagram.labeled_forward_sequence(identifier1.str, identifier2.str, right_sequence[3].str)]
	else:
		if(identifier1.str == identifier2.str):
			return [Diagram.unlabeled_circular_sequence(identifier1.str)]
		else:
			return [Diagram.unlabeled_forward_sequence(identifier1.str, identifier2.str)]


def traverse(abstract_syntax_tree: ParseTree) -> List[callable]:
	sequences = Program(abstract_syntax_tree)
	return sequences, SYMBOL_TABLE
