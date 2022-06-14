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


from PIL import Image, ImageDraw, ImageFont
from typing import List


from Classes.DrawTable import DrawSymbol
from Classes.SymbolTable import SymbolTable


def labeled_backward_sequence(A: str, B: str, label: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_backward_sequence")
		print(A)
		print(B)
		print(label)
		print()
		#TODO

	return draw_backward_sequence


def labeled_circular_sequence(A: str, label: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_circular_sequence")
		print(A)
		print(label)
		print()
		#TODO

	return draw_circular_sequence


def labeled_forward_sequence(A: str, B: str, label: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		A = [drawn_symbol for drawn_symbol in drawn_symbols if(drawn_symbol.name == A)][0]
		B = [drawn_symbol for drawn_symbol in drawn_symbols if(drawn_symbol.name == B)][0]

		draw_area.line((A.x_pos, y_pos, B.x_pos, y_pos), fill=(255,255,255))
		print("draw_forward_sequence")
		print(A)
		print(B)
		print(label)
		print()
		#TODO

	return draw_forward_sequence


def unlabeled_backward_sequence(A: str, B: str) -> None:
	def draw_backward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_backward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_backward_sequence


def unlabeled_circular_sequence(A: str) -> None:
	def draw_circular_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_circular_sequence")
		print(A)
		print()
		#TODO

	return draw_circular_sequence


def unlabeled_forward_sequence(A: str, B: str) -> None:
	def draw_forward_sequence(draw_area: ImageDraw, y_pos: int, drawn_symbols: List[DrawSymbol]) -> None:
		return
		print("draw_forward_sequence")
		print(A)
		print(B)
		print()
		#TODO

	return draw_forward_sequence


def write_symbols(draw_area: ImageDraw, symbol_table: SymbolTable) -> List[DrawSymbol]:
	draw_symbols: List[DrawSymbol] = []
	for x, symbol in enumerate(symbol_table):
		x_pos = x * 200 + 200
		draw_symbol = DrawSymbol(symbol.name, symbol.value, x_pos)
		draw_symbol.draw(draw_area)

		draw_symbols.append(draw_symbol)
	return draw_symbols


def create_canvas(sequences: List[callable], symbol_table: SymbolTable) -> Image:
	width = (len(symbol_table) - 1) * 200 + 400
	height = (len(sequences) - 1) * 150 + 300  # 100 top, 100 bottom, 32 Object, 68 buffer
	image = Image.new(mode="RGBA", size=[width, height])
	return image


def draw(sequences: List[callable], symbol_table: SymbolTable) -> None:
	image = create_canvas(sequences, symbol_table)
	draw_area = ImageDraw.Draw(image)
	drawn_symbols: List[DrawSymbol] = write_symbols(draw_area, symbol_table)
	for y, sequence in enumerate(sequences):
		print(type(sequence))
		print(sequence)
		print(sequence(draw_area, (y*150) + 166, drawn_symbols))

	image.show()
