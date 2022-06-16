#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.06.16                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import math
from PIL import ImageDraw
from typing import Set, Tuple, Union


def check_params(function_name: str, **params) -> None:
	for name, value in params.items():
		if(value is None):
			raise Exception(f"Parameter '{name}' cannot be None for Arrow::{function_name}")


class Arrow:
	DEFAULT_ANGLE = 25
	DEFAULT_LENGTH = 20

	X, Y = 0, 1
	MIN, MAX = 0, 1


	def __init__(self, tip_point: set, line_angle: float=None, *, draw_area: ImageDraw=None, start_point: set=None,
	  head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH):
		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::()")
		self.draw_area: ImageDraw = draw_area
		self.head_angle: float = head_angle
		self.head_length: int = head_length
		self.start_point: set = start_point
		self.line_angle: float = line_angle
		self.tip_point: set = tip_point


	# ————————————————————————————————————————————————————— DRAW ————————————————————————————————————————————————————— #

	def draw(self: object=None, *, draw_area: ImageDraw=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> bool:
		if(self is not None):
			draw_area = self.draw_area if(draw_area is None) else draw_area
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("draw", **{"start_point": start_point, "draw_area": draw_area, "tip_point": tip_point,
		  "head_angle": head_angle, "head_length": head_length})

		Arrow.draw_head(self, draw_area=draw_area, line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		draw_area.line(start_point+tip_point, fill=(255, 255, 255))


	def draw_head(self: object=None, *, draw_area: ImageDraw=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> None:
		if(self is not None):
			draw_area = self.draw_area if(draw_area is None) else draw_area
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("draw_head", **{"draw_area": draw_area, "tip_point": tip_point, "head_angle": head_angle,
		  "head_length": head_length})

		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::draw_head")

		line_angle: float = Arrow.calculate_line_angle(start_point, tip_point) if(line_angle is None) else line_angle
		point1 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		point2 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=-head_angle,
		  head_length=head_length)

		draw_area.polygon((tip_point, point1, point2), fill=(255, 255, 255))


	# ————————————————————————————————————————————————— CALCULATIONS ————————————————————————————————————————————————— #

	def dimensions(self: object=None, *, draw_area: ImageDraw=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> Set[int]:
		if(self is not None):
			draw_area = self.draw_area if(draw_area is None) else draw_area
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("dimensions", **{"start_point": start_point, "tip_point": tip_point, "head_angle": head_angle,
		  "head_length": head_length})

		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::draw_head")

		line_angle: float = Arrow.calculate_line_angle(start_point, tip_point) if(line_angle is None) else line_angle
		point1 = Arrow.head_point(line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		point2 = Arrow.head_point(line_angle=line_angle, tip_point=tip_point, head_angle=-head_angle,
		  head_length=head_length)

		points = [point1, point2, start_point, tip_point]
		# [[x_min, y_min], [x_max, y_max]]
		min_max = [[points[0][Arrow.X], points[0][Arrow.Y]], [points[0][Arrow.X], points[0][Arrow.Y]]]
		for point in points:
			for xy in range(2):
				min_max[Arrow.MIN][xy] = point[xy] if(point[xy] < min_max[Arrow.MIN][xy]) else min_max[Arrow.MIN][xy]
				min_max[Arrow.MAX][xy] = point[xy] if(point[xy] > min_max[Arrow.MAX][xy]) else min_max[Arrow.MAX][xy]

		return min_max


	def head_point(self: object=None, *, head_angle: float=None, head_length: int=None, line_angle: float=None,
	  tip_point: set=None) -> Union[Tuple[int, int], None]:
		if(self is not None):
			line_angle = self.line_angle if(line_angle is None) else line_angle
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("head_point", **{"line_angle": line_angle, "tip_point": tip_point, "head_angle": head_angle,
		  "head_length": head_length})

		vector_x = math.cos(math.radians(head_angle - 180)) * head_length
		vector_y = math.sin(math.radians(head_angle - 180)) * head_length

		cos_line_angle = math.cos(math.radians(line_angle))
		sin_line_angle = math.sin(math.radians(line_angle))

		x_rotation = vector_x * cos_line_angle - vector_y * sin_line_angle
		y_rotation = vector_x * sin_line_angle + vector_y * cos_line_angle

		x_tranlation = x_rotation + tip_point[0]
		y_tranlation = y_rotation + tip_point[1]

		return (x_tranlation, y_tranlation)


	@staticmethod
	def calculate_line_angle(start: set, end: set) -> float:
		if(end[0] == start[0]):
			return 90.0 if(end[1] > start[1]) else -90

		line_angle: float = math.degrees(math.atan((end[1]-start[1]) / (end[0]-start[0])))

		if(end[0] < start[0]):
			line_angle -= 180

		return line_angle


def test():
	from PIL import Image

	image = Image.new(mode="RGBA", size=[600, 600])
	draw_area = ImageDraw.Draw(image)

	start = (100, 300)
	end = (500, 300)
	arrow = Arrow(end, draw_area=draw_area, start_point=start)
	arrow.draw()
	print(arrow.dimensions())


	start = (100, 100)
	end = (500, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	arrow = Arrow(end, line_angle, draw_area=draw_area)
	arrow.draw_head()
	draw_area.line(start+end, fill=(255, 255, 255))

	start = (500, 100)
	end = (100, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	Arrow.draw_head(draw_area=draw_area, line_angle=line_angle, tip_point=end)
	draw_area.line(start+end, fill=(255, 255, 255))

	start = (300, 100)
	end = (300, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	Arrow.draw(draw_area=draw_area, line_angle=line_angle, start_point=start, tip_point=end)
	print(Arrow.dimensions(draw_area=draw_area, line_angle=line_angle, start_point=start, tip_point=end))

	image.show()


if __name__ == '__main__':
	test()
