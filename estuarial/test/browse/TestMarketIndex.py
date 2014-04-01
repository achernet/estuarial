"""
Test for the user-facing market index interfaces.

Author: Ben Zaitlen and Ely Spears
"""
import unittest
import numpy as np
from pandas.util.testing import assert_frame_equal 
from estuarial.browse.market_index import MarketIndex

class TestMarketIndex(unittest.TestCase):
    """
    Check that user-facing market index code is backed by expected files and
    performs as expected.
    """

    def setUp(self):
        """
        Created needed objects for testing that creation and use of MarketIndex
        satisfies requirements.
        """
        self.m = MarketIndex()
        self._QUERY_HANDLER_ATTR = "_query_handler"
        self._CONSTITUENT_QUERIES_ATTR = "_constituent_queries"


    def test___init__(self):
        """
        Test that constructed instance has a handle to a class that provides
        the constituent index queries.
        """
        has_query_handler = hasattr(
            self.m, 
            self._QUERY_HANDLER_ATTR
        )

        has_constituent_queries = hasattr(
            self.m, 
            self._CONSTITUENT_QUERIES_ATTR
        )

        has_both_attrs = (has_query_handler, has_constituent_queries)

        message = ("Expected both '{}' and '{}' attributes to exist on "
                   "instance of MarketIndex, but 'hasattr' returned '{}'")

        self.assertTrue(
            all(has_both_attrs),
            message.format(
                self._QUERY_HANDLER_ATTR, 
                self._CONSTITUENT_QUERIES_ATTR,
                has_both_attrs
            )
        )


    def test__constituents_signature(self):
        """
        Check that slice arguments are handled correctly and that appropriate
        exceptions are raised when slice arguments are bad.
        """
        # Requires input as a tuple.
        with self.assertRaises(ValueError):
            self.m._constituents_signature([1, 2])

        # Requires length-2 slices.
        with self.assertRaises(ValueError):
            self.m._constituents_signature((1, 2, 3))

        # Requires length-2 slices.
        with self.assertRaises(ValueError):
            self.m._constituents_signature((1,))

        # 2nd argument slices do not support having None for start or stop.
        with self.assertRaises(IndexError):
            self.m._constituents_signature(np.s_[1, 1:])
        with self.assertRaises(IndexError):
            self.m._constituents_signature(np.s_[1, :])
        with self.assertRaises(IndexError):
            self.m._constituents_signature(np.s_[1, :1])

        # Tests for correct output on slices.
        message = ("_constituents_signature failed to handle slices in the "
                   "second slice dimension.")

        # Ordinary slice.
        expected_output = (1, 2, 3)
        actual_output = self.m._constituents_signature(np.s_[1, 2:3])
        self.assertEqual(expected_output, actual_output, message)

        # Same start and stop.
        expected_output = (1, 2, 2)
        actual_output = self.m._constituents_signature(np.s_[1, 2:2])
        self.assertEqual(expected_output, actual_output, message)

        # Second dimension single value instead of slice.
        expected_output = (1, 2, 2)
        actual_output = self.m._constituents_signature(np.s_[1, 2])
        self.assertEqual(expected_output, actual_output, message)
        

    def test_constituents(self):
        """
        Check that calls to retrieve constituents work as expected.
        """
        #TODO: this really needs a good mocking framework so that we don't
        # rely on open DB connections to perform the test. 
        spx_data = self.m.constituents('SP500', '2012-12-31', '2012-12-31')
        djx_data = self.m.constituents('DowJones', '2012-12-31', '2012-12-31')

        self.assertTrue(len(spx_data) > 0, "Failed to retrieve SPX test data.")
        self.assertTrue(len(djx_data) > 0, "Failed to retrieve DJX test data.")


    def test___getitem__(self):
        """
        Check that call through __getitem__ are correctly interpreted as call 
        through constituents.
        """
        #TODO: this really needs a good mocking framework so that we don't
        # rely on open DB connections to perform the test. 
        spx_data = self.m.constituents('SP500', '2012-12-31', '2012-12-31')
        djx_data = self.m.constituents('DowJones', '2012-12-31', '2012-12-31')

        spx_gi = self.m['SP500', '2012-12-31':'2012-12-31']   
        djx_gi = self.m['DowJones', '2012-12-31':'2012-12-31']

        try:
            assert_frame_equal(spx_data, spx_gi)
        except AssertionError as pandas_assert_error:
            message = ("Function call to `constituents` for getting SPX data "
                       "does not match `__getitem__`")
            raise AssertionError(message)

        try:
            assert_frame_equal(djx_data, djx_gi)
        except AssertionError as pandas_assert_error:
            message = ("Function call to `constituents` for getting DJX data "
                       "does not match `__getitem__`")
            raise AssertionError(message)
        
            
if __name__ == "__main__":
    unittest.main()
        
