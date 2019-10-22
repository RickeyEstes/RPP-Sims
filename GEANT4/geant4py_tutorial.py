#----------imports----------#
from Geant4 import *
import g4py.ezgeom
from g4py.ezgeom import G4EzVolume
import g4py.NISTmaterials
import g4py.EMSTDpl
import g4py.ParticleGun, g4py.MedicalBeam

import matplotlib.pyplot as plt
import random
import time
import thread
import numpy as np
#----file imports--------#
from geom_constructor import GeomConstructor 
# from beam import BeamInitializer
from beam2 import MyPrimaryGeneratorAction, MyRunAction, MyEventAction, MySteppingAction, MyField, Plotter

global std_dev_pos_x_right_LIST
global std_dev_pos_x_left_LIST
global std_dev_pos_y_right_LIST
global std_dev_pos_y_left_LIST
global std_dev_pos_z_right_LIST
global std_dev_pos_z_left_LIST

std_dev_pos_x_right_LIST = []
std_dev_pos_x_left_LIST = []
std_dev_pos_y_right_LIST = []
std_dev_pos_y_left_LIST = []
std_dev_pos_z_right_LIST = []
std_dev_pos_z_left_LIST = []

PLT = Plotter()

class Constructor(object):
	def __init__(self):
		# from EZsim.EZgeom import G4EzVolume
		g4py.NISTmaterials.Construct()
		# set DetectorConstruction to the RunManager
		# G4VUserDetectorConstruction.Construct()
		g4py.ezgeom.Construct()
		exN03PL = g4py.EMSTDpl.PhysicsListEMstd()
		gRunManager.SetUserInitialization(exN03PL)
		# reset world material
		air= gNistManager.FindOrBuildMaterial("G4_AIR")
		# g4py.ezgeom.SetWorldMaterial(air)

		# myDC= MyDetectorConstruction()
		# gRunManager.SetUserInitialization(myDC)



	def construct(self):
		# dummy box
		GC = GeomConstructor()
		# GC.ConstructBox("Detector Box", air, [0., 0., 0.], cm, [20., 20., 40.])

		# calorimeter placed inside the box
		# cal= G4EzVolume("Calorimeter") #initialize volume
		nai= gNistManager.FindOrBuildMaterial("G4_SODIUM_IODIDE")
		material1 = G4Material.GetMaterial("G4_W")

		# GC.ConstructOrb("Orb", nai, [10., 10., 10.], cm, 10.)

		# GC.ConstructTube("Tube", au, [-1., -1., -1.], cm, 10., 30., 30., 0, 300.)
		scale_factor = 5
		# GC.ConstructSphere("Sphere", material1 , [0., 0., 0.], cm, 0, 1., 0., 360., 0., 180)
		# GC.ConstructSphere("Sphere", material1 , [0., 0., 0.], cm, 9.5*scale_factor, 10.*scale_factor, 0., 360., 0., 180)

	# GC.ConstructCone("Cone", nai, [-20., -20., -20.], cm, 0., 20., 0., 0., 25., 0., 180) # dphi = 359.9999 is basically 360, but we can still see it
		# gRunManager.Initialize()


class Visualizer(object):

	def visualizer(self, view_angle):
		# time.sleep(.1)

		gApplyUICommand("/vis/sceneHandler/create OGLSX OGLSX")
		gApplyUICommand("/vis/viewer/create OGLSX oglsxviewer")
		gApplyUICommand("/vis/drawVolume")
		# gApplyUICommand("/globalField/verbose level")
		# gApplyUICommand("/MagneticFieldModels/UniformField/SetBVec 3. 1. 1. Tesla")

		gApplyUICommand("/vis/viewer/select oglsxviewer")
		gApplyUICommand("/vis/ogl/set/displayListLimit 100000")
		gApplyUICommand("/vis/scene/add/trajectories")

		gApplyUICommand("/tracking/storeTrajectory 1")
		gApplyUICommand("/vis/scene/endOfEventAction accumulate")
		gApplyUICommand("/vis/scene/endOfRunAction accumulate")

		gApplyUICommand("/vis/viewer/set/viewpointThetaPhi 0" + str(angle))
		gApplyUICommand("/vis/viewer/zoom 1.00001")
		
		gApplyUICommand("/vis/viewer/update")



