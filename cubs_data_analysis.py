"""
Jeremy Eldredge
IS 303 - A06

Chicago Cubs Data Anlysis
Analyzes data from the current 2026 MLB season to find star players.

Inputs:
- csv data from baseball-reference.com
- cubs_hitting_data.csv: 22 rows, columns: Rk,Player,Age,Pos,WAR,G,PA,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,
    BA,OBP,SLG,OPS,OPS+,rOBA,Rbat+,TB,GIDP,HBP,SH,SF,IBB,Pos,Awards,Player-additional
- cubs_pitching_data.csv: 28 rows, columns: Rk,Player,Age,Pos,WAR,W,L,W-L%,ERA,G,GS,GF,CG,SHO,SV,IP,H,
    R,ER,HR,BB,IBB,SO,HBP,BK,WP,BF,ERA+,FIP,WHIP,H9,HR9,BB9,SO9,SO/BB,Awards,Player-additional

Processes:
- load_data(): reads CSV into DataFrame
- clean_data(): delete pitchers from hittig data, clean player names
- validate_data(): assert no negative stats, verifies all values not null
- analyze_data(): avg age of pitchers vs hitters (both), BA by defensive position (hitters), HR by salary (hitters), avg ERA and SO/BB rate of starters vs releivers (pitchers)
- create_chart(): bar chart of HR by salary

Outputs:
- Avg age of pitchers and hitters (printed table)
- Batting average per defensive position (printed table)
- Bar chart of HR by salary (HR/$) saved as HR_by_salary.png
- ERA and SO/BB rate starters vs releivers (printed table)
"""

import pandas as pd 
import matplotlib.pyplot as plt

def load_hitting_data(filepath):
    # load CSV and return a DataFrame
    df_hitting = pd.read_csv(filepath)
    print(f"Loaded {len(df_hitting)} rows from {filepath}")
    return df_hitting

def load_pitching_data(filepath):
    # load CSV and return a DataFrame
    df_pitching = pd.read_csv(filepath)
    print(f"Loaded {len(df_pitching)} rows from {filepath}")
    return df_pitching

df_hitting = load_hitting_data("cubs_hitting_data.csv")
df_pitching = load_pitching_data("cubs_pitching_data.csv")

# clean data: remove pitchers from hitting data, remove symbols from names
def clean_hitter_data(df):

    # remove rows of players with no batting average (pitchers)
    df = df.dropna(subset=["BA"])

    # remove (#) or (*) from end of player names
    df["Player"] = df["Player"].str.rstrip("*#")

    # remove awards and Player-additional columns
    df = df.drop(columns=['Awards','Player-additional'])

    print(f"Cleaned {len(df)} rows from cubs_hitting_data.csv")
    return df

def clean_pitcher_data(df):
    # remove (#) or (*) from end of player names
    df["Player"] = df["Player"].str.rstrip("*#")

    # remove pitchers with null SO/BB values
    df = df.dropna(subset=["SO/BB"])

    # remove awards and Player-additional columns
    df = df.drop(columns=['Awards','Player-additional'])

    print(f"Cleaned {len(df)} rows from cubs_pitching_data.csv")
    return df

df_hitting = clean_hitter_data(df_hitting)
df_pitching = clean_pitcher_data(df_pitching)

def validate_data(df):
    assert df["BA"].notna().all(), "BA still has missing values"
    assert df["SO/BB"].notna().all(), "SO/BB still has missing values"
    assert len(df) > 0, "DataFrame is empty after cleaning"

def analyze_hitting_data(df):
    hitter_avg_age = df[df['Age'].mean()]
    