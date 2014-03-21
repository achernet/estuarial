import yaml
from sqlalchemy.sql import and_
from estuarial.array.arraymanagementclient import ArrayManagementClient

def parse_query_url(query_url):
    with open(query_url, 'r') as stream:
        obj = yaml.load(stream, Loader=yaml.CLoader)

    type_name = obj.keys()[0]
    type_data = obj[type_name]
    func_names = type_data.keys()

    kw_args = []
    queries = []
    docstrings = []
    function_dict = {}

    # Acquire keyword arguments, if any, and the queries.
    for f_name in func_names:
        function_desc = obj[f_name]
        queries.append(function_desc['query'])
        docstrings.append()

        if function_desc['type'] == 'conditional':
            kw_args.append(function_desc['conditionals'])
        elif function_desc['type'] == 'raw':
            kw_args.append([])
        else:
            raise ValueError("SQL query entry may not have type {}".format(
                    function_desc['type']))

        def cur_function(self, **kwargs):

            # Enforce that the function is called with the conditionals
            # as key word arguments.
            assert set(kwargs) == set(function_desc['conditionals'])

            # Obtain and build the query and conditional statements.
            # Note: this block will be re-purposed for each kind of
            # logical handling of the arguments.
            aclient = ArrayManagementClient()
            arr = aclient[query_url]
            conditions = [getattr(arr, attr) == val 
                          for attr, val in kwargs.iteritems()]
            return arr.select(and_(*conditions))
        cur_function.__doc__ = function_desc['doc']
        cur_function.__name__ = function_desc[f_name]
        function_dict[f_name] = cur_function
        
    return type(type_name, (object,), function_dict)
        



if __name__ == __main__:
    query_url = "/home/ely/continuum/estuarial/estuarial/test/test_yaml.yaml"
    UniverseBuilder = parse_query_url(query_url)
    import pdb; pdb.set_trace()
        
    
        

        
        

        