if __name__ == '__main__':
	Constructor = Constructor()
	Constructor.construct()
	VIS = Visualizer()

	initialMomenta = []
	finalMomenta = []

	angle = 35
	zoom = 1.5
	be_ratio = np.arange(1e-7, 1e-2, .00005) # ratio between magnetic field (varied) and particle energy (fixed @ 2.5 MeV)
	# be_ratio = [1]
	print(len(be_ratio))
	time.sleep(1)

	for be in be_ratio:

		# angle += 0.075 # +0.075 is a recommended delta theta
		# for be in be_ratio:
		print "\n", "NEW BE_RATIO: ", be, "\n"
		# time.sleep(1)

		PLT # initialize the x y z lists for the plotter
		# set user actions ...
		PGA_1 = MyPrimaryGeneratorAction()
		gRunManager.SetUserAction(PGA_1)

		myEA = MyEventAction()
		gRunManager.SetUserAction(myEA)

		mySA = MySteppingAction()
		gRunManager.SetUserAction(mySA)


		vectorList = [
				# [1., 1., 1.], 
			 	# [10., 10., 10.]
			 	list(np.multiply([1, 1, 1], be))
			 	# list(np.multiply([0, 0.1, 0.1], be))
			 	# list(np.multiply([0.1, 0.1, 0.1], be))
			 	# list(np.multiply([0.1, 0.1, 0.1], be))
			 	# list(np.multiply([0.1, 0.1, 0.1], be))
			 	# list(np.multiply([0.1, 0.1, 0.1], be))

			 	# [0., 0., 1]
			 	# [0,0,0]
			 ]
		for v in vectorList: 
			fieldMgr = gTransportationManager.GetFieldManager()
			myField = G4UniformMagField(G4ThreeVector(v[0],v[1],v[2]))
			# myField = MyField(1)
			fieldMgr.SetDetectorField(myField)
			fieldMgr.CreateChordFinder(myField)
			# print "|B-field| = ", vectorList[0][0]

		myRA = MyRunAction()
		gRunManager.SetUserAction(myRA)
		# px, py, pz = PLT.listReturner()
		# print len(px), len(py), len(pz)
		# PLT.grapher() 

		gRunManager.Initialize()

		# scoreSD= ScoreSD()
		# myDC.SetSDtoScoreVoxel(scoreSD)

		gRunManager.BeamOn(1)
		std_devs_LIST = PLT.dataReturner()
		PLT.wipeData()

		VIS.visualizer(angle)



		std_dev_pos_x_right_LIST = std_devs_LIST[0]
		std_dev_pos_x_left_LIST = std_devs_LIST[1]
		std_dev_pos_y_right_LIST = std_devs_LIST[2]
		std_dev_pos_y_left_LIST = std_devs_LIST[3]
		std_dev_pos_z_right_LIST = std_devs_LIST[4]
		std_dev_pos_z_left_LIST = std_devs_LIST[5]

		print std_dev_pos_x_right_LIST
		print std_dev_pos_x_left_LIST
		print std_dev_pos_y_right_LIST
		print std_dev_pos_y_left_LIST
		print std_dev_pos_z_right_LIST
		print std_dev_pos_z_left_LIST
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.plot(be_ratio, std_dev_pos_x_right_LIST, label='std_dev_pos_x_right')
	ax1.plot(be_ratio, std_dev_pos_x_left_LIST, label='std_dev_pos_x_left')
	ax1.plot(be_ratio, std_dev_pos_y_right_LIST, label='std_dev_pos_y_right')
	ax1.plot(be_ratio, std_dev_pos_y_left_LIST, label='std_dev_pos_y_left')
	ax1.plot(be_ratio, std_dev_pos_z_right_LIST, label='std_dev_pos_z_right')
	ax1.plot(be_ratio, std_dev_pos_z_left_LIST, label='std_dev_pos_z_left')	
	
	plt.xlabel("Ratio of B-field to Particle Beam Energy", fontsize=20)
	plt.ylabel("Std. Dev. of Particle Cluster", fontsize=20)
	plt.legend(loc='upper right')
	# plt.scatter(be_ratio, std_dev_pos_x_right_LIST)
	plt.show()











