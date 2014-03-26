class KeywordHandler(object):
    """
    """
    # Map augmented keyword names into the
    # names getattr needs to look them up
    SUPPORTED_SQL = {
        "is":"is_",
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
        "startswith":"startswith",
    }

    # Map of logicals supported from operator module.
    SUPPORTED_OPS = {
        "":"eq", # So that date=blah just works.
        "not_equal":"ne",
        "greater_than":"gt",
        "greater_than_or_equal":"ge",
        "less_than":"lt",
        "less_than_or_equal":"le"
    }


    def __init__(self, array_client):
        self.array_client = array_client

    def supported_sql(self):
        return self.SUPPORTED_SQL

    def supported_ops(self):
        return self.SUPPORTED_OPS

    def sql_bind(self, base_arg, sql_primitive_name):
        """
        Returns a function.
        """
        sql_name = self.SUPPORTED_SQL[sql_primitive_name] # Use .get?
        sql_func = getattr(getattr(self.array_client, base_arg), sql_name)
        return sql_func
    
    def op_bind(self, base_arg, op_name):
        """
        Returns a function
        """
        import operator
        op = getattr(operator, self.SUPPORTED_OPS[op_name]) # Use .get?
        return lambda other: op(getattr(self.array_client, base_arg), other) 
        

if __name__ == "__main__":
    pass
    
