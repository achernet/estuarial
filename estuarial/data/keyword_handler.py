"""
Handle binding keyword arguments to SQL and operator functions.

Author: Ben Zaitlen and Ely Spears
"""
import operator
import functools

class KeywordHandler(object):
    """
    With an array client object (array_client), this class binds special words
    to counterpart SQL function or operator names. Given a base argument named 
    base_arg and some SQL or operator name, op_name, the class will look up 
    whether op_name is a supported operation and translate it into op_function, 
    the actual function name to be used.

    If op_function is a form of SQL exposed by the sqlalchemy api, then the
    method sql_bind allows for retrieving the function described by

        array_client.<base_arg>.<op_function>

    If op_function is instead a supported function from the operator module,
    a new function will be created in the method op_bind as:

        lambda x: op_function(array_client.<base_arg>, x)

    array_client.<base_arg> refers to the sqlalchemy ColumnClause object
    exposed as an attribute on array_client based on the yaml that was used to
    construct it.

    The returned function from with sql_bind or op_bind can then be used to
    provide extended SQL or operator functionality from a limited set of
    keyword arguments to a calling function that uses KeywordHandler.
    """

    # Map from human-readable names (keys) that can serve as augmented keyword
    # arguments, into the actual sqlalchemy names for the sql functions.
    _SUPPORTED_SQL = {"is":"is_",
                      "is_not":"isnot",
                      "in":"in_",
                      "not_in":"notin_",
                      "like":"like",
                      "not_like":"notlike",
                      "ilike":"ilike",
                      "not_ilike":"notilike",
                      "between":"between",
                      "contains":"contains",
                      "endswith":"endswith",
                      "startswith":"startswith"}

    # Map of logicals supported from operator module. Note that operator.eq
    # gets no special name mapping to it. This allows for just plain <base_arg>
    # as a keyword to map to equality with the value passed for that argument.
    # So if "date" is a conditional argument named in the yaml file, then saying
    # "date=foo" maps to "operator.eq(date, foo)" whereas saying 
    # "date_not_equal=foo" is required if you want to achieve "date != foo"
    _SUPPORTED_OPS = {"":"eq",
                      "not_equal":"ne",
                      "greater_than":"gt",
                      "greater_than_or_equal":"ge",
                      "less_than":"lt",
                      "less_than_or_equal":"le"}
    
    def __init__(self, array_client):
        """
        Assign an instance of the array backend client to the keyword
        handler when it is constructed.

        Params
        ------
        array_client: An array client object that implements a subset of
        the sqlalchemy api and contains possible keyword argument names
        as bound sqlalchemy ColumnClause objects.

        Returns
        -------
        None. Just adds the array_client attribute to the class instance.
        """
        self.array_client = array_client

    def supported_sql(self):
        """
        Convenience function to return class's dict of operations supported
        from the the sqlalchemy API subset exposed by an array client instance.

        Params
        ------
        None.

        Returns
        -------
        supported_sql: Dictionary of shorthand names (keys) mapping to alchemy
        sql module attributes (values) that represent functions supported for 
        binding on keywords.
        """
        supported_sql = self._SUPPORTED_SQL
        return supported_sql

    def supported_ops(self):
        """
        Convenience function to return class's dict of operations supported
        from the operator module.

        Params
        ------
        None.

        Returns
        -------
        supported_ops: Dictionary of shorthand names (keys) mapping to operator
        module attributes (values) that represent functions supported for 
        binding on keywords.
        """
        supported_ops = self._SUPPORTED_OPS
        return supported_ops

    def sql_bind(self, base_arg, sql_primitive_name):
        """
        Looks up a sqlalchemy function name (sql_name) that is keyed by
        sql_primitive_name, and then retrieves and returns the bound sql-
        alchemy function described by:

            self.array_client.<base_arg>.<sql_name>

        Params
        ------
        base_arg: A string naming a conditional (keyword) argument such that it
        exists as an attribute on self.array_client. Since array_client was
        created via a yaml stating the query parameters, it will have bound
        sql-alchemy attributes for the various keyword arguments.
        
        sql_primitive_name: A string naming one of the exposed alchemy functions
        supported in (the values of) KeywordHandler._SUPPORTED_SQL. The alchemy
        function will appear as an attribute on self.array_client.

        Returns
        -------
        keyword_sql_function: A handle to the function described by getting the
        sql_primitive_name attribute on the base_arg attribute of array_client.

        Effectively, if sql_name = self._SUPPORTED_SQL[sql_primitive_name], then
        keyword_sql_function = self.array_client.<base_arg>.<sql_name>.
        """
        # Map the requested name into the actual name exposed by alchemy.
        sql_name = self._SUPPORTED_SQL[sql_primitive_name]

        # For the base_arg passed (e.g. "date" or "ticker" or some keyword
        # declared in a yaml file) get the attribute from the array client that
        # was constructed for that name.
        array_client_keyword = getattr(self.array_client, base_arg)

        # The array_client_keyword is an alchemy construct, so it will have
        # attributes such as "in_", "between", etc., as in the alchemy API. Get
        # the attribute from that API that matches sql_name. This will be a
        # function that, when called with arguments, creates a SQL object that
        # can be passed to the alchemy API's select function.
        keyword_sql_function = getattr(array_client_keyword, sql_name)

        # Return this keyword-derived function.
        return keyword_sql_function
    
    def op_bind(self, base_arg, op_primitive_name):
        """
        Looks up a operator module function name (op) that is keyed by
        op_primitive_name, and then retrieves and returns the bound sql-
        alchemy function described by:

            lambda x: op(self.array_client.<base_arg>, x)

        For example, if op_name is "greater_than" and it maps to operator.gt,
        then 

            lambda x: op(self.array_client.<base_arg>, x) 

        is the same as a function that, given x, evaluates the expression 
        
            self.array_client.<base_arg> > x

        which yields a sqlalchemy object that can be passed to the array_client
        select function.

        Params
        ------
        base_arg: A string naming a conditional (keyword) argument such that it
        exists as an attribute on self.array_client. Since array_client was
        created via a yaml stating the query parameters, it will have bound
        sql-alchemy attributes for the various keyword arguments.
        
        op_primitive_name: A string naming one of the exposed alchemy functions
        supported in (the values of) KeywordHandler._SUPPORTED_SQL. The alchemy
        function will appear as an attribute on self.array_client.

        Returns
        -------
        keyword_sql_function: A handle to the function described by getting the
        sql_primitive_name attribute on the base_arg attribute of array_client.

        Effectively, if sql_name = self._SUPPORTED_SQL[sql_primitive_name], then
        keyword_sql_function = self.array_client.<base_arg>.<sql_name>.
        """
        # Map the requested operation name into an operator-as-function
        # provided by the operator module.
        op_name = self._SUPPORTED_OPS[op_primitive_name]

        # Get that operator from the module.
        op = getattr(operator, op_name)

        # For the base_arg passed (e.g. "date" or "ticker" or some keyword
        # declared in a yaml file) get the attribute from the array client that
        # was constructed for that name.
        array_client_keyword = getattr(self.array_client, base_arg)

        # Create a function from op by binding the first argument to be the
        # alchemy-based array_client_keyword. When the function is called on a
        # value, it will be the same as op(array_client_keyword, value). So if
        # op wound up being "==" (operator.eq) this would mean an alchemy object
        # would be created as array_client_keyword == value.
        keyword_op_function = functools.partial(op, array_client_keyword)
        
        # Returns the keyword-derived operator module function.
        return keyword_op_function
        
if __name__ == "__main__":
    pass
    
