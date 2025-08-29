#!/usr/bin/env python3
"""
Election Meta-Analysis: Comprehensive Analysis of Voter Behavior Patterns

This script performs deep analysis of election data to find meaningful connections
between different election results and voter behavior shifts across multiple cycles.

Key Analyses:
1. Primary to General Election Shifts (Bernie -> Biden/Trump)
2. County-level Rightward Shifts (2016-2024, 2020-2024)
3. Ted Cruz Primary Performance vs. General Election Shifts
4. Cross-cycle Correlation Analysis
5. Voter Migration Patterns
6. Geographic Clustering Analysis

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ElectionMetaAnalyzer:
    """Comprehensive election data analyzer for finding voter behavior patterns."""
    
    def __init__(self):
        """Initialize the analyzer with data loading."""
        self.data = {}
        self.combined_df = None
        self.load_all_data()
        
    def load_all_data(self):
        """Load all available election data files."""
        print("Loading election data...")
        
        # Load 2016 data
        try:
            with open("2016.primary.json", "r") as fp:
                self.data['2016_primary'] = json.load(fp)
            print("✓ Loaded 2016 primary data")
        except FileNotFoundError:
            print("✗ 2016 primary data not found")
            
        try:
            with open("2016.general.json", "r") as fp:
                self.data['2016_general'] = json.load(fp)
            print("✓ Loaded 2016 general data")
        except FileNotFoundError:
            print("✗ 2016 general data not found")
            
        # Load 2020 data
        try:
            with open("2020.primary.dem.json", "r") as fp:
                self.data['2020_primary_dem'] = json.load(fp)
            print("✓ Loaded 2020 Democratic primary data")
        except FileNotFoundError:
            print("✗ 2020 Democratic primary data not found")
            
        try:
            with open("2020.general.json", "r") as fp:
                self.data['2020_general'] = json.load(fp)
            print("✓ Loaded 2020 general data")
        except FileNotFoundError:
            print("✗ 2020 general data not found")
            
        # Load 2022 data
        try:
            with open("2022.json", "r") as fp:
                self.data['2022'] = json.load(fp)
            print("✓ Loaded 2022 data")
        except FileNotFoundError:
            print("✗ 2022 data not found")
            
        # Load 2018 data
        try:
            with open("2018.general.json", "r") as fp:
                self.data['2018_general'] = json.load(fp)
            print("✓ Loaded 2018 general data")
        except FileNotFoundError:
            print("✗ 2018 general data not found")
    
    def process_2016_primary(self):
        """Process 2016 primary data into DataFrame."""
        if '2016_primary' not in self.data:
            return None
            
        races = self.data['2016_primary']
        data = []
        
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
                
                # Handle the results structure (not candidates)
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        row[f"prim_16_{candidate_key}_{party}"] = votes
                        total += votes
                else:
                    # Fallback to candidates structure if it exists
                    for candidate in county.get("candidates", []):
                        candidate_key = candidate["candidate_id"].split("-")[0]
                        votes = candidate["votes"]
                        row[f"prim_16_{candidate_key}_{party}"] = votes
                        total += votes
                
                row[f"prim_16_{party}_total"] = total
                
                # Calculate percentages
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
                
                data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2016_general(self):
        """Process 2016 general election data."""
        if '2016_general' not in self.data:
            return None
            
        race = self.data['2016_general']
        data = []
        
        for county in race["counties"]:
            row = {"county": county["name"]}
            total = 0
            
            # Handle the results structure
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"pres_16_{candidate_key}"] = votes
                    total += votes
            else:
                # Fallback to candidates structure if it exists
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    votes = candidate["votes"]
                    row[f"pres_16_{candidate_key}"] = votes
                    total += votes
            
            row["pres_16_total"] = total
            
            # Calculate percentages
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
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2020_primary_dem(self):
        """Process 2020 Democratic primary data."""
        if '2020_primary_dem' not in self.data:
            return None
            
        race = self.data['2020_primary_dem']
        data = []
        
        for county in race["counties"]:
            row = {"county": county["name"]}
            total = 0
            
            # Handle the results structure
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"prim_20_{candidate_key}_dem"] = votes
                    total += votes
            else:
                # Fallback to candidates structure if it exists
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    votes = candidate["votes"]
                    row[f"prim_20_{candidate_key}_dem"] = votes
                    total += votes
            
            row["prim_20_dem_total"] = total
            
            # Calculate percentages
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
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2020_general(self):
        """Process 2020 general election data."""
        if '2020_general' not in self.data:
            return None
            
        race = self.data['2020_general']
        data = []
        
        for county in race["counties"]:
            row = {"county": county["name"]}
            total = 0
            
            # Handle the results structure
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"pres_20_{candidate_key}"] = votes
                    total += votes
            else:
                # Fallback to candidates structure if it exists
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    votes = candidate["votes"]
                    row[f"pres_20_{candidate_key}"] = votes
                    total += votes
            
            row["pres_20_total"] = total
            
            # Calculate percentages
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
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2022_data(self):
        """Process 2022 election data."""
        if '2022' not in self.data:
            return None
            
        races = self.data['2022']
        county_data = {}  # Use dict to aggregate by county
        
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
                    
                county_name = county["name"]
                
                # Initialize county row if not exists
                if county_name not in county_data:
                    county_data[county_name] = {"county": county_name}
                
                total = 0
                
                for candidate in county["candidates"]:
                    candidate_key = candidate["nyt_id"].split("-")[0]
                    votes = candidate["votes"]["total"]
                    county_data[county_name][f"{race_key}_22_{candidate_key}"] = votes
                    total += votes
                
                county_data[county_name][f"{race_key}_22_total"] = total
                
                # Calculate percentages
                for candidate in county["candidates"]:
                    candidate_key = candidate["nyt_id"].split("-")[0]
                    county_data[county_name][f"{race_key}_22_{candidate_key}_pct"] = (
                        candidate["votes"]["total"] / total if total > 0 else 0
                    )
        
        # Convert dict to DataFrame
        data = list(county_data.values())
        return pd.DataFrame(data)
    
    def process_2018_general(self):
        """Process 2018 general election data."""
        if '2018_general' not in self.data:
            return None
            
        races = self.data['2018_general']
        data = []
        
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
            
            # Handle the results structure
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    row[f"gov_18_{candidate_key}"] = votes
                    total += votes
            else:
                # Fallback to candidates structure if it exists
                for candidate in county.get("candidates", []):
                    candidate_key = candidate["candidate_id"].split("-")[0]
                    votes = candidate["votes"]
                    row[f"gov_18_{candidate_key}"] = votes
                    total += votes
            
            row["gov_18_total"] = total
            
            # Calculate percentages
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
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def combine_all_data(self):
        """Combine all processed data into a single DataFrame."""
        print("Combining all election data...")
        
        dfs = []
        
        # Process each dataset
        df_2016_primary = self.process_2016_primary()
        if df_2016_primary is not None:
            dfs.append(df_2016_primary)
            print("✓ Processed 2016 primary data")
            
        df_2016_general = self.process_2016_general()
        if df_2016_general is not None:
            dfs.append(df_2016_general)
            print("✓ Processed 2016 general data")
            
        df_2020_primary = self.process_2020_primary_dem()
        if df_2020_primary is not None:
            dfs.append(df_2020_primary)
            print("✓ Processed 2020 Democratic primary data")
            
        df_2020_general = self.process_2020_general()
        if df_2020_general is not None:
            dfs.append(df_2020_general)
            print("✓ Processed 2020 general data")
            
        df_2022 = self.process_2022_data()
        if df_2022 is not None:
            dfs.append(df_2022)
            print("✓ Processed 2022 data")
            
        df_2018 = self.process_2018_general()
        if df_2018 is not None:
            dfs.append(df_2018)
            print("✓ Processed 2018 general data")
        
        # Merge all dataframes on county
        if dfs:
            self.combined_df = dfs[0]
            for df in dfs[1:]:
                self.combined_df = self.combined_df.merge(df, on="county", how="outer")
            
            print(f"✓ Combined data: {len(self.combined_df)} counties, {len(self.combined_df.columns)} columns")
            return self.combined_df
        else:
            print("✗ No data to combine")
            return None
    
    def calculate_voter_shifts(self):
        """Calculate various voter shift metrics."""
        if self.combined_df is None:
            print("No combined data available")
            return
            
        print("Calculating voter shift metrics...")
        
        # 1. Bernie to Biden/Trump shifts (2016 primary -> 2020 general)
        if all(col in self.combined_df.columns for col in ['prim_16_sanders_dem_pct', 'pres_20_biden_pct', 'pres_20_trump_pct']):
            self.combined_df['bernie_to_biden_shift'] = (
                self.combined_df['pres_20_biden_pct'] - self.combined_df['prim_16_sanders_dem_pct']
            )
            self.combined_df['bernie_to_trump_shift'] = (
                self.combined_df['pres_20_trump_pct'] - self.combined_df['prim_16_sanders_dem_pct']
            )
            print("✓ Calculated Bernie to Biden/Trump shifts")
        
        # 2. Rightward shifts between elections
        if all(col in self.combined_df.columns for col in ['pres_16_trump_pct', 'pres_20_trump_pct']):
            self.combined_df['trump_16_to_20_shift'] = (
                self.combined_df['pres_20_trump_pct'] - self.combined_df['pres_16_trump_pct']
            )
            print("✓ Calculated Trump 2016-2020 shift")
        
        # 3. Ted Cruz primary performance vs. general shifts
        if all(col in self.combined_df.columns for col in ['prim_16_cruz_rep_pct', 'pres_16_trump_pct']):
            self.combined_df['cruz_primary_vs_trump_general'] = (
                self.combined_df['prim_16_cruz_rep_pct'] - self.combined_df['pres_16_trump_pct']
            )
            print("✓ Calculated Cruz primary vs. Trump general correlation")
        
        # 4. Cross-cycle Republican performance
        if all(col in self.combined_df.columns for col in ['pres_16_trump_pct', 'gov_18_schuette_pct', 'pres_20_trump_pct']):
            self.combined_df['rep_performance_16_18_20'] = (
                self.combined_df['pres_16_trump_pct'] + 
                self.combined_df['gov_18_schuette_pct'] + 
                self.combined_df['pres_20_trump_pct']
            ) / 3
            print("✓ Calculated Republican performance average 2016-2020")
    
    def analyze_bernie_bernie_connections(self):
        """Analyze connections between Bernie Sanders performance and other outcomes."""
        print("\n=== BERNIE SANDERS CONNECTION ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Find columns related to Bernie Sanders
        bernie_cols = [col for col in self.combined_df.columns if 'sanders' in col.lower() or 'bernie' in col.lower()]
        print(f"Found {len(bernie_cols)} Bernie-related columns: {bernie_cols}")
        
        # Analyze correlations with Bernie performance
        if 'prim_16_sanders_dem_pct' in self.combined_df.columns:
            bernie_16 = self.combined_df['prim_16_sanders_dem_pct']
            
            correlations = []
            for col in self.combined_df.columns:
                if col == 'prim_16_sanders_dem_pct' or 'county' in col:
                    continue
                if 'pct' in col and self.combined_df[col].dtype in ['float64', 'int64']:
                    corr = bernie_16.corr(self.combined_df[col])
                    if not pd.isna(corr):
                        correlations.append({
                            'variable': col,
                            'correlation': corr,
                            'abs_correlation': abs(corr)
                        })
            
            # Sort by absolute correlation
            correlations_df = pd.DataFrame(correlations).sort_values('abs_correlation', ascending=False)
            
            print("\nTop 15 correlations with Bernie Sanders 2016 primary performance:")
            print(correlations_df.head(15))
            
            # Analyze specific connections
            if 'pres_20_biden_pct' in self.combined_df.columns:
                bernie_biden_corr = bernie_16.corr(self.combined_df['pres_20_biden_pct'])
                print(f"\nBernie 2016 → Biden 2020 correlation: {bernie_biden_corr:.4f}")
                
                # Counties where Bernie won but Biden underperformed
                bernie_strong = self.combined_df[bernie_16 > bernie_16.median()]
                biden_underperformance = bernie_strong['pres_20_biden_pct'] < bernie_strong['pres_20_biden_pct'].median()
                print(f"Counties where Bernie was strong but Biden underperformed: {biden_underperformance.sum()}")
    
    def analyze_ted_cruz_connections(self):
        """Analyze Ted Cruz primary performance connections."""
        print("\n=== TED CRUZ CONNECTION ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        if 'prim_16_cruz_rep_pct' in self.combined_df.columns:
            cruz_16 = self.combined_df['prim_16_cruz_rep_pct']
            
            # Find correlations with Cruz performance
            correlations = []
            for col in self.combined_df.columns:
                if col == 'prim_16_cruz_rep_pct' or 'county' in col:
                    continue
                if 'pct' in col and self.combined_df[col].dtype in ['float64', 'int64']:
                    corr = cruz_16.corr(self.combined_df[col])
                    if not pd.isna(corr):
                        correlations.append({
                            'variable': col,
                            'correlation': corr,
                            'abs_correlation': abs(corr)
                        })
            
            correlations_df = pd.DataFrame(correlations).sort_values('abs_correlation', ascending=False)
            
            print("\nTop 15 correlations with Ted Cruz 2016 primary performance:")
            print(correlations_df.head(15))
            
            # Analyze Cruz vs. Trump general performance
            if 'pres_16_trump_pct' in self.combined_df.columns:
                cruz_trump_corr = cruz_16.corr(self.combined_df['pres_16_trump_pct'])
                print(f"\nCruz 2016 primary → Trump 2016 general correlation: {cruz_trump_corr:.4f}")
                
                # Counties where Cruz was strong but Trump underperformed
                cruz_strong = self.combined_df[cruz_16 > cruz_16.median()]
                trump_underperformance = cruz_strong['pres_16_trump_pct'] < cruz_strong['pres_16_trump_pct'].median()
                print(f"Counties where Cruz was strong but Trump underperformed: {trump_underperformance.sum()}")
    
    def analyze_rightward_shifts(self):
        """Analyze rightward shifts between election cycles."""
        print("\n=== RIGHTWARD SHIFT ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Calculate rightward shifts
        shifts = []
        
        if all(col in self.combined_df.columns for col in ['pres_16_trump_pct', 'pres_20_trump_pct']):
            trump_shift = self.combined_df['pres_20_trump_pct'] - self.combined_df['pres_16_trump_pct']
            shifts.append(('Trump 2016→2020', trump_shift))
            
            # Find counties with biggest rightward shifts
            biggest_rightward = trump_shift.nlargest(10)
            print(f"\nCounties with biggest rightward shift (Trump 2016→2020):")
            for county, shift in biggest_rightward.items():
                county_name = self.combined_df.loc[county, 'county']
                print(f"  {county_name}: {shift:.4f}")
        
        if all(col in self.combined_df.columns for col in ['gov_18_schuette_pct', 'gov_22_dixon_pct']):
            gov_shift = self.combined_df['gov_22_dixon_pct'] - self.combined_df['gov_18_schuette_pct']
            shifts.append(('Governor 2018→2022', gov_shift))
            
            # Find counties with biggest rightward shifts
            biggest_rightward = gov_shift.nlargest(10)
            print(f"\nCounties with biggest rightward shift (Governor 2018→2022):")
            for county, shift in biggest_rightward.items():
                county_name = self.combined_df.loc[county, 'county']
                print(f"  {county_name}: {shift:.4f}")
        
        # Analyze what predicts rightward shifts
        for shift_name, shift_data in shifts:
            print(f"\nAnalyzing predictors of {shift_name}:")
            
            correlations = []
            for col in self.combined_df.columns:
                if 'county' in col or shift_name.split()[0].lower() in col.lower():
                    continue
                if 'pct' in col and self.combined_df[col].dtype in ['float64', 'int64']:
                    corr = shift_data.corr(self.combined_df[col])
                    if not pd.isna(corr):
                        correlations.append({
                            'variable': col,
                            'correlation': corr,
                            'abs_correlation': abs(corr)
                        })
            
            if correlations:
                correlations_df = pd.DataFrame(correlations).sort_values('abs_correlation', ascending=False)
                print(f"Top 10 predictors of {shift_name}:")
                print(correlations_df.head(10))
    
    def analyze_voter_migration_patterns(self):
        """Analyze patterns of voter migration between parties and candidates."""
        print("\n=== VOTER MIGRATION PATTERN ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Create migration matrix
        migration_data = []
        
        # Bernie → Biden migration
        if all(col in self.combined_df.columns for col in ['prim_16_sanders_dem_pct', 'pres_20_biden_pct']):
            bernie_16 = self.combined_df['prim_16_sanders_dem_pct']
            biden_20 = self.combined_df['pres_20_biden_pct']
            
            # Calculate retention rate
            retention_rate = (bernie_16 * biden_20).sum() / (bernie_16 ** 2).sum()
            print(f"Bernie 2016 → Biden 2020 retention rate: {retention_rate:.4f}")
            
            # Find counties with high Bernie support but low Biden support
            high_bernie_low_biden = self.combined_df[
                (bernie_16 > bernie_16.quantile(0.75)) & 
                (biden_20 < biden_20.quantile(0.25))
            ]
            print(f"Counties with high Bernie support but low Biden support: {len(high_bernie_low_biden)}")
            
            if len(high_bernie_low_biden) > 0:
                print("Examples:")
                for _, row in high_bernie_low_biden.head(5).iterrows():
                    print(f"  {row['county']}: Bernie {row['prim_16_sanders_dem_pct']:.4f} → Biden {row['pres_20_biden_pct']:.4f}")
        
        # Trump 2016 → 2020 retention
        if all(col in self.combined_df.columns for col in ['pres_16_trump_pct', 'pres_20_trump_pct']):
            trump_16 = self.combined_df['pres_16_trump_pct']
            trump_20 = self.combined_df['pres_20_trump_pct']
            
            retention_rate = (trump_16 * trump_20).sum() / (trump_16 ** 2).sum()
            print(f"\nTrump 2016 → Trump 2020 retention rate: {retention_rate:.4f}")
            
            # Find counties where Trump gained support
            trump_gainers = self.combined_df[trump_20 > trump_16]
            print(f"Counties where Trump gained support: {len(trump_gainers)}")
            
            # Find counties where Trump lost support
            trump_losers = self.combined_df[trump_20 < trump_16]
            print(f"Counties where Trump lost support: {len(trump_losers)}")
    
    def perform_geographic_clustering(self):
        """Perform geographic clustering analysis to find regional patterns."""
        print("\n=== GEOGRAPHIC CLUSTERING ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Select percentage columns for clustering
        pct_cols = [col for col in self.combined_df.columns if 'pct' in col and self.combined_df[col].dtype in ['float64', 'int64']]
        
        if len(pct_cols) < 2:
            print("Not enough percentage columns for clustering")
            return
            
        # Prepare data for clustering
        cluster_data = self.combined_df[pct_cols].fillna(0)
        
        # Standardize the data
        scaler = StandardScaler()
        cluster_data_scaled = scaler.fit_transform(cluster_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        self.combined_df['cluster'] = kmeans.fit_predict(cluster_data_scaled)
        
        # Analyze clusters
        print(f"Created {kmeans.n_clusters} geographic clusters")
        
        for cluster_id in range(kmeans.n_clusters):
            cluster_counties = self.combined_df[self.combined_df['cluster'] == cluster_id]
            print(f"\nCluster {cluster_id}: {len(cluster_counties)} counties")
            
            # Show top counties in this cluster
            print("Sample counties:", ", ".join(cluster_counties['county'].head(5).tolist()))
            
            # Show cluster characteristics
            cluster_means = cluster_counties[pct_cols].mean()
            top_characteristics = cluster_means.nlargest(5)
            print("Top characteristics:")
            for var, mean_val in top_characteristics.items():
                print(f"  {var}: {mean_val:.4f}")
    
    def generate_correlation_matrix(self):
        """Generate comprehensive correlation matrix."""
        print("\n=== COMPREHENSIVE CORRELATION ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Select percentage columns
        pct_cols = [col for col in self.combined_df.columns if 'pct' in col and self.combined_df[col].dtype in ['float64', 'int64']]
        
        if len(pct_cols) < 2:
            print("Not enough percentage columns for correlation analysis")
            return
            
        # Calculate correlation matrix
        corr_matrix = self.combined_df[pct_cols].corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(pct_cols)):
            for j in range(i+1, len(pct_cols)):
                corr_val = corr_matrix.iloc[i, j]
                if not pd.isna(corr_val):
                    correlations.append({
                        'var1': pct_cols[i],
                        'var2': pct_cols[j],
                        'correlation': corr_val,
                        'abs_correlation': abs(corr_val)
                    })
        
        # Sort by absolute correlation
        correlations_df = pd.DataFrame(correlations).sort_values('abs_correlation', ascending=False)
        
        print(f"\nTop 20 strongest correlations:")
        print(correlations_df.head(20))
        
        # Find surprising correlations (high correlation between seemingly unrelated variables)
        print(f"\nMost surprising correlations (high correlation between different election cycles):")
        surprising_corrs = correlations_df[
            (correlations_df['abs_correlation'] > 0.7) &
            (
                (correlations_df['var1'].str.contains('16') & correlations_df['var2'].str.contains('20')) |
                (correlations_df['var1'].str.contains('20') & correlations_df['var2'].str.contains('16')) |
                (correlations_df['var1'].str.contains('18') & correlations_df['var2'].str.contains('22')) |
                (correlations_df['var2'].str.contains('18') & correlations_df['var1'].str.contains('22'))
            )
        ]
        print(surprising_corrs.head(10))
    
    def run_complete_analysis(self):
        """Run the complete meta-analysis."""
        print("=" * 60)
        print("ELECTION META-ANALYSIS: COMPREHENSIVE VOTER BEHAVIOR ANALYSIS")
        print("=" * 60)
        
        # Combine all data
        self.combine_all_data()
        
        if self.combined_df is None:
            print("Failed to combine data. Exiting.")
            return
        
        # Calculate voter shifts
        self.calculate_voter_shifts()
        
        # Run all analyses
        self.analyze_bernie_bernie_connections()
        self.analyze_ted_cruz_connections()
        self.analyze_rightward_shifts()
        self.analyze_voter_migration_patterns()
        self.perform_geographic_clustering()
        self.generate_correlation_matrix()
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        
        # Save combined data
        self.combined_df.to_feather("election_meta_analysis.ft")
        print("Saved combined data to election_meta_analysis.ft")
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(self.combined_df)}")
        print(f"  Variables: {len(self.combined_df.columns)}")
        print(f"  Memory usage: {self.combined_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

def main():
    """Main function to run the analysis."""
    analyzer = ElectionMetaAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
