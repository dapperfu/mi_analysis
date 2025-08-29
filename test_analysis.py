#!/usr/bin/env python3
"""
Simple test script for election analysis
"""

import json
import pandas as pd
import numpy as np

def main():
    print("Starting election analysis test...")
    
    # Test loading data
    try:
        with open("2016.primary.json", "r") as fp:
            data_2016_primary = json.load(fp)
        print(f"✓ Loaded 2016 primary data: {len(data_2016_primary)} races")
        
        # Look at the structure
        for i, race in enumerate(data_2016_primary):
            print(f"Race {i}: {race.get('race_id', 'Unknown')}")
            if 'counties' in race:
                print(f"  Counties: {len(race['counties'])}")
                if len(race['counties']) > 0:
                    print(f"  Sample county: {race['counties'][0]['name']}")
                    if 'results' in race['counties'][0]:
                        print(f"  Results keys: {list(race['counties'][0]['results'].keys())}")
                    elif 'candidates' in race['counties'][0]:
                        print(f"  Candidates: {len(race['counties'][0]['candidates'])}")
        
        # Test processing one race
        if len(data_2016_primary) > 0:
            race = data_2016_primary[0]
            print(f"\nProcessing race: {race.get('race_id', 'Unknown')}")
            
            data = []
            for county in race["counties"]:
                row = {"county": county["name"]}
                total = 0
                
                # Handle the results structure
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        row[f"prim_16_{candidate_key}"] = votes
                        total += votes
                else:
                    # Fallback to candidates structure
                    for candidate in county.get("candidates", []):
                        candidate_key = candidate["candidate_id"].split("-")[0]
                        votes = candidate["votes"]
                        row[f"prim_16_{candidate_key}"] = votes
                        total += votes
                
                row["prim_16_total"] = total
                
                # Calculate percentages
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        row[f"prim_16_{candidate_key}_pct"] = (
                            votes / total if total > 0 else 0
                        )
                else:
                    for candidate in county.get("candidates", []):
                        candidate_key = candidate["candidate_id"].split("-")[0]
                        row[f"prim_16_{candidate_key}_pct"] = (
                            candidate["votes"] / total if total > 0 else 0
                        )
                
                data.append(row)
            
            df = pd.DataFrame(data)
            print(f"✓ Created DataFrame: {len(df)} counties, {len(df.columns)} columns")
            print(f"Columns: {list(df.columns)}")
            print(f"\nFirst few rows:")
            print(df.head())
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
