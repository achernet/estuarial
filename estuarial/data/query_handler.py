"""
Construct (directly from a yaml DSL) Python classes that can perform flexible
queries including support for common SQL operations on keyword args.

Author: Ben Zaitlen and Ely Spears
"""
import os
import yaml
from sqlalchemy import sql
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

    For example, consider the following sample composite query file which is
    saved in "/test/test_example.yaml" relative to QueryHandler._FILE_DIR.
    
    #######################################################
    #AccountingData:                                      #
    #    inventory:                                       #
    #        doc: This is a query for inventory.          #
    #        conditionals:                                #
    #            account_id: A customer's account number. #
    #            shipping_date: The shipping date.        #
    #        query: >                                     #
    #            SELECT                                   #
    #                  a.account_id as account_id         #
    #                , b.shipping_id as shipping_id       #
    #                , a.customer_name                    #
    #                , b.shipping_date                    #
    #                , b.order_volume                     #
    #                , b.total_sales                      #
    #            FROM account_table a                     #
    #            JOIN shipping_table b                    #
    #                ON a.account_id = b.shipping_id      #
    #                                                     #
    #    payroll:                                         #
    #        doc: This is a payroll query.                #
    #        conditionals:                                #
    #            branch_id: A branch id number            #
    #            city: A city name                        #
    #        query: >                                     #
    #            SELECT                                   #
    #                  a.branch_id                        #
    #                , b.city                             #
    #                , a.total_payroll as branch_payroll  #
    #                , b.total_payroll as city_payroll    #
    #            FROM branch_table a                      #
    #            JOIN branch_location_table b             #
    #                ON a.branch_id = b.branch_id         #
    #######################################################

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
    # Base directory where the array backend searches for all files.
    # Should be determined by settings in library config. 
    _BASE_DIR = os.path.abspath(ArrayManagementClient().basedir)
    # TODO: remove reliance on constructing client to get directory name.

    _FILE_DIR = pjoin(_BASE_DIR, "CUSTOM_SQL")  # Dir for user-supplied yaml
    _DATA_ROOT = os.path.split(_BASE_DIR)[1]    # Root query dir name
    _AUTOGEN_DIR = pjoin(_BASE_DIR, "AUTO_GEN") # Location for auto gen yamls

    _PATH_SEP = "__"                        # Sentinel to flatten url names
    _YAML_EXT = ".yaml"                     # Extension for yamls
    _NO_ARG_DOC = "None.\n"                 # Param doc when no kwargs given
    _PARAMS_HEADER = "\n\nParams\n------\n" # Param header for docstring text
    _AUTOGEN_SUFFIX = ".autogen"            # Autogen dir name suffix
    _SINGLE_QUERY_HEADER = "SQL"            # Required in single-query yamls

    _DOC = "doc"                   # docstring infor from yaml
    _QUERY = "query"               # raw query string from yaml
    _CONDITIONALS = "conditionals" # keyword arg names from yaml
    _KW_DELIMITER = "_"            # Used when augmenting keyword arg names.

    # Label for raised exception displayed when generated functions encounter
    # invalid keyword arguments.
    _INVALID_KWARG_MSG = "[unsupported] "

    
    def _path_sanitizer(self, some_path):
        """
        Replace filesystem slashes with _PATH_SEP, so that within the autogen
        folder, autogen names still retain some of the directory structure of
        the source location they came from.

        Params
        ------
        some_path: String naming a path to sanitize for autogen.

        Returns
        -------
        The result is some_path, where the os module's path separator is 
        replaced by QueryHandler._PATH_SEP, allowing directories in the path
        to remain intact when the name is flattened to prefix an autogen
        directory.
        """
        dirs, file_name = os.path.split(some_path)
        dirs = dirs.replace(os.path.sep, self._PATH_SEP)
        return dirs + self._PATH_SEP + file_name

    def _publish_queries(self, class_url):
        """
        Creates a CUSTOM_SQL directory where the autogenerated queries will go.
        Publishes one yaml file per function key found in composite yaml named
        by class_url.

        Expects class_url to specify valid yaml, and for the url to be relative
        to "<_BASEDIR>/CUSTOM_SQL/".

        Params
        ------
        class_url: String naming a relative path to a composite yaml. Path must
        be relative to "<QueryHandler._BASEDIR>/CUSTOM_SQL/"

        Returns
        -------
        As a 4-tuple:
        query_files: List of the written single-query yamls.

        type_name: Top-level data key from the yaml, used as the name of the
        created type.

        type_data: A dict containing the function keys and subsequent query
        data from the yaml.

        func_names: A list of the function name keys from the composite yaml.
        """
        # This is needed to conform to the ArrayManagement requirement that 
        # array clients must connect to query URLs that are relative to its 
        # known data path and the query files must have a single query. This
        # function does the mapping from a composite url to the set of single-
        # query urls.

        # Ensure the relative class_url is extended to specify the full path
        # according to QueryHandler._FILE_DIR -- a parameter that should be 
        # part of the library config.
        full_url = pjoin(self._FILE_DIR, class_url)

        # Acquire the query annotations from yaml file.
        with open(full_url, 'r') as stream:
            obj = yaml.load(stream, Loader=yaml.CLoader)

        type_name = obj.keys()[0]     # Class name at absolute top of yaml.
        type_data = obj[type_name]    # Sub-dict of all data for this yaml.
        func_names = type_data.keys() # List of function names declared in yaml

        # Create a sub-directory for placing any autogenerated single-query
        # yaml files that arise from the class_url's composite yaml.
        sanitized_url = self._path_sanitizer(class_url)
        class_dir = (pjoin(self._AUTOGEN_DIR, sanitized_url) + 
                     self._AUTOGEN_SUFFIX)

        try:
            os.mkdir(class_dir)
        except OSError as os_error:
            # If directory exists already, ignore the Exception, otherwise
            # re-raise.
            if os_error.errno != 17:
                raise os_error

        # Prepare the names of the autogenerated single-query yamls. Key these
        # on the name of the function they correspond to.
        query_files = {}
        for f_name in func_names:

            # The single-query yaml files have a fixed convention of starting
            # with a top level name given by QueryHandler._SINGLE_QUERY_HEADER
            function_yaml = {
                self._SINGLE_QUERY_HEADER:{f_name:type_data[f_name]}}

            # The file's path points to the created class directory and is
            # named <function_name>.yaml.
            output_file = pjoin(class_dir, f_name) + self._YAML_EXT
            
            # Dump the contents as yaml to the file.
            with open(output_file, 'w') as output:
                yaml.dump(function_yaml, output)

            # Record this autogen file location for later use.
            query_files[f_name] = output_file

        # Return a bunch of the metadata needed for creating the class
        # from the composite yaml.
        return (query_files, # Dict of (function name, autogen file) pairs. 
                type_name,   # Name of the created class.
                type_data,   # Contents of the original composite yaml.
                func_names)  # List of function names from composite yaml.

    def _publish_docstring(self, function_description):
        """
        Develops the function's docstring and keyword arg docs from the
        description and returns it as a string. Also returns a list of the
        discovered keyword arguments.

        Expects the dictionary of function data from the Yaml to be passed
        in as function_description.

        Params
        ------
        function_description: A dictionary of the data from a composite yaml
        that describes a query function.

        Returns
        -------
        known_args: A list of the keyword args as strings.
        
        function_doc: The docstring of the function.
        """
        # Get annotated keyword args and docs.
        known_docs = function_description.get(self._CONDITIONALS, {})
        known_args = known_docs.keys()

        # Prepare header for parameter section of docstring.
        function_doc = function_description[self._DOC] + self._PARAMS_HEADER

        # Process arg-specific docs into function's docstring. Modify this
        # region to produce different Sphinx-compliant output.
        for k_arg in known_args:
            function_doc += "{}: {}\n".format(k_arg, known_docs[k_arg])

        # If no args, add description for no-arg case
        if not known_args:
            function_doc += self._NO_ARG_DOC
            
        return (known_args,   # List of known keyword arg names.
                function_doc) # The full docstring for the created function.

    def _function_factory(self, query_url, function_name, known_args):
        """
        Given a query file path (containing a single query), the name of the
        function to be created, the data (doc and query string) from the yaml 
        file for this function, and the list of known conditional arguments,
        this method will create and return a function that performs the 
        described query.

        Params
        ------
        query_url: full path to single query file (optionally can just be the
        path relative to QueryHandler._DATA_ROOT).

        function_name: the name of the function to be created.

        known_args: a list of the keyword arguments, derived from the 
        "conditionals" key in the yaml.

        Returns
        -------
        function: The created function object.
        """
        # Ensure that the url is relative to QueryHandler._DATA_ROOT.
        url = query_url.split(self._DATA_ROOT)[1]
        
        # Grab needed QueryHandler constants since referring to 'self' won't
        # refer to QueryHandler in the function body below.
        KW_DELIMITER = self._KW_DELIMITER
        INVALID_KWARG_MSG = self._INVALID_KWARG_MSG

        def function(self, **kwargs):                    
            kwarg_responses = {}                   # Contain alchemy functions
            alchemy_where_statements = []          # Contain WHERE clauses
            aclient = ArrayManagementClient()      # Instantiate array backend
            arr = aclient.aclient[url]             # Connect array to url
            kw_handler = KeywordHandler(arr)       # Handler for sql binding
            op_names = kw_handler.supported_ops()  # Supported comparison ops
            sql_names = kw_handler.supported_sql() # Supported sql attributes

            # Extend each basic kw_arg that comes form the yaml "conditionals"
            # into a series of many keyword args, one for each supported SQL or
            # OP known to KeywordHandler.
            for base_arg in known_args:

                # Remove case-sensitivity of conditional column names.
                base_arg = base_arg.lower()

                # For each alchemy attribute, bind that attribute of the 
                # array's alchemy-based version of base_arg to a new keyword 
                # arg name that augments base_arg with the sql attribute name.
                for sql_name in sql_names:
                    compound_arg = base_arg + KW_DELIMITER + sql_name
                    kwarg_responses[compound_arg] = (
                        kw_handler.sql_bind(base_arg, sql_name))

                # For each regular comparison operator, "op", supported, bind a 
                # lambda (from KeywordHandler) that will perform 
                # op(base_arg, val) whenever passed "val" as an argument.
                for op_name in op_names:
                    if op_name == "": # Special case of "==" bound to base_arg.
                        compound_arg = base_arg
                    else:
                        compound_arg = base_arg + KW_DELIMITER + op_name
                    kwarg_responses[compound_arg] = (
                        kw_handler.op_bind(base_arg, op_name))

            # Look at the actual keywords and values supplied when the user 
            # calls the function. Look up the appropriate bound response as 
            # added to kwarg_responses above, and invoke it on the user 
            # supplied value. This generates a bound alchemy WHERE conditon.
            # Accumulate all such WHERE conditions for passing into select.
            for user_supplied_kw, user_supplied_val in kwargs.iteritems():
                lower_kw = user_supplied_kw.lower()

                # Fetch the function to use in response to this keyword.
                try:
                    response_function = kwarg_responses[lower_kw]
                except KeyError as key_error:
                    message = (INVALID_KWARG_MSG + 
                               "unrecognized keyword argument '{}'")
                    raise TypeError(message.format(lower_kw))

                # Depending on what type of sequence the user supplied value
                # is, call the response function on the value's contents.
                if isinstance(user_supplied_val, (tuple, list, set)):
                    where_condition = response_function(*user_supplied_val)
                elif isinstance(user_supplied_val, dict):
                    where_condition = response_function(**user_supplied_val)
                else:
                    where_condition = response_function(user_supplied_val)
                # TODO: should the arg unpacking above handle numpy arrays or
                # Pandas?

                # Append the resultant alchemy-bound statement to build the
                # list of WHERE conditionals.
                alchemy_where_statements.append(where_condition)
                    
            # Combine all of the WHERE conditionals with AND. If there are no
            # conditions, use None to denote running an unconditional query.
            select_arg = (sql.and_(*alchemy_where_statements) 
                          if alchemy_where_statements else None)
                    
            # Return the result of the array client's selection using the built
            # WHERE conditionals.
            return arr.select(select_arg)

        # Return the constructed function.
        return function

    def create_type_from_yaml(self, class_url):
        """
        Expects class_url to point to a properly formatted .yaml file
        for ingesting a set of related queries as functions exposed
        on a new class.
        """
        type_dict = {} # Container for attributes for created class.

        # Get necessary data extracted from composite yaml.
        query_files, type_name, type_data, func_names = (
            self._publish_queries(class_url))

        # For each function name declared in composite yaml, create a
        # python function that exposes its query.
        for function_name in func_names:

            # Single-query yaml for this function
            query_url = query_files[function_name]

            # Doc, conditionals, and query data from function's yaml section.
            function_desc = type_data[function_name] 

            # Retrieve query string
            query = function_desc[self._QUERY] 

            # Argument names and function docstring.
            known_args, function_doc = self._publish_docstring(function_desc)

            # Create the function wrapper for this query.
            f = self._function_factory(query_url, function_name, known_args)

            # Patch name and docstring intended by the user.
            f.__name__, f.__doc__ = function_name, function_doc

            # Place the function and metadata into the type dict.
            type_dict[function_name] = f
            type_dict["__" + function_name + "_file"] = query_url
            type_dict["__" + function_name + "_query"] = query
            type_dict["__" + function_name + "_kwargs"] = known_args

        # Return created class object.
        return type(type_name, (object,), type_dict)        
        
if __name__ == "__main__":


    if False:
        test_query_url = "test/test_example.yaml"
        qh = QueryHandler()
        AccountingData = qh.create_type_from_yaml(test_query_url)
        ad = AccountingData()
    else:
        test_query_url = "test/test_composite.yaml"
        qh = QueryHandler()
        UniverseBuilder = qh.create_type_from_yaml(test_query_url)
        ub = UniverseBuilder()

        # Inferred 'gicsec' query API:
        #ub.gicsec()             # <--- Callable. No args at the moment just for testing.
        #print ub.__gicsec_kwargs # <--- Function signature for this query.
        #print ub.__gicsec_query  # <--- Query saved as a string from file.

        # Inferred 'spx' query API:
        #ub.spx_universe() 
        #print ub.__spx_universe_kwargs 
        #print ub.__spx_universe_query 

        # Example of actually perfomring a query (assumes TR VPN):
        ex_date = '2013-12-31'
        df = ub.spx_universe(DATE_=ex_date, ITICKER='SPX_IDX')

        print "Result for SPX IDX query for {}".format(ex_date)
        print df.head()
