class Node():
    
    def __init__(self,labels,attributes):
        self._attributes = {}
        self._edges_in = []
        self._edges_out = []
        self._labels = []
        self._edge_labels = []
        
        self.add_labels(labels)
        self.attributes = attributes
    
    def add_edge_in(self, edge_in):
        self._edges_in.append(edge_in)
        for label in edge_in.get_labels():
            self._edge_labels[label].append(edge_in)
    
    def add_edge_out(self, edge_out):
        self._edges_out.append(edge_out)
        for label in edge_out.get_labels():
            self._edge_labels[label].append(edge_out)
    
    def add_labels(self, labels):
        self._labels.extend(labels)
        
    def get_labels(self):
        return tuple(self._labels)
    
class DataNode(Node):
    '''special node type representing a concrete source of raw data'''
    

class Edge(object):
    '''represents an edge between 2 nodes'''

    def __init__(self,start_node,end_node,wt,labels):
        self._start_node = start_node
        self._end_node = end_node
        self._labels = labels
        self._wt = wt
        
    def get_labels(self):
        return tuple(self._labels)
    
    def add_labels(self, labels):
        self._labels.extend(labels)
           
class TimeSeriesEdge(Edge):
    '''represents an edge between 2 nodes with timeseries weights'''   
    def __init__(self,start_node,end_node,wt_vector, labels):
        Edge.__init__(self,start_node,end_node, labels)
        self._wt_vector = wt_vector

class TSSemiHyperEdge(Edge):
    '''For representing group membership relationships over time.
        Represents a connection between a single start node and many end nodes.
        End nodes are stored as an ordered list and weights are stored as a timeseries matrix.
        Wt_matrix may contain numerical weights or an integer mask'''
    def __init__(self,start_node,end_node_list,wt_matrix, labels):
        self._start_node = start_node
        self._end_node_list = end_node_list
        self._wt_matrix = wt_matrix
        self._labels = labels



class TSHyperGraph():
    _nodes = []
    _edges = []
    _node_labels = {}
    _edge_labels = {}
    
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._node_labels = {}
        self._edge_labels = {}
    
    def add_edge(self,start_node,end_node, wt, labels):
        edge = Edge(start_node, end_node, wt, labels)
        start_node.add_edge_out(edge)
        end_node.add_edge_in(edge)
        
        self._edges.append((start_node,end_node))
    
    def add_ts_semihyperedge(self, start_node, end_node_list, wt_matrix, labels):
        hyperedge = TSSemiHyperEdge(start_node, end_node_list, wt_matrix, lables)
        start_node.add_edge_out(hyperedge)
        for end in end_node_list:
            end.add_edge_in(hyperedge)
            
        for label in labels:
            self._edge_labels[label].extend(hyperedge)
            
    def add_ts_edge(self, start_node, end_node, wt_vector, labels):
        ts_edge = TimeSeriesEdge(start_node, end_node, wt_vector, labels)
        start_node.add_edge_out(ts_edge)
        end_node.add_edge_in(ts_edge)
        
    def add_node(self,node):
        self._nodes.append(node)
        
        for label in node.get_labels():
            if not self._node_labels.has_key(label):
                   self._node_labels[label] = []
               
            self._node_labels[label].append(node)
            
            
    def get_nodes_by_label(self, label):
        if self._node_labels.has_key(label):
            return self._node_labels[label]
        else: 
            return []
        
    def get_edge_labels(self):
        return tuple(self._edge_labels)
        
    def get_node_labels(self):
        return tuple(self._node_labels)
    

if __name__ == '__main__':
    node1 = Node(["Node","1"],{"name":"node1_name"})
    node2 = Node(["Node","2"],{"name":"node2_name"})
    
    g = TSHyperGraph()
    g.add_node(node1)
    g.add_node(node2)
    g.add_edge(node1,node2,1,[])
