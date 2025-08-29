#!/usr/bin/env python3
"""
Debug script to check DataFrame structures before merging
"""

import json
import pandas as pd

def debug_dataframes():
    """Check the structure of each DataFrame before merging."""
    
    # Load data
    with open("2016.primary.json", "r") as fp:
        data_2016_primary = json.load(fp)
    
    with open("2016.general.json", "r") as fp:
        data_2016_general = json.load(fp)
    
    with open("2020.primary.dem.json", "r") as fp:
        data_2020_primary = json.load(fp)
    
    with open("2020.general.json", "r") as fp:
        data_2020_general = json.load(fp)
    
    with open("2022.json", "r") as fp:
        data_2022 = json.load(fp)
    
    with open("2018.general.json", "r") as fp:
        data_2018 = json.load(fp)
    
    # Process each dataset
    print("=== Processing DataFrames ===\n")
    
    # 2016 Primary
    print("1. 2016 Primary:")
    df_2016_primary = process_2016_primary(data_2016_primary)
    if df_2016_primary is not None:
        print(f"   Shape: {df_2016_primary.shape}")
        print(f"   Columns: {list(df_2016_primary.columns)}")
        print(f"   Sample counties: {df_2016_primary['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # 2016 General
    print("2. 2016 General:")
    df_2016_general = process_2016_general(data_2016_general)
    if df_2016_general is not None:
        print(f"   Shape: {df_2016_general.shape}")
        print(f"   Columns: {list(df_2016_general.columns)}")
        print(f"   Sample counties: {df_2016_general['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # 2020 Primary
    print("3. 2020 Primary:")
    df_2020_primary = process_2020_primary(data_2020_primary)
    if df_2020_primary is not None:
        print(f"   Shape: {df_2020_primary.shape}")
        print(f"   Columns: {list(df_2020_primary.columns)}")
        print(f"   Sample counties: {df_2020_primary['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # 2020 General
    print("4. 2020 General:")
    df_2020_general = process_2020_general(data_2020_general)
    if df_2020_general is not None:
        print(f"   Shape: {df_2020_general.shape}")
        print(f"   Columns: {list(df_2020_general.columns)}")
        print(f"   Sample counties: {df_2020_general['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # 2022
    print("5. 2022:")
    df_2022 = process_2022(data_2022)
    if df_2022 is not None:
        print(f"   Shape: {df_2022.shape}")
        print(f"   Columns: {list(df_2022.columns)}")
        print(f"   Sample counties: {df_2022['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # 2018
    print("6. 2018:")
    df_2018 = process_2018(data_2018)
    if df_2018 is not None:
        print(f"   Shape: {df_2018.shape}")
        print(f"   Columns: {list(df_2018.columns)}")
        print(f"   Sample counties: {df_2018['county'].head(3).tolist()}")
    
    print("\n" + "="*50 + "\n")
    
    # Test merge
    print("=== Testing Merge ===\n")
    
    dfs = []
    if df_2016_primary is not None:
        dfs.append(("2016 Primary", df_2016_primary))
    if df_2016_general is not None:
        dfs.append(("2016 General", df_2016_general))
    if df_2020_primary is not None:
        dfs.append(("2020 Primary", df_2020_primary))
    if df_2020_general is not None:
        dfs.append(("2020 General", df_2020_general))
    if df_2022 is not None:
        dfs.append(("2022", df_2022))
    if df_2018 is not None:
        dfs.append(("2018", df_2018))
    
    if dfs:
        print(f"Found {len(dfs)} DataFrames to merge")
        
        # Start with first DataFrame
        combined = dfs[0][1]
        print(f"Starting with {dfs[0][0]}: {combined.shape}")
        
        # Merge each subsequent DataFrame
        for name, df in dfs[1:]:
            print(f"\nMerging {name}: {df.shape}")
            print(f"Combined counties before: {len(combined)}")
            print(f"New DataFrame counties: {len(df)}")
            
            # Check for common counties
            common_counties = set(combined['county']) & set(df['county'])
            print(f"Common counties: {len(common_counties)}")
            
            # Merge
            combined = combined.merge(df, on="county", how="outer")
            print(f"Combined shape after merge: {combined.shape}")
            print(f"Combined counties after: {len(combined)}")

def process_2016_primary(data):
    """Process 2016 primary data."""
    races = data
    all_data = []
    
    for race in races:
        if "republican" in race["race_id"]:
            party = "rep"
        elif "democrat" in race["race_id"]:
            party = "dem"
        else:
            continue
            
        for county in race["counties"]:
            row = {"county": county["name"]}
            total = 0
            
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"prim_16_{candidate_key}_{party}"] = votes
                    total += votes
            else:
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    votes = candidate["votes"]
                    row[f"prim_16_{candidate_key}_{party}"] = votes
                    total += votes
            
            row[f"prim_16_{party}_total"] = total
            
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"prim_16_{candidate_key}_{party}_pct"] = (
                        votes / total if total > 0 else 0
                    )
            else:
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    row[f"prim_16_{candidate_key}_{party}_pct"] = (
                        candidate["votes"] / total if total > 0 else 0
                    )
            
            all_data.append(row)
    
    return pd.DataFrame(all_data)

def process_2016_general(data):
    """Process 2016 general data."""
    race = data
    all_data = []
    
    for county in race["counties"]:
        row = {"county": county["name"]}
        total = 0
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"pres_16_{candidate_key}"] = votes
                total += votes
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                votes = candidate["votes"]
                row[f"pres_16_{candidate_key}"] = votes
                total += votes
        
        row["pres_16_total"] = total
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"pres_16_{candidate_key}_pct"] = (
                    votes / total if total > 0 else 0
                )
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                row[f"pres_16_{candidate_key}_pct"] = (
                    candidate["votes"] / total if total > 0 else 0
                )
        
        all_data.append(row)
    
    return pd.DataFrame(all_data)

def process_2020_primary(data):
    """Process 2020 primary data."""
    race = data
    all_data = []
    
    for county in race["counties"]:
        row = {"county": county["name"]}
        total = 0
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"prim_20_{candidate_key}_dem"] = votes
                total += votes
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                votes = candidate["votes"]
                row[f"prim_20_{candidate_key}_dem"] = votes
                total += votes
        
        row["prim_20_dem_total"] = total
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"prim_20_{candidate_key}_dem_pct"] = (
                    votes / total if total > 0 else 0
                )
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                row[f"prim_20_{candidate_key}_dem_pct"] = (
                    candidate["votes"] / total if total > 0 else 0
                )
        
        all_data.append(row)
    
    return pd.DataFrame(all_data)

