# random graph
# set of nodes as early adopter 
#other node
# set of behaviors: A and B , I set 1 for A and 2 for B (earlyadoptre will adopt the behavior A )
# payoff for adopting the behaivior : alpha and beta

import networkx as nx
from networkx import *
import operator
from operator import itemgetter
import sys
import math 
import random 
from random import choice 
from config_com import Config
#import psyco
#psyco.full()

class Casscade(object):


        def cascade_Parallel(self,nodeBehaviors,inGraph,earlyAdoptorInitialSize,adoptionThreshold,in_community):
		if Config.plotGraph:
			in_pos = nx.fruchterman_reingold_layout(inGraph)
			try:
				from allPlot import plotGraph
			except:
                        	raise
			graphObj = plotGraph()	

                adoptionStep  = 0
		adoptionStep_in = 0
		adoptionStep_out = 0	
	
                Flag= True
                step = 1

                stepDic ={}
		stepDic_in ={}
		stepDic_out ={}

                updatedNodeBehaviors={}

                countRemaingB = len(nodeBehaviors)- earlyAdoptorInitialSize
		countRemaingB_in = len(nodeBehaviors)/Config.clustered_numberCommuinities- earlyAdoptorInitialSize
		countRemaingB_out = (len(nodeBehaviors)/Config.clustered_numberCommuinities) * (Config.clustered_numberCommuinities -1)

		stepDic[0] = countRemaingB
		stepDic_in[0] = countRemaingB_in
		stepDic_out[0] = countRemaingB_out

                nodeadoptionProb = {} # keep adoption prob for each node

		#analysis
		#border ={}

                for i in nodeBehaviors:
                        updatedNodeBehaviors[i]=nodeBehaviors[i]

			if random.uniform(0,1) < adoptionThreshold:
                        	nodeadoptionProb[i] = adoptionThreshold - Config.epsilon
			else:
				nodeadoptionProb[i] = adoptionThreshold + Config.epsilon
			
 
                while Flag == True:
			##plot each time step
			timecount_in = 0
			timecount_out = 0
			timecount = 0

			if Config.plotGraph:
				print "plot"
				whiteNodes = []
                		redNodes = []
				for i in nodeBehaviors:  ###nodeBehaviors[behavio][commun]
                        		if nodeBehaviors[i][0] == 2:
                                		whiteNodes.append(i)
                        		else:
                                		redNodes.append(i)
                		graphObj.drawGraph(inGraph,whiteNodes,redNodes,adoptionStep,earlyAdoptorInitialSize,in_pos)
			####
                        for i in nodeBehaviors:
                                if countRemaingB > 0 and nodeBehaviors[i][0] !=1:
                                        countAbehaviorNeighbor = 0
                                        countBbehaviorNeighbor = 0
                                        if not len(inGraph[i])==0:
                                                for j in inGraph[i]:
                                                        if nodeBehaviors[j][0]==1:
                                                                countAbehaviorNeighbor +=1
                                                        else:
                                                                countBbehaviorNeighbor +=1
                                                prcentageNeighborWithA = float(countAbehaviorNeighbor)/(countAbehaviorNeighbor+countBbehaviorNeighbor)
                                                if  nodeadoptionProb[i] < prcentageNeighborWithA:
                                                        updatedNodeBehaviors[i]=(1,updatedNodeBehaviors[i][1])

                                                        countRemaingB -=1
							if nodeBehaviors[i][1] == in_community:
                                				countRemaingB_in -=1
								timecount_in +=1
								timecount += 1
				                        else:
                                				countRemaingB_out -=1
								timecount_out += 1
								timecount +=1

							
                                        else :
                                                pass
			if not timecount == 0:
	                        adoptionStep +=1
			if not timecount_in == 0:
				adoptionStep_in +=1
			if not timecount_out == 0:
                                adoptionStep_out +=1



                        for i in updatedNodeBehaviors:
                                nodeBehaviors[i]= updatedNodeBehaviors[i]
                        stepDic[step]= countRemaingB# countNodeWithBafter
			stepDic_in[step]= countRemaingB_in
			stepDic_out[step]= countRemaingB_out

                        if not countRemaingB > 0:
                                Flag = False
                        if stepDic[step]== stepDic[step-1]:
                                Flag=False
                        step +=1

                countA = float(len(nodeBehaviors) - countRemaingB)/len(nodeBehaviors)
		countA_in =float(len(nodeBehaviors)*0.5 - countRemaingB_in)/len(nodeBehaviors)
                countA_out =float(len(nodeBehaviors)*0.5 - countRemaingB_out)/len(nodeBehaviors)

		#countA_in =float(len(nodeBehaviors)*0.25 - countRemaingB_in)/len(nodeBehaviors)
		#countA_out =float(len(nodeBehaviors)*0.75 - countRemaingB_out)/len(nodeBehaviors)
               	#print adoptionStep , adoptionStep_in, adoptionStep_out,countA , countA_in, countA_out 
		return adoptionStep , adoptionStep_in, adoptionStep_out,countA , countA_in, countA_out

    def select_seed_randomly_community(self,node_count,seed_size,graph,node_community):
        node_state ={}
        count = 0
        starting_community =[]
        for node in nodes(graph):
            node_state[node]=(2,node_community[node])
            if node_community[node]==0:
                starting_community.append(node)

        while count < seed_size:
            node = random.choice(starting_community)
            if node_state[node]==2:
                node_state[node]=1
                count +=1
        return node_state ,0

    def select_seed_randomly(self,node_count,seed_size,graph):
        # select set of nodes from graph to be seed
        # change  node's state from 2 to 1 if a node is selected to be a seed
        node_state ={}
        count =0
        for node in nodes(graph):
            node_state[node]=2
        while count <seed_size:
            node = random.choice(nodes(graph)
            if node_state[node]==2:
                node_state[node] =1
                count +=1
        return node_state

    def select_seed_maxdigree(self,node_count,seed_size,graph):
        # select set of nodes from graph to be seed
        # change  node's state from 2 to 1 if a node is selected to be a seed
        node_state ={}
        count = 0
        for node in nodes(graph):
            node_state[node]= 2
            
        sorted_nodes_bydegree = sorted(graph.degree_iter(),key=itemgetter(1),reverse=True) 
        while count < seed_size:
            top_node = sortedNodes.pop(0)
            if topNode:
                seed = topNode[0]
                if node_state[node]==2:
                    node_state[node]=1
                    count +=1
	   return node_state

	



