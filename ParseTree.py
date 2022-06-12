#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.12                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


class ParseTree:
	def __init__(self, type: str, tokens: list):
		self.type: str = type
		self.tokens: list = tokens


	def __str__(self):
		return self.type + "".join(["\n    " + "\n    ".join(str(token).split("\n")) for token in self.tokens])