def process_2020_general(data):
    """Process 2020 general data."""
    race = data
    all_data = []
    
    for county in race["counties"]:
        row = {"county": county["name"]}
        total = 0
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"pres_20_{candidate_key}"] = votes
                total += votes
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                votes = candidate["votes"]
                row[f"pres_20_{candidate_key}"] = votes
                total += votes
        
        row["pres_20_total"] = total
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"pres_20_{candidate_key}_pct"] = (
                    votes / total if total > 0 else 0
                )
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                row[f"pres_20_{candidate_key}_pct"] = (
                    candidate["votes"] / total if total > 0 else 0
                )
        
        all_data.append(row)
    
    return pd.DataFrame(all_data)

def process_2022(data):
    """Process 2022 data."""
    races = data
    all_data = []
    
    for race in races:
        # Check the office field instead of race_name
        if "Governor" in race.get("office", ""):
            race_key = "gov"
        elif "Attorney General" in race.get("office", ""):
            race_key = "ag"
        elif "Secretary of State" in race.get("office", ""):
            race_key = "sos"
        else:
            continue
            
        for county in race["reporting_units"]:
            if county["level"] == "state":
                continue
                
            row = {"county": county["name"]}
            total = 0
            
            for candidate in county["candidates"]:
                candidate_key = candidate["nyt_id"].split("-")[0]
                votes = candidate["votes"]["total"]
                row[f"{race_key}_22_{candidate_key}"] = votes
                total += votes
            
            row[f"{race_key}_22_total"] = total
            
            for candidate in county["candidates"]:
                candidate_key = candidate["nyt_id"].split("-")[0]
                row[f"{race_key}_22_{candidate_key}_pct"] = (
                    candidate["votes"]["total"] / total if total > 0 else 0
                )
            
            all_data.append(row)
    
    return pd.DataFrame(all_data)

def process_2018(data):
    """Process 2018 data."""
    races = data
    all_data = []
    
    # Find the governor race
    governor_race = None
    for race in races:
        if "governor" in race.get("race_name", "").lower():
            governor_race = race
            break
    
    if not governor_race:
        print("No governor race found in 2018 data")
        return None
        
    for county in governor_race["counties"]:
        row = {"county": county["name"]}
        total = 0
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"gov_18_{candidate_key}"] = votes
                total += votes
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                votes = candidate["votes"]
                row[f"gov_18_{candidate_key}"] = votes
                total += votes
        
        row["gov_18_total"] = total
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                row[f"gov_18_{candidate_key}_pct"] = (
                    votes / total if total > 0 else 0
                )
        else:
            for candidate in county.get("candidates", []):
                candidate_key = candidate["candidate_id"].split("-")[0]
                row[f"gov_18_{candidate_key}_pct"] = (
                    candidate["votes"] / total if total > 0 else 0
                )
        
        all_data.append(row)
    
    return pd.DataFrame(all_data)

if __name__ == "__main__":
    debug_dataframes()
