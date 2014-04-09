.. _fundamentals:

##########
Worldscope
##########

Worldscope contains standardized presentations of publicly reported financial statements (balance sheets, income
and cash flow statements) for 57,000 companies globally.

Worldcope Access
----------------

Exploratory Style::

    spx = fd.UniverseBuilder.spx_idx('2013-12-04')
    spx.cash['2009-01-01':'2014-01-01']
    spx.ni['2009-01-01':'2014-01-01']
    ....

Functional Style::


    universe = #some universe of seccodes
    dt_list = ('2000-01-01, '2014-01-01')
    metrics = [NI,CASH,TL]
    tr.worldscope(universe,metrics,dt_list)


To get a full list of metrics for worldscope please see

Worldscope MetaData
-------------------

::

    estuarial.metrics.ws.<tab><tab>
    #or
    metrics.ws.find_metrics('DEBT')
             Number                                               Name
    197    18282                                   CONVERTIBLE DEBT
    215    18232                  CURRENT PORTION OF LONG TERM DEBT
    817     1251                           INTEREST EXPENSE ON DEBT
    929     3251                                     LONG TERM DEBT
    930     8226                     LONG TERM DEBT % COMMON EQUITY
    931     8277              LONG TERM DEBT % COMMON EQUITY (GAAP)
    932     8279  LONG TERM DEBT % COMMON EQUITY (GAAP) - 3 YEAR...
    933     8281  LONG TERM DEBT % COMMON EQUITY (GAAP) - 5 YEAR...
    934     8230          LONG TERM DEBT % COMMON EQUITY - 5 YR AVG
    ...
    ...
