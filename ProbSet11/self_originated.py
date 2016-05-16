import string

## Nodes
class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __lt__(self, other):
        if int(self.name) < int(other.name):
            return True
        else:
            return False
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    
## Edge
class Edge(object):
    def __init__(self, src, dest, total_weight, outside_weight):
        self.src, self.dest = src, dest
        self.total_weight, self.outside_weight = total_weight, outside_weight
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return str(self.src) + '->' + str(self.dest)

## Path class
class Path(object):
    def __init__(self, digraph, src, dest, nodes):
        self.digraph, self.src, self.dest, self.nodes = digraph, src, dest, nodes
        self.total_weight, self.outside_weight = 0, 0
        self.calc_total()
        self.calc_outside()

    def calc_total(self):
        self.total_weight = 0
        for i in range(len(self.nodes) - 1):
            self.total_weight += self.digraph.edge_weight[(self.nodes[i], self.nodes[i+1])]

    def calc_outside(self):
        self.outside_weight = 0
        for i in range(len(self.nodes) - 1):
            self.outside_weight += self.digraph.edge_outside_weight[(self.nodes[i], self.nodes[i+1])]

## Digraph
class Digraph(object):
    def __init__(self, mapFileName):
        self.nodes = set([])
        self.edges = {}
        self.edge_weight = {}
        self.edge_outside_weight = {}

        self.memo = {}
 
        self.origin = None
        self.goal = None
        self.trial = []
        self.maxOutside = 10000
        self.maxTotal = 10000

        self.load_map(mapFileName)

# Digraph initilization
    def load_map(self, mapFileName):
        text = open(mapFileName, 'r')
        for line in text:
            line = line.strip()
            line = line.split()
            self.read_line(line)
        'sort nodes for each'
        for node in self.edges:
            self.edges[node].sort()
            
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
        self.edge_weight[(src, dest)] = edge.total_weight
        self.edge_outside_weight[(src, dest)] = edge.outside_weight

# Helper functions
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def parentsOf(self, child):
        parents = []
        for node in self.nodes:
            if child in self.edges[node]:
                parents.append(node)
        parents.sort()
        return parents

    def total_weight(self, src, dest):
        return self.total_weight[(src, dest)]
    def outside_weight(self, src, dest):
        return self.outside_weight[(src, dest)]
    def total_path_weight(self, path):
        total = 0
        if len(path) < 2:
            return total
        for i in range(len(path) - 1):
            total += self.total_weight(path[i], path[i+1])
        return total
    def outside_path_weight(self, path):
        total = 0
        if len(path) < 2:
            return total
        for i in range(len(path) - 1):
            total += self.outside_weight(path[i], path[i+1])
        return total

## Depth-first search
    def fullDFS(self, origin, goal):
        self.DFS(origin, origin, goal)
        return self.memo[(origin, goal)]
 

    def DFS(self, origin, current, goal):
        if current == goal:
            print 'goal achieved'
            return
##        if goal in self.childrenOf(current):
##            if (origin, current) in self.memo:
##                self.memo[(origin, goal)] = Path(self, origin, goal, self.memo[(origin, current)].nodes + [goal])
##            else:
##                self.memo
##            return
        for node in self.childrenOf(current):
            if self.node_already_in_path(node, origin, current):
                continue
            print node
            path_nodes = self.call_path_nodes(origin, current, node)
            path = Path(self, origin, node, path_nodes)
            self.memo_paths(path_nodes)
            if (node, goal) in self.memo:
                complete_nodes = path.nodes + self.memo([node,goal]).nodes
                complete = Path(self, origin, goal, complete_nodes)
                self.memo_paths(complete_nodes)
                return
            self.DFS(origin, node, goal)
        print 'returning'
        return

    def call_path_nodes(self, origin, current, node):
        if origin == current:
            return [origin, node]
        else:
            return self.memo[(origin, current)].nodes + [node]

    def node_already_in_path(self, node, origin, current):
        if (origin, current) in self.memo:
            if node in self.memo[(origin, current)].nodes:
                return True
        else:
            return False

    def memo_paths(self, nodes):
        for x in nodes:
            for y in nodes:
                if x == y or nodes.index(y) < nodes.index(x):
                    continue
                path = Path(self, x, y, nodes[nodes.index(x):(nodes.index(y) + 1)])
                if (x,y) not in self.memo or path.total_weight < self.memo[(x,y)].total_weight:
                    self.memo[(x,y)] = path

# Depth-limited search
    def call_depth_limited(self, path, goal, depth):
        completed = []
        for i in range(limit):
            result = self.depth_limited(self, origin, limit, 0)

    def depth_limited(self, path, goal, limit, depth):
        if path[-1] == goal:
            return path
        elif limit == depth:
            return 0
        else:
            children = self.childrenOf(path[-1])
            
        
        

# String function
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k).ljust(2) + ' -> ' + str(d).rjust(2) + '\n'
        return res[:-1]

## __main__
MIT = Digraph('mit_map.txt')
