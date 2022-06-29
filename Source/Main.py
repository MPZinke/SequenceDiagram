#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################

from sys import stderr


from Classes.ParseTree import ParseTree
from Classes.Token import TokenErr
import Diagram
import LexicalAnalysis
import SemanticAnalysis
import SyntacticAnalysis


def main():
	with open("CompileProcess.sequence", "r") as file:
		try:
			tokens: list = LexicalAnalysis.parse([line.strip() for line in file.readlines()])
			print([token.type for token in tokens])
			abstract_syntax_tree: ParseTree = SyntacticAnalysis.parse(tokens)
			print(abstract_syntax_tree)
			sequences, symbol_table = SemanticAnalysis.traverse(abstract_syntax_tree)
			print(symbol_table)
			Diagram.draw(sequences, symbol_table)

		except TokenErr as error:
			print(error, file=stderr)



if __name__ == '__main__':
	main()
