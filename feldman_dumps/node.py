class Node(object):
    
    def __init__(self,labels,attributes):
        self._edges_in = ()
        self._edges_out = ()
        self._labels = ()
        self._edge_labels = {}
        
        self.add_labels(labels)
        self.attributes = attributes
    
    def add_edge_in(self, edge_in):
        self._edges_in = self._edges_in + (edge_in,)
                
        for label in edge_in.get_labels():
            self._edge_labels[label].append(edge_in)
    
    def add_edge_out(self, edge_out):
        self._edges_out = self._edges_out + (edge_out,)
        
        for label in edge_out.get_labels():
            self._edge_labels[label].append(edge_out)
    
    def add_labels(self, labels):
        self._labels = self._labels + tuple(labels)
        
    def get_labels(self):
        return self._labels
    
class DataNode(Node):
    '''special node type representing a concrete source of raw data'''
    
class SQLTableNode(DataNode):
    '''represent a DataNode pointing to a SQL table'''
    
class CSVNode(DataNode):
    '''represents a DataNode pointing to a single csv file imgested to a pandas object'''
    
class JSONNode(DataNode):
    '''represents a DataNode that ingests a single json file and stores it as a dict'''