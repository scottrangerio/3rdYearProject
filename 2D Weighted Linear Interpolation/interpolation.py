from sys import path, stderr
path.insert(0, '../Shared')

from point import Point
from statistics import mean
from collections import Sequence

def interpolate(pointOne, pointTwo, steps, startEndInclusive, weights):
	# The distances between each point's coordinates in cartasian space
	if isinstance(weights, Sequence) == False:
		print("The weights provided are not a sequence", file=stderr)
		return

	if validateWeights(weights) == False:
		print("Invalid weights provided", file=stderr)
		return

	xDistance = abs(pointOne.x - pointTwo.x)
	yDistance = abs(pointOne.y - pointTwo.y)
	intervals = steps + 1

	xDistancePerStep = xDistance / intervals
	yDistancePerStep = yDistance / intervals

	interpolatedPoint = pointOne.copy()

	if startEndInclusive:
		yield pointOne

	for index in range(0, steps):
		if pointOne.x < pointTwo.x:
			interpolatedPoint.x += xDistancePerStep * weights[index]
		elif pointOne.x > pointTwo.x:
			interpolatedPoint.x -= xDistancePerStep * weights[index]

		if pointOne.y < pointTwo.y:
			interpolatedPoint.y += yDistancePerStep * weights[index]
		elif pointOne.y > pointTwo.y:
			interpolatedPoint.y -= yDistancePerStep	* weights[index]

		yield interpolatedPoint

	if startEndInclusive:
		yield pointTwo

def validateWeights(weights):
	return mean(weights) == 1

for point in interpolate(Point(1,1), Point(6, 6), 4, True, [3, 0.5, 0.5, 0.5, 0.5]):
	print(point)