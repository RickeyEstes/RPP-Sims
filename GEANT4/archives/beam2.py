#----------imports----------#
from Geant4 import * 
import random
import numpy as np
import scipy.stats as ss
from scipy.signal import find_peaks
import pandas as pd
import seaborn as sns  # for nicer graphics

## matplotlib stuff
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from time import sleep
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import time


global bound_lower
global bound_upper

bound_lower = 490 # only consider the cluster within these bounds, range of 100
bound_upper = bound_lower + 400
# bound_upper = 550

global vectorCount
vectorCount = 500 # number of scattered e+ per run

# global energy
# energy = SP.sendEnergy()

global pos_3D_right
pos_3D_right = []
global n_sd_pos_3D_right_LIST
sd_pos_3D_right_LIST = []
global n_pos_3D_right_LIST
n_pos_3D_right_LIST = []
global n_sd_pos_3D_right_LIST
n_sd_pos_3D_right_LIST = []

global pos_3D_left
pos_3D_left = []
global n_sd_pos_3D_left_LIST
sd_pos_3D_left_LIST = []
global n_pos_3D_left_LIST
n_pos_3D_left_LIST = []
global n_sd_pos_3D_left_LIST
n_sd_pos_3D_left_LIST = []

global cluster_time_LIST
cluster_time_LIST = []

global p3D
global px
global py
global pz

p3D = []
px = []
py = []
pz = []


global m3D
global mx
global my
global mz

m3D = []
mx = []
my = []
mz = []

global cluster_sizes_LIST
cluster_sizes_LIST = []

global SEE_count
SEE_count = 0

#--- for a specific cluster ---#
global C_positions_LIST
global C_momenta_LIST

C_positions_LIST = []
C_momenta_LIST = []

#----------code starts here!----------#
class WipeData(object):
	# wipe lists for next data collection
	def wipe(self):
		pos_3D_right[:] = []
		pos_3D_left[:] = []
		p3D[:] = []
		m3D[:] = []
		px[:] = []
		py[:] = []
		pz[:] = []

	def wipeElectronCounter(self):
		SEE_count = 0
		pass

	def wipeTime(self):
		cluster_time_LIST[:] = []

	def wipeComps(self):
		sd_pos_3D_right_LIST[:] = []
		n_pos_3D_right_LIST[:] = []
		n_sd_pos_3D_right_LIST[:] = []
		sd_pos_3D_left_LIST[:] = []
		n_pos_3D_left_LIST[:] = []
		n_sd_pos_3D_left_LIST[:] = []

WIPE = WipeData()

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

# class RecordMomenta

