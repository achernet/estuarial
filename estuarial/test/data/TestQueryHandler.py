"""
Unit tests for QueryHandler.

Author: Ben Zaitlen and Ely Spears
"""
import operator
import unittest
import functools
from estuarial.data.yaml_handler import YamlHandler
from estuarial.data.query_handler import QueryHandler
from estuarial.data.keyword_handler import KeywordHandler
from estuarial.array.arraymanagementclient import ArrayManagementClient

class TestQueryHandler(unittest.TestCase):

    def setUp(self):
        """
        There are items needed for testing the QueryHandler:
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


        self.query_handler = QueryHandler()
        self.test_composite_yaml = "test_yaml.yaml"

        # Arguments expected from the test composite yaml file.

    def test__class_constants(self):
        """
        Places checks for the needed class constants.
        """
        pass

    def test__publish_queries(self):
        """
        1. Test that a directory is created when once is not present.
        2. Test that no OSError is raised when trying to create a
           directory if it does exist.
        3. Test that any autogen files created conform to the required
           yaml format. TODO: move this into some util validation code.
        4. Test that the output arguments are as expected.
        """
        # Remove the directory that will be created.
        # Execute the function and save arguments.
        # Check that directory was created.
        # Execute the function again and assert no exceptions.
        # Examine and validate each of the autogen-written files.

    def test__publish_docstring(self):
        """
        """
        pass

    def test__function_factory(self):
        """
        """
        pass
        
    def test_create_type_from_yaml(self):
        """
        """
        pass

if __name__ == "__main__":
    unittest.main()
        
