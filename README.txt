===============================================================================
IS303-A06 - CHICAGO CUBS DATA ANALYSIS
===============================================================================

A Python data-analysis pipeline that examines the 2026 Chicago Cubs roster to
identify the team's most productive and most cost-effective players.

Course: IS 303 - Assignment A06
Author: Jeremy Eldredge


-------------------------------------------------------------------------------
OVERVIEW
-------------------------------------------------------------------------------

cubs_data_analysis.py loads three CSVs of 2026 Cubs data, cleans and validates
them, then answers a few questions about the roster:

  * How does hitter age compare to pitcher age?
  * Which defensive positions produce the most offense (OPS)?
  * Which players deliver the most WAR per dollar of salary?
  * Do starting pitchers strike out more batters per walk than relievers?


-------------------------------------------------------------------------------
DATA
-------------------------------------------------------------------------------

All data comes from Baseball Reference, 2026 Chicago Cubs:
https://www.baseball-reference.com/teams/CHC/2026.shtml

  File                        Rows  Cols  Contents
  ------------------------------------------------------------------------
  cubs_hitting_data.csv         21    34  Season batting stats
                                          (BA, OBP, SLG, OPS, WAR, ...)
  cubs_pitching_data.csv        27    37  Season pitching stats
                                          (ERA, WHIP, SO/BB, WAR, ...)
  cubs_contracts_data.csv       46    15  Salary and contract details
                                          by player

Key columns used: Player, Age, Pos, OPS, WAR, SO/BB, and the 2026 salary field.


-------------------------------------------------------------------------------
HOW IT WORKS
-------------------------------------------------------------------------------

The script runs as a linear pipeline: load -> clean -> validate -> analyze.

1. LOAD
   load_hitting_data(), load_pitching_data(), and load_contract_data() read
   each CSV into a pandas DataFrame.

2. CLEAN
   clean_hitter_data()    - drops pitchers (rows with no BA), strips * and #
                            and IL notes from names, removes the Team Totals
                            row, and drops unused columns.
   clean_pitcher_data()   - strips name symbols, drops rows missing Pos or
                            SO/BB, and recodes closers (CL) as relievers (RP).
   clean_contracts_data() - converts salary strings like $12.5M to numeric
                            dollars and drops future contract years.

3. VALIDATE
   validate_hitter_data(), validate_pitcher_data(), and
   validate_contracts_data() assert that key columns have no nulls, that
   salaries are positive, and that no DataFrame is empty after cleaning.

4. ANALYZE
   analyze_hitting_data()  - reports average hitter age, groups OPS by
                             position, merges hitters with contracts to
                             compute WAR per $1M, and saves the scatter plot.
   analyze_pitching_data() - reports average pitcher age and SO/BB by role.


-------------------------------------------------------------------------------
RUNNING IT
-------------------------------------------------------------------------------

    pip install pandas matplotlib
    python cubs_data_analysis.py

Run from the repository root so the script can find the CSVs. Results print to
the console, and the chart is written to WAR_by_salary.png.


-------------------------------------------------------------------------------
FINDINGS
-------------------------------------------------------------------------------

  * Left field leads the team in OPS at .819, well above the ~.700 league
    average - though on a 40-man roster that mostly reflects Ian Happ alone.

  * Pitchers are older than hitters: 31.6 years on average versus 28.2.

  * Pete Crow-Armstrong is the best value on the roster, producing 3.13 WAR
    per $1M of salary.

  * Starters out-perform relievers in SO/BB, 3.27 to 2.83.

See WAR_by_salary.png for the WAR-by-salary scatter plot.


-------------------------------------------------------------------------------
LIMITATIONS
-------------------------------------------------------------------------------

The dataset covers only the Cubs' current 40-man roster, so most positions
have a single occupant - "best position by OPS" is really "that player's OPS."
Adding every MLB team's roster, or historical Cubs seasons, would make the
position and value comparisons meaningful.

The full write-up is in analysis.txt.


-------------------------------------------------------------------------------
FILES
-------------------------------------------------------------------------------

  cubs_data_analysis.py     analysis pipeline
  cubs_hitting_data.csv     batting stats
  cubs_pitching_data.csv    pitching stats
  cubs_contracts_data.csv   salary data
  WAR_by_salary.png         generated chart
  analysis.txt              written analysis and reflection
  README.txt                this file
