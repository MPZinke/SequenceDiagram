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


from os.path import join
from PIL import ImageFont
from pathlib import Path


SOURCE_DIR = str(Path(__file__).absolute().parent.parent)  # .../Source
RESOURCES_DIR = join(SOURCE_DIR, "Resources")  # .../Source/Resources

LARGE_FONT = ImageFont.truetype(join(RESOURCES_DIR, "FiraCode-Bold.ttf"), size=32)


class DrawSymbol:
	def __init__(self, name: str, value: str, x_pos: int):
		self.name: str = name
		self.value: str = value
		self.x_pos: int = x_pos


	def draw(self, draw_area) -> None:
		text_width, text_height = draw_area.textsize(self.value, font=LARGE_FONT)
		draw_area.text((self.x_pos - text_width / 2, 100), self.value, font=LARGE_FONT)
		draw_area_height = draw_area._image._size[1]

		draw_area.line((self.x_pos, 100+text_height+10, self.x_pos, draw_area_height-100), fill=(255,255,255))
