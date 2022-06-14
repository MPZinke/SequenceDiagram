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


from Token import TokenErr


class Symbol:
	def __init__(self, name, type, value):
		self.name: str = name
		self.type: str = type
		self.value: str = value


	def __eq__(self, right) -> bool:
		return self.name == right.name and self.type == right.type


class SymbolTable:
	def __init__(self):
		self.symbols: List[Symbol] = []


	def __contains__(self, name) -> bool:
		for symbol in self.symbols:
			if(symbol.name == name):
				return True

		return False


	def __str__(self):
		lengths =  {"name": 0, "type": 0, "value": 0}
		for symbol in self.symbols:
			for attr, length in lengths.items():
				if(len(getattr(symbol, attr)) > length):
					lengths[attr] = len(getattr(symbol, attr))

		strings = []
		for symbol in self.symbols:
			string = "| {name:{name_len}} | {type:{type_len}} | {value:{value_len}} |"
			values = {key+"_len": f" <{str(value)}" for key, value in lengths.items()}
			strings.append(string.format(**{**values, **{key: getattr(symbol, key) for key in lengths}}))

		return "\n".join(strings)


	def lookup(self, name) -> Symbol:
		for symbol in self.symbols:
			if(symbol.name == name):
				return symbol

		return None


	def append(self, name, type, value) -> None:
		self.symbols.append(Symbol(name, type, value))
