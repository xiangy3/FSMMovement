from pandac.PandaModules import OrthographicLens, TransparencyAttrib, loadPrcFileData, Point2, Vec2
from utils import directionInDegrees, directionalVector, clampVectorLength, MAX_VELOCITY,\
	randomBinomial
from FSMExamples import *


class SteeringOutput:
	def __init__(self, acceleration, angluarVelocity):
		self.linear = acceleration
		self.angular = angluarVelocity
		
	def __str__(self):
		return "(%f,%f)" % (self.linear, self.angular)

class PlayerAndMovement:
	def __init__(self, kinematic, steering):
		self.kinematic = kinematic
		self.steering = steering
	
	def update(self, dt):
		steeringInstruction = self.steering.getSteering()
		self.kinematic.update(dt, steeringInstruction)


class KinematicLinear:
	def __init__(self, character):
		self.character = character
	def getSteering(self):
		return SteeringOutput(0, 0)

class KinematicStop:
	def __init__(self, character):
		self.character = character
	def getSteering(self):
		negVelocity = -self.character.velocity
		return SteeringOutput(negVelocity*2, 0)

class KinematicStationary(KinematicStop):
	def __init__(self, character):
		KinematicStop.__init__(self, character)
			
class KinematicCircular:
	def __init__(self, character):
		self.character = character
	def getSteering(self):
		currHeading = directionInDegrees(self.character.velocity) + 5
		speed = self.character.velocity.length()
		newVelocity = directionalVector(currHeading, 10*speed)
		return SteeringOutput(newVelocity, 0)

class KinematicSeek:
	def __init__(self, character, target):
		self.character = character
		self.target = target
		
	def getSteering(self):
		dirToTarget = self.target.position - self.character.position
		dirToTarget.normalize();
		steeringVelocity = dirToTarget * MAX_VELOCITY
		return SteeringOutput(steeringVelocity, 0)

class KinematicFlee:
	def __init__(self, character, target):
		self.character = character
		self.target = target
		
	def getSteering(self):
		dirToTarget = -(self.target.position - self.character.position)
		dirToTarget.normalize();
		steeringVelocity = dirToTarget * MAX_VELOCITY
		return SteeringOutput(steeringVelocity, 0)

class KinematicWander:
	def __init__(self, character):
		self.character = character
		
	def getSteering(self):
		currVelocity = self.character.velocity
		currSpeed = currVelocity.length()
		currHeading = directionInDegrees(currVelocity)
		
		newHeading = currHeading + randomBinomial() * 10
		targetVelocity = directionalVector(newHeading, currSpeed)
		steeringVelocity = (targetVelocity - currVelocity) / 0.05
		print(steeringVelocity)
		return SteeringOutput(steeringVelocity, 0)
	
class KinematicSeekAndArrive:
	def __init__(self, character, target):
		self.character = character
		self.target = target
		self.satisfactionRadius = 100
		self.timeToTarget = 1
		
	def getSteering(self):
		dirToTarget = self.target.position - self.character.position
		distance = dirToTarget.length() 
		if distance < self.satisfactionRadius:
			return KinematicStop(self.character).getSteering()
		
		requiredSpeed = distance / self.timeToTarget
		steeringVelocity = dirToTarget
		steeringVelocity.normalize();
		if requiredSpeed > MAX_VELOCITY:
			steeringVelocity *= MAX_VELOCITY
		else:
			steeringVelocity *= requiredSpeed
		return SteeringOutput(steeringVelocity, 0)

class KinematicFSM:
	def __init__(self, character, target, FSM, steerings):
		self.character = character
		self.target = target
		self.fsm = FSM
		self.steerings = steerings

	def processInput(self, inputInfo):
		self.fsm.request(inputInfo)
		print(self.fsm.state)
		
	def getSteering(self):
		return self.steerings[self.fsm.state].getSteering()
