"""
Provides helper function `distributeby` for distributed version of groupby-
-apply. Heavily dependent on IPython.parallel and manual use of `ipcluster` or
manually created IPython distributed computing engines.

Treat as experimental.

Author: Ely M. Spears
"""

def distributeby(data_frame, 
                 group_names, 
                 target_function, 
                 serial=False):
    """
    Group a pandas DataFrame, then pass the groups via a blocking, load-
    balanced IPython parallel View object, to have a given function executed 
    on each group in parallel.

    It is assumed that withi the function defintion of `target_function`, any
    import statements are made such that the function can execute on remote
    IPython.parallel engines. You can alternatively use the DirectView's
    `sync_imports` context manager to manually propagate imports to the engines
    before distributing.

    Params
    ------
    data_frame: The pandas.DataFrame to be grouped and processed.
    group_names: String or list of strings, naming columns to group by.
    target_function: Picklable Callable to be called with a group as lone arg.
    serial: Boolean (default False). Forces serial pandas/apply execution.

    Returns
    -------
    The same thing (DataFrame or Series) as returned by pandas.groupby.apply.
    

    Example
    -------
    dfrm = pandas.DataFrame(
        {"A":np.random.rand(1000,),
         "group1":np.random.randint(10, size=(1000,)),
         "group2":np.random.randint(5, size=(1000,))}
    )

    def some_func(data_frame):
        import numpy as np
        return np.ptp((1 + data_frame.A).values)

    group_results = distributeby(dfrm, ["group1", "group2"], some_func)

    # Equivalent to the following serial execution:
    dfrm.groupby(["group1", "group2"], as_index=False).apply(some_func)
    """
    import importlib
    from itertools import izip
    from pandas.core.groupby import _get_axes, _is_indexed_like

    # Set-up needed IPython.parallel objects. Revert to serial mode if fails.
    try:
        from IPython.parallel import Client
        client = Client()
        direct_view = client[:]
        load_balanced_view = client.load_balanced_view()
        load_balanced_view.block = True

    except Exception as e:
        print (
            "... received the following exception when trying to import "
            "IPython.parallel:\n{}\n\nProceeding with serial execution of "
            "pandas.DataFrame.groupby.apply ...\n".format(e)
        )
        serial = True

    # Offer a debugging/fail-over mode to force serial execution.
    if serial:
        return data_frame.groupby(group_names).apply(target_function)

    # Create pandas groups.
    group_obj = data_frame.groupby(group_names, as_index=False)
    groups = dict(list(group_obj))
    group_indx = groups.keys()
    group_data = groups.values()

    # Map the per-group function to each group. Get results as ordered list
    # in case multiple jobs are handled by a single engine (making a dict un-
    # available).
    results = load_balanced_view.map(target_function, group_data)
    client.close()

    # Determine, just as pandas does, whether any of the groups had a mutated
    # index during the apply function.
    for key, group, result  in izip(group_indx, group_data, results):
        object.__setattr__(group, 'name', key)
        group_axes = _get_axes(group)
        if not _is_indexed_like(result, group_axes):
            mutated = True

    # Leverage pandas's pre-existing code for handling the alignment and
    # indexing of the results returned by apply.
    output = (
        group_obj
            ._wrap_applied_output(group_indx, results, mutated)
            .sort_index()
    )

    return output
    

if __name__ == "__main__":
    import time
    import pandas
    import numpy as np

    # A toy example showing common, simple circumstances under which
    # `distributeby` on a failry low-tech 4-core laptop is about 2x
    # faster than pandas.groupby.apply.
    ex_size = 500000
    toy_dfrm = pandas.DataFrame(
        {"A":np.random.randn(ex_size,), 
         "lab1":np.random.randint(15, size=(ex_size,)), 
         "lab2":np.random.randint(4, size=(ex_size,))}
    )

    # Define a function to test distributed.
    def f(data_frame):
        """
        Add some noise and perform a rolling regression in a DataFrame.
        """
        import pandas
        import numpy as np
        noise = 10*np.random.randn(len(data_frame))
        data_frame['B'] = data_frame['A'] + noise
        result = pandas.ols(
            y=data_frame.A, 
            x=data_frame.B, 
            window=20, 
            min_periods=5, 
            intercept=True
        ).beta

        return result


    ########################
    # Time a test example. #
    ########################
    groups = ['lab1', 'lab2']

    # Plain, serial pandas.
    #toy_dfrm.groupby(groups).apply(f)
    
    # Distributed version.
    st_time = time.time()
    distributeby(toy_dfrm, groups, f)
    p_elapsed = time.time() - st_time

    # Serial version.
    st_time = time.time()
    distributeby(toy_dfrm, groups,f, serial=True).head(10)
    s_elapsed = time.time() - st_time

    print p_elapsed, s_elapsed


        

    
