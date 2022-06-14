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


from ParseTree import ParseTree, wrap_parse_type
from SymbolTable import SymbolTable
from Token import TokenErr


SYMBOL_TABLE = SymbolTable()


@wrap_parse_type
def Program(program: ParseTree) -> List[callable]:
	if(program.tokens == 0):
		return []

	else:
		return Expression(program.tokens[0])


def Expression(expression: ParseTree) -> List[callable]:
	execution: List[callable] = []
	for symbol in expression:
		execution += globals()[symbol.type](symbol)

	return execution


def Declaration(declaration: ParseTree) -> List[callable]:
	identifier = declaration[0][0]
	string = declaration[2][0]

	if(identifier.string in SYMBOL_TABLE):
		raise TokenErr("LN: {line} COL: {column}::Redefinition of declaration '{string}'", identifier)

	SYMBOL_TABLE.append(identifier.string, declaration.type, string.string)

	return []


def Sequence(sequence: ParseTree) -> List[callable]:
	execution: List[callable] = []
	# for symbol in sequence:

	return execution


def traverse(abstract_syntax_tree: ParseTree) -> List[callable]:
	program = Program(abstract_syntax_tree)
	print(str(SYMBOL_TABLE))
	return program




# Take in ParseTree

# Read ParseTree
# 	Symbols -> SymbolTable
# 	Statement -> Added To Semantic Tree

# Determine execution for ParseTree
