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


class SymbolTable:
	def __init__(self, name):
		self.name = name


TERMINALS = []
NON_TERMINALS = [Program, Expression, Declaration, Sequence, LeftSequence, RightSequence]

# Take in ParseTree

# Read ParseTree
# 	Symbols -> SymbolTable
# 	Statement -> Added To Semantic Tree

# Determine execution for ParseTree
