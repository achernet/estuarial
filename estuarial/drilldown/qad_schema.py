"""
Reflect the QAD schema from Thomson Reuters using auto-generated composite Yaml
documents inferred from queries that read the database's metadata. 
"""
import pandas
import numpy as np
from estuarial.query.raw_query import RAW_QUERY

def get_active_table_names():
    """
    Grab list of all table names on the database. Do some filtering to remove
    tables from deprecated schemas and to prepend the correct schema prefix.
    """
    rq = RAW_QUERY()
    tables = rq.raw_query("SELECT * FROM sys.tables")
    schemas = (
        rq.raw_query("SELECT * FROM sys.schemas")
        .rename(columns={"name":"schema_name"})
    )

    tables = pandas.merge(
        tables, 
        schemas.set_index("schema_id")[["schema_name"]], 
        left_on="schema_id", 
        right_index=True
    )

    tables["name"] = tables["schema_name"] + "." + tables["name"]
    return tables.name.values.tolist()


def get_key_columns(sp_help_results, sp_fkeys_results=None):
    """
    Build and execute a query that retrieves key columns from a particular
    table. Returns a list of regular keys and also a list of foreign keys.
    """
    primary_key_defs = sp_help_results['constraints'].constraint_type.map(
        lambda x: x.startswith("PRIMARY KEY")
    )
 
    # Process primary keys if there were any.
    if primary_key_defs.any():
        primary_keys = (
            sp_help_results['constraints'][primary_key_defs]
            .constraint_keys
            .values[0]
            .split(", ")
        )
    else:
        primary_keys = []

    # Process foreign keys if there were any.
    if sp_fkeys_results is None:
        foreign_keys = []
    
    return primary_keys, foreign_keys


def get_column_names_and_types(sp_help_results):
    """
    Build and execute a query that retrieves the available columns and their
    data types from a particular table.
    """
    # Convert the `sp_help` result set for column information into a dict of
    # the column names and their SQL types.
    column_metadata = sp_help_results['columns']
    column_type_dictionary = dict(
        zip(column_metadata.Column_name.values.tolist(), 
            column_metadata.Type.values.tolist())
    )
    
    return column_type_dictionary


def execute_sp_fkeys(table_name):
    """
    Execute the `sp_fkeys` procedure to acquire foreign key information.
    """
    rq = RAW_QUERY()
    tmp_conn = rq.aclient.raw_config.pyodbc.connect(
        rq.aclient.raw_config.connstring
    )

    # Execute the foreign key stored procedure and convert the data.
    tmp_curs = tmp_conn.cursor()
    tmp_curs.execute("EXEC sp_fkeys @pktable_name='{}';".format(table_name))
    raw_result_set = tmp_curs.fetchall()
    column_names = [elem[0] for elem in tmp_curs.description]
    tuple_data = [tuple(row) for row in raw_result_set]

    # Return a DataFrame with None entries if no foreign keys.
    return pandas.DataFrame(
        tuple_data if tuple_data else [[None for elem in column_names]],
        columns=column_names
    )


def execute_sp_help(table_name):
    """
    Execute the `sp_help` procedure, unpackage all returned result sets
    and convert them to Pandas, then return a tuple of the result sets.
    """
    rq = RAW_QUERY()

    tmp_conn = rq.aclient.raw_config.pyodbc.connect(
        rq.aclient.raw_config.connstring
    )

    # Execute the `sp_help` stored procedure.
    tmp_curs = tmp_conn.cursor()
    tmp_curs.execute("EXEC sp_help '{}';".format(table_name))

    # Made up names for result sets based on names reported at the T-SQL docs:
    # < http://technet.microsoft.com/en-us/library/ms187335.aspx >
    result_set_names = [
        "constraints",
        "indexes", 
        "filegroups", 
        "rowguide", 
        "identities", 
        "columns", 
        "owner", 
    ]

    # For each retrieved result set, place the converted data into a pandas
    # data frame.
    retrieved_data = {}
    has_next_set = True
    while has_next_set:
        try:
            raw_result_set = tmp_curs.fetchall()
            column_names = [elem[0] for elem in tmp_curs.description]

            converted_data = pandas.DataFrame(
                [tuple(row) for row in raw_result_set],
                columns=column_names
            )

            # Ensures only the named result sets can appear.
            result_set = result_set_names.pop()
            retrieved_data[result_set] = converted_data
            has_next_set = tmp_curs.nextset()

        # pyODBC error happens on the last check of a result set when
        # executing stored procedures. Break out of the while loop instead.
        except Exception as e:
            break

    return retrieved_data


def make_index_documentation(sp_help_results):
    """
    Parse result set on SQL indexes into readable documentation.
    """
    doc_prefix = "            "
    indexes = sp_help_results["indexes"]
    index_doc = doc_prefix + "Indexes\n" + doc_prefix + "-------\n"
    for i, row in indexes.iterrows():
        index_doc += doc_prefix + "name: {}\n".format(row.ix["index_name"])
        index_doc += doc_prefix + "keys: {}\n".format(row.ix["index_keys"])
        index_doc += (
            doc_prefix + 
            "description: {}\n\n\n".format(row.ix["index_description"])
        )
    return index_doc

