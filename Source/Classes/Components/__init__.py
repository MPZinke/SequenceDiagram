#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Set


from Classes.Canvas import Canvas


class Component:
	def __init__(self, *, canvas: Canvas=None, size: Set[int]=None, start: Set[int]=None):
		self.canvas: Canvas = canvas
		self.start: Set[int] = start


	def __reduce__(self):
		return str(self)


	def __str__(self):
		return f"{{size: {self.dimensions()}, start: {self.start}}}"


	def center(self) -> Set[int]:
		width, height = self.dimensions()
		return (self.start[0] + (width / 2), self.start[1] + (height / 2))


	def dimensions(self) -> Set[int]:
		raise Exception("Component::dimensions is a virtual method and must be overridden before usage")


	@classmethod
	def check_params(cls, function_name: str, **params) -> None:
		for name, value in params.items():
			if(value is None):
				class_name: str = str(cls).split(".")[-1][:-2]
				raise Exception(f"Parameter '{name}' cannot be None for {class_name}::{function_name}")
