# image1  = slicer.app.layoutManager().sliceWidget("Red").sliceLogic().GetBackgroundLayer().GetVolumeNode()
# image1Name = image1.GetName()
# image1 = sitk.ReadImage( sitkUtils.GetSlicerITKReadWriteAddress( image1Name ) )

# image2  = slicer.app.layoutManager().sliceWidget("Red").sliceLogic().GetBackgroundLayer().GetVolumeNode()
# image2Name = image2.GetName()
# image2 = sitk.ReadImage( sitkUtils.GetSlicerITKReadWriteAddress( image2Name ) )


# lilImage = sitk.AddImageFilter(image1,image2)

# newNode=slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
# slicer.mrmlScene.AddNode(newNode)
# newNode.SetName('cuby')
# sitk.WriteImage( lilImage, sitkUtils.GetSlicerITKReadWriteAddress( newNode.GetName() ) )


imageArray= []
vtkCollection = slicer.mrmlScene.GetNodesByClass('vtkMRMLScalarVolumeNode')
for i in range(vtkCollection.GetNumberOfItems()):
	imageArray.append(sitk.ReadImage( sitkUtils.GetSlicerITKReadWriteAddress( vtkCollection.GetItemAsObject(i).GetName() ) ))

avgImage = imageArray[0]
for i in range(1,len(imageArray)):
	avgImage += imageArray[i]

avgImage /= len(imageArray)
avgImageNode=slicer.mrmlScene.CreateNodeByClass('vtkMRMLScalarVolumeNode')
slicer.mrmlScene.AddNode(avgImageNode)
avgImageNode.SetName('avgImage')
sitk.WriteImage( avgImage, sitkUtils.GetSlicerITKReadWriteAddress( avgImageNode.GetName() ) )