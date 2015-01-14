import NeedleFinder
import numpy as np
import csv
import random
widget = slicer.modules.NeedleFinderWidget
l = NeedleFinder.NeedleFinderLogic()
import time as t


path = [ 0 for i in range(100)]
path[24] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 24 NRRD/Manual/2013-02-25-Scene-without-CtrPt.mrml'
path[28] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 28 NRRD/Auto-Eval-LB/Scene.mrml'
path[29] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 29 NRRD/Manual/2013-02-26-Scene-without-CtrPts.mrml'
path[30] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 30 NRRD/Manual/2013-02-26-Scene-without-CtrPt.mrml'
path[31] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 31 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[33] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 33 NRRD/Auto-Eval-LB/2013-02-27-Scene.mrml'

path[34] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 34 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
# path[35] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 35 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[37] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 37 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[38] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 38 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[40] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 40 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'

def saveCubes(number):
    slicer.util.loadScene(path[number])
    for i in range(len(l.returnTips())):
        tipPosition = l.ijk2ras(l.returnTips()[i])
        volumeNode = slicer.app.layoutManager().sliceWidget("Red").sliceLogic().GetBackgroundLayer().GetVolumeNode() 
        sImage = sitk.ReadImage( sitkUtils.GetSlicerITKReadWriteAddress( volumeNode.GetName() ) )
        # volumeNode.GetIJKToRASDirectionMatrix(volumeNode)
        backgroundNode  = slicer.app.layoutManager().sliceWidget("Red").sliceLogic().GetBackgroundLayer().GetVolumeNode()
        backgroundNodeName = backgroundNode.GetName()
        backgroundImage = sitk.ReadImage( sitkUtils.GetSlicerITKReadWriteAddress( backgroundNodeName ) )
        bgOrigin=backgroundImage.GetOrigin()
        #
        rimage = sitk.Image(40, 40, 40, sitk.sitkUInt16)
        rimage.SetSpacing([0.5,0.5,0.5])
        #rimage.SetDirection([-1,0,0,0,-1,0,0,0,1])
        rimage.SetOrigin([-tipPosition[0]-10,-tipPosition[1]-10,tipPosition[2]-10]) #-np.array([1,1,1]
        #rimage.SetDirection([1,0,0]
        tx = sitk.Transform()
        #
        lilImage = sitk.Resample(sImage, rimage, tx, sitk.sitkNearestNeighbor, sitk.sitkUInt16)
        newNode=slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
        slicer.mrmlScene.AddNode(newNode)
        newNode.SetName('cuby')
        sitk.WriteImage( lilImage, sitkUtils.GetSlicerITKReadWriteAddress( newNode.GetName() ) )
        lilImage.SetOrigin([0,0,0])
        filename = "/Users/guillaume/Projects/github/NeedleFinderProjectWeek/NeedleTips/"+volumeNode.GetName() + "-"+str(i)+".nii"
        # print filename
        sitk.WriteImage( lilImage, filename )

