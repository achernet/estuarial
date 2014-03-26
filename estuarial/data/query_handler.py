import os
import yaml
from sqlalchemy.sql import and_
from os.path import join as pjoin
from estuarial.util.config.config import expanduser
from estuarial.data.keyword_handler import KeywordHandler
from estuarial.array.arraymanagementclient import ArrayManagementClient

class QueryHandler(object):
    """
    Provides method `create_type_from_yaml` which converts a composite yaml
    query definition file into a new Python class. The created class will
    have functions available corresponding to each named query in the yaml.

    The keyword arguments for these functions will include any conditional
    arguments given in the yaml, as well as augmented keyword arguments that
    allow for SQL operations to be performed on the conditional argument names.

    For example, consider the following sample composite query file which might
    be saved in some file called "accounting_data.yaml".

    (The #'s below are just to delimit the example file and are not part of the
    yaml file itself.)
    
    #####
    #AccountingData:
    #    inventory:
    #        doc: This is a query for inventory.
    #        conditionals:
    #            account_id: A customer's account number.
    #            shipping_date: The shipping date.
    #        query: >
    #            SELECT 
    #                  a.account_id as account_id
    #                , b.shipping_id as shipping_id
    #                , a.customer_name
    #                , b.shipping_date
    #                , b.order_volume
    #                , b.total_sales
    #            FROM account_table a
    #            JOIN shipping_table b
    #                ON a.account_id = b.shipping_id
    #
    #    payroll:
    #        doc: This is a payroll query.
    #        conditionals:
    #            branch_id: A branch id number
    #            city: A city name
    #        query: >
    #            SELECT
    #                  a.branch_id
    #                , b.city
    #                , a.total_payroll as branch_payroll
    #                , b.total_payroll as city_payroll
    #            FROM branch_table a
    #            JOIN branch_location_table b
    #                ON a.branch_id = b.branch_id
    #####

    The QueryHandler.create_type_from_yaml function will create a new Python
    class, AccountingData that has two functions:

        # These return pandas.DataFrame representations of the data returned
        # from the query.
        AccountingData.inventory
        AccountingData.payroll

    and will have attributes for the known conditional arguments and the query
    strings as well:

        # The file location of a generated yaml file that stores just the 
        # "inventory" section from the composite yaml file.
        AccountingData.__inventory_file

        # A string of the raw query for the inventory function.
        AccountingData.__inventory_query
        
        # A list of strings naming the different conditional arguments that 
        # were listed for the inventory function.
        AccountingData.__inventory_kwargs

        # These are repeated for any other functions as well:
        AccountingData.__payroll_file
        AccountingData.__payroll_query
        AccountingData.__payroll_kwargs

    Let's look at the inventory query. Because the file declares 
    accounting_id as a conditional name, that name will be interpreted as
    something that should be available as an argument for the inventory
    function, such as inventory(accounting_id=10). 

    Under the hood, this will generate a SQL WHERE condition (as in, 
    WHERE accounting_id = 10) that will get applied to the base results of
    whatever plain query was given for the inventory entry in the yaml file.

    In this manner, the function inventory acts like a specifier for WHERE
    conditions for the query it was given, such that only the items listed as
    conditionals can appear in the WHERE statements.

    So if we wanted to see the result of the inventory query where account_id
    is 10 and shipping date is 2012-12-31, we could say:

        qh = QueryHandler()
        AccountingData = qh.create_type_from_yaml('accounting_data.yaml')
        ad = AccountingData()
        data = ad.inventory(accounting_id=10, shipping_date='2012-12-31')

    But what about more options for the arguments you ask? This is handled with
    special keyword arguments that extend the given conditional names to
    include other operations, like BETWEEN or >= or IS NOT. These are shown
    below:

        # No use of any WHERE conditions
        ad.inventory()

        # WHERE account_id = 10
        ad.inventory(account_id=10)

        # WHERE account_id != 10
        ad.inventory(account_id_not_equal=10)

        # WHERE account_id > 10
        ad.inventory(account_id_greater_than=10)

        # WHERE account_id >= 10
        ad.inventory(account_id_greater_than_or_equal=10)

        # WHERE account_id < 10
        ad.inventory(account_id_less_than=10)

        # WHERE account_id <= 10
        ad.inventory(account_id_less_than_or_equal=10)

        # WHERE account_id BETWEEN 10 AND 20
        ad.inventory(account_id_between=(10, 20))

        # WHERE account_id IN (10, 11, 12)
        ad.inventory(account_id_in=(10, 11, 12))

        # WHERE account_id NOT IN (10, 11, 12)
        ad.inventory(account_id_not_in=(10, 11, 12))

        # WHERE account_id IS NULL
        ad.inventory(account_id_is=None)

        # WHERE account_id IS NOT NULL
        ad.inventory(account_id_is_not=None)
        ad.inventory(account_id_not_equal=None)

    To demonstrate string operations, we'll use the city variable from the
    payroll function:

        # WHERE city LIKE '%York%'
        ad.payroll(city_like=" '%York%' ")

        # WHERE city NOT LIKE '%York%'
        ad.payroll(city_not_like=" '%York%' ")

        # WHERE city ILIKE '%york%'
        ad.payroll(city_ilike=" '%york%' ")

        # WHERE city NOT ILIKE '%york%'
        ad.payroll(city_not_ilike=" '%york%' ")

    And some string conveniences are defined for matching the start or end of
    a string, and also checking if a string contains something. The appropriate
    SQL equivalent is given, assuming <pattern> represents the text to be 
    matched.

        # WHERE city LIKE '%<pattern>%'
        ad.payroll(city_contains="<pattern>")

        # WHERE city LIKE '<pattern>%'
        ad.payroll(city_startswith="<pattern>")        

        # WHERE city LIKE '%<pattern>'
        ad.payroll(city_endswith="<pattern>")     

    The "doc" keyword that appeared in the yaml file will create the function's
    documentation, along with the keyword arguments:

        help(ad.inventory)
        print ad.inventory.__doc__
        
    These will display:

        This is a query for inventory.
    
        Params
        ------
        account_id: A customer's account number.
        shipping_date: The shipping date.
    """
    # Array backend's base directory for locating query urls.
    BASEDIR = os.path.abspath(ArrayManagementClient().basedir)

    # Sub-folder of base dir for all autogenerated materials.
    AUTOGENDIR = pjoin(BASEDIR, "AUTO_GEN")

    # Sub-folder of base dir where assumed all custom files.
    FILEDIR = pjoin(BASEDIR, "CUSTOM_SQL")

    # Root directory name as far as query URLs are concerned.
    DATAROOT = "SQL_DATA"

    # Suffix to use for auto-gen folders coming from files, to
    # avoid having the folders end in '.yaml.'
    SUFFIX = ".autogen"

    def _parse_yaml(self, yaml_url):
        """
        Opens a compsite yaml of queries and returns a 3-tuple of the base name
        for the type that's to be created, the dictionary of data for that type
        and the list of names for the functions that will be created from the
        data.

        Params
        ------
        yaml_url: String naming a full path to a composite yaml file.

        Returns
        -------
        As a 3-tuple:
        type_name: Top-level data key from the yaml, used as the name of the
        created type.

        type_data: A dict containing the function keys and subsequent query
        data from the yaml.

        func_names: A list of the function name keys from the composite yaml.
        """
        with open(yaml_url, 'r') as stream: # Yaml should be validated here.
            obj = yaml.load(stream, Loader=yaml.CLoader)
        type_name = obj.keys()[0]
        type_data = obj[type_name]
        func_names = type_data.keys()
        return type_name, type_data, func_names

    def _publish_queries(self, class_url):
        """
        Creates a CUSTOM_SQL directory where the autogenerated queries will go.
        Publishes one yaml file per function key found in a composit yaml named
        by class_url.

        This is needed to conform to the ArrayManagement requirement that array
        clients must connect to query URLs that are relative to its known data
        path (from SQL_DATA) and the query files must have a single query. This
        function does the mapping from a composite url to the set of 
        single-query urls.

        Expects class_url to specify valid yaml, and for the url to be relative
        to BASEDIR.

        Params
        ------
        class_url: String naming a relative path to a composite yaml. Path must
        be relative to QueryHandler.BASEDIR

        Returns
        -------
        As a 5-tuple:
        query_files: List of the written single-query yamls.

        classdir: Path naming the created auto-gen directory where the queries
        have ben written.

        The following are returned by this function via an internal call to 
        _parse_yaml. See _parse_yaml for output information.

        type_name
        type_data
        func_names

        """
        full_url = pjoin(self.FILEDIR, class_url)
        type_name, type_data, func_names = self._parse_yaml(full_url)

        try:
            classdir = pjoin(self.AUTOGENDIR, class_url) + self.SUFFIX
            os.mkdir(classdir)
        except:
            # Should handle some errors and re-raise.
            pass

        query_files = {}
        for f_name in func_names:
            function_yaml = {"SQL":{f_name:type_data[f_name]}}
            output_file = pjoin(classdir, f_name) + ".yaml"
            with open(output_file, 'w') as output:
                yaml.dump(function_yaml, output)
            query_files[f_name] = output_file

        return query_files, classdir, type_name, type_data, func_names

    def _publish_docstring(self, function_description):
        """
        Expects the dictionary of function data from the Yaml to be passed
        in as function_description.

        Develops the function's docstring and keyword arg docs from the
        description and returns it as a string. Also returns a list of the
        discovered keyword arguments.

        Params
        ------
        function_description: A dictionary of the data form a composite yaml
        that describes a query function.

        Returns
        -------
        known_args: A list of the keyword args as strings.
        
        function_doc: The docstring of the function.
        """
        # Get annotated keyword args and docs.
        known_args_docs = function_description.get('conditionals', {})
        known_args = known_args_docs.keys()

        # Process arg-specific docs onto function's docstring.
        function_doc = function_description['doc'] + "\n\nParams\n------\n"
        if known_args == {}:
            function_doc += "None.\n"
        else:
            for k_arg in known_args:
                function_doc += k_arg + ": " + known_args_docs[k_arg] + "\n"
        return known_args, function_doc

    def _function_factory(self, 
                          query_url, 
                          function_name, 
                          function_desc, 
                          known_args):
        """
        """
        url = query_url.split(self.DATAROOT)[1]
        def function(self, **kwargs):                    
            aclient = ArrayManagementClient()
            arr = aclient.aclient[url]

            # Create a Keyword Handler.
            kw_handler = KeywordHandler(arr)
            op_names = kw_handler.supported_ops()
            sql_names = kw_handler.supported_sql()

            # For each arg in known_args, loop over each
            # supported sql word and make a function that
            # gets invoked on the kw val, <base_arg>_<sql_word>
            kw_arg_responses = {}
            for base_arg in known_args:
                base_arg = base_arg.lower()
                for sql_name in sql_names:
                    compound_arg = base_arg + "_" + sql_name
                    kw_arg_responses[compound_arg] = (
                        kw_handler.sql_bind(base_arg, sql_name))

                for op_name in op_names:
                    if op_name == "":
                        compound_arg = base_arg
                    else:
                        compound_arg = base_arg + "_" + op_name
                    kw_arg_responses[compound_arg] = (
                        kw_handler.op_bind(base_arg, op_name))

            # To be used for more verbose documentation?
            all_possible_args = kw_arg_responses.keys()

            # Form the array backend object's connection.
            # This should be wrapped in a connection handling class.

            # Form the conditions needed to communicate the
            # logical request of the function's invoker.
            none = lambda *args, **kwargs: None
            conditions = []
            for attr, val in kwargs.iteritems():
                attr = attr.lower()
                response_function = kw_arg_responses.get(attr, none)
                if isinstance(val, (tuple, list, set)):
                    conditions.append(response_function(*val))
                elif isinstance(val, dict):
                    conditions.append(response_function(**val))
                else:
                    conditions.append(response_function(val))
                    
            # Handle case of no arguments.
            select_arg = and_(*conditions) if conditions else None
                    
            return arr.select(select_arg)
        return function

    def create_type_from_yaml(self, class_url):
        """
        Expects class_url to point to a properly formatted .yaml file
        for ingesting a set of related queries as functions exposed
        on a new class.
        """
        type_dict = {}
        #try:
        #    self.validate_yaml(class_url)
        #except:
        #    pass

        query_files, classdir, type_name, type_data, func_names = (
            self._publish_queries(class_url))

        for function_name in func_names:
            query_url = query_files[function_name]
            function_desc = type_data[function_name]
            query = function_desc["query"]
            known_args, function_doc = self._publish_docstring(function_desc)

            # Create the function wrapper for this query.
            f = self._function_factory(query_url, 
                                       function_name, 
                                       function_desc, 
                                       known_args)

            # Give the function attribute the name and docstring intended by
            # the user.
            f.__name__, f.__doc__ = function_name, function_doc

            # Place the function and metadata into the type dict.
            type_dict[function_name] = f
            type_dict["__" + function_name + "_file"] = query_url
            type_dict["__" + function_name + "_query"] = query
            type_dict["__" + function_name + "_kwargs"] = known_args

        return type(type_name, (object,), type_dict)        
        
if __name__ == "__main__":
    import os

    test_query_url = "test_yaml.yaml"
    UniverseBuilder = QueryHandler().create_type_from_yaml(test_query_url)
    ub = UniverseBuilder()

    # Inferred 'gicsec' query API:
    #ub.gicsec()             # <--- Callable. No args at the moment just for testing.
    print ub.__gicsec_kwargs # <--- Function signature for this query.
    print ub.__gicsec_query  # <--- Query saved as a string from file.

    # Inferred 'spx' query API:
    #ub.spx_universe() 
    print ub.__spx_universe_kwargs 
    print ub.__spx_universe_query 

    # Example of actually perfomring a query (assumes TR VPN):
    ex_date = '2013-12-31'
    df = ub.spx_universe(DATE_=ex_date, ITICKER='SPX_IDX')

    print "Result for SPX IDX query for {}".format(ex_date)
    print df.head()
