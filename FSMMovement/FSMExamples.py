from direct.fsm.FSM import FSM
from random import choice

class AvatarFSM(FSM):
	def __init__(self):
		FSM.__init__(self, 'Avatar Control')
		self.defaultTransitions = None
		self._broadcastStateChanges = None
		self._FSM__requestQueue = None
		self.state = 'Rest'
		self.name = 'Avatar Control'
		
		self.nextState = {
							('Rest', 'low health') : 'Rest',
							('Rest', 'good health') : 'Wander',
							('Rest', 'enemy seen') : 'Flee',
							('Rest', 'enemy disappear') : 'Rest',
							
							('Wander', 'low health') : 'Rest',
							('Wander', 'good health') : 'Wander',
							('Wander', 'enemy seen') : 'Fight',
							('Wander', 'enemy disappear') : 'Wander',
							
							('Fight', 'low health') : 'Flee',
							('Fight', 'good health') : 'Fight',
							('Fight', 'enemy seen') : 'Flee',    # should not happen
							('Fight', 'enemy disappear') : 'Flee',
							  
							('Flee', 'low health') : 'Flee',
							('Flee', 'good health') : 'Fight',
							('Flee', 'enemy seen') : 'Flee',
							('Flee', 'enemy disappear') : 'Rest'
		}
	def enterFight(self):
		print("Enter fight")
	def exitFight(self):
		print("Enter fight")
	def defaultFilter(self, request, args):
		key = (self.state, request)
		return self.nextState.get(key)

class SteeringFSM(FSM):
	def __init__(self):
		FSM.__init__(self, 'Steering')
		self.defaultTransitions = None
		self._broadcastStateChanges = None
		self._FSM__requestQueue = None
		self.state = 'Linear'
		self.name = 'Steering'
		
		self.nextState = {
							('Linear', 'close') : 'Seek',
							('Linear', 'medium') : 'Flee',
							('Linear', 'far') : 'Linear',
							
							('Flee', 'close') : 'Seek',
							('Flee', 'medium') : 'Flee',
							('Flee', 'far') : 'Linear',
									  
							('Seek', 'close') : 'Seek',
							('Seek', 'medium') : 'Seek',
							('Seek', 'far') : 'Linear',
		}
		
	def defaultFilter(self, request, args):
		key = (self.state, request)
		return self.nextState.get(key)
class stateObservationFSM(FSM):
	def __init__(self):
		FSM.__init__(self, 'Avatar Control')
		self.defaultTransitions = None
		self._broadcastStateChanges = None
		self._FSM__requestQueue = None
		self.state = 'sleep'
		self.name = 'Avatar Control'
		
		self.nextState = {
							('sleep', 'tired') : 'sleep',
							('sleep', '!tired') : 'patrol',
							('sleep', 'enemyVisible') : 'defend',
							('sleep', '!enemyVisible') : 'sleep',
							
							('patrol', 'tired') : 'sleep',
							('patrol', '!tired') : 'patrol',
							('patrol', 'enemyVisible') : 'defend',
							('patrol', '!enemyVisible') : 'patrol',
							
							('defend', 'tired') : 'defend',
							('defend', '!tired') : 'defend',
							('defend', 'enemyVisible') : 'defend',
							('defend', '!enemyVisible') : 'patrol',
			
		}
	def defaultFilter(self, request, args):
		key = (self.state, request)
		return self.nextState.get(key)

	
if __name__ == "__main__":
# 	fsm = AvatarFSM()
# 	
# 	states = fsm.nextState.keys()
# 	inputs = ['low health', 'good health', 'enemy seen', 'enemy disappear']
# 	
# 	states = set([state for (state, I) in fsm.nextState.keys()])
# 	
# 	for S in states:
# 		for I in inputs:
# 			fsm.state = S
# 			fsm.request(I)
# 			print("(%s,%s) -> %s)" % (S, I, fsm.state))
	
	fsm=stateObservationFSM()
	states = fsm.nextState.keys()
	inputs = ['tired','!tired','enemyVisible','!enemyVisible']	
	states = set([state for (state, I) in fsm.nextState.keys()])
 	
	for S in states:
		for I in inputs:
			fsm.state = S
			fsm.request(I)
			print("(%s,%s) -> %s)" % (S, I, fsm.state))		
