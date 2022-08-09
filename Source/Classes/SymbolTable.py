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


from Classes.Token import TokenErr


class Symbol:
	def __init__(self, name, type, value):
	# def __init__(self, id, name, type, value):
		# self.id: str = id
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


	def __iter__(self) -> iter:
		return iter(self.symbols)


	def __len__(self) -> int:
		return len(self.symbols)


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


	def __reduce__(self):
		return str(self)


	# def append(self, id: str, name: str, type: str, value: str) -> None:
	def append(self, name: str, type: str, value: str) -> None:
		self.symbols.append(Symbol(name, type, value))


	def lookup(self, name) -> Symbol:
		for symbol in self.symbols:
			if(symbol.name == name):
				return symbol

		return None


	def order(self, name) -> int:
		for x in range(len(self.symbols)):
			if(self.symbols[x].name == x):
				return x

		return -1


	def order_id(self, id) -> int:
		for x in range(len(self.symbols)):
			if(self.symbols[x].id == x):
				return x

		return -1


	def unique_id(self, name: str) -> str:
		name_count = 0
		unique_id = f"{name}-{name_count}"
		while(-1 < self.order_id(unique_id)):
			name_count += 1

		return unique_id
