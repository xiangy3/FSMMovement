from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import OrthographicLens, TransparencyAttrib, loadPrcFileData, Point2, LVector3
from direct.task import Task
import random, sys
from utils import *
from kinematics import *
from steering import *

WINDOW_SZ = 700
AVATAR_RAD = 10

# This helps reduce the amount of code used by loading objects, since all of
# the objects are pretty much the same.
def loadObject(tex, scale, color):
	global loader, camera, render
	# Every object uses the plane model and is parented to the camera
	# so that it faces the screen.
	obj = loader.loadModel("models/plane")
	obj.reparentTo(render)
	obj.setP(-90)

	obj.setScale(scale)
	
	# This tells Panda not to worry about the order that things are drawn in
	# (ie. disable Z-testing).  This prevents an effect known as Z-fighting.
	obj.setBin("unsorted", 0)
	obj.setDepthTest(False)
	obj.setTransparency(TransparencyAttrib.MAlpha)
	
	tex = loader.loadTexture('textures/' + tex)
	obj.setTexture(tex, 1)
	obj.setColor(color)
	
	return obj

class MovementDemo(ShowBase):

	def __init__(self):
		global taskMgr, base
		# Initialize the ShowBase class from which we inherit, which will
		# create a window and set up everything we need for rendering into it.
		ShowBase.__init__(self)
		
		lens = OrthographicLens()
		lens.setFilmSize(WINDOW_SZ, WINDOW_SZ)
		base.cam.node().setLens(lens)

		# Disable default mouse-based camera control.  This is a method on the
		# ShowBase class from which we inherit.
		self.disableMouse()
		
		# point camera down onto x-y plane
		camera.setPos(LVector3(0, 0, 1))
		camera.setP(-90)
		
		self.setBackgroundColor((0, 0, 0, 1))
		self.bg = loadObject("stars.jpg", WINDOW_SZ, (0, 0, 0, 1))
		
		self.accept("escape", sys.exit)  # Escape quits
		self.accept("space", self.newGame, [])  # Escape quits
	
		speed = random.random() * 45 + 5
		N = WINDOW_SZ / 2
		
		targetColor = (1, 0, 0, 1)
		target = loadObject("ship.png", 2*AVATAR_RAD, targetColor)
		targetKinematic = Kinematic(Point2(0, 0), 0, speed, target, WINDOW_SZ)
		#targetSteering = KinematicCircular(targetKinematic)
		#targetSteering = KinematicStationary(targetKinematic)
		targetSteering = KinematicLinear(targetKinematic)
		self.target = PlayerAndMovement(targetKinematic, targetSteering)
		
		avatarColor = (0, 1, 0, 1)
		avatar = loadObject("ship.png", 2*AVATAR_RAD, avatarColor)
		avatarKinematic = Kinematic(Point2(0, 0), 0, speed, avatar, WINDOW_SZ)

		avatarLinear = KinematicLinear(avatarKinematic)
		avatarSeek = KinematicSeek(avatarKinematic, targetKinematic)
		avatarFlee = KinematicFlee(avatarKinematic, targetKinematic)
		steerings = { 'Linear' : avatarLinear, 'Seek' : avatarSeek, 'Flee' : avatarFlee }
		fsm = SteeringFSM()
		self.avatarSteering = KinematicFSM(avatarKinematic, targetKinematic, fsm, steerings)
		self.avatar = PlayerAndMovement(avatarKinematic, self.avatarSteering)
		self.newGame()
		self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")

	def gameLoop(self, task):
		global globalClock
		dt = globalClock.getDt()
		dist = (self.avatar.kinematic.position - self.target.kinematic.position).length()
		if dist < 200:
			self.avatar.steering.processInput('close')
		elif dist < 300:
			self.avatar.steering.processInput('medium')
		else:
			self.avatar.steering.processInput('far')

		self.avatar.update(dt)
		self.target.update(dt)
		return Task.cont
		
	def newGame(self):
		N = WINDOW_SZ / 4
		speed = getRandom(20, 50)
		
		self.avatar.kinematic.position = Point2(-N, -N)
		self.avatar.kinematic.orientation = getRandom(0, 360)
		heading = getRandom(0, 360) 
		self.avatar.kinematic.velocity = directionalVector(heading, speed) 
		
		self.target.kinematic.position = Point2(N, N)
		self.target.kinematic.orientation = getRandom(0, 360)
		heading = getRandom(0, 360) 
		self.target.kinematic.velocity = directionalVector(heading, speed) 
		

loadPrcFileData("", "win-size %d %d" % (WINDOW_SZ, WINDOW_SZ))
demo = MovementDemo()
demo.run()
