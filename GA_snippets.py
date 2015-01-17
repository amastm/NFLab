Guillaume=False #for file paths

print "example usage in slicer python console: geneticAlgorithm(24)"

import random, copy
import operator
import NeedleFinder
import numpy as np
import csv
widget = slicer.modules.NeedleFinderWidget
l = NeedleFinder.NeedleFinderLogic()
import time as t

path = [ 0 for i in range(100)]

#Andres file system (cases copies from AMIGO share)
path[24] = '/home/amastmeyer/Pictures/Case  024/NRRD/Manual/2013-02-25-Scene-without-CtrPt.mrml'
path[29] = '/home/amastmeyer/Pictures/Case  029/NRRD/Manual/2013-02-26-Scene-without-CtrPts.mrml'
path[30] = '/home/amastmeyer/Pictures/Case  030/NRRD/Manual/2013-02-26-Scene-without-CtrPt.mrml'
path[31] = '/home/amastmeyer/Pictures/Case  031/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[34] = '/home/amastmeyer/Pictures/Case  034/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[35] = '/home/amastmeyer/Pictures/Case  035/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[37] = '/home/amastmeyer/Pictures/Case  037/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[38] = '/home/amastmeyer/Pictures/Case  038/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
path[40] = '/home/amastmeyer/Pictures/Case  040/NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'

#MICCAI13 results in Andres files
path[24] = '/home/amastmeyer/Pictures/Case  024/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[28] = '/home/amastmeyer/Pictures/Case  028/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[29] = '/home/amastmeyer/Pictures/Case  029/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[30] = '/home/amastmeyer/Pictures/Case  030/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[31] = '/home/amastmeyer/Pictures/Case  031/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[33] = '/home/amastmeyer/Pictures/Case  033/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[34] = '/home/amastmeyer/Pictures/Case  034/NRRD/Auto-Eval-LB/SceneNoCtrlPts.mrml'
path[37] = '/home/amastmeyer/Pictures/Case  037/NRRD/Manual Alireza/SceneNoCtrlPts.mrml'
path[38] = '/home/amastmeyer/Pictures/Case  038/NRRD/Manual Alireza/SceneNoCtrlPts.mrml'
path[40] = '/home/amastmeyer/Pictures/Case  040/NRRD/Manual Alireza/SceneNoCtrlPts.mrml'

if Guillaume: #Guillaumes file system
  path[24] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 24 NRRD/Manual/2013-02-25-Scene-without-CtrPt.mrml'
  path[29] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 29 NRRD/Manual/2013-02-26-Scene-without-CtrPts.mrml'
  path[30] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 30 NRRD/Manual/2013-02-26-Scene-without-CtrPt.mrml'
  path[31] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 31 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
  path[34] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 34 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
  path[35] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 35 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
  path[37] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 37 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
  path[38] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 38 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'
  path[40] = '/Users/guillaume/Dropbox/AMIGO Gyn Data NRRD (1)/Case 40 NRRD/Manual/2013-02-27-Scene-without-CtrPts.mrml'

def resetNeedleDetection(l, script=False):
  while slicer.util.getNodes('python-catch*') != {}:
    nodes = slicer.util.getNodes('python-catch*')
    for node in nodes.values():
      slicer.mrmlScene.RemoveNode(node)
  l.previousValues=[[0,0,0]]
  l.round=1
  # reset report table
  l.table =None
  l.row=0
  l.initTableView()
  

def costFunction(chrm,caseID, writeResults = True):
  resetNeedleDetection(l,script=True)
  widget.radiusNeedleParameter.setValue(chrm[1])
  widget.sigmaValue.setValue(chrm[2]) # change parameter sigma
  widget.gradientPonderation.setValue(chrm[3])
  widget.exponent.setValue(chrm[4])
  widget.numberOfPointsPerNeedle.setValue(chrm[0])
  l.startValidation(script=True)
  results = l.evaluate(script=True) # calculate HD distances
  if writeResults:
    if Guillaume:
      l.exportEvaluation(results, '/Users/guillaume/Projects/github/NeedleFinderProjectWeek/'+str(caseID)+'.csv')
    else:
      l.exportEvaluation(results, '/home/amastmeyer/'+str(caseID)+'-cost.csv')
  HD=np.array(results)
  # print HD
  cost = np.sum(HD[:,0]>2)
  # cost = 1
  fitness =  1 /float(cost+.00000001)
  results = [cost, fitness]
  return results 

