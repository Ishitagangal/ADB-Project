import os
from Transaction import  Transaction


class Graph:
    def __init__(self):
        """
         Initializes this Graph. A graph is represented
        as a dictionary mapping nodes to lists of neighbors.
        """
        self.graph = dict()
        self.vertices = []
        self.startingNode = None
        self.visitedCount = {}
        self.cycleTransactions = []

    def addEdge(self, start, end):
        """
        Inserts the given nodes into the graph as a directional mapping of start -> end
        If a lock is acquired by a transaction on a variable then the arrow goes from Variable -> Transaction
        If a transaction wants a lock but wasn't able to acquire it then arrow goes from Transaction -> Variable
        :param start: the initial vertex/node
        :param end: the terminal vertex/node
        """
        if start not in self.graph:
            self.graph[start] = list()
        if end not in self.graph:
            self.graph[end] = list()
        elif end is None or end in self.graph[start]:
            return
        self.graph[start].append(end)

    def addVertices(self, T, V):
        if T not in self.vertices:
            self.vertices.append(T)
        if V not in self.vertices:
            self.vertices.append(V)

    def removeEdge(self, nodeToRemove):
        """
        Removes the given node from the graph, as well as any references to it
        among the neighbor lists of other nodes.
        :param nodeToRemove: the node to remove from the graph
        :return: True if nodeToRemove was successfully removed, and False if it wasn't found.
        """
        if nodeToRemove not in self.graph:
            return False
        self.graph.pop(nodeToRemove)
        # Remove edges leading to that node from other nodes
        for node, neighbors in self.graph.items():
            self.graph[node] = [neighbor for neighbor in neighbors if neighbor != nodeToRemove]
        return True

    def removeSpecificEdge(self, transaction, variable):
        """
        Removes edge from transaction to variable on state change
        :param transaction:  input transaction
        :param variable:  variable to be removed

        """
        if transaction in self.graph:
            if variable in self.graph[transaction]:
                self.graph[transaction].remove(variable)

    def getNeighbors(self, node):
        """
        Returns the list of neighbors for node or None if node does not exist
        :param node: node to find neighbors of
        :return:
        """
        if node not in self.graph:
            return None
        return self.graph[node]

    def keys(self):
        """
        :return: a list of this Graph's keys
        """
        return self.graph.keys()

    def isCyclic(self):
        """
        If there is a cycle, it adds all the transactions in the cycle to list: cycleTransactions
        This list is then used to find youngest transaction that should be aborted.
        :return: False if there is no cycle else True
        """
        # Initial list of all nodes in the graph
        copy = self.graph
        nodes = list(copy.keys())
        self.cycleTransactions = []
        # Loop through each node in the graph
        for node in nodes:
            # We need this check because the dict is constantly being modified (node removal)
            if node in copy.keys():
                # If the node was part of the cycle append it to cycleTransactions
                if self.isPartOfCycle(node) and isinstance(node, Transaction):
                    self.cycleTransactions.append(node)

        if len(self.cycleTransactions) == 0:
            # print("No Cycle")
            return False
        # if len(self.cycleTransactions) == 1:
        #     print("Cycle in transaction:" + str(self.cycleTransactions[0]))
        #     return False
        else:
            # print(str(self.cycleTransactions))
            # print("Cycle in graph detected")
            # newlist = sorted(self.cycleTransactions, key=lambda x: x.startTime, reverse=True)
            # print("Loop is :" + str(newlist[0].name))
            return True

    def isPartOfCycle(self, startingNode):
        """
        Returns True if the given node is part of a cycle and False otherwise.
        :param startingNode:  the node at which to start the search
        :return:
        """
        # Reset node visitation counters on each iteration of the algorithm
        self.visitedCount.clear()
        # Keep track of the starting node
        self.startingNode = startingNode
        # And initiate the helper algorithm
        return self.partOfCycle(previousNode=None, currentNode=startingNode)

    def partOfCycle(self, previousNode, currentNode):
        """
        Returns True if self.startingNode is part of a cycle and False otherwise.
        :param previousNode: the node that led us to currentNode
        :param currentNode: the node we're currently visiting
        :return:
        """
        # This is so we avoid tracking all graph nodes. Only do it for nodes in the current path.
        if currentNode not in self.visitedCount:
            self.visitedCount[currentNode] = 0

        # Mark the node as having been visited one more time
        self.visitedCount[currentNode] += 1

        # If the node was visited twice, it's part of a cycle only if we're back to starting node
        if self.visitedTwice(currentNode):
            return currentNode == self.startingNode

        # If the current node hasn't been visited twice, move on to its neighbors
        for neighbor in self.graph[currentNode]:
            if (neighbor in self.visitedCount and self.visitedTwice(neighbor)) or \
                    self.partOfCycle(currentNode, neighbor):
                return True

        # No cycle
        return False

    def visitedTwice(self, node):
        ''' Returns True if the given node has been visited twice and False otherwise. '''
        return self.visitedCount[node] == 2

    def __str__(self):
        ''' Returns the contents of this graph in string form. '''
        # self.printGraph()
        return self.graph.__str__()

    # def printGraph(self):
    #     for u, v in self.graph:
    #         print( u +" ->" + v.name)
