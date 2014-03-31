"""
Encapsulate queries for market index constituent data.

Author: Ben Zaitlen and Ely Spears
"""
import pandas
import numpy as np
from estuarial.util.decorators import target_getitem
from estuarial.data.query_handler import QueryHandler

@target_getitem('constituents', api_mapper='_constituents_signature')
class MarketIndex(object):
    """
    Provider for market index constituents.
    """
    _MARKET_INDEX_URL = "browse/market_index.yaml"
    
    # Map between convenience-function layer names and the functions and
    # arguments needed for them.
    _SUPPORTED_INDICES = {
        "DowJones":("dowjones_universe", "DJX_IDX"),
        "SP500":("spx_universe", "SPX_IDX")
    }


    def __init__(self):
        """
        Set up the query url connection for fetching index constituents.

        Params
        ------
        None.

        Returns
        -------
        None.
        """
        self._query_handler = QueryHandler()

        # Load the class definition from yaml and immediately create an
        # instance.
        self._constituent_queries = (
            self._query_handler.create_type_from_yaml(
                self._MARKET_INDEX_URL
            )
        )()


    def _constituents_signature(self, slice_args):
        """
        Handler for arguments passed in through `__getitem__` but intended for
        `constituents`.

        Params
        ------
        slice_args: A `tuple` of the arguments that were passed in through 
        `__getitem__`.

        Returns
        -------
        A `tuple` of the positional arguments to be passed in to the function
        `constituents`.
        """
        if not isinstance(slice_args, tuple):
            message = ("Item getting for market indices requires a two-"
                       "dimensional array-index. Instead received: {}")
            raise ValueError(message.format(slice_args))
            
        elif len(slice_args) != 2:
            message = ("Item getting for market indices requires a two-"
                       "dimensional slice. The first dimension is the name of "
                       "the index. The second dimension is a slice over "
                       "time periods. Instead received {}")
            raise ValueError(message.format(slice_args))

        # Peel off the needed arguments for passing them into `constituents`.
        index = slice_args[0]
        try:
            start_period = slice_args[1].start
            end_period = slice_args[1].stop

            if start_period is None or end_period is None:
                message = ("Unbounded date indexing is not supported.")
                raise ValueError(message)

            # TODO: Add support for what happens with step (does this mean
            # the returns data is sorted different? Can start be greater than
            # stop?

        except AttributeError:
            start_preiod = slice_args[1]
            end_period = slice_args[1]

        return (index, start_period, end_period)
        

    def constituents(self, index, start_period, end_period):
        """
        Retrieve constituents for a given index across a date range.

        Params
        ------
        index: String naming one of the supported indices for which data will
        be fetched.

        start_period: String or datetime naming a period for the beginning of
        the date range over which data will be fetched.

        end_period: String or datetime naming a period for the end of the date
        range over which data will be fetched.

        Returns
        -------
        pandas DataFrame containing the requested data.
        """
        index_function, index_iticker = self._SUPPORTED_INDICES[index]
        function_handle = getattr(self._constituent_queries, index_function)
        return function_handle(date__between=(start_period, end_period),
                               iticker=index_iticker)

if __name__ == "__main__":
    m = MarketIndex()
    tmp1 = m.constituents("SP500", '2012-12-31', '2012-12-31')
    tmp2 = m['SP500', '2012-12-28':'2012-12-31']

    tmp3 = m.constituents("DowJones", '2012-12-31', '2012-12-31')
    tmp4 = m['DowJones', '2012-12-28':'2012-12-31']

