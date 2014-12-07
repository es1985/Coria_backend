import graph_tool.all as gt
import networkx as nx
import matplotlib as mp
import matplotlib.pyplot as plt

g = nx.Graph()
g.add_edge(1,2)
g.add_edge(2,3)
g.add_edge(1,8)
print(g.nodes())
print(g.edges())
adj = nx.adjacency_matrix(g)
print(adj)

test = gt.Graph(directed=False)
test_name = test.new_vertex_property("string")
c1=test.add_vertex()
test_name[test.vertex(c1)] = "A"
c2=test.add_vertex()
test_name[test.vertex(c2)] = "B"
c=test.add_vertex()
test_name[test.vertex(c)] = "C"
test.add_edge(c1, c2)
gt.graph_draw(test)
found = gt.find_vertex(test,test_name,"C")
print(found)
if found <> []:
    print("Index of B is")
    print(found[0])
    if (int(found[0])==1):
        print("True") 
    else :
        print("False")

#print('Index of B is',vertex.pop(0))

for v in test.vertices():
    print v
    print test.vertex(v)
    print test_name[v]
#    print(vp[test.vertex(v)])


def convert_graph(g):
#converts a networkX graph to graph_tool
#important : NetworkX node indexes start with 1, whereas Graph tool node indexes start with 0
    j = gt.Graph(directed=False)
    j.vertex_index
    j.add_vertex(len(adj))
    num_vertices = adj.shape[0]
    print (num_vertices)
    for i in range(num_vertices - 1):
        for l in range(i + 1, num_vertices):
            if adj[i,l] != 0:
                j.add_edge(i, l)
    return j

j = convert_graph(g)

for v in j.vertices():
    print(v)
for e in j.edges():
    print(e)

bg = nx.betweenness_centrality(g)
vp,ep = gt.betweenness(j)

print(bg)

#for u in range(1,len(bg)+1):
#    print u
#    print(bg[u])

for v in j.vertices():
    print v
    print(vp[j.vertex(v)])

#nx.draw(g)
#plt.draw()
#plt.show()
#gt.graph_draw(j)


#g = gt.collection.data["polblogs"]
#v1 = g.add_vertex()
#v2 = g.add_vertex()
#v3 = g.add_vertex()
#e = g.add_edge(v2, v1)
#f = g.add_edge(v3, v1)
#print(v1.out_degree())
#vp,ep = gt.betweenness(g)
#print(vp[g.vertex(1)])
#print(vp[g.vertex(2)])
#print(vp)
#print(type(vp))
#gt.graph_draw(g)
#print(vp[1],ep[1])
#gt.graph_draw(g.vp)
#gt.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18,output_size=(200, 200), output="two-nodes.png")