'''
parameters list:

Number of control points:
3 -> 12  +1 int 

Radius (mm):
0.5 -> 5  +0.5  

Sigma :
1 -> 40 +1 int 

Neighborhood ponderation : 
0 -> 25 +1 int 

Center ponderation : 
0 -> 10 +1 int 
'''

rangeTable=[]
rangeTable.append([3,12])
rangeTable.append([1,5])
rangeTable.append([1,40])
rangeTable.append([0,25])
rangeTable.append([0,10])


def geneticAlgorithm(caseID, populationSize=10, nbOfGenerations=100):
  firstTime = 1
  slicer.util.loadScene( path[caseID] )
  # [ctrlpt, radius, sigma, neigh, center]
  popSize=populationSize
  sample_pop =[]
  tried_params = []
  tried_fitness = []
  for i in range(popSize):
    sample_pop.append([np.random.randint(3,12), np.random.randint(1,6), np.random.randint(1,40), np.random.randint(0,25), np.random.randint(0,10)]) # a feasible solution
  if firstTime:
    start = t.time()
    costFunction(sample_pop[0], caseID, False)
    firstTime = 0
    finish = t.time()
    duration = finish - start
    expectedDuration = duration * populationSize * nbOfGenerations
    durationString = (expectedDuration.__divmod__(3600)[0]).__format__('.0f') +'h'
    durationString += (expectedDuration.__divmod__(60)[0]).__format__('.0f')+ 'min'
    durationString += (expectedDuration.__divmod__(60)[1]).__format__('.0f')+ 's'
    message = 'The Genetic Algorithm will take approximately ' +durationString+ ' to complete.'
    message += '\n Do you want to continue?'
    ret = messageBox = qt.QMessageBox.question( qt.QDialog(), 'Attention',message,qt.QMessageBox.Ok, qt.QMessageBox.Cancel)
  for generation in range(nbOfGenerations):
    if ret != qt.QMessageBox.Ok:
      break
    # print "generation: ",generation
    #high cost ~ low fitness 1/... 
    fitness_list=[]  
    for i in range(popSize):
      if not sample_pop[i] in tried_params: #to avoid doing several times the same calculation
        params = sample_pop[i]
        fitness = costFunction(params, caseID)[1]
        tried_params.append(params)
        tried_fitness.append(fitness)
        fitness_list.append(fitness)
        if Guillaume:
          l.exportEvaluation(params+[fitness], '/Users/guillaume/Projects/github/NeedleFinderProjectWeek/'+str(caseID)+'-fitness.csv')
        else:
          l.exportEvaluation(params+[fitness], '/home/amastmeyer/'+str(caseID)+'-fitness.csv')
        # print fitness_list
        fitness_sum = reduce( operator.add, fitness_list)
        prob_list =map((lambda x: x/fitness_sum),fitness_list)
        cum_value = 0
        cum_prob_list = []
        for prob in prob_list:
          cum_prob_list.append( cum_value + prob )
          cum_value += prob
        cum_prob_list[-1] = 1.0
    #selection
    selected = []
    size = popSize #*0.75
    for i in xrange(size):
      rn = random.random()
      for j, cum_prob in enumerate(cum_prob_list):
        if rn<= cum_prob:
          selected.append(j)
          break
    # simple crossover (1 point)
    parent1=sample_pop[selected[np.random.randint(0,len(selected))]]
    parent2=sample_pop[selected[np.random.randint(0,len(selected))]]
    # for i in range(5):
    #   offspring[i]=[]
    # crossover point
    pt = np.random.randint(0,5)
    offspring1 = parent1[:pt] + parent2[pt:]
    offspring2 = parent2[:pt] + parent1[pt:]
    sample_pop.append(offspring1)
    sample_pop.append(offspring2)
    # multi crossover points 
    pt1 = np.random.randint(0,5)
    pt2 = np.random.randint(pt1,5)
    offspring1 = parent1[:pt1] + parent2[pt1:pt2] + parent1[pt2:]
    offspring2 = parent2[:pt1] + parent1[pt1:pt2] + parent2[pt2:]
    sample_pop.append(offspring1)
    sample_pop.append(offspring2)
    # value mutation
    chrm = sample_pop[selected[np.random.randint(0, len(selected))]]
    element_position = random.randint(0, len(chrm)-1 )
    chrm[element_position] = np.random.randint(rangeTable[element_position][0], rangeTable[element_position][1] )
    # print "Population size: ", len(sample_pop)
  #ideas for generation stop criterion:
  #find the best, lower than a thresh.: STOP
  #compare them all for difference, if smaller than certain number, STOP