def make_constraint_documentation(sp_help_results):
    """
    Parse result set on SQL constraint/keys into readable documentation.
    """
    doc_prefix = "            "
    constraints = sp_help_results["constraints"]
    constraint_doc = (
        doc_prefix + 
        "Constraints/Keys\n" + 
        doc_prefix + 
        "----------------\n"
    )

    for i, row in constraints.iterrows():
        constraint_doc += (
            doc_prefix + 
            "name: {}\n".format(row.ix["constraint_name"])
        )

        constraint_doc += (
            doc_prefix + 
            "keys: {}\n".format(row.ix["constraint_keys"])
        )

        constraint_doc += (
            doc_prefix + 
            "description: {}\n\n\n".format(row.ix["constraint_type"])
        )

    # Leave off the last newline to reduce whitespace from following sections.
    return constraint_doc[:-1]


def make_function_documentation(sp_help_results, table_name):
    """
    Provide documentation about a table's columns, types, keys, and indexes.
    """
    # Placeholders in case of no index or constraint info retrieved.
    empty_index_df = pandas.DataFrame([None], columns=["index_name"])
    empty_constraint_df = pandas.DataFrame([None], columns=["constraint_name"])

    # Placeholders in case of no column/type info retrieved.
    columns_df_columns = ["Column_name", "Type"]
    empty_columns_df = pandas.DataFrame(
        [[None, None]], 
        columns=columns_df_columns
    )

    # Top-line documentation and columns with type info.
    doc_yaml_prefix = "            " # To get Yaml indendation correct.
    doc_string = (
        "Reflexive function to provide access to table '{}'.\n\n".format(
            table_name
        )
    )

    doc_string += doc_yaml_prefix 
    doc_string += "The table provides the following columns:\n\n"
    doc_string += doc_yaml_prefix

    doc_string += (
        sp_help_results.get("columns", empty_columns_df)[columns_df_columns]
        .set_index("Column_name")
        .to_string().replace("\n", "\n" + doc_yaml_prefix) + "\n\n\n"
    ) 

    # Print-out of any indexes built on the table.
    index_docs = make_index_documentation(sp_help_results)
    doc_string += index_docs

    # Print-out of any keys / foreign keys / constraints on the table.
    constraint_docs = make_constraint_documentation(sp_help_results)
    doc_string += constraint_docs

    return doc_string

    
def make_conditionals_dictionary(column_type_dictionary, 
                                 primary_keys, 
                                 foreign_keys):
    """
    From the set of all columns and types, create docstring for each column and
    annotate it with key status. Return a dictionary mapping names of columns
    to their docstrings.
    """
    conditonals_dictionary = {}
    for column, column_type in column_type_dictionary.iteritems():
        doc = "A column of SQL type '{}'.".format(column_type)
        if column in primary_keys:
            doc += " Column is a primary key."

        if column in foreign_keys:
            doc += " Column is a foreign key."

        if column in primary_keys + foreign_keys:
            conditonals_dictionary[column] = doc

    return conditonals_dictionary


def make_conditionals_yaml_block(keys):
    """
    From a dictionary of <key>:<docstring> pairs, create a block of Yaml code
    that represents a composite Yaml's conditionals section.
    """
    line_terminator = "\n            "
    yaml_block = ""
    for key, doc in keys.iteritems():
        doc = doc.replace("\n", " ")
        yaml_block += ("{}: {}".format(key, doc) + line_terminator)
    return yaml_block


def make_function_yaml(name, table, doc, conditonals):
    """
    From the requirements for the function-specific section of a composite Yaml
    generate the needed Yaml segment.
    """

    per_function_yaml="""
    {name}:
        doc: |
            {doc}
        conditionals:
            {conditionals}
        query: >
            SELECT *
            FROM {table}


    """
    return per_function_yaml.format(
        name=name, 
        doc=doc, 
        conditionals=conditonals, 
        table=table
    )

def make_composite_schema_yaml():
    """
    Get the list of all tables and filter it according to schema. Then iterate
    through all tables, making a yaml-query for that table. The end result is a
    very large composite Yaml document with all of the tables mapped as 
    functions.
    """
    import time
    base_yaml = "QADSchema:\n"
    table_names = get_active_table_names()
    num_tables = len(table_names)
    num_succeeded = 0
    num_failed = 0

    for i, table in enumerate(table_names):
        print "Running for table: {}...\n".format(table)
        st_time = time.time()


        try:
            sp_help_results = execute_sp_help(table)
            column_type_dictionary = get_column_names_and_types(
                sp_help_results
            )

            primary_keys, foreign_keys = get_key_columns(sp_help_results)
            conditonals_dictionary = make_conditionals_dictionary(
                column_type_dictionary, 
                primary_keys, 
                foreign_keys
            )

            doc = make_function_documentation(sp_help_results, table)
            name = table.replace(".", "_")
            conditionals_doc = make_conditionals_yaml_block(
                conditonals_dictionary
            )

            function_yaml = make_function_yaml(
                name, 
                table, 
                doc, 
                conditionals_doc
            )

            base_yaml += function_yaml + "\n"

            ed_time = time.time()
            elapsed = round(ed_time - st_time, 3)
            print (
                "Completed for table name '{}' in {}s. {}/{}\n=====\n".format(
                    table, 
                    elapsed, 
                    i, 
                    num_tables
                )
            )
            num_succeeded +=1
            
        except:
            print (
                "Failed (skipping) for table name '{}'. {}/{}\n=====\n".format(
                    table,
                    i,
                    num_tables
                )
            )
            num_failed += 1

    print "Num succeeded: {}\n".format(num_succeeded)
    print "Num failed: {}\n".format(num_failed)
    return base_yaml
        
if __name__ == "__main__":

    import time
    st_time = time.time()
    tmp = make_composite_schema_yaml()
    with open("/home/ely/test_all.yaml", "w") as fl:
        fl.write(tmp)
    ed_time = time.time()
    print ed_time - st_time




