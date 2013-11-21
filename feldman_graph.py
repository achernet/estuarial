from node import Node
from edge import Edge

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
        
        self._edges.append(edge)
    
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
            
    def get_all_nodes(self):
        return self._nodes
            
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
    node1 = Node(("Node","1"),{"name":"node1_name"})
    node2 = Node(("Node","2"),{"name":"node2_name"})
    
    g = TSHyperGraph()
    g.add_node(node1)
    g.add_node(node2)
    g.add_edge(node1,node2, None, None)