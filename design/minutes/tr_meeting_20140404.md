# Estuarial meeting 04/04/2014
Participants: Daniel Meisner, Ben Zaitlen, Matt Harward and Ely Spears

## Topics and keywords
estuarial, alpha-release, bug-fixes, blaze, bokeh, project-roadmap

## Summary
- First soft release scheduled for Wednesday, April 9 (with a one-day budder
  in case any last minute issues arise).

- There is a need for some larger-scale demos. For first release, target 
  creation of a demo that loads a cross-section of securities over time,
  calculates a rolling beta for each security against a benchmark, and performs
  some analysis with the data. The current proposal for analysis is to group
  stocks into quantiles by their beta to the U.S. market and provide some
  summary statistics about returns in different beta buckets. Assigned to 
  @spearsem.

- Documentation for first release: user guide, developer guide, release notes,
  and roadmap. Install guide for drivers, Wakari (plus Wakari upgrade).
  Assigned to @quasiben.

- Roadmap meeting scheduled for Wednesday, April 9. Meeting will address plans 
  for future integration with Blaze and Bokeh, the extent to which out-of-core
  computations will be important to Estuarial, and some of the project manage-
  ment details for time allocation to integrating with Blaze.

- For the time being, pinging Dan and Jason via Flowdock or email is still the
  preferred way to get support on SQL-side questions. This may shift to more
  regular meetings during which bundles of support questions will be addressed
  in one session -- as we think about the roadmap we should also think about
  the level of SQL-side support that will be needed to ensure fast turnaround
  and delivery times.