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
from typing import Set, Tuple, Union


from Classes.Canvas import Canvas


def check_params(function_name: str, **params) -> None:
	for name, value in params.items():
		if(value is None):
			raise Exception(f"Parameter '{name}' cannot be None for Arrow::{function_name}")


class Arrow:
	DEFAULT_ANGLE = 25
	DEFAULT_LENGTH = 20

	X, Y = 0, 1
	MIN, MAX = 0, 1


	def __init__(self, tip_point: set, *, line_angle: float=None, canvas: Canvas=None, start_point: set=None,
	  head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH):
		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::()")
		self.canvas: Canvas = canvas
		self.head_angle: float = head_angle
		self.head_length: int = head_length
		self.start_point: set = start_point
		self.line_angle: float = line_angle
		self.tip_point: set = tip_point


	# ————————————————————————————————————————————————————— DRAW ————————————————————————————————————————————————————— #

	def draw(self: object=None, *, canvas: Canvas=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> bool:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("draw", **{"start_point": start_point, "canvas": canvas, "tip_point": tip_point,
		  "head_angle": head_angle, "head_length": head_length})

		Arrow.draw_head(self, canvas=canvas, line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		canvas.line(start_point+tip_point, fill=(255, 255, 255))


	def draw_head(self: object=None, *, canvas: Canvas=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> None:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("draw_head", **{"canvas": canvas, "tip_point": tip_point, "head_angle": head_angle,
		  "head_length": head_length})

		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::draw_head")

		line_angle: float = Arrow.calculate_line_angle(start_point, tip_point) if(line_angle is None) else line_angle
		point1 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		point2 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=-head_angle,
		  head_length=head_length)

		canvas.polygon((tip_point, point1, point2), fill=(255, 255, 255))


	# ————————————————————————————————————————————————— CALCULATIONS ————————————————————————————————————————————————— #

	def bounds(self: object=None, *, canvas: Canvas=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> Set[int]:
		if(self is not None):
			canvas = self.canvas if(canvas is None) else canvas
			line_angle = self.line_angle if(line_angle is None) else line_angle
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point
			head_angle = self.head_angle if(head_angle is None) else head_angle
			head_length = self.head_length if(head_length is None) else head_length

		check_params("bounds", **{"start_point": start_point, "tip_point": tip_point, "head_angle": head_angle,
		  "head_length": head_length})

		if(line_angle is None and start_point is None):
			raise Exception("'line_angle' and 'start_point' cannot both be None for Arrow::draw_head")

		line_angle: float = Arrow.calculate_line_angle(start_point, tip_point) if(line_angle is None) else line_angle
		point1 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=head_angle,
		  head_length=head_length)
		point2 = Arrow.head_point(self, line_angle=line_angle, tip_point=tip_point, head_angle=-head_angle,
		  head_length=head_length)

		points = [point1, point2, start_point, tip_point]
		# [[x_min, y_min], [x_max, y_max]]
		bounds = [[points[0][Arrow.X], points[0][Arrow.Y]], [points[0][Arrow.X], points[0][Arrow.Y]]]
		for point in points:
			for xy in range(2):
				bounds[Arrow.MIN][xy] = point[xy] if(point[xy] < bounds[Arrow.MIN][xy]) else bounds[Arrow.MIN][xy]
				bounds[Arrow.MAX][xy] = point[xy] if(point[xy] > bounds[Arrow.MAX][xy]) else bounds[Arrow.MAX][xy]

		return bounds


	def center(self: object=None, *, start_point: set=None, tip_point: set=None) -> Set[int]:
		if(self is not None):
			start_point = self.start_point if(start_point is None) else start_point
			tip_point = self.tip_point if(tip_point is None) else tip_point

		check_params("center", **{"start_point": start_point, "tip_point": tip_point})

		return ((tip_point[0] + start_point[0]) / 2, (tip_point[1] + start_point[1]) / 2)


	def dimensions(self: object=None, *, canvas: Canvas=None, line_angle: float=None, start_point: set=None,
	  tip_point: set=None, head_angle: float=DEFAULT_ANGLE, head_length: int=DEFAULT_LENGTH) -> Set[int]:
		bounds = Arrow.bounds(self, canvas=canvas, line_angle=line_angle, start_point=start_point,
		  tip_point=tip_point, head_angle=head_angle, head_length=head_length)

		MAX, MIN = Arrow.MAX, Arrow.MIN
		X, Y = Arrow.X, Arrow.Y
		return [bounds[MAX][X] - bounds[MIN][X], bounds[MAX][Y] - bounds[MIN][Y]]


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

		return (int(x_tranlation), int(y_tranlation))


	@staticmethod
	def calculate_line_angle(start: set, end: set) -> float:
		if(end[0] == start[0]):
			return 90.0 if(end[1] > start[1]) else -90

		line_angle: float = math.degrees(math.atan((end[1]-start[1]) / (end[0]-start[0])))

		if(end[0] < start[0]):
			line_angle -= 180

		return line_angle


	# ———————————————————————————————————————————————— TRANSFORMATION ———————————————————————————————————————————————— #

	def translate(self, x: int, y: int) -> None:
		self.tip_point = (self.tip_point[Arrow.X]+x, self.tip_point[Arrow.Y]+y)

		if(self.start_point is not None):
			self.start_point = (self.start_point[Arrow.X]+x, self.start_point[Arrow.Y]+y)



def test():
	from PIL import Image

	image = Image.new(mode="RGBA", size=[600, 600])
	canvas = Canvas.Draw(image)

	start = (100, 300)
	end = (500, 300)
	arrow = Arrow(end, canvas=canvas, start_point=start)
	arrow.draw()
	print(arrow.dimensions())


	start = (100, 100)
	end = (500, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	arrow = Arrow(end, canvas=canvas, line_angle=line_angle)
	arrow.draw_head()
	canvas.line(start+end, fill=(255, 255, 255))

	start = (500, 100)
	end = (100, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	Arrow.draw_head(canvas=canvas, line_angle=line_angle, tip_point=end)
	canvas.line(start+end, fill=(255, 255, 255))

	start = (300, 100)
	end = (300, 500)
	line_angle: float = Arrow.calculate_line_angle(start, end)
	Arrow.draw(canvas=canvas, line_angle=line_angle, start_point=start, tip_point=end)
	print(Arrow.dimensions(canvas=canvas, line_angle=line_angle, start_point=start, tip_point=end))

	image.show()


if __name__ == '__main__':
	test()
