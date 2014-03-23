import yaml
import copy
from sqlalchemy.sql import and_
from estuarial.array.arraymanagementclient import ArrayManagementClient

class QueryHandler(object):
    @classmethod
    def create_type_from_yaml(self, query_url):
        attr_dict = {}
        with open(query_url, 'r') as stream: # Yaml should be validated here.
            obj = yaml.load(stream, Loader=yaml.CLoader)
        type_name = obj.keys()[0]
        type_data = obj[type_name]
        func_names = type_data.keys()
        for f_name in func_names:
            function_desc = type_data[f_name]
            known_args = function_desc.get('conditionals', [])  
            def function_factory(f_name, function_desc, known_args):
                def function(self, **kwargs):                    
                    # Querying turned off for testing.
                    if False:
                        assert set(kwargs.keys()) == set(known_args)
                        aclient = ArrayManagementClient()
                        arr = aclient[query_url]
                        conditions = [
                            getattr(arr, attr) == val # Logic changes here.
                            for attr, val in kwargs.iteritems()
                        ]
                        return arr.select(and_(*conditions))
                    else:
                        print "*** {}".format(f_name)
                return function

            cur_function = function_factory(f_name, function_desc, known_args)
            cur_function.__doc__ = function_desc['doc']
            cur_function.__name__ = f_name
            attr_dict[f_name] = cur_function
            attr_dict["__" + f_name + "_query"] = function_desc["query"]
            attr_dict["__" + f_name + "_kwargs"] = known_args
        return type(type_name, (object,), attr_dict)        
        
if __name__ == "__main__":
    import os

    test_query_url = os.path.abspath('..') + "/test/test_yaml.yaml"
    UniverseBuilder = QueryHandler.create_type_from_yaml(test_query_url)
    ub = UniverseBuilder()

    # Inferred 'gicsec' query API:
    ub.gicsec()              # <--- Callable. No args at the moment just for testing.
    print ub.__gicsec_kwargs # <--- Function signature for this query.
    print ub.__gicsec_query  # <--- Query saved as a string from file.

    # Inferred 'spx' query API:
    ub.spx_universe() 
    print ub.__spx_universe_kwargs 
    print ub.__spx_universe_query 
