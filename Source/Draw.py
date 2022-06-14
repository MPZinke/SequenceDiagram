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


from PIL import Image, ImageDraw


from Classes.SymbolTable import SymbolTable


def labeled_backward_sequence(A: str, B: str, label: str) -> None:
	def draw_backward_sequence() -> None:
		print("draw_backward_sequence")
		print(A)
		print(B)
		print(label)
		print()
		#TODO

	return draw_backward_sequence


def labeled_circular_sequence(A: str, label: str) -> None:
	def draw_circular_sequence() -> None:
		print("draw_circular_sequence")
		print(A)
		print(label)
		print()
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(A: str, B: str, label: str) -> None:
	def draw_forward_sequence() -> None:
		print("draw_forward_sequence")
		print(A)
		print(B)
		print(label)
		print()
		#TODO

	return draw_forward_sequence


def unlabeled_backward_sequence(A: str, B: str) -> None:
	def draw_backward_sequence() -> None:
		print("draw_backward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_backward_sequence


def unlabeled_circular_sequence(A: str) -> None:
	def draw_circular_sequence() -> None:
		print("draw_circular_sequence")
		print(A)
		print()
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(A: str, B: str) -> None:
	def draw_forward_sequence() -> None:
		print("draw_forward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_forward_sequence


def draw_symbols(symbol_table: SymbolTable) -> Image:
	image, draw = create_canvas()
	for x, symbol in enumerate(symbol_table):
		draw.text((10, 10*x + 10), symbol.value, fill=(255,255,255))

	image.show()



def create_canvas() -> Image:
	image = Image.new(mode="RGBA", size=[2560, 1080])
	return image, ImageDraw.Draw(image)
