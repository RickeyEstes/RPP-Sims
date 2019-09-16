from Geant4 import *
import g4py.ezgeom
from g4py.ezgeom import G4EzVolume
import g4py.NISTmaterials
import g4py.EMSTDpl



# def ConstructGeom():
# 	print "* Constructing geometry..."
# 	g4py.ezgeom.Construct()
# 	g4py.NISTmaterials.Construct()
# 	# reset world material
# 	air= G4Material.GetMaterial("G4_AIR")
# 	g4py.ezgeom.SetWorldMaterial(air)

# 	# a target box is placed
# 	global target
# 	target= G4EzVolume("Target")
# 	au= G4Material.GetMaterial("G4_Au")
# 	target.CreateTubeVolume(au, 0., 1.*cm, 1.*mm)
# 	target.PlaceIt(G4ThreeVector(0.,0.,-10.*cm))

# ConstructGeom()

# from EZsim.EZgeom import G4EzVolume
g4py.NISTmaterials.Construct()
# set DetectorConstruction to the RunManager
g4py.ezgeom.Construct()
exN03PL = g4py.EMSTDpl.PhysicsListEMstd()
gRunManager.SetUserInitialization(exN03PL)
# reset world material
air= gNistManager.FindOrBuildMaterial("G4_AIR")
g4py.ezgeom.SetWorldMaterial(air)
# dummy box
detector_box=G4EzVolume("DetectorBox")
detector_box.CreateBoxVolume(air, 20.*cm, 20.*cm, 40.*cm)
detector_box.PlaceIt(G4ThreeVector(0.,0.,20.*cm))
# calorimeter placed inside the box
cal= G4EzVolume("Calorimeter")
nai= gNistManager.FindOrBuildMaterial("G4_SODIUM_IODIDE")
cal.CreateBoxVolume(nai, 5.*cm, 5.*cm, 30.*cm)
dd= 5.*cm
for ical in range(-1, 2):
	calPos= G4ThreeVector(dd*ical, 0., 0.)
	cal.PlaceIt(calPos, ical+1, detector_box)
gRunManager.Initialize()

while True:
	gApplyUICommand("/vis/sceneHandler/create OGLSX OGLSX")
	gApplyUICommand("/vis/viewer/create OGLSX oglsxviewer")
	gApplyUICommand("/vis/drawVolume")
	gApplyUICommand("/vis/viewer/update")