#metrics.py
import networkx as nx
import numpy as np
import datetime as dt
import graph_tool.all as gt

def clustering_coefficient(self,node):
  print ('Calculating clustering_coefficient for node',node)
  #in the first run calculate the metric for all nodes at once and save in a hash of the instance to access later
  #NOTE: this should result in a performance gain, but for very large graphs this might be a problem.
  #      in this case, just returning nx.clustering(self.graph, node) might be better
  if not hasattr(self, 'all_clustering_coefficients'):
    self.all_clustering_coefficients = nx.clustering(self.graph)

  #get the actual value from the pre-calculated hash
  return self.all_clustering_coefficients[node]

def degree(self, node):
  print('Calculating degree for node', node)  
  return self.graph.degree(node)


def average_neighbor_degree(self,node):
  print('Calculating average_neighbour_degree for node',node)
  # same caching technique as in self.clustering_coefficient
  # might also break for very large graphs
  # nx.average_neighbor_degree(self.graph, nodes=node) might be the way to go

  if not hasattr(self, 'all_average_neighbor_degrees'):
    self.all_average_neighbor_degrees = nx.average_neighbor_degree(self.graph)
  return self.all_average_neighbor_degrees[node]

def iterated_average_neighbor_degree(self, node):  
  print('Calculating iterated_average_neighbor degree for node',node)
  first_level_neighbors = self.graph.neighbors(node)
#  print ('First level neigbors are', first_level_neighbors)
  second_level_neighbors = [] 
#  print ('Second level neigbors are', second_level_neighbors)
  # get all two-hop nodes
  for first_level_neighbor in first_level_neighbors:
    current_second_level_neighbors = self.graph.neighbors(first_level_neighbor)
    second_level_neighbors.extend(current_second_level_neighbors)

  #remove one-hop nodes and self
  relevant_nodes = set(second_level_neighbors) - set(first_level_neighbors) - set([node])
  
  degree_sum = 0
  for relevant_node in relevant_nodes:
    degree_sum += self.graph.degree(relevant_node)

  if float(len(relevant_nodes)) <> 0:
     return float(degree_sum)/float(len(relevant_nodes))
  else:
     return 0

def eccentricity(self, node):
  print('Calculating eccentricity for node', node)
  if not hasattr(self, 'all_eccentricities'):
    l = gt.label_largest_component(self.graph_gt['graph_gt'],directed = None) #find the largest component
    print ('Found the largest component')
#    print ("Printing labeled largest component",l.a)  
    u = gt.GraphView(self.graph_gt['graph_gt'], vfilt=l)   # extract the largest component as a graph
    print('The number of vertices in the largest component is',u.num_vertices())
    print('The number of vertices in the original graph is', nx.number_of_nodes(self.graph))
#    if  nx.is_connected(self.graph) == True:
    if (u.num_vertices() == nx.number_of_nodes(self.graph)):
        print ("Graph is connected")
        self.all_eccentricities = nx.eccentricity(self.graph)
        print ("Calculated all eccentricities")
#        print("Eccentricities are",self.all_eccentricities)
        return self.all_eccentricities[node]
    else:
      #  return 0
        print("Graph is disconnected")
        self.all_eccentricities = {}
  if (self.all_eccentricities != {}): 
        print("Returning eccentricity for",node,"-",self.all_eccentricities[node])      
        return self.all_eccentricities[node]
  else:
        print("Returning 0")
        return 0  

def betweenness_centrality(self, node):
  print('Calculating betweenness_centrality for node',node)
  if not hasattr(self, 'all_betweenness_centralities'):
    self.all_betweenness_centralities = nx.betweenness_centrality(self.graph)
  return self.all_betweenness_centralities[node]


def betweenness_centrality_gt(self, node):
    print('Calculating betweenness_centrality with graph_tool for node',node)
