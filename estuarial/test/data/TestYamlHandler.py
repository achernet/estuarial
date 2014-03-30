"""
Unit tests for YamlHandler, ensuring that it validates Yaml as expected.

Author: Ben Zaitlen and Ely Spears
"""
import yaml
import unittest
from estuarial.data.yaml_handler import YamlHandler

class TestYamlHandler(unittest.TestCase):
    """
    Exercises the code responsible for validating that singleton or composite
    yaml documents adhere to the standards required for the query and caching
    system to load them and make use of the queries within them.
    """

    def setUp(self):
        """
        Prepare handler objects and paths needed for testing that composite
        SQL-query yaml documents are processed and correctly converted into 
        
        """
        self.yaml_handler = YamlHandler()

        # Make a few valid variable names and invalid ones for testing.
        self.valid_vars = ("_name", "Variable", "v4r_7", "_", "_2")
        self.invalid_vars = (
            "3rd_x", 
            "foo.bar", 
            "var$foo", 
            "TypeError", 
            "if", 
            "elif", 
            "else", 
            "True",
            "False",
            "true",
            "false", 
            "None"
        )

        # A set of conditional values that have valid names and docs.
        self.synthetic_valid_conditionals = {
            "some_var":"some doc",
            "some_other_var":u"some unicode doc",
            "some_undocumented_var":None
        }

        # Testing that an empty set of conditionals is valid.
        self.synthetic_valid_conditionals_empty = {}


        # Invalid because name is not a permissible variable name.
        self.synthetic_invalid_conditional_name = {
            "foo.bar":"some doc"
        }

        # Invalid because name is not of an allowed type.
        self.synthetic_invalid_conditional_name_type = {
            (1,2,3):"some_doc"
        }

        # Invalid because doc string is of an invalid type.
        self.synthetic_invalid_conditional_doc_type = {
            "some_var":(1,2,3)
        }


        self.valid_sythetic_singleton_yamls = (
            """SQL:
                   some_name:
                       doc: some docs
                       query: some query
            """,

            # With conditionals
            """SQL:
                   some_name:
                       doc: some docs
                       conditionals:
                           cond1: cond1 docs 
                           cond2: cond2 docs
                       query: some query
            """,

            # Missing conditional docs is OK.
            """SQL:
                   some_name:
                       doc: some docs
                       conditionals:
                           cond1: 
                           cond2: cond2 docs
                       query: some query
            """,
        )


        self.invalid_synthetic_singleton_yamls = (
            # Invalid top-level identifier.
            """MySQL:
                   some_name:
                       doc: some doc
                       query: some query
            """,

            # Invalid variable name for the query function name.
            """SQL:
                   1st_name:
                       doc: some doc
                       query: some query
            """,

            # Missing documentation content
            """SQL:
                   some_name:
                       doc: 
                       query: some query
            """,

            # Missing documentation attribute
            """SQL:
                   some_name: 
                       query: some query
            """,

            # Missing query content
            """SQL:
                   some_name:
                       doc: some docs
                       query:
            """,

            # Missing query attribute
            """SQL:
                   some_name:
                       doc: some docs
            """,

            # Unrecognized attribute
            """SQL:
                   some_name:
                       doc: some docs
                       foo: foo text
                       query: some query
            """,

            # Invalid conditional name
            """SQL:
                   some_name:
                       doc: some docs
                       conditionals:
                           1st_cond: some docs 
                           cond2: cond2 docs
                       query: some query
            """,

            # Conditionals not given as a dictionary
            """SQL:
                   some_name:
                       doc: some docs
                       conditionals:
                           - cond1 
                           - cond2
                       query: some query
            """,

            # Multiple entries in a singleton yaml.
            """SQL:
                   some_name:
                       doc: some docs
                       query: some query

                   some_name2:
                       doc: some docs
                       query: some query
            """,

            # Multiple top level keys
            ("""SQL:
                   some_name:
                       doc: some docs
                       query: some query

             """ + "\n" +
             """OtherSQL:
                   some_name:
                       doc: some docs
                       query: some query
            """)
        )    


        # Because validating recursively calls the singlteton validator, not
        # as many test cases are needed here.
        self.valid_sythetic_composite_yamls = (
            """ClassName:
                   some_name:
                       doc: some docs
                       query: some query

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
            """,
        )

        self.invalid_synthetic_composite_yamls = (
            # Has zero query-based functions.
            """ClassName:
            """,

            # Invalid classname
            """1stName:
                   some_name:
                       doc: some docs
                       query: some query

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
            """,

            # Invalid function name
            """ClassName:
                   1stname:
                       doc: some docs
                       query: some query

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
            """,

            # Missing function docs.
            """ClassName:
                   some_name:
                       doc: 
                       query: some query

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
            """,

            # Missing query
            """ClassName:
                   some_name:
                       doc: some docs

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
            """,

            # Conditionals not a dict.
            """ClassName:
                   some_name:
                       doc: some docs

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           - foo
                           - bar
            """,

            # Multiple top-level names
            ("""ClassName:
                   some_name:
                       doc: some docs

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
             """ + "\n" +
             """ClassName2:
                   some_name:
                       doc: some docs

                   name2:
                       doc: some docs
                       query: some query
                       conditionals:
                           foo: foo doc
                           bar:
             """),
        )            


    def test__class_constants(self):
        """
        Places checks for the needed class constants. This will force 
        programmers to adjust the unit tests accordingly if they adjust the
        class constant.
        """

        required_class_constants = (
            '_SQL_SENTINEL',
            '_BOOL_NONE_NAMES',
            '_PYTHON_NAMING_REGEXP',
            '_OPTIONAL_QUERY_ITEMS',
            '_REQUIRED_QUERY_ITEMS',
            '_CONDITIONAL_KEY_TYPES',
            '_CONDITIONAL_VALUE_TYPES',
        )

        for class_constant in required_class_constants:
            has_constant = hasattr(YamlHandler, class_constant)
            message = "Failed to find required class constant '{}'"
            self.assertTrue(has_constant, message.format(class_constant))

    def test___init__(self):
        """
        Check that constructor provides required instance constants.
        """
        yaml_handler = YamlHandler()

        required_instance_constants = (
            '_REQUIRED_ARG_CHECKERS',
            '_OPTIONAL_ARG_CHECKERS',
        )

        for instance_constant in required_instance_constants:
            has_constant = hasattr(yaml_handler, instance_constant)
            message = ("Failed to find required instance constant '{}'. "
                       "Ensure that YamlHandler constructor creates it.")
            self.assertTrue(has_constant, message.format(instance_constant))

    def test_valid_variable(self):
        """
        Check that regexp checking for valid variable is right.
        """


        # Check that valid names are declared valid.
        for valid_var in self.valid_vars:
            message = "Expected '{}' to be declared a valid variable name."
            self.assertTrue(self.yaml_handler.valid_variable(valid_var),
                            message.format(valid_var))

        # Check that invalid names are declared invalid.
        for invalid_var in self.invalid_vars:
            with self.assertRaises(NameError):
                self.yaml_handler.valid_variable(invalid_var)


    def test_valid_conditionals(self):
        """
        Check that validation of conditional names works.
        """
        valid_dicts = (self.synthetic_valid_conditionals,
                       self.synthetic_valid_conditionals_empty)

        invalid_dicts = {
            NameError:self.synthetic_invalid_conditional_name,
            TypeError:self.synthetic_invalid_conditional_name_type,
            TypeError:self.synthetic_invalid_conditional_doc_type
        }

        # Check that valid conditionals are declared valid.
        for conditionals_dict in valid_dicts:
            self.assertTrue(
                self.yaml_handler.valid_conditionals(conditionals_dict),
                "Expected test conditionals '{}' to be declared valid.".format(
                    conditionals_dict
                )
            )

        # Check that invalid conditionals cause an exception to raise.
        for exception_type, conditionals_dict in invalid_dicts.iteritems():
            self.assertRaises(
                exception_type,
                self.yaml_handler.valid_conditionals,
                conditionals_dict,
            )


    def test_valid_sql_singleton(self):
        """
        Test that validation of a singleton sql query yaml works.
        """
        for valid_yaml in self.valid_sythetic_singleton_yamls:
            yaml_data = yaml.load(stream=valid_yaml, Loader=yaml.CLoader)
            self.assertTrue(
                self.yaml_handler.valid_sql_singleton(yaml_data),
                ("Expected yaml contained in string below to yield a valid "
                 "singleton yaml file:\n{}").format(valid_yaml)
            )

        for invalid_yaml in self.invalid_synthetic_singleton_yamls:
            yaml_data = yaml.load(stream=invalid_yaml, Loader=yaml.CLoader)
            with self.assertRaises(Exception):
                self.yaml_handler.valid_sql_singleton(yaml_data)


    def test_valid_sql_composite(self):
        """
        Check that validation of a composite yaml file works.
        """
        for valid_yaml in self.valid_sythetic_composite_yamls:
            yaml_data = yaml.load(stream=valid_yaml, Loader=yaml.CLoader)
            self.assertTrue(
                self.yaml_handler.valid_sql_composite(yaml_data),
                ("Expected yaml contained in string below to yield a valid "
                 "composite yaml file:\n{}").format(valid_yaml)
            )

        for invalid_yaml in self.invalid_synthetic_composite_yamls:
            yaml_data = yaml.load(stream=invalid_yaml, Loader=yaml.CLoader)
            with self.assertRaises(Exception):
                self.yaml_handler.valid_sql_composite(yaml_data)

                print "***\n"
                print invalid_yaml


if __name__ == "__main__":
    unittest.main()
        
