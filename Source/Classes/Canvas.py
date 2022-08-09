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


from PIL import Image, ImageDraw
from typing import Any, Set, Union


class Canvas:
	def __init__(self, size: Set[int], mode: str="RGBA"):
		self.size: Set[int] = size
		self.mode: str = mode
		self.image: Image = Image.new(mode=mode, size=self.size)
		self.draw_area: ImageDraw = ImageDraw.Draw(self.image)


	def dimensions(self) -> Set[int]:
		return self.size


	def resize(self, width: int, height: int, offset: Union[Set, None]=None) -> None:
		self.size = (width, height)
		new: Image = Image.new(size=self.size, mode=self.mode)
		new.paste(self.image, offset if(offset is not None) else (0, 0))
		self.image = new
		self.draw_area = ImageDraw.Draw(self.image)


	def show(self):
		self.image.show()


	def __getattr__(self, method: str) -> Any:
		def wrapper(*args: list, **kwargs: dict):
			return getattr(self.draw_area, method)(*args, **kwargs)
		return wrapper


def test():
	from os.path import join
	from pathlib import Path
	from PIL import ImageFont

	source_dir = str(Path(__file__).absolute().parent.parent)  # .../Source
	resources_dir = join(source_dir, "Resources")  # .../Source/Resources
	small_font = ImageFont.truetype(join(resources_dir, "FiraCode-Bold.ttf"), size=16)

	canvas = Canvas([500, 500])
	canvas.text((10, 10), "Hello", fill=(255, 255, 255), font=small_font)
	canvas.resize((200, 200))
	canvas.show()



if __name__ == '__main__':
	test()
