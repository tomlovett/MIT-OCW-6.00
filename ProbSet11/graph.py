# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest, total_weight, outside_weight):
       self.src = src
       self.dest = dest
       self.total_weight = total_weight
       self.outside_weight = outside_weight
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)


## Digraph
class Digraph(object):
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
       self.total_weight = {}
       self.outside_weight = {}
       self.completed_paths = []
       self.memo = {}
       self.maxOutside = 10000
       self.maxTotal = 10000
       self.shortest = []
       self.start = None
       self.goal = None

# Digraph initilization
   def read_line(self, line):
       src, dest, total_weight, outside_weight = line[0], line[1], int(line[2]), int(line[3])
       try:
          self.addNode(src)
       except:
          pass
       try:
          self.addNode(dest)
       except:
          pass
       edge = Edge(src, dest, total_weight, outside_weight)
       self.addEdge(edge)
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
       self.total_weight[(src, dest)] = edge.total_weight
       self.outside_weight[(src, dest)] = edge.outside_weight

# Helper Functions - children, weight calculations
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
      
   def get_total_weight(self, src, dest):
       if dest not in self.childrenOf(src):
          print 'MISSING LINK -', src, dest
          raise ValueError
       return self.total_weight[(src, dest)]
   def get_outside_weight(self, src, dest):
       if dest not in self.childrenOf(src):
          print 'MISSING LINK -', src, dest
          raise ValueError
       return self.outside_weight[(src, dest)]
   def get_path_total_weight(self, path):
       total = 0
       if len(path) < 2:
          return total
       for i in range(len(path) - 1):
          total += self.get_total_weight(path[i], path[i+1])
       return total
   def get_path_outside_weight(self, path):
       total = 0
       if len(path) < 2:
          return total
       for i in range(len(path) - 1):
          total += self.get_outside_weight(path[i], path[i+1])
       return total

# DFS
   def full_DFS(self, start, goal):
      self.shortest, self.trial = None, [start]
      self.start, self.goal = start, goal
      self.DFS()
      self.parseCompleted()

   def DFS(self):
      if start == goal:
         self.completed_paths.append(self.trial)
         return 'success'

      if self.get_path_total_weight(self.trial) > self.maxTotal or self.get_path_outside_weight > self.maxOutside:
         'fail; up and over'

      for node in self.childrenOf(start):
         if node in self.trial:
            continue
         self.trial.append(node)
         self.DFS(node, goal)

   def completed_path(self):
      if self.trial[0] != self.start or self.trial[-1] != self.goal:
         print 'incorrect path start or goal - ', self.trial
         return 'ehhh'
      if self.shortest == None:
         self.shortest = self.trial[:]
         return
      else:
         if 

# String function
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k).ljust(2) + ' -> ' + str(d).rjust(2) + '\n'
       return res[:-1]

class Path(Digraph):             # obsolete in current iteration
    def __init__(self, start):
        self.nodes = [start]
    def __len__(self):
        return len(self.nodes)
    def add_node(self, node):
        self.nodes.append(node)

    def __str__(self):
        res = ''
        for node in self.nodes:
           res = res + node + ' '
        return res[:-1]
        