class Plotter(object):
	"graphs 3D positions"

	def __init__(self):
		pass

	def dataCollection(self, posf, momf, tcluster):

		radius = np.sqrt(np.square(posf[0]) + np.square(posf[1]) + np.square(posf[2]))
		# if tcluster > 25: # weird set of outlier <---- INTERESTING PHENOMENON
		# if tcluster > 3 and tcluster < 4:

		# print momf

		p3D.append(posf)
		# print len(p3D)
		m3D.append(momf)

		px.append(posf[0])
		# print "py = ", len(py)
		py.append(posf[1])
		pz.append(posf[2])

		mx.append(momf[0])
		my.append(momf[1])
		mz.append(momf[2])

		if posf[0] < 0 and posf[1] < 0 and posf[2] < 0 and -radius < -bound_lower and -radius > -bound_upper:
			pos_3D_left.append(radius)
			cluster_time_LIST.append(tcluster)
		if posf[0] > 0 and posf[1] > 0 and posf[2] > 0 and radius > bound_lower and radius < bound_upper:
			pos_3D_right.append(radius)
			cluster_time_LIST.append(tcluster)

		radius_lower = np.sqrt(3 * np.square(bound_lower))
		radius_upper = np.sqrt(3 * np.square(bound_upper))


		if radius > bound_lower and radius < bound_upper:
			cluster_time_LIST.append(tcluster)


	def dataAnalysis(self):
		# results = open("RESULTS/results_10212019_1.txt", "a")

		n_pos_3D_right = len(pos_3D_right)
		mean_pos_3D_right = np.mean(pos_3D_right)
		self.std_dev_pos_3D_right = np.std(pos_3D_right)
		if self.std_dev_pos_3D_right == 0:
			self.std_dev_pos_3D_right = 0.0001
		median_pos_3D_right = np.median(pos_3D_right)
		n_sd_pos_3D_right = float(n_pos_3D_right / self.std_dev_pos_3D_right)

		n_pos_3D_left = len(pos_3D_left)
		mean_pos_3D_left = np.mean(pos_3D_left)
		self.std_dev_pos_3D_left = np.std(pos_3D_left)
		if self.std_dev_pos_3D_left == 0:
			self.std_dev_pos_3D_left = 0.0001
		median_pos_3D_left = np.median(pos_3D_left)
		n_sd_pos_3D_left = float(n_pos_3D_left / self.std_dev_pos_3D_left)

		sd_pos_3D_right_LIST.append(self.std_dev_pos_3D_right)
		n_sd_pos_3D_right_LIST.append(n_sd_pos_3D_right)
		n_pos_3D_right_LIST.append(n_pos_3D_right)

		sd_pos_3D_left_LIST.append(self.std_dev_pos_3D_left)
		n_sd_pos_3D_left_LIST.append(n_sd_pos_3D_left)
		n_pos_3D_left_LIST.append(n_pos_3D_left)



	def dataReturner(self):

		return [sd_pos_3D_right_LIST, sd_pos_3D_left_LIST], \
			   [n_pos_3D_right_LIST, n_pos_3D_left_LIST], \
			   [n_sd_pos_3D_right_LIST, n_sd_pos_3D_left_LIST], \
			   cluster_time_LIST, \
			   cluster_sizes_LIST
		pass

	def grapher(self):

		fig = plt.figure()
		# Axes3D.scatter(self.px, self.py, self.pz)

		# first subplot: a 3D scatter plot of positions
		ax = fig.add_subplot(111, projection='3d')
		axmin = -600 
		axmax = 600
		axes = plt.gca()
		axes.set_xlim([axmin,axmax])
		axes.set_ylim([axmin,axmax])
		axes.set_zlim([axmin,axmax])

		ax.set_xlabel('mm')
		ax.set_ylabel('mm')
		ax.set_zlabel('mm')

		ax.scatter(px, py, pz)
		scale_fac = 50
		# for i in np.arange(0, len(px)):
		# 	a = Arrow3D([px[i], px[i] + mx[i]*scale_fac], [py[i], py[i] + my[i]*scale_fac], [pz[i], pz[i] + mz[i]*scale_fac], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
		# 	ax.add_artist(a)


		plt.title("3D Positions of Randomly Scattered e+")

		# plt.draw() 
		
		plt.show()

		# second subplot: a histogram of positions
		# fig, axs = plt.subplots(3, sharey=True, sharex=False, tight_layout=False)

	def computeClusterMomentum(self):
		# pass
		# print clusterCenter

		# positions = open("positions.txt", "a")
		# momenta = open("momenta.txt", "a")

		clusterx = []
		clustery = []
		clusterz = []

		momx = []		
		momy = []
		momz = []

		# print "length of p3D = ", len(p3D)

		for pos in p3D:
			difference = np.sqrt((clusterCenter[0] - pos[0])**2+ \
								 (clusterCenter[1] - pos[1])**2+ \
								 (clusterCenter[2] - pos[2])**2)

			pos_index = p3D.index(pos)

			if difference < 160:
				clusterx.append(pos[0] - clusterCenter[0])
				clustery.append(pos[1] - clusterCenter[1])
				clusterz.append(pos[2] - clusterCenter[2])

				momx.append(m3D[pos_index][0])
				momy.append(m3D[pos_index][1])
				momz.append(m3D[pos_index][2])

		# print "number of clustered positrons = ", len(clusterx)

		# saving data
		C_positions_LIST[:] = []
		C_momenta_LIST[:] = []

		for index in range(len(clusterx)):
			position = [clusterx[index], clustery[index], clusterz[index]]
			momentum = [momx[index], momy[index], momz[index]]
			
			# positions.write("["+ str(position[0])+ ", "+ str(position[1])+ ", "+ str(position[2])+ "]"+"\n")
			# momenta.write("["+ str(momentum[0])+ ", "+ str(momentum[1])+ ", "+ str(momentum[2])+ "]"+"\n")

			C_positions_LIST.append(position)
			C_momenta_LIST.append(momentum)


		print len(C_positions_LIST), "\n", len(C_momenta_LIST)
		fig = plt.figure()
		# Axes3D.scatter(self.px, self.py, self.pz)

		# first subplot: a 3D scatter plot of positions
		ax = fig.add_subplot(111, projection='3d')
		axmin = -160 
		axmax = 160
		axes = plt.gca()
		axes.set_xlim([axmin,axmax])
		axes.set_ylim([axmin,axmax])
		axes.set_zlim([axmin,axmax])

		ax.set_xlabel('mm')
		ax.set_ylabel('mm')
		ax.set_zlabel('mm')

		ax.scatter(clusterx, clustery, clusterz)
		for i in np.arange(0, len(clusterx)):
			a = Arrow3D([clusterx[i], clusterx[i] + 1000*momx[i]], [clustery[i], clustery[i] + 1000*momy[i]], [clusterz[i], clusterz[i] + 1000*momz[i]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
			ax.add_artist(a)


		plt.title("A single cluster")

		# plt.draw() 
		
		plt.show()

	def clusterDataReturner(self):

		positions = C_positions_LIST
		momenta = C_momenta_LIST

		return positions, momenta

	def computeClusterSize(self):
		n_bins = 25
		position_LIST = [px, py, pz]
		for i in position_LIST:
			# fig2, ax2 = plt.subplots(2, sharey=True, sharex=False, tight_layout=False)
			range_LIST = []
			positive = []
			negative = []
			# counts, bins, bars = axs[position_LIST.index(i)].hist(i, bins=n_bins) 
			# print counts, "\n\n", bins

			# separate x, y, z into positive and negative
			for pos in i: 
				# print pos
				if pos > 0:
					positive.append(pos)
				if pos < 0:
					negative.append(pos)
			frame = 0
			for i in [positive, negative]:
				# print "sign change" , i, "\n"
				# plt.hist(i, bins=n_bins)
				counts, bins = np.histogram(i, bins=n_bins)
				counts = list(counts)
				# print counts, "\n\n", "bins", "\n", bins
				for freq in counts:
					# gets rid of any outliers
					if freq not in np.arange(5, 150): 
						index = counts.index(freq)
						np.delete(bins, index)
				# takes the range of each pos/neg without outliers
				rng = np.max(bins) - np.min(bins)
				range_LIST.append(rng)
				# print range_LIST
				frame += 1
			#combines the pos/neg ranges to get the real range
			true_range = np.sum(range_LIST)
			# print true_range
			if true_range < 200:
				cluster_sizes_LIST.append(true_range)
		print "avg cluster size = ", np.mean(cluster_sizes_LIST)
				# print "\n", "Range = ", true_range, "\n"

		# plt.show()

PLT = Plotter()

class MyPrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):
	"My Primary Generator Action"

	def __init__(self, energy, energyUnit, center):
		G4VUserPrimaryGeneratorAction.__init__(self)
		self.particleGun = G4ParticleGun(1)
		# print("\n Particle gun defined \n")
		self.energy = energy
		self.energyUnit = energyUnit
		global clusterCenter
		clusterCenter = center

	def GeneratePrimaries(self, event):
		# Particle param
		#################################################
		locationArray = [0, 0, 0]

		particle = "e+"
		# energy_2 = 2.5
		energyUnit = self.energyUnit 
		dimensionUnit = cm

		energy = self.energy
		self.particleGun.SetParticleByName(particle) # define particle
		self.particleGun.SetParticleEnergy(energy*energyUnit) # define particle energy 

		for i in range(0, vectorCount): # creates random momentum vectors originating from [0, 0, 0]
			mx = random.uniform(-1,1)
			my = random.uniform(-1,1)
			mz = random.uniform(-1,1)
			momentumArray = [mx, my, mz]
			self.particleGun.SetParticlePosition(G4ThreeVector(locationArray[0], locationArray[1], locationArray[2])*dimensionUnit) # define first particle generator location
			self.particleGun.SetParticleMomentumDirection(G4ThreeVector(momentumArray[0], momentumArray[1], momentumArray[2])*dimensionUnit) # define first particle generator momentum
			self.particleGun.GeneratePrimaryVertex(event)
		#################################################

#-------------------------------------------------------------------
class MyRunAction(G4UserRunAction):
	"My Run Action"

	def EndOfRunAction(self, run):
		# PLT.grapher()
		PLT.computeClusterMomentum()
		PLT.computeClusterSize()
		# print(cluster_sizes_LIST)
		PLT.dataAnalysis()
		# WIPE.wipeElectronCounter()
		global SEE_count
		# print SEE_count/2
		# time.sleep(1)
		# SEE_count = 0
		WIPE.wipe()
		# print "*** End of Run"
		# print "- Run sammary : (id= %d, #events= %d)" \
		# % (run.GetRunID(), run.GetNumberOfEventToBeProcessed())

# ------------------------------------------------------------------
class MyEventAction(G4UserEventAction):
	"My Event Action"

	def EndOfEventAction(self, event):
		# print "See count", SEE_count
		pass

# ------------------------------------------------------------------
class MySteppingAction(G4UserSteppingAction):
	"My Stepping Action"

	def UserSteppingAction(self, step):
		preStepPoint = step.GetPreStepPoint()
		postStepPoint = step.GetPostStepPoint()

		# change = step.particleChange()
		track = step.GetTrack()
		parentId = track.GetParentID()
		particleName = track.GetDefinition().GetParticleName() 
		# print particleName
		touchable = track.GetTouchable()
		KE = track.GetKineticEnergy()

		# kinetic energy in MeV - PRE
		# initialKE = preStepPoint.GetKineticEnergy() 
		# kinetic energy in MeV - POST
		# finalKE = postStepPoint.GetKineticEnergy()

		if particleName == 'e+':
			# print "positron"
			p_test = [step.GetDeltaPosition().x,step.GetDeltaPosition().y,step.GetDeltaPosition().z]
			p = [postStepPoint.GetPosition().x, postStepPoint.GetPosition().y, postStepPoint.GetPosition().z] # (mm)
			# p and p_test are the SAME 
			t_test = step.GetDeltaTime()
			t = track.GetGlobalTime() # (ns)
			# t and t_test are the SAME

			m = [postStepPoint.GetMomentum().x, postStepPoint.GetMomentum().y, postStepPoint.GetMomentum().z]
			# m = [step.GetDeltaMomentum().x, step.GetDeltaMomentum().y, step.GetDeltaMomentum().z] # equal to the postStepPoint momentum
			mm = np.sqrt((m[0])**2 + (m[1])**2 + (m[2])**2)
			# momenta - PRE
			initialMomentum = [preStepPoint.GetMomentum().x, preStepPoint.GetMomentum().y, preStepPoint.GetMomentum().z]
			# momenta - POST
			# print KE, "\n", p, "\n", initialMomentum, "\n", finalMomentum, "\n\n" 
			# energy = step.GetTotalEnergyDeposit()
			# print p 
			PLT.dataCollection(p, m, t) # calls data collection and analysis on final positions and momenta
			# return initialMomentum, finalMomentum 
		if particleName == 'e-':
			global SEE_count
			# print "electron"
			SEE_count += 1
			# print SEE_count

