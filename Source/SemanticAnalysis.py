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


import Draw
from Classes.ParseTree import ParseTree, check_parse_type
from Classes.SymbolTable import SymbolTable
from Classes.Token import TokenErr


SYMBOL_TABLE = SymbolTable()


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


@check_parse_type
def Declaration(declaration: ParseTree) -> List[callable]:
	identifier = declaration[0]
	string = declaration[2]

	if(identifier.str in SYMBOL_TABLE):
		raise TokenErr("Redefinition of declaration '{str}'", identifier)

	SYMBOL_TABLE.append(SYMBOL_TABLE.unique_id(identifier.str), identifier.str, declaration.type, string.str)

	return []


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
			return [Draw.labeled_circular_sequence(identifier1.str, left_sequence[3].str)]
		else:
			return [Draw.labeled_backward_sequence(identifier1.str, identifier2.str, left_sequence[3].str)]
	else:
		if(identifier1.str == identifier2.str):
			return [Draw.unlabeled_circular_sequence(identifier1.str)]
		else:
			return [Draw.unlabeled_backward_sequence(identifier1.str, identifier2.str)]



def RightSequence(right_sequence: ParseTree) -> List[callable]:
	if((identifier1 := right_sequence[0]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier1)

	if((identifier2 := right_sequence[2]).str not in SYMBOL_TABLE):
		raise TokenErr("Unknown sequence '{str}'", identifier2)

	if(SYMBOL_TABLE.order(identifier2) < SYMBOL_TABLE.order(identifier1)):
		raise TokenErr(f"{{str}} declared before {identifier2.str}, but listed as sequenced after", identifier1)

	if(len(right_sequence) == 4):
		if(identifier1.str == identifier2.str):
			return [Draw.labeled_circular_sequence(identifier1.str, right_sequence[3].str)]
		else:
			return [Draw.labeled_forward_sequence(identifier1.str, identifier2.str, right_sequence[3].str)]
	else:
		if(identifier1.str == identifier2.str):
			return [Draw.unlabeled_circular_sequence(identifier1.str)]
		else:
			return [Draw.unlabeled_forward_sequence(identifier1.str, identifier2.str)]


def traverse(abstract_syntax_tree: ParseTree) -> List[callable]:
	sequences = Program(abstract_syntax_tree)
	print(str(SYMBOL_TABLE))  #TESTING
	# for function in sequences:  #TESTING
		# function()  #TESTING

	Draw.draw(sequences, SYMBOL_TABLE)  #TESTING
	return sequences, SYMBOL_TABLE
