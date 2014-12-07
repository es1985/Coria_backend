import networkx as nx
import graph_tool.all as gt

class FileImporter(object):
  def __init__(self,filename):
    # initialize data file to parse and new empty graph
    print ('Starting file importer!')
    self.data_file  = open(filename)
    self.graph      = nx.Graph()
    self.graph_gt   = gt.Graph(directed=False)
    self.graph_gt_labels = self.graph_gt.new_vertex_property("double") 
   
  def read(self):
    for line in self.data_file:
      print("Parsing line",line)  
      self.parse_line(line)
    return self.graph 
#    return {'graph':self.graph, 'graph_gt':self.graph_gt, 'graph_gt_labels':self.graph_gt_labels}
    #self.graph,self.graph_gt,self.graph_gt_labels
 
  def read_gt(self):
      return {'graph_gt':self.graph_gt, 'graph_gt_labels':self.graph_gt_labels}

  def parse_line(self, line):
    # split each line on tabstop
    # first field specifies the source node
    # second field specifies the target node

    fields = line.strip().split("\t")
    from_node = int(fields[0])
    to_node = int(fields[1])
    
#    print('\n')
#    print('From node is',from_node)
#    print('To node is',to_node)
    # add edge to the networkx graph
    if (from_node <> to_node):
        self.graph.add_edge(from_node, to_node)
#    print('Network X graph has the following number of nodes',self.graph.number_of_nodes())
#    print('Network X graph has the following number of edges',self.graph.number_of_edges())
  
    
    
    #add edge to the graph_tool graph and create a property map of labels
    #check if nodes are already present and create new ones if not
    #temp = gt.Graph(directed=False)
    #temp_name = temp.new_vertex_property("string") 
    temp = self.graph_gt
    temp_name = self.graph_gt_labels
    
    check = None
    if (from_node <> to_node): #check if from_node is the same as to_node
        index_from = gt.find_vertex(temp,temp_name,from_node)
#    print('Index from is',index_from)
        index_to = gt.find_vertex(temp,temp_name,to_node) 
#    print('Index to is',index_to)
        if (index_from == [] and index_to == []):
#        print('No idences are found')
            c1 = temp.add_vertex()
            temp_name[temp.vertex(c1)] = from_node
#        print('Temp_name is now',temp_name[temp.vertex(c1)])
            c2 = temp.add_vertex()
            temp_name[temp.vertex(c2)] = to_node
#        print('Temp_name is now',temp_name[temp.vertex(c2)])
        if (index_from <> [] and index_to == []) :
#       print('Index from is')
#        print(index_from[0])
            c1 = index_from[0]
        #print('C1 is',c1)
            c2 = temp.add_vertex()
        #print('C2 is'),
        #print(c2)
            temp_name[temp.vertex(c2)] = to_node
#        print('Temp_name is now',temp_name[temp.vertex(c2)])
        if (index_to <> [] and index_from ==[]) :
#        print('Index to is')
#        print(index_to[0])
            c1 = temp.add_vertex()     
            c2 =  index_to[0]
            temp_name[temp.vertex(c1)] = from_node
#        print('Temp_name is now',temp_name[temp.vertex(c1)])
        if (index_from <> [] and index_to <> []) :
#        print('Both vertices found')
            c1 = index_to[0]
            c2 = index_from[0]
            check = temp.edge(c1,c2) #check if the edge is already present
#    print('Check is',check)
        if (check == None):
#            print("Adding edge between",c1,"and",c2)        
            temp.add_edge(c1, c2)
    
    #print(temp_name)    
    self.graph_gt = temp
    self.graph_gt_labels = temp_name

#    Check whether GT and NetworkX graphs have the same number of nodes and edges
#    if (self.graph_gt.num_vertices() <> self.graph.number_of_nodes()):
#        print('Unequal number of vertices detected at from node',from_node,'to node',to_node)   
#        print('Number of vertices in Gt Graph is',self.graph_gt.num_vertices())
#        print('Number of vertices in NetworkX is',self.graph.number_of_nodes())  
#    else:
#        print('Equal number of vertices in both graphs')        
    
#    if (self.graph_gt.num_edges() <> self.graph.number_of_edges()):
#        print('Unequal number of edges detected at from node',from_node,'to node',to_node)
#        print('Number of vertices in Gt Graph is',self.graph_gt.num_edges())
#        print('Number of vertices in NetworkX is',self.graph.number_of_edges())   
#    else:
#        print('Equal number of edges in both graphs')
            
#  if (self.graph.number_of_nodes() <> self.graph_gt.
#    print('Graph tool graph is',self.graph_gt)
#    print('Graph tool labels map is',self.graph_gt_labels)
    
    

   
