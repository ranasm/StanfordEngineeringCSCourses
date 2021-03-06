# -*- coding: utf-8 -*-
"""StanfordCS221Lecture6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uVAueBmJSdsegA2op6Q0775XpyoTYvnG
"""

#Lecture 6
'''
Tram Search Problem:
Imagine streets with blocks are numbered from 1 to n. 
Walking from block s to block s+1 takes 1 minute
Taking a magic tram from block s to block 2s takes 2 minutes

Question: How to travel from 1 to n in the least time?
'''

#Throughout all lectures, Professor Liang and Professor Sadigh emphasize a "Model/Inference/Learning" paradign
#Model=Problem Setup (no algorithms, just setting the problem structure)
#Inference=Algorithms/predictions
#Learning=Learn the parameters of the model (if not available)

#MODEL
class TransportationProblem(object):
  def __init__(self,N):
    self.N=N
  def startState(self):
    return 1
  def isEnd(self,state):
    if state==self.N:
      return True
  def SuccandCost(self,state):
    #For the state you are currently in, return (action/newState/cost)
    result=[]
    if state+1<=self.N:
      result.append(('walk',state+1,1))
    if state*2<=self.N:
      result.append(('tram',state*2,2))
    return result

#Neatly format solution
def printSolution(CostAndPath):
  cost=CostAndPath[0]
  totalpath=CostAndPath[1]
  print('Total Cost: {}'.format(cost))
  for path in totalpath:
    print(path)

import heapq 

#Create PriorityQueue for Uniform Cost Search (UCS)
#Needed to simulate a Frontier
#Note: In UCS, we have explored, frontier, and unexplored sets

#Note: In this data structure, we use BOTH a heap and dictionary
#Heap to pop minimum cost state and cost from frontier (constant time)
#Dictionary to check if current priority is better than recorded priority 
#for a given state
class PriorityQueue:
  def __init__(self):
    self.Done=-100000
    self.heap=[]
    self.priorities={}

  #Insert state and respective priority into heap if state isnt in the heap or
  #the newPriority is smaller than existing priority
  def update(self,state,newPriority):
    oldPriority=self.priorities.get(state)
    if oldPriority==None or newPriority<oldPriority:
      self.priorities[state]=newPriority
      heapq.heappush(self.heap,(newPriority,state))
      return True
    return False

  #Returns state with minimum priority
  def removeMin(self):
    while len(self.heap)>0:
      priority,state=heapq.heappop(self.heap)
      if self.priorities[state]==self.Done:
        continue
      self.priorities[state]=self.Done
      return (state,priority)
    return (None,None)#Nothing left to return

#INFERENCE

#UCS in a nutshell:
#  Accounts for cycles!!
#  Add stuff to frontier, pop off stuff from frontier 
#  (ie Move stuff from unexplored set to explored set)
def uniformCostSearch(problem):
  frontier=PriorityQueue()
  frontier.update(problem.startState(),0)
  while True:
    state,pastCost=frontier.removeMin()
    if problem.isEnd(state):
      return (pastCost,[])
    for action,nextstate,cost in problem.SuccandCost(state): #add children
      frontier.update(nextstate,pastCost+cost)

problem=TransportationProblem(40)
printSolution(uniformCostSearch(problem))

'''
Structured Perceptron Problem (LEARNING)

This is the inverse of problem stated above. This is now a search problem without costs. 

Task: Find the costs associated with each action

Your given a sequence of actions with the best path solution. Our goal is to find weights.
'''

#MODEL
class TransportationProblemStructuredPerceptron(object):
  def __init__(self,N,weights):
    self.N=N
    self.weights=weights
  def startState(self):
    return 1
  def isEnd(self,state):
    if state==self.N:
      return True
  def SuccandCost(self,state):
    #For the state you are currently in, return (action/newState/cost)
    result=[]
    if state+1<=self.N:
      result.append(('walk',state+1,self.weights['walk']))
    if state*2<=self.N:
      result.append(('tram',state*2,self.weights['tram']))
    return result

#Bring back dynammic programming algorithm from lecture 5
#Algorithm: Dynammic Programming (only works for acyclic graphs)
def dynammicProgramming(problem):
  cache={}
  result=float('+inf')
  history=[]
  def futureCost(state):
    if problem.isEnd(state):
      return 0
    if state in cache:
      return cache[state][0]

    result=min((cost+futureCost(nextstate),action,nextstate,cost) for action,nextstate,cost in problem.SuccandCost(state))

    #Alternative method to find result
    #for action,nextstate,cost in problem.SuccandCost(state):
    #  result=min(result,cost+futureCost(nextstate,result)) 

    cache[state]=result
    return result[0]
  
  #TODO: Currently, cache returns empty dictionary when using colab
  #state=problem.startState()
  #while not problem.isEnd(state):
    #temp,action,nextstate,cost=cache[state]
    #history.append=((action,nextstate,cost))
    #state=nextstate

  return (futureCost(problem.startState()),history)

problem=TransportationProblem(10)