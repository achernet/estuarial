# Estuarial meeting 03/21/2014
Participants: Daniel Meisner, Ben Zaitlen, and Ely Spears (notes taker)

## Topics and keywords
estuarial, alpha-release, bug-fixes, calendar, point-in-time, entity, 
lookback-logic blaze, autogeneration

## Minutes
### Summary
@spearsem opened the meeting with a quick recap of the current work and 
upcoming milestones:

- Alpha release (repository being made public, but not yet advertised) is
slated for the second week of April (targeting April 8).

- Integration with blaze. This will be initially handled by Ben Z. as per 
[this commentfrom @aterrel](
https://github.com/ContinuumIO/blaze/pull/196#issuecomment-38324632). The
current design idea is to wrap estuarial's use of blaze inside of a query-
handling layer. This will allow developer's to possibly swap out reliance on 
blaze if they prefer something else. It will also let the estuarial team keep 
working and only open up a small exposure to the ArrayManagement tool for short
term caching ability.

- Cleaning up the current package structure. @quasiben is handling a branch for
this now. Changes will include some adjustments to sub-package location and
streamlining the config and setup process. These changes are slated for Monday,
March 24.

- Ensuring code works with new yaml style just as with former fsql style. This
is joint work with @spearsem and @quasiben after the clean-up branch is merged.

- Creating documentation, developer documentation, unit tests, and notebook
demos. Both @spearsem and @quasiben will stop all current development on 
Wednesday, March 26, to prioritize these items for the first release.

### Design Points
@danmeisner started a discussion on important design points to keep in mind as
we move forward, with @spearsem and @quasiben adding points too:

- How to manage multiple connections and connections to multiple sources?
- How to extend query-handling to non-SQL based queries.
- How to expose multiple function signatures / interfaces for each query. For
  example, the query `select * from my_table` with conditionals `date` and
  `id` might need to auto-gen functions that allow the date to be selected
  within a range (`between`) or with equality. If this was generated into a
  Python function called `my_table_query` with args `date` and `id`, what's
  a good api choice so that it's callable in these different ways, e.g. so that
  the following would all be supported in some way:

      my_table_query(date=between(dt1, dt2), id=in_(list_of_ids))
      my_table_query(date=dt1, id=sample_id)

- Calendar objects and lookback options. @danmeisner mentioned that the API
  results will depend heavily on what kind of calendar alignment is desired by
  the user. We'll need facilities to query the existing TR calendar tables, but
  also may need to support some option config options for setting up lookback
  logic. Many quetions arose: should any lookback logic be default? This could
  lead to problems if a user did not expect the default lookback logic. It
  seems like the safest choice is to only query against whatever is in the
  tables as a default. But for aligning fiscal reports by common date
  conventions, or by restricting to only dates where a certain property is 
  satisfied (@danmeisner mentioned dates where the Vix is above a certain
  level), we'll need to provide some lookback or date-restriction options. This
  is related to the Pandas customizable business-day functionality so maybe we
  can take notes from that implementation. This also has very similar design
  issues as the constiuent universe / index problem too, so if we can abstract
  some of these details out into a generic basket-of-entities handler, where
  entities can be stocks, dates, etc., that might be a good goal.

- Mapping facilities. @danmeisner brought up mapping between different
  identifier types. Say a user queries against the RKD data and against IBES and
  ends up with data on similar dates, yet different identifiers. We need to
  provide a point-in-time mapping from one identifier to another, at least for
  all of the built-in data sets. Making this an abstract tool that can suck in
  a user's custom-made mapping tables is also desirable, so that the same 
  mapping code can be used whether for the user's personal archive of .csv
  files or across Thomson Reuters databases.

- Some other speculative thoughts: do we want to use some available finance
  data sets, like the Kenneth French Data Library, to pre-build some MySQL 
  tables that come pre-installed with the tools? That way open source devs
  can at least query against those toy data sets when testing, and the tool can
  be immediately useful to people even before they decide whether they want to
  buy data from Thomson Reuters? I've performed this before, it's a somewhat
  time-consuming task but it might be very nice to provide out-of-the box data
  to show off how the querying works, and even how to extend the API to handle
  additional queries. We'd need to check on licensing. Note also that French
  updates his data quarterly. We could just take a single snapshot though and
  simply document that we provide French data as-of some date.

- Some other questions: how will large queries be handles (e.g. where the
  number of tokens in an "in" statement is larger than the MSSQL limit)? How
  will table references be handled when they are part of an argument, such as
  "where Foo.Date = X' if the user does not want to rename "Foo.Date"?
  