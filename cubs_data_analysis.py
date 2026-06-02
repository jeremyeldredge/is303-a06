"""
Jeremy Eldredge
IS 303 - A06

Chicago Cubs Data Anlysis
Analyzes data from the current 2026 MLB season to find star players.

Inputs:
- cubs_hitting_data.csv: 22 rows, columns: Rk,Player,Age,Pos,WAR,G,PA,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,
    BA,OBP,SLG,OPS,OPS+,rOBA,Rbat+,TB,GIDP,HBP,SH,SF,IBB,Pos,Awards,Player-additional
- cubs_pitching_data.csv: 28 rows, columns: Rk,Player,Age,Pos,WAR,W,L,W-L%,ERA,G,GS,GF,CG,SHO,SV,IP,H,
    R,ER,HR,BB,IBB,SO,HBP,BK,WP,BF,ERA+,FIP,WHIP,H9,HR9,BB9,SO9,SO/BB,Awards,Player-additional

Processes:
- load_data(): reads CSV into DataFrame
- clean_data(): convert numbers from strings, clean player names
- validate_data(): assert no negative stats, verifies all values not null
- analyze_data(): avg age of pitchers vs hitters (both), BA by defensive position (hitters), HR by salary (hitters), avg ERA and SO rate of starters vs releivers (pitchers)
- create_chart(): bar chart of HR by salary

Outputs:
- Avg age of pitchers and hitters (printed table)
- Batting average per defensive position (printed table)
- Bar chart of HR by salary (HR/$) saved as HR_by_salary.png
- ERA and SO rate starters vs releivers (printed table)
"""

import pandas as pd
