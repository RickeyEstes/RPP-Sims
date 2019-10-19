#----------imports----------#
from Geant4 import * 
import random
import numpy as np
## matplotlib stuff
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import sleep
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

#----------code starts here!----------#
class Plotter(object):
	"graphs 3D momenta"

	def __init__(self):
		self.px = []
		self.py = []
		self.pz = []
	
	def dataCollection(self, final_momentum):
		self.px.append(final_momentum[0])
		self.py.append(final_momentum[1])
		self.pz.append(final_momentum[2])

		self.pos3D = np.sqrt(np.square(self.px) + np.square(self.py) + np.square(self.pz)) # 3D position

		print("DATA STORED")
		print len(self.px), "\n", len(self.py), "\n", len(self.pz), "\n"

	def listReturner(self):
		print("momnenta returned by plotter")
		return self.px, self.py, self.pz

	def grapher(self):
		fig = plt.figure()
		# Axes3D.scatter(self.px, self.py, self.pz)

		# first subplot: a 3D scatter plot of positions
		ax = fig.add_subplot(111, projection='3d')
		axmin = -600 # what units are these???????
		axmax = 600
		axes = plt.gca()
		axes.set_xlim([axmin,axmax])
		axes.set_ylim([axmin,axmax])
		axes.set_zlim([axmin,axmax])

		ax.set_xlabel('X position units')
		ax.set_ylabel('Y position units')
		ax.set_zlabel('Z position units')

		ax.scatter(self.px, self.py, self.pz)

		# second subplot: a histogram of positions
		fig, axs = plt.subplots(4, sharey=True, tight_layout=False)
		n_bins = 100
		axs[0].hist(self.px, bins=n_bins) # histogram of 3D position x
		axs[1].hist(self.py, bins=n_bins) # histogram of 3D position y
		axs[2].hist(self.pz, bins=n_bins) # histogram of 3D position z
		axs[3].hist(self.pos3D, bins=n_bins) # histogram of 3D position magnitude
 
		plt.show()

PLT = Plotter()

class MyPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):
	"My Primary Generator Action"

	def __init__(self):
		G4VUserPrimaryGeneratorAction.__init__(self)
		self.particleGun = G4ParticleGun(1)
		print("\n Particle gun defined \n")

	def GeneratePrimaries(self, event):


		# Particle param
		#################################################
		spaceParamDict = {}
		vectorCount = 1000
		locationArray = [0, 0, 0]

		particle = "e+"

		energy_1 = 2.5
		energy_2 = 2.5
		energyUnit = MeV 
		dimensionUnit = cm

		self.particleGun.SetParticleByName(particle) # define particle
		self.particleGun.SetParticleEnergy(energy_1*energyUnit) # define particle energy 

		for i in range(0,vectorCount): # creates random momentum vectors originating from [0, 0, 0]
			px = random.uniform(-1,1)
			py = random.uniform(-1,1)
			pz = random.uniform(-1,1)
			momentumArray = [px, py, pz]
			self.particleGun.SetParticlePosition(G4ThreeVector(locationArray[0], locationArray[1], locationArray[2])*dimensionUnit) # define first particle generator location
			self.particleGun.SetParticleMomentumDirection(G4ThreeVector(momentumArray[0], momentumArray[1], momentumArray[2])*dimensionUnit) # define first particle generator momentum
			self.particleGun.GeneratePrimaryVertex(event)
		#################################################

#-------------------------------------------------------------------
class MyRunAction(G4UserRunAction):
	"My Run Action"

	def EndOfRunAction(self, run):
		PLT.grapher()
		print "*** End of Run"
		print "- Run sammary : (id= %d, #events= %d)" \
		% (run.GetRunID(), run.GetNumberOfEventToBeProcessed())

# ------------------------------------------------------------------
class MyEventAction(G4UserEventAction):
	"My Event Action"

	def EndOfEventAction(self, event):
		#print "*** dE/dx in current step=", step.GetTotalEnergyDeposit()
		pass

# ------------------------------------------------------------------
class MySteppingAction(G4UserSteppingAction):
	"My Stepping Action"

	def UserSteppingAction(self, step):
		preStepPoint = step.GetPreStepPoint()
		postStepPoint = step.GetPostStepPoint()

		track = step.GetTrack()
		touchable = track.GetTouchable()
		KE = track.GetKineticEnergy()


		# kinetic energy in MeV - PRE
		# initialKE = preStepPoint.GetKineticEnergy() 
		# kinetic energy in MeV - POST
		# finalKE = postStepPoint.GetKineticEnergy()

		m = [track.GetMomentum().x, track.GetMomentum().y, track.GetMomentum().z] # equal to the postStepPoint momentum
		p = [track.GetPosition().x, track.GetPosition().y, track.GetPosition().z]
		mm = np.sqrt((m[0])**2 + (m[1])**2 + (m[2])**2)

		# momenta - PRE
		initialMomentum = [preStepPoint.GetMomentum().x, preStepPoint.GetMomentum().y, preStepPoint.GetMomentum().z]
		# momenta - POST
		finalMomentum = [postStepPoint.GetMomentum().x, postStepPoint.GetMomentum().y, postStepPoint.GetMomentum().z]

		print touchable, "\n", KE, "\n", p, "\n", initialMomentum, "\n", finalMomentum, "\n\n" 
		# energy = step.GetTotalEnergyDeposit()



		PLT.dataCollection(p)
		# PLT.grapher()

		# return initialMomentum, finalMomentum
		pass 

class MyField(G4MagneticField):
	"My Magnetic Field"

	def GetFieldValue(self, pos, time):
		vectorList = [
						# [1., 1., 1.], 
					 	# [10., 10., 10.]
					 	[0.1, 0.1, 0.1]
					 	# [0,0,0]
					 ]
		for v in vectorList:

			bfield = G4ThreeVector()
			bfield.x = v[0]*tesla
			bfield.y = v[1]*tesla
			bfield.z = v[2]*tesla
			# print "\n", "B-field activated", "\n" ### gets rid of other prints for some reason
			return bfield