#    print('Self is',self.graph_gt['graph_gt'])
#    print('Self is also',self.graph_gt['graph_gt_labels'])
#    def convert_graph(g):
#converts a networkX graph to graph_tool
#important : NetworkX node indexes start with 1, whereas Graph tool node indexes start with 0
#        adj = nx.adjacency_matrix(g)
#        j = gt.Graph(directed=False)
#        j.add_vertex(len(adj))
#        num_vertices = adj.shape[0]
#        for i in range(num_vertices - 1):
#            for l in range(i + 1, num_vertices):
#                if adj[i,l] != 0:
#                    j.add_edge(i, l)
#        return j
    
    
    if not hasattr(self, 'all_betweenness_centralities_gt'):
        vp,ep = gt.betweenness(self.graph_gt['graph_gt'])
        self.all_betweenness_centralities_gt = vp         
               
    node_label = gt.find_vertex(self.graph_gt['graph_gt'],self.graph_gt['graph_gt_labels'],node)
#    print("Node",node,"has index",node_label)
#    print('Vp is',vp)    
#    print('Betweenness centrality of node',node,'is',vp[self.graph_gt['graph_gt'].vertex(node_label[0])])
            
    return self.all_betweenness_centralities_gt[self.graph_gt['graph_gt'].vertex(node_label[0])] 

def average_shortest_path_length(self, node):
  print('Calculating average_shortes_path_length for node',node)
  # caching average_shortest_path_length for all nodes at one failed
  # already switched to single calculation

  #get all shortest path lengths
  all_shortest_path_lengths_for_node = nx.shortest_path_length(self.graph, source=node)

  #calculate average
  sum_of_lengths = 0
  for target in all_shortest_path_lengths_for_node:
    sum_of_lengths += all_shortest_path_lengths_for_node[target]
  
  return float(sum_of_lengths)/len(all_shortest_path_lengths_for_node)


#############
# advanced metrics
#############
def correct_clustering_coefficient(self,node):
  print('Calculating correct_clustering_coefficient for node',node)
  clustering_coefficient = float(self.redis.hget(self.node_prefix+str(node),'clustering_coefficient'))
  degree = float(self.redis.hget(self.node_prefix+str(node), 'degree'))
  corrected_cc = clustering_coefficient + (degree * clustering_coefficient) / float(4)
  return corrected_cc

def correct_average_neighbor_degree(self,node):
  print('Calculating correct_average_neighbor degree for node',node)
  avgnd = float(self.redis.hget(self.node_prefix+str(node), 'average_neighbor_degree'))
  
  neighbors = self.graph.neighbors(node)
  number_of_neighbors = float(len(neighbors))
  neighbor_degrees = []
  for neighbor in neighbors:
    neighbor_degrees.append(self.graph.degree(neighbor))

  #using numpy median and standard deviation implementation
  numpy_neighbor_degrees = np.array(neighbor_degrees)
  median = np.median(numpy_neighbor_degrees)
  standard_deviation = np.std(numpy_neighbor_degrees)
  
  if avgnd == 0.0 or number_of_neighbors == 0.0 or standard_deviation == 0.0:
    return avgnd
  else:
    return avgnd + ( ((median - avgnd) / standard_deviation) / number_of_neighbors ) * avgnd


def correct_iterated_average_neighbor_degree(self, node):
  print('Calculating correct_iterated_avverage_neighbour_gegree for node',node)
  avgnd = float(self.redis.hget(self.node_prefix+str(node), 'iterated_average_neighbor_degree'))

  first_level_neighbors = self.graph.neighbors(node)
  second_level_neighbors = []

  # get all two-hop nodes
  for first_level_neighbor in first_level_neighbors:
    current_second_level_neighbors = self.graph.neighbors(first_level_neighbor)
    second_level_neighbors.extend(current_second_level_neighbors)

  #remove one-hop neighbors and self
  relevant_nodes = set(second_level_neighbors) - set(first_level_neighbors) - set([node])

  number_of_nodes = len(relevant_nodes)
  node_degrees = []
  for rel_node in relevant_nodes:
    node_degrees.append(self.graph.degree(rel_node))

  numpy_node_degrees = np.array(node_degrees)
  median = np.median(numpy_node_degrees)
  standard_deviation = np.std(numpy_node_degrees)

  if avgnd == 0.0 or number_of_nodes == 0.0 or standard_deviation == 0.0:
    return avgnd
  else:
    return avgnd + ( ((median - avgnd) / standard_deviation) / number_of_nodes ) * avgnd
  

