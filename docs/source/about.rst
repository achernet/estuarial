Design
======

The Financial Entity and Licensed Data Manager (Estuarial) is an open source project built in partnership with
Continuum Analytics.  Estuarial is the client-side "glue" between our quant research data and the python big data
ecosystem.  Our main goal is to reduce the time and cost for our clients to assimilate new content sets.

We provide a modular framework for exposing federated data and metadata with a consistent API.  Estuarial currently
handles a variety of data formats including csv, hdf5, json, xml, and SQL databases.  Estuarial comes
'batteries included' with a catalogue of SQL queries wrapped into Python objects for accessing QADirect.
Additionally, Estuarial provides a YAML-based markup language for auto-magically transforming queries to Python objects
on load.

Our design emphasizes performance for quant workflows involving extremely large datasets.  Estuarial applies constraints
and transformations as near to the data storage as possible. This allows users to work with datasets that would
otherwise be too large to load into memory or transfer across a network.  Estuarial can deploy to a single machine, or
in an enterprise context as a distributed system.

Benefits:

* A single API to access data from TR, 3rd party, and in-house sources.
* Use TR concordance with in-house data.
* Simple function calls instead of complex SQL queries.
* Organize and catalog all of your data.
* 100% Free and Open Source for ultimate transparency and extensibility.