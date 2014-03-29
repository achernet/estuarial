"""
Unit tests for QueryHandler.

Author: Ben Zaitlen and Ely Spears
"""
import os
import yaml
import types
import shutil
import unittest
from os.path import join as pjoin
from estuarial.data.yaml_handler import YamlHandler
from estuarial.data.query_handler import QueryHandler
from estuarial.data.keyword_handler import KeywordHandler
from estuarial.array.arraymanagementclient import ArrayManagementClient

class TestQueryHandler(unittest.TestCase):
    """
    Exercises the code responsible for creating classes from composite Yaml
    documents, publishing their methods and documentation, and handling
    paths for finding custom SQL code relative to the module's known paths.
    """

    def setUp(self):
        """
        Prepare handler objects and paths needed for testing that composite
        SQL-query yaml documents are processed and correctly converted into 
            (1) autogenerated singleton SQL-query yaml documents
            (2) Python classes with correctly exposed functions corresponding
                to each query, and with correctly formatted documentation.
        """
        self.yaml_handler = YamlHandler()
        self.query_handler = QueryHandler()

        # Hard-coded reference to a Yaml file existing in the custom SQL
        # test directory for unit testing. Do not change unless you know
        # what you're doing.
        self._TEST_DIR = "test"
        self._TEST_FILE = "test_composite.yaml"

        # Test file relative to QueryHandler._FILE_DIR.
        self.custom_sql_test_file = pjoin(self._TEST_DIR, self._TEST_FILE)
        
        # NOTE:
        #     The above test file name should only refer to things in the 
        #     "test/" sub-directory of the array client's known location for
        #     custom SQL. Don't change this.
        if not os.path.split(self.custom_sql_test_file)[0] == self._TEST_DIR:
            message = ("Unit test must only operate on custom SQL files "
                       "stored in the '{}' subdirectory of the custom SQL "
                       "directory. Found {} instead. \n\tIf this file is in "
                       "the test directory, ensure the prefix '{}' is part of "
                       "the file name in the unit test definition.")

            raise ValueError(
                message.format(self._TEST_DIR, 
                               self.custom_sql_test_file, 
                               self._TEST_DIR)
            )
        
        # Expanded full path name.
        self.full_custom_sql_test_file = pjoin(
            self.query_handler._FILE_DIR, 
            self.custom_sql_test_file
        )

        # Full location of the autogen directory that should result from
        # the test yaml file's name and path.
        self.expected_autogen_directory = pjoin(
            self.query_handler._AUTOGEN_DIR,
            (self.query_handler._path_sanitizer(self.custom_sql_test_file) +
             self.query_handler._AUTOGEN_SUFFIX)
        )

        # Expected class attributes created for each autogen function.
        self.expected_file_attr = self.query_handler._FILE_ATTR
        self.expected_query_attr = self.query_handler._QUERY_ATTR
        self.expected_kwargs_attr = self.query_handler._KWARGS_ATTR

    def safe_remove(self, dir_name):
        """
        Helper function to safely remove the auto-gen directories created in
        the course of publishing the singleton queries and docstrings.
        """
        print "\nUnit test will remove {}".format(dir_name)

        # Only allow removal of the autogen directory.
        if not (dir_name == self.expected_autogen_directory):
            message = ("For unit tests, only removal of the expected auto",
                       "gen directory is permitted. Tried to remove {}")
                
            raise ValueError(message.format(dir_name))
            
        # Force unit tests to be carried out only on files in the autogen
        # path. Prevents attempts to delete anything not auto-generated.            
        if not (self.query_handler._AUTOGEN_DIR in 
                self.expected_autogen_directory):
            message = ("Attempted to remove {}, which is not located in "
                       "the autogenerated path {}")

            raise ValueError(
                message.format(self.expected_autogen_directory,
                               self.query_handler._AUTOGEN_DIR)
            )

        try:
            shutil.rmtree(dir_name)
        except OSError as os_error:
            if os_error.errno != 2:
                raise os_error


    def test__class_constants(self):
        """
        Places checks for the needed class constants. This will force 
        programmers to adjust the unit tests accordingly if they adjust the
        class constant.
        """
        required_class_constants = (
            '_BASE_DIR',
            '_FILE_DIR',
            '_DATA_ROOT', 
            '_AUTOGEN_DIR',
            '_PATH_SEP',
            '_YAML_EXT',
            '_NO_ARG_DOC', 
            '_PARAMS_HEADER',
            '_AUTOGEN_SUFFIX', 
            '_SINGLE_QUERY_HEADER',
            '_DOC', 
            '_QUERY',
            '_CONDITIONALS', 
            '_KW_DELIMITER',
        )

        for class_constant in required_class_constants:
            has_constant = hasattr(self.query_handler, class_constant)
            message = "Failed to find required class constant '{}'"
            self.assertTrue(has_constant, message.format(class_constant))


    def test__path_sanitizer(self):
        """
        Check that flattening file names for autogen works.
        """
        test_path_elements = ("some", "path", "elements", "foo.py")
        test_path = os.path.sep.join(test_path_elements)
        sanitized_path = self.query_handler._path_sanitizer(test_path)
        expected_sanitized_path = self.query_handler._PATH_SEP.join(
            test_path_elements
        )

        self.assertEqual(sanitized_path, expected_sanitized_path)


    def test__publish_queries(self):
        """
        Checks that QueryHandler can create an autogen directory when given a
        path to a composite yaml file and that an OSError isn't generated if
        the directory already exists. Checks that autogen singleton yaml files
        satisfy the yaml validation step so that the written files are valid
        yaml.
        """

        # Remove directory that would be autogen created from test yaml file,
        # if it exists. 
        self.safe_remove(self.expected_autogen_directory)

        # invoke function that should autogen create it, and ensure that it is 
        # created. 
        _ = self.query_handler._publish_queries(self.custom_sql_test_file)

        autogen_directory_created = os.path.isdir(
            self.expected_autogen_directory
        )

        self.assertTrue(autogen_directory_created, 
                        "Failed to create autogen directory.")

        # Execute the function again to ensure no exceptions due to the fact
        # that the autogen directory will already exist at this point, and also
        # to pull in the output arguments for further testing.

        (query_files, # Dict of (function name, autogen file) pairs. 
         type_name,   # Name of the created class.
         type_data,   # Contents of the original composite yaml.
         func_names   # List of function names from the yaml file.
         ) = self.query_handler._publish_queries(self.custom_sql_test_file)

        # Examine and validate each of the autogen-written files.
        for file_name, file_path in query_files.iteritems():
            with open(file_path, 'r') as yaml_stream:

                loaded_data_from_yaml = yaml.load(stream=yaml_stream, 
                                                  Loader=yaml.CLoader)

                is_autogen_valid = (
                    self.yaml_handler.valid_sql_singleton(
                        loaded_data_from_yaml
                    )
                )

                self.assertTrue(is_autogen_valid)

        # Remove the autogenerated directory and files so that the execution of
        # this test method doesn't leave any filesystem side effect.
        self.safe_remove(self.expected_autogen_directory)


    def test__publish_docstring(self):
        """
        Check that when dosctrings are autogenerated from Yaml, the function
        docstrings, arguments, and argument docstrings are published correctly
        and with appropriate formatting.
        """
        # Create loaded dict from yaml.
        with open(self.full_custom_sql_test_file, 'r') as full_yaml:
            loaded_data_from_yaml = yaml.load(stream=full_yaml, 
                                              Loader=yaml.CLoader)

        top_level_key = loaded_data_from_yaml.keys()[0]
        function_level_data = loaded_data_from_yaml[top_level_key]

        # For each function name in the dict, get the results of publishing
        # its arg list and docstring.
        for f_name, f_data in function_level_data.iteritems():
            args, docs = self.query_handler._publish_docstring(f_data)
            manual_conditionals_data = f_data.get(
                self.query_handler._CONDITIONALS, 
                {}
            )

            # Compare the 'conditionals' keys to args to ensure they match.
            self.assertEqual(set(args), set(manual_conditionals_data.keys()))

            # For each conditional, ensure that its doc string made it into
            # the published function docstring.
            for arg in args:
                arg_is_documented = str(manual_conditionals_data[arg]) in docs

                message = ("Published docstring for function '{}' has missing "
                           "docstring for its argument '{}': '{}'.")

                self.assertTrue(
                    arg_is_documented, 
                    message.format(f_name, arg, manual_conditionals_data[arg])
                )
            
            # Ensure function's top-level doc string from yaml is in function
            # docstring.
            function_is_documented = f_data[self.query_handler._DOC] in docs

            message = ("Published docstring for function '{}' is missing "
                       "docstring from yaml: '{}'")

            self.assertTrue(
                function_is_documented, 
                message.format(f_name, f_data[self.query_handler._DOC])
            )

            # Ensure it contains the sentinel for the Params section. 
            params_header_found = self.query_handler._PARAMS_HEADER in docs

            message = ("Published docstring for function '{}' fails to have a "
                       "parameter header section.")

            self.assertTrue(params_header_found, message.format(f_name))


    def test__function_factory(self):
        """
        Check that a method object is returned and does not raise a TypeError 
        for any of the arguments that should be supported (even if it does 
        raise errors due to lack of database connection during testing.)

        Check that method does raise TypeError for keyword that is not on the
        supported list.

        Whether or not the function will work is then a matter of the unit
        tests for the array backend and the call to the alchemy 'select' 
        function, so not appropriate for testing here.
        """
        
        (query_files, # Dict of (function name, autogen file) pairs. 
         type_name,   # Name of the created class.
         type_data,   # Contents of the original composite yaml.
         func_names   # List of function names from the yaml file.
         ) = self.query_handler._publish_queries(self.custom_sql_test_file)


        # For each generated singleton query file, create the function that
        # will correspond to that query.
        for f_name, f_file in query_files.iteritems():
            
            # Get the keyword args and doc for the function.
            known_args, function_doc = (
                self.query_handler._publish_docstring(type_data[f_name])
            )

            # Make the function.
            test_function = self.query_handler._function_factory(f_file, 
                                                                 f_name, 
                                                                 known_args)

            # For all potential keyword arguments for the function, check that
            # a type error with the known message is not raised.
            supported_extension_args = (
                KeywordHandler._SUPPORTED_SQL.keys() +
                KeywordHandler._SUPPORTED_OPS.keys()
            )

            for base_arg in known_args:
                for supported_extension in supported_extension_args:

                    # Create the extended argument, e.g. if base arg is "date"
                    # and supported extension is "between", the the argument to
                    # check is "date_between", when "_" is the KW_DELIMITER.
                    extended_arg = (
                        base_arg + 
                        self.query_handler._KW_DELIMITER + 
                        supported_extension
                    ) if supported_extension != "" else base_arg

                    # Pass the valid extended argument to the function. Any
                    # Exception is allowed to pass through other than an
                    # exception stating that the argument is invalid.
                    try:
                        test_function(None, **{extended_arg:"foo"})
                    except Exception as exception:
                        unrecognized = exception.message.startswith(
                            self.query_handler._INVALID_KWARG_MSG
                        )

                        if unrecognized:
                            raise exception

            # For some argument that is not supported, ensure that it *does*
            # raise an exception with the expected label.
            crazy_kwarg = {"__foo_bar_baz__":"foo"}
            try:
                test_function(None, **crazy_kwarg)
            except Exception as exception:
                unrecognized = exception.message.startswith(
                    self.query_handler._INVALID_KWARG_MSG
                )
                self.assertTrue(unrecognized)
            
        # Clean up the created autogen files.
        self.safe_remove(self.expected_autogen_directory)

    def test_create_type_from_yaml(self):
        """
        Check that a Python class is created from a composite yaml url. Inspect
        the loaded yaml data directly and compare the class's attributes with
        those expected from the yaml document.
        """
        # First get the raw Yaml data, for comparing the contents of the created
        # class
        (query_files, # Dict of (function name, autogen file) pairs. 
         type_name,   # Name of the created class.
         type_data,   # Contents of the original composite yaml.
         func_names   # List of function names from the yaml file.
         ) = self.query_handler._publish_queries(self.custom_sql_test_file)

        # Create the desired class.
        created_class = self.query_handler.create_type_from_yaml(
            self.custom_sql_test_file
        )

        self.assertIsInstance(created_class, types.TypeType)

        # Check that class's name matches the top-level composite yaml key.
        class_name = created_class.__name__
        message = ("Expected created class to have name '{}' from yaml, but "
                   "found '{}' instead.").format(type_name, class_name)
        self.assertEqual(type_name, class_name, message)
        
        
        # For each function required of the class, validate that it is created
        # and has the required contents.
        for f_name in func_names:

            # Ensure that the created class has the function.
            test_function = getattr(created_class, f_name)
            self.assertIsInstance(test_function, types.MethodType)

            # Validate the function's name and docstring.
            args, docs = self.query_handler._publish_docstring(
                type_data[f_name]
            )
            self.assertEqual(test_function.__doc__, docs)
            self.assertEqual(test_function.__name__, f_name)

            # Bind the specific function name into the expected formatted 
            # class attribute names, for e.g. gile locations.
            file_attr, query_attr, kwargs_attr = map(
                lambda x: x.format(f_name),
                (self.expected_file_attr,
                 self.expected_query_attr,
                 self.expected_kwargs_attr)
            )
            
            # Check for this function name that all of the expected hidden
            # class attributes that were created for it.
            has_file_attr = hasattr(created_class, file_attr)
            has_query_attr = hasattr(created_class, query_attr)
            has_kwargs_attr = hasattr(created_class, kwargs_attr)
            all_attrs = (has_file_attr, has_query_attr, has_kwargs_attr)
            has_all_attrs = all(all_attrs)

            message = ("Expected class attributes '{}' to exist, but "
                       "'hasattr' returns '{}' when checking for them.")

            self.assertTrue(
                has_all_attrs, 
                message.format(
                    (file_attr, query_attr, kwargs_attr), 
                    all_attrs
                )
            )
                            
            # Check that formatted class attributes contain the expected 
            # content.
            self.assertEqual(getattr(created_class, file_attr),
                             query_files[f_name])

            self.assertEqual(getattr(created_class, query_attr),
                             type_data[f_name][self.query_handler._QUERY])

            self.assertEqual(set(getattr(created_class, kwargs_attr)),
                             set(args))


        # Clean up the created autogen files.
        self.safe_remove(self.expected_autogen_directory)

if __name__ == "__main__":
    unittest.main()
        
