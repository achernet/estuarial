"""
Central location for decorators used by the Estuarial system.

Author: Ben Zaitlen and Ely Spears
"""

def target_getitem(function_name, api_mapper=None):
    """
    A decorator factory method that annotates the name of a function belonging
    to a class that will be used as the target for any use of __getitem__ from
    that class.

    Params
    ------
    function_name: String naming a function of the decorated class that will be
    called whenever `__getitem__` is invoked.

    api_mapper: (Optional, default is `None`) String naming a function of the
    decorated class that will process whatever is passed to `__getitem__` first
    to sanitize or handle slicing syntax and arguments before they are passed
    into the function named by `function_name`.

    Returns
    -------
    A decorator that can be applied to a class to induce the described 
    `__getitem__` behavior.


    Examples
    --------

        @target_getitem('bar')
        class Foo(object):
            def bar(self, x, y1, y2):
                return [x + y for y in range(y1, y2)]

        f = Foo()
        f[1, 2, 3] # returns [3]

    By default, the decorator will just pass each dimension of the requested 
    slice directly as the corresponding positional argument of the annotated 
    function. E.g., in the above example, `f[1, 2, 3]` means to simply reflect 
    the argument `1` into the first position, `2` into the second position, 
    etc., of a function call to `bar`.

    There is optional support for fancier handling that allows the api of the
    function to be mapped or handled, by passing in the name of another function
    on the class that does the handling:

        @target_getitem('bar', api_mapper='baz')
        class Foo(object):
            def bar(self, x, y1, y2):
                return [x + y for y in range(y1, y2)]

            def baz(self, slice_args):
                "Map slice arguments into the api for function `bar`."
                if len(slice_args) == 2:
                    args= (slice_args[0], 
                           slice_args[1].start, 
                           slice_args[1].stop)
                elif:
                    len(slice_args) == 3:
                        args = slice_args
                else: 
                    message = "Expected either 3 args or 1 arg and 1 slice."
                    raise ValueError(message)

                return args

    
         f = Foo()
         f[1, 2, 3]    # returns [3]
         f[1, 2:3]     # also returns [3] since `baz` parses the slice.
         f[1, 2, 3, 4] # will raise an Exception, wrong argument signature.

    """
    def decorator(klass):
        def __getitem__(self, slice_args):

            # Get a handle to any argument sanitizer if given.
            if api_mapper is None:
                # If no sanitizer is given, then it's expected that whatever
                # is passed directly to __getitem__ can be passed directly
                # to the target function.
                sanitizer = lambda *args: args
            else:
                sanitizer = getattr(self, api_mapper)

            # Get a handle to the target function.
            dispatcher = getattr(self, function_name)

            # Get sanitized arguments
            sanitized_args = sanitizer(slice_args)

            # Return dispatcher result on sanitized arguments
            return dispatcher(*sanitized_args)

        # Patch this version of `__getitem__` onto the class and return the
        # modified class.
        klass.__getitem__ = __getitem__
        return klass

    # Return the decorator that performs the above `__getitem__` modifications.
    return decorator
