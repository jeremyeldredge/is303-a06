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
- cubs_contracts_data.csv: player salary data for 2026

Processes:
- load_hitting_data(), load_pitching_data(), load_contract_data(): each reads a CSV into a DataFrame
- clean_hitter_data(): removes pitchers (rows with no BA), cleans player names, drops unused columns
- clean_pitcher_data(): cleans player names, removes rows missing Pos or SO/BB, drops unused columns
- clean_contracts_data(): parses 2026 salary strings to numeric values, drops unused columns
- validate_hitter_data(), validate_pitcher_data(), validate_contracts_data(): assert key columns have no nulls and DataFrames are non-empty
- analyze_hitting_data(): avg hitter age, OPS by defensive position, WAR per salary dollar; generates scatter plot
- analyze_pitching_data(): avg pitcher age, SO/BB rate by position (SP vs RP)

Outputs:
- Average age of hitters (printed)
- Average OPS by defensive position (printed table)
- Scatter plot of WAR by 2026 salary saved as WAR_by_salary.png
- Average age of pitchers (printed)
- Average SO/BB rate by pitcher role (printed table)
"""

import pandas as pd 
import matplotlib.pyplot as plt



# load both csv files into DataFrames
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

def load_contract_data(filepath):
    # load CSV and return a DataFrame
    df_contracts = pd.read_csv(filepath)
    print(f"Loaded {len(df_contracts)} rows from {filepath}")
    return df_contracts



# clean data: remove pitchers from hitting data, remove symbols from names
def clean_hitter_data(df):

    # remove rows of players with no batting average (pitchers)
    df = df.dropna(subset=["BA"])

    # remove (#) or (*) from end of player names
    df["Player"] = df["Player"].str.replace("*","").str.replace("#","")

    # remove awards and Player-additional columns
    df = df.drop(columns=['Awards','Player-additional'])

    df['Player']=df['Player'].str.replace(" (10-day IL)","")
    df = df[df['Player'] != 'Team Totals']

    print(f"Cleaned {len(df)} rows from cubs_hitting_data.csv")
    return df

def clean_pitcher_data(df):
    # remove (#) or (*) from end of player names
    df["Player"] = df["Player"].str.rstrip("*#")

    # remove pitchers without position listed
    df = df.dropna(subset=['Pos'])

    # change CL positiion to RP
    df.loc[df['Pos'] == 'CL', 'Pos'] = 'RP'

    # remove pitchers with null SO/BB values
    df = df.dropna(subset=["SO/BB"])

    # remove awards and Player-additional columns
    df = df.drop(columns=['Awards','Player-additional'])

    print(f"Cleaned {len(df)} rows from cubs_pitching_data.csv")
    return df

def clean_contracts_data(df):
   df['2026'] = df['2026'].str.replace('$','').str.replace('M','').str.replace('k','')
   df['2026'] = pd.to_numeric(df['2026'], errors='coerce') * 1_000_000
   df.loc[df['Name'] == 'Pete Crow-Armstrong', '2026'] = df.loc[df['Name'] == 'Pete Crow-Armstrong', '2026'] / 1000  
   # this player's salary is listed in thousands instead of millions, so divide by 1000 to correct
   df = df.dropna(subset=['2026'])

   # remove unneccesary columns
   df = df.drop(columns=['Yrs','Acquired','Contract Status','SrvTm','Agent','2027','2028','2029','2030','2031','2032','Name-additional'])

   print(f"Cleaned {len(df)} rows from cubs_contracts_data.csv")
   return df



# data validation
def validate_hitter_data(df):
    assert df["BA"].notna().all(), "BA still has missing values"
    assert len(df) > 0, "DataFrame is empty after cleaning"
    print(f"Validated {len(df)} rows of hitter data")
    return df

def validate_pitcher_data(df):
    assert df["SO/BB"].notna().all(), "SO/BB still has missing values"
    assert len(df) > 0, "DataFrame is empty after cleaning"
    print(f"Validated {len(df)} rows of pitcher data")
    return df

def validate_contracts_data(df):
    assert df["2026"].notna().all(), "2026 salary still has missing values"
    assert (df['2026'] > 0).all(), "2026 has zero or negative salaries"
    assert len(df) > 0, "DataFrame is empty after cleaning"
    print(f"Validated {len(df)} rows of contract data")
    return df

# data analysis
# avg age of pitchers vs hitters (both), OPS by defensive position (hitters), WAR by salary (hitters), SO/BB rate of starters vs releivers (pitchers)
def analyze_hitting_data(df):

    hitter_avg_age = df['Age'].mean()
    print(f"Average hitter age: {hitter_avg_age:.1f} yrs")

    print("Average OPS by position:")
    print(df.groupby("Pos")["OPS"].mean().round(3).sort_values(ascending=False))

    df_merged = df.merge(df_contracts, left_on='Player', right_on='Name')
    df_merged["WAR per $1M"] = df_merged['WAR'] / df_merged['2026'] * 1000000
    print(df_merged[['Player','WAR','2026','WAR per $1M']].sort_values('WAR per $1M', ascending = False).round(2))

    # chart must be created inside this function because df_merged is not global
    plt.scatter(df_merged['WAR'], df_merged['2026'], color='green')
    plt.title("WAR per $1M - 2026 Chicago Cubs")
    plt.xlabel("WAR (Wins Above Replacement)")
    plt.ylabel("2026 Salary")
    plt.tight_layout()
    plt.savefig("WAR_by_salary.png")
    plt.show()

def analyze_pitching_data(df):

    pitcher_avg_age = df['Age'].mean()
    print(f"Average pitcher age: {pitcher_avg_age:.1f} yrs")

    print (f"SO/BB by role (SP vs RP): {df.groupby('Pos')["SO/BB"].mean()}")


# --- Main Pipeline --- 
df_hitting = load_hitting_data("cubs_hitting_data.csv")
df_pitching = load_pitching_data("cubs_pitching_data.csv")
df_contracts = load_contract_data("cubs_contracts_data.csv")
print("="*50)
df_hitting = clean_hitter_data(df_hitting)
df_pitching = clean_pitcher_data(df_pitching)
df_contracts = clean_contracts_data(df_contracts)
print("="*50)
df_hitting = validate_hitter_data(df_hitting)
df_pitching = validate_pitcher_data(df_pitching)
df_contracts = validate_contracts_data(df_contracts)
print("="*50)
analyze_hitting_data(df_hitting)
analyze_pitching_data(df_pitching)

