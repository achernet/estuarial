"""
Validates yaml format used by Estuarial for composite and singleton SQL query
specifications.

Author: Ben Zaitlen and Ely Spears
"""
import re
import yaml
import types
import keyword
import __builtin__

class YamlHandler(object):
    """
    Provides methods for validating that the data loaded from a yaml file is
    suitable for use in the systems -- that it has the required and optional 
    keywords.
    """
    # String expected at the top level of singleton sql yaml documents.
    _SQL_SENTINEL = "SQL"

    # Regexp to match valid strings for Python variable names.
    _PYTHON_NAMING_REGEXP = "[_A-Za-z][_a-zA-Z0-9]*$"

    # Disallowed names because of the risk of overwriting / confusing with
    # the default Python literals for these names.
    _BOOL_NONE_NAMES = ("True", "False", "None", "true", "false", "none", "")

    # Names and types for optional data in SQL yaml
    _OPTIONAL_QUERY_ITEMS = {"conditionals":(dict,)}

    # Required names and types in SQL yaml.
    _REQUIRED_QUERY_ITEMS = {"doc":(str, unicode), "query":(str, unicode)}

    # Types permitted for the keys and values of the 'conditionals' section.
    _CONDITIONAL_KEY_TYPES = (str, unicode)
    _CONDITIONAL_VALUE_TYPES = (str, unicode, types.NoneType)

    def __init__(self):
        """
        Construct the callable checker functions for any named arguments that
        require additional checking beyond type validation.

        Params
        ------
        None.

        Returns
        -------
        None.
        """
        # Space to declare callables that should be executed on the sub-dict
        # or parameter value for the specified keyword. These are implemented
        # as instance methods and thus are configured on instantiation.
        self._REQUIRED_ARG_CHECKERS = {}
        self._OPTIONAL_ARG_CHECKERS = {"conditionals":self.valid_conditionals}

    def valid_variable(self, variable):
        """
        Validates that a string to be used as a variable name conforms to
        standard Python naming conventions that won't disrupt common getattr
        access, that variable name does not conflict with Python keywords or
        built-in names.

        Params
        ------
        variable: A string intended to be used in naming a Python object.

        Returns
        -------
        valid: A Boolean describing whether the passed string is valid or not.
        """
        is_valid_string = re.match(self._PYTHON_NAMING_REGEXP, variable) 
        is_not_reserved_keyword = (not keyword.iskeyword(variable))
        is_not_builtin = (variable not in dir( __builtin__ ))
        is_not_bool_none = (variable not in self._BOOL_NONE_NAMES)

        valid = all((is_valid_string, 
                     is_not_reserved_keyword, 
                     is_not_builtin,
                     is_not_bool_none))
        
        # If the variable name is not valid, raise an exception.
        if not valid:
            message = ("Attempted to declare conditional variable named '{}'.\n"
                       "This name is either an invalid variable name or else "
                       "shadows a reserved keyword or builtin name.")

            raise NameError(message.format(variable))

        # Returns True when method succeeds.
        return valid

    def valid_conditionals(self, conditional_dict):
        """
        Validates sub-dictionary of conditional variable names and their doc-
        strings from loaded yaml data. Checks that all loaded values are of
        correct type and checks that all variable names will conform to Python
        standard for getattr attribute access ("dot" syntax).

        Params
        ------
        conditional_dict: A dictionary (from loaded yaml) of the conditional 
        names (keys) and doc-strings (values).

        Returns
        -------
        names_are_valid: A Boolean describing whether all of the conditonal
        names can serve as valid Python variable names.
        """
        # Get the intended variable names for the conditionals
        conditional_keys = conditional_dict.keys()

        # Ensure conditional names and their doc values are of allowable types.
        for conditional in conditional_keys:

            # Raise an exception if conditional name is not a string type.
            if not isinstance(conditional, self._CONDITIONAL_KEY_TYPES):

                message = "Received conditional '{}' that is not of type in {}"

                raise TypeError(message.format(conditional, 
                                               self._CONDITIONAL_KEY_TYPES))

            # Raise an exception if conditional name is not accompanied by a
            # string-type (or None) doc string value.
            if not isinstance(conditional_dict[conditional], 
                              self._CONDITIONAL_VALUE_TYPES):

                message = "Received invalid docstring type for conditional '{}'"

                raise TypeError(message.format(conditional))

        # After ensuring all types are ok, check if variable names adhere to
        # standards required for Python's natural getattr "dot" syntax to work.
        names_are_valid = all(map(self.valid_variable, conditional_keys))

        # Returns True when method succeeds.
        return names_are_valid
            
    def valid_sql_singleton(self, 
                            loaded_data_from_yaml, 
                            top_level_sentinel=None):
        """
        Determines if the loaded contents from a yaml file are valid. This
        function is provided for yaml files that contain only one parameterized
        query. 

        Params
        ------
        loaded_data_from_yaml: The Python dict that results from loading a
        single-query yaml file.

        top_level_sentinel: A string expected as the solve top-level key of the
        yaml data. The default will imply that this sentinel value must be 
        the value contained in YamlHandler._SQL_SENTINEL, leaving some 
        flexibility for having different sentinels and validating different 
        types of queries ingested from yaml formats.

        Returns
        -------
        True -- if the function finds no reason to raise an exception due to
        incorrect formatting, then it will return True.
        """
        # For default args, assume single-query yaml format must have top
        # level name matching the chosen sql sentinel value.
        if top_level_sentinel is None:
            top_level_sentinel = self._SQL_SENTINEL

        # Ensure that top-level signifies this is a SQL parameter file.
        top_level_keys = loaded_data_from_yaml.keys()
        has_one_top_level_key = (len(top_level_keys) == 1)
        top_level_key_is_sql = (top_level_keys[0] == top_level_sentinel)

        if not (has_one_top_level_key and top_level_key_is_sql):

            message = ("Single top-level key '{}' not found in yaml. Check\n"
                       "indentation levels to ensure only a single top-level\n"
                       "key exists and matches.")

            raise ValueError(message.format(self._SQL_SENTINEL))

        # Ensure there is only one function defined.
        function_level_data = loaded_data_from_yaml[self._SQL_SENTINEL]
        function_level_keys = function_level_data.keys()
        has_one_function_key = (len(function_level_keys) == 1)

        if not has_one_function_key:
            message = ("Found {} yaml function declarations when only 1 is "
                       "permitted.")

            raise ValueError(message.format(len(function_level_keys)))

        # Check that the function-level key is a valid Python identifier.
        f_key = function_level_keys[0]
        if not self.valid_variable(f_key):
            raise NameError(
                "Function name from yaml must be a valid Python "
                "variable identifier, but received: '{}'".format(f_key)
            )

        # Get query-level data and keys and ensure no duplicates.
        query_level_data = function_level_data[f_key]
        query_level_keys = query_level_data.keys()

        no_duplicates = (len(set(query_level_keys)) == len(query_level_keys))

        if not no_duplicates:
            message = "No duplicate fields permitted, but found {}."

            raise ValueError(message.format(query_level_keys))


        # Check required items
        for require_key, require_type in self._REQUIRED_QUERY_ITEMS.iteritems():

            # Check that the required key is actually used.
            if not require_key in query_level_keys:
                message = "Required field '{}' not found in yaml data."
                raise LookupError(message.format(require_key))

            # Check that the data type for this key is permissible.
            if not isinstance(query_level_data[require_key], require_type):
                message = ("Data for required field '{}' is not correct type.\n"
                           "Found type '{}' but require type in {}")

                raise TypeError(message.format(
                        require_key, 
                        type(query_level_data[require_key]),
                        require_type))

            # If extra checkers are present for this key, run them and
            # raise an exception if they do not succeed.
            if require_key in self._REQUIRED_ARG_CHECKERS:
                checker = self._REQUIRED_ARG_CHECKERS[require_key]
                is_valid = checker(query_level_data[require_key])
                if not is_valid:
                    message = ("Section '{}' from yaml failed validity "
                               "checking.")
                    
                    raise ValueError(message.format(require_key))

        # Check all keys for the optional items
        for query_key in query_level_keys:
            
            # If it's a required item, it was already checked, so skip it.
            if query_key in self._REQUIRED_QUERY_ITEMS.keys():
                continue

            # If it's an optional item, process it.
            elif query_key in self._OPTIONAL_QUERY_ITEMS.keys():

                # Raise exception if the optional argument's data is
                # of the wrong type.
                permissible_types = self._OPTIONAL_QUERY_ITEMS[query_key]
                if not isinstance(query_level_data[query_key], 
                                  permissible_types):

                    message = ("For yaml data field '{}', incorrect type '{}' "
                               "was found. Type expected to be in {}.")

                    raise TypeError(message.format(
                            query_key,
                            type(query_level_data[query_key]),
                            permissible_types))

                # If extra checkers exist for this key, call them and raise
                # exception if they do not succeed.
                if query_key in self._OPTIONAL_ARG_CHECKERS:
                    checker = self._OPTIONAL_ARG_CHECKERS[query_key]
                    is_valid = checker(query_level_data[query_key])
                    if not is_valid:
                        message = ("Section '{}' from yaml failed validity "
                                   "checking.")
                        
                        raise ValueError(message.format(query_key))

            # Otherwise the key is invalid. Raise an exception.
            else:
                invalid_parm = "Unrecognized optional yaml parameter: '{}'."
                raise ValueError(invalid_parm.format(query_key))

        # If the method succeeds, return True
        return True

    def valid_sql_composite(self, loaded_data_from_yaml):
        """
        """
        # Ensure there is only one top-level name
        top_level_keys = loaded_data_from_yaml.keys()
        has_one_top_level_key = (len(top_level_keys) == 1)
        if not has_one_top_level_key:
            message = ("Composite yaml document has multiple collections: {}\n"
                       "Only one top-level name is allowed per file.")

            raise ValueError(message.format(top_level_keys))

        class_name = top_level_keys[0]

        # Ensure top-level name is valid Python name.
        top_level_is_valid = self.valid_variable(top_level_keys[0])
        if not top_level_is_valid:
            message = ("Top level yaml key '{}' is not valid Python variable "
                       "name.")
            
            raise ValueError(message.format(class_name))

        # Ensure there are 1 or more second-level keys.
        function_level_data = loaded_data_from_yaml[class_name]
        function_level_keys = function_level_data.keys()
        has_function_keys = (len(function_level_keys) >= 1)

        if not has_function_keys:
            message = "Yaml data for '{}' is empty."
            raise ValueError(message.format(class_name))

        # For each function level name, make a synthetic dictionary as if that
        # dict represented a single-query yaml for the function name.
        for function_name, function_data in function_level_data.iteritems():

            # Place YamlHandler._SQL_SENTINEL as the synthetic top level key.
            synthetic_singleton = {
                self._SQL_SENTINEL:{function_name:function_data}}

            # Remaining validation checks via valid_sql_singleton.
            is_subdict_valid = self.valid_sql_singleton(synthetic_singleton)

            if not is_subdict_valid:
                message = "Yaml sub-section for function name '{}' is invalid."
                raise ValueError(message.format(function_name))
        
        # If the method succeeds, return True.
        return True

if __name__ == "__main__":
    import os
    y_handler = YamlHandler()

    test_single_yaml = os.path.abspath(
        "./catalog/SQL_DATA/FUNDAMENTALS/RKD2/rkd_fundamentals.qad")
    with open(test_single_yaml, 'r') as single_file:
        single_data = yaml.load(stream=single_file, Loader=yaml.CLoader)

    # test_composite_yaml = os.path.abspath("../test/data/test_yaml.yaml")
    # with open(test_composite_yaml, 'r') as composite_file:
    #     composite_data = yaml.load(stream=composite_file, Loader=yaml.CLoader)

    
    print y_handler.valid_sql_singleton(single_data)
    # print y_handler.valid_sql_composite(composite_data)
#