from panda3d.core import Vec2
from math import sin, cos, radians, degrees
from pandac.PandaModules import Point2
from steering import SteeringOutput
from utils import directionInDegrees, clampVectorLength, clampValue, MAX_VELOCITY, MAX_ROTATIONAL_VELOCITY

class Kinematic:

	def __init__(self, pos, heading, speed, pandaObject, fieldLimit):
		self.halfField = fieldLimit / 2
		self.position = pos
		rads = radians(heading)
		#self.orientation = rads		# orientation is same as direction of travel
		self.velocity = Vec2(cos(rads), sin(rads)) * speed
		self.rotation = 0				# angular velocity
		self.pandaObject = pandaObject	# 
	
	def update(self, dt, steering):
		if steering == None:
			steering = SteeringOutput(0, 0)

		self.position += self.velocity * dt
		self.orientation += self.rotation * dt
		
		self.velocity += steering.linear * dt
		self.rotation += steering.angular * dt
		
		clampVectorLength(self.velocity, MAX_VELOCITY)
		self.rotation = clampValue(self.rotation, -MAX_ROTATIONAL_VELOCITY, MAX_ROTATIONAL_VELOCITY)
		
		# Perform wrap-around
		if self.position.getX() <= -self.halfField:
			self.position.setX(self.halfField)
		elif self.position.getX() >= self.halfField:
			self.position.setX(-self.halfField)
		elif self.position.getY() <= -self.halfField:
			self.position.setY(self.halfField)
		elif self.position.getY() >= self.halfField:
			self.position.setY(-self.halfField)
			
		self.pandaObject.setPos(self.position.getX(), self.position.getY(), 0)
		vel = self.velocity
		self.pandaObject.setH(directionInDegrees(vel) - 90)	# point in direction of movement
	
	def distance(self, other):
		return (self.position - other.position).length()
	
	def directionTo(self, other):
		return directionInDegrees(other.position-self.position)

	def __str__(self):
		return "ID=%d Pos=%s Vel=%s Speed=%f Radius=%f" % \
		        (self.id, self.pos.__str__(), self.vel.__str__(), self.speed, self.rad)


if __name__ == "__main__":
	o1 = Kinematic(Point2(5, 0), 45, 5, None, 100)
	o2 = Kinematic(Point2(3, -3), 135, 1, None, 100)
	print(o1.distance(o2))
	print(o1.directionTo(o2))
