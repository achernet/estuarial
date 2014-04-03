"""
Test the decorators provided by estuarial.util.

Author: Ben Zaitlen and Ely Spears
"""
import unittest
from estuarial.util import decorators


class TestDecorators(unittest.TestCase):
    """
    """
    class ApiMapperCalled(Exception):
        """
        Placeholder exception for detecting when the API mapper is called.
        """
        pass


    class DispatcherCalled(Exception):
        """
        Placeholder exception for detecting when the dispatcher is called.
        """
        pass


    def setUp(self):
        """
        Creates classes that are decorated with the different modes of use of
        `target_getitem`. Each raises a custom Exception at the point where 
        a check must be made that the correct functions are being called.
        """

        # Decorated class for testing that dispatcher gets called.
        @decorators.target_getitem('bar')
        class Foo(object):
            def bar(self, *args):
                raise TestDecorators.DispatcherCalled


        # Decorated class for testing that an API mapper is called.
        @decorators.target_getitem('bar', api_mapper='baz')
        class FooWithMapper(object):
            def bar(self, *args):
                pass

            def baz(self, slice_args):
                raise TestDecorators.ApiMapperCalled


        # Decorated class to ensure that argument filtering happens correctly.
        @decorators.target_getitem('bar')
        class FooReturnsSame(object):
            def bar(self, *args):
                return args


        # Decorated class to ensure that API mapping happens correctly.
        @decorators.target_getitem('bar', api_mapper='baz')
        class FooMapperReturnsSame(object):
            def bar(self, *args):
                return args

            def baz(self, slice_args):
                return slice_args        


        self.foo = Foo()
        self.foo_with_mapper = FooWithMapper()
        self.foo_returns_same  = FooReturnsSame()
        self.foo_mapper_returns_same  = FooMapperReturnsSame()


    def test_target_getitem(self):
        """
        Checks that `target_getitem` correctly dispatches `__getitem__` 
        arguments to a designated function. Also checks that if an API
        mapper is specified, that it is called.
        """
        with self.assertRaises(self.DispatcherCalled):
            self.foo[1,2,3]

        with self.assertRaises(self.ApiMapperCalled):
            self.foo_with_mapper[1,2,3]

        # Test plain foo
        plain_foo_is_correct = (
            self.foo_returns_same[1] == (1,),
            self.foo_returns_same[1:5] == (slice(1, 5, None),),
            self.foo_returns_same[1, 2, 3] == (1, 2, 3),
            self.foo_returns_same[1, 2:3] == (1, slice(2, 3, None))
        )

        message = "Error processing `__getitem__` args to dispatcher function."
        self.assertTrue(all(plain_foo_is_correct), message)

        # Test foo with mapper.
        mapper_foo_is_correct = (
            self.foo_mapper_returns_same[1] == (1,),
            self.foo_mapper_returns_same[1:5] == (slice(1, 5, None),),
            self.foo_mapper_returns_same[1, 2, 3] == (1, 2, 3),
            self.foo_mapper_returns_same[1, 2:3] == (1, slice(2, 3, None))
        )

        message = "Error processing `__getitem__` args to api-mapper function."
        self.assertTrue(all(mapper_foo_is_correct), message)


if __name__ == "__main__":
    unittest.main()

