.. _release_notes:

#############
Release Notes
#############

v0.1 (April 2014)
=================
* Defined singleton and composite Yaml spec for SQl queries
* ArrayManagementClient provides caching hook to ArrayManagement
* QueryHandler generates Python classes from composite Yaml documents.
* Consituent handling API:
   - MarketIndex for S&P BMI, S&P 500, Dow Jones, and Russell
   - UniverseBuilder for US, Canada, and GICS classifications.
* Metadata for available items in RKD and WorldScope.
* Ability to execute raw query strings against QAD databases.
* Demo showing workflow for beta-sorted quintile returns.


###################
Roadmap & TODO List
###################

v0.2 (Goal: July 2014)
======================
* Architectural choices about API for drilldown and query
* Entity mapping system to automatically align data from different vendors
* Example gallery with SQLite, PostgreSQL demos.
* API for users to add their own database config based on their local drivers

Long-term TODO list
===================
* API choices regarding ArrayManagement vs. Blaze and out-of-core needs.
* API choices for integration with matplotlib, pandas, and Bokeh.
