"""
Unit tests for KeywordHandler.

Author: Ben Zaitlen and Ely Spears
"""
import operator
import unittest
import functools
from estuarial.data.keyword_handler import KeywordHandler
from estuarial.array.arraymanagementclient import ArrayManagementClient

class TestKeywordHandler(unittest.TestCase):

    def setUp(self):
        """
        There are four items needed for testing the KeywordHandler:
          1. An array client backend instance.

          2. Test yaml url that the client can connect to. This will be forced
             to reside relative to the client's basedir attribute.

          3. When the client is constructed from the url, you need to have
             exposed some conditional keyword args that get bound as alchemy
             ColumnClause objects -- this is exactly what is being tested.

          4. The connected array client object, which is needed for the 
             constructor of KeywordHandler.
        """
        self.aclient = ArrayManagementClient()
        self.example_url = '/UNIVERSE_SQL/dowjones_universe.yaml'
        self.example_keywords = ("date_", "iticker")
        self.array = self.aclient.aclient[self.example_url]
        self.keyword_handler = KeywordHandler(self.array)

        # Some additional helper variables to reduce repeated code.
        self._SUPPORTED_SQL = "_SUPPORTED_SQL"
        self._SUPPORTED_OPS = "_SUPPORTED_OPS"
        self.array_client_attribute = "array_client"
        self.column_clauses = map(lambda x: getattr(self.array, x), 
                                  self.example_keywords)

    def test__SUPPORTED_SQL(self):
        """
        Ensures that the values in KeywordHandler._SUPPORTED_SQL are all valid
        alchemy attributes that exist on the exposed ColumnClause objects.
        """
        for column_clause in self.column_clauses:
            for _, sql_attr in self.keyword_handler._SUPPORTED_SQL.iteritems():
                self.assertTrue(hasattr(column_clause, sql_attr))

    def test__SUPPORTED_OPS(self):
        """
        Ensures that the values in KeywordHandler._SUPPORTED_OPS are all valid
        operator module attributes.
        """
        for column_clause in self.column_clauses:
            for _, op_attr in self.keyword_handler._SUPPORTED_OPS.iteritems():
                self.assertTrue(hasattr(operator, op_attr))

    def test___init__(self):
        """
        Check that constructor assigns array_client attribute and that created
        instance has _SUPPORTED_SQL and _SUPPORTED_OPS.
        """
        for attr in [self._SUPPORTED_SQL,
                     self._SUPPORTED_OPS,
                     self.array_client_attribute]:
            self.assertTrue(hasattr(self.keyword_handler, attr))

    def test_supported_sql(self):
        """
        Check that supported_sql() returns _SUPPORTED_SQL
        """
        supported_sql_function_call = self.keyword_handler.supported_sql()
        supported_sql_attribute = getattr(self.keyword_handler, 
                                          self._SUPPORTED_SQL)
        self.assertEqual(supported_sql_function_call, supported_sql_attribute)

    def test_supported_ops(self):
        """
        Check that supported_ops() returns _SUPPORTED_OPS
        """
        supported_ops_function_call = self.keyword_handler.supported_ops()
        supported_ops_attribute = getattr(self.keyword_handler, 
                                          self._SUPPORTED_OPS)
        self.assertEqual(supported_ops_function_call, supported_ops_attribute)

    def test_sql_bind(self):
        """
        Check that argument-name and sql-name pair will correctly bind to the 
        analogous sql-name attribute on the array_client.<argument-name> 
        aclhemy object. 

        Check that passing an unsupported name (such as a misspelling) will
        raise appropriate exceptions.
        """
        # Get the dict of sql items to check.
        all_sql_items = self.keyword_handler.supported_sql()

        # For all possible (argument-name, sql-name) pairs, check that the 
        # handler binds to the expected sqlaclhemy api object.
        for base_arg_name in self.example_keywords:
            for sql_name, sql_api_name in all_sql_items.iteritems():

                # Use the handler's binding function.
                auto_bound_sql = self.keyword_handler.sql_bind(base_arg_name,
                                                               sql_name)

                # Manually get the attributes that the handler should be binding.
                manual_bound_sql = getattr(
                    getattr(self.keyword_handler.array_client, base_arg_name), 
                    sql_api_name)
                                 
                # Assert that fetching the attributes manually would produce the
                # same result as calling the handler's bind function.
                self.assertEqual(auto_bound_sql, manual_bound_sql)

                
        # Check that misspelling a base argument name results in an exception.
        misspelled_base_name = self.example_keywords[0][::-1]
        example_sql_name = all_sql_items.keys()[0]
        self.assertRaises(Exception, 
                          self.keyword_handler.sql_bind, 
                          misspelled_base_name, 
                          example_sql_name)

        # Check that misspelling a sql name results in an exception.
        example_base_name = self.example_keywords[0]
        misspelled_sql_name = all_sql_items.keys()[0][::-1] + "_foo_bar"
        self.assertRaises(Exception, 
                          self.keyword_handler.sql_bind, 
                          example_base_name, 
                          misspelled_sql_name)
        
    def test_op_bind(self):
        """
        Check that argument-name and op-name pair will correctly bind to the 
        analogous operator module attribute. 

        Check that passing an unsupported name (such as a misspelling) will
        raise appropriate exceptions.
        """
        # A helper function for determining if two partially bound functions
        # are logically the same.
        def are_equal(partial_func1, partial_func2):
            same_base_func = (partial_func1.func is partial_func2.func)
            same_args = (partial_func1.args == partial_func2.args)
            same_kwargs = (partial_func1.keywords == partial_func2.keywords)
            return all((same_base_func, same_args, same_kwargs))

        # Get the dict of sql items to check.
        all_ops_items = self.keyword_handler.supported_ops()

        # For all possible (argument-name, sql-name) pairs, check that the 
        # handler binds to the expected sqlaclhemy api object.
        for base_arg_name in self.example_keywords:
            for op_name, op_api_name in all_ops_items.iteritems():

                # Use the handler's binding function.
                auto_bound_op = self.keyword_handler.op_bind(base_arg_name,
                                                             op_name)

                # Manually get the attributes that the handler should be binding.
                op_api_function = getattr(operator, op_api_name)
                alchemy_base_object = getattr(self.keyword_handler.array_client, 
                                              base_arg_name)

                # Manually perform the partial binding that the handler performs.
                manual_bound_op = functools.partial(op_api_function,
                                                    alchemy_base_object)
                                 
                # Assert that fetching the attributes manually would produce the
                # same result as calling the handler's bind function.
                self.assertTrue(are_equal(auto_bound_op, manual_bound_op))

                
        # Check that misspelling a base argument name results in an exception.
        misspelled_base_name = self.example_keywords[0][::-1]
        example_ops_name = all_ops_items.keys()[0]
        self.assertRaises(Exception, 
                          self.keyword_handler.op_bind, 
                          misspelled_base_name, 
                          example_ops_name)

        # Check that misspelling an ops name results in an exception.
        example_base_name = self.example_keywords[0]
        misspelled_ops_name = all_ops_items.keys()[0][::-1] + "_foo_bar"
        self.assertRaises(Exception, 
                          self.keyword_handler.op_bind, 
                          example_base_name, 
                          misspelled_ops_name)

if __name__ == "__main__":
    unittest.main()
        
