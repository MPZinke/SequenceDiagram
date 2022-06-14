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


SYMBOL_TABLE = SymbolTable()


@wrap_parse_type
def Program(program: ParseTree) -> List[callable]:
	if(program.tokens == 0):
		return []

	else:
		return Expression(program.tokens[0])


def Expression(expression: ParseTree) -> List[callable]:
	execution = []
	for symbol in expression:
		if(symbol.type == "Declaration"):
			execution += Declaration(symbol)
		elif(symbol.type == "Expression"):
			execution += Expression(symbol)
		# elif(symbol.type == "Sequence"):
		# 	execution += Sequence(symbol)

	return execution


def Declaration(declaration: ParseTree) -> List[callable]:
	identifier = declaration[0]
	string = declaration[2]

	if(str(identifier) in SYMBOL_TABLE):
		raise TokenException("LN: {line} COL: {column}::Redefinition of declaration '{string}'", declaration[0])

	SYMBOL_TABLE.append(identifier[0].string, declaration.type, string[0].string)

	return []



def traverse(abstract_syntax_tree: ParseTree) -> List[callable]:
	program = Program(abstract_syntax_tree)
	print(str(SYMBOL_TABLE))
	return program




# Take in ParseTree

# Read ParseTree
# 	Symbols -> SymbolTable
# 	Statement -> Added To Semantic Tree

# Determine execution for ParseTree
