from pandac.PandaModules import Vec2, Point2
from math import *
import random

MAX_VELOCITY = 100
MAX_ROTATIONAL_VELOCITY = 90

def getRandom(lo, hi):
	delta = hi - lo
	return random.random() * delta + lo

def directionalVector(heading, speed):
	rads = radians(heading)
	return Vec2(cos(rads), sin(rads)) * speed

def directionInDegrees(vec):
	return degrees(atan2(vec.getY(), vec.getX()))

def clampVectorLength(vec, maxLength):
	if vec.length() > maxLength:
		vec.normalize();
		vec *= maxLength
		
def clampValue(value, lo, hi):
	if value < lo:
		return lo
	elif value > hi:
		return hi
	else:
		return value
	
def randomBinomial():
	return random.random() - random.random()