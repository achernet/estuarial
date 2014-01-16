class Edge(object):
    '''represents an edge between 2 nodes'''
  
    def __init__(self,start_node,end_node,wt,labels):
        self._start_node = start_node
        self._end_node = end_node
        self._labels = labels
        self._wt = wt
        
    def get_labels(self):
        if(self._labels is not None):
            return self._labels
        else:
            return ()
    
    def add_labels(self, labels):
        if(self._labels is not None):
            self._labels = self._labels + tuple(labels)
           
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