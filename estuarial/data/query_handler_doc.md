Extended documentation for `QueryHandler` from `query_handler.py`.

Provides method `create_type_from_yaml` which converts a composite yaml
query definition file into a new Python class. The created class will
have functions available corresponding to each named query in the yaml.

The keyword arguments for these functions will include any conditional
arguments given in the yaml, as well as augmented keyword arguments that
allow for SQL operations to be performed on the conditional argument names.

For example, consider the following sample composite query file which is
saved in "/test/test_example.yaml" relative to `QueryHandler._FILE_DIR`.

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

The `QueryHandler.create_type_from_yaml` function will create a new Python
class, `AccountingData` that has two functions:

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

Let's look at the `inventory` query. Because the file declares 
`accounting_id` as a conditional name, that name will be interpreted as
something that should be available as an argument for the `inventory`
function, such as `inventory(accounting_id=10)`. 

Under the hood, this will generate a SQL `WHERE` condition (as in, 
`WHERE accounting_id = 10`) that will get applied to the base results of
whatever plain query was given for the inventory entry in the yaml file.

In this manner, the function inventory acts like a specifier for `WHERE`
conditions for the query it was given, such that only the items listed as
conditionals can appear in the `WHERE` statements.

So if we wanted to see the result of the inventory query where `account_id`
is 10 and `shipping_date` is '2012-12-31', we could say:

    qh = QueryHandler()
    AccountingData = qh.create_type_from_yaml('test/test_example.yaml')
    ad = AccountingData()
    data = ad.inventory(accounting_id=10, shipping_date='2012-12-31')

But what about more options for the arguments you ask? 

This is handled with special keyword arguments that extend the given
conditional names to include other operations, like `BETWEEN` or `>=` or 
`IS NOT`. These are shown below:

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

To demonstrate string operations, we'll use the `city` variable from the
`payroll` function:

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
SQL equivalent is given, assuming `<pattern>` represents the text to be 
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

