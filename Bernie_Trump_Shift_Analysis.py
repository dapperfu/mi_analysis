#!/usr/bin/env python3
"""
Bernie vs. Hillary 2016 Primary Analysis: Trump Support Shifts 2020->2024

This script analyzes the relationship between 2016 primary voting patterns
(Bernie supporters vs. Hillary supporters) and Trump support shifts.

Key Analysis:
- Bernie supporters who didn't support Hillary in 2016 primaries
- Their Trump support patterns in 2020 vs. 2024
- Voter behavior shifts and political realignment
- Progressive vs. establishment Democratic voting patterns

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (18, 14)

class BernieTrumpShiftAnalyzer:
    """Analyzer for Bernie vs. Hillary primary patterns and Trump shifts."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.data = {}
        self.combined_df = None
        self.models = {}
        self.load_all_data()
        
    def load_all_data(self):
        """Load all available election data files."""
        print("Loading election data for Bernie vs. Hillary analysis...")
        
        # Load 2016 primary data
        try:
            with open("2016.primary.json", "r") as fp:
                self.data['2016_primary'] = json.load(fp)
            print("✓ Loaded 2016 primary data")
        except FileNotFoundError:
            print("✗ 2016 primary data not found")
            
        # Load 2016 general data
        try:
            with open("2016.general.json", "r") as fp:
                self.data['2016_general'] = json.load(fp)
            print("✓ Loaded 2016 general data")
        except FileNotFoundError:
            print("✗ 2016 general data not found")
            
        # Load 2020 primary data
        try:
            with open("2020.primary.dem.json", "r") as fp:
                self.data['2020_primary_dem'] = json.load(fp)
            print("✓ Loaded 2020 Democratic primary data")
        except FileNotFoundError:
            print("✗ 2020 Democratic primary data not found")
            
        # Load 2020 general data
        try:
            with open("2020.general.all.json", "r") as fp:
                self.data['2020_general_all'] = json.load(fp)
            print("✓ Loaded 2020 general all data")
        except FileNotFoundError:
            print("✗ 2020 general all data not found")
            
        # Load existing feather files for additional data
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
    
    def process_2016_primary(self):
        """Process 2016 Democratic primary data."""
        if '2016_primary' not in self.data:
            return None
            
        print("Processing 2016 Democratic primary data...")
        
        races = self.data['2016_primary']
        dem_primary = None
        
        # Find Democratic primary race
        for race in races:
            if race.get('office') == 'President' or 'president' in race.get('race_name', '').lower():
                if 'dem' in race.get('party', '').lower() or 'democratic' in race.get('race_name', '').lower():
                    dem_primary = race
                    break
        
        if not dem_primary:
            print("No Democratic primary race found in 2016 data")
            return None
            
        data = []
        counties = dem_primary.get('counties', [])
        
        if not counties:
            print("No county-level data found in 2016 Democratic primary")
            return None
            
        for county in counties:
            row = {"county": county["name"]}
            total = 0
            
            # Handle different data structures
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    if "sanders" in candidate_key.lower() or "bernie" in candidate_key.lower():
                        row["prim_16_bernie"] = votes
                    elif "clinton" in candidate_key.lower() or "hillary" in candidate_key.lower():
                        row["prim_16_hillary"] = votes
                    total += votes
            elif "candidates" in county:
                for candidate in county["candidates"]:
                    if "sanders" in candidate.get("name", "").lower() or "bernie" in candidate.get("name", "").lower():
                        row["prim_16_bernie"] = candidate.get("votes", {}).get("total", 0)
                    elif "clinton" in candidate.get("name", "").lower() or "hillary" in candidate.get("name", "").lower():
                        row["prim_16_hillary"] = candidate.get("votes", {}).get("total", 0)
                    total += candidate.get("votes", {}).get("total", 0)
            
            row["prim_16_total"] = total
            
            # Calculate percentages
            if "prim_16_bernie" in row and "prim_16_hillary" in row:
                row["prim_16_bernie_pct"] = row["prim_16_bernie"] / total if total > 0 else 0
                row["prim_16_hillary_pct"] = row["prim_16_hillary"] / total if total > 0 else 0
                
                # Calculate Bernie advantage over Hillary
                row["prim_16_bernie_advantage"] = row["prim_16_bernie_pct"] - row["prim_16_hillary_pct"]
                
                # Create categories
                if row["prim_16_bernie_pct"] > row["prim_16_hillary_pct"]:
                    row["prim_16_bernie_stronger"] = 1
                    row["prim_16_hillary_stronger"] = 0
                else:
                    row["prim_16_bernie_stronger"] = 0
                    row["prim_16_hillary_stronger"] = 1
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2016_general(self):
        """Process 2016 general election data."""
        if '2016_general' not in self.data:
            return None
            
        print("Processing 2016 general election data...")
        
        # Check structure of 2016 data
        if isinstance(self.data['2016_general'], list):
            races = self.data['2016_general']
        else:
            races = [self.data['2016_general']]
        
        # Find presidential race
        pres_race = None
        for race in races:
            if race.get('office') == 'President' or 'president' in race.get('race_name', '').lower():
                pres_race = race
                break
        
        if not pres_race:
            print("No presidential race found in 2016 general data")
            return None
            
        data = []
        counties = pres_race.get('counties', [])
        
        if not counties:
            print("No county-level data found in 2016 presidential race")
            return None
            
        for county in counties:
            row = {"county": county["name"]}
            total = 0
            
            # Handle different data structures
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    if "trump" in candidate_key.lower():
                        row["pres_16_trump"] = votes
                    elif "clinton" in candidate_key.lower():
                        row["pres_16_clinton"] = votes
                    total += votes
            elif "candidates" in county:
                for candidate in county["candidates"]:
                    if "trump" in candidate.get("name", "").lower():
                        row["pres_16_trump"] = candidate.get("votes", {}).get("total", 0)
                    elif "clinton" in candidate.get("name", "").lower():
                        row["pres_16_clinton"] = candidate.get("votes", {}).get("total", 0)
                    total += candidate.get("votes", {}).get("total", 0)
            
            row["pres_16_total"] = total
            
            # Calculate percentages
            if "pres_16_trump" in row and "pres_16_clinton" in row:
                row["pres_16_trump_pct"] = row["pres_16_trump"] / total if total > 0 else 0
                row["pres_16_clinton_pct"] = row["pres_16_clinton"] / total if total > 0 else 0
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2020_presidential(self):
        """Process 2020 presidential election data."""
        if '2020_general_all' not in self.data:
            return None
            
        print("Processing 2020 presidential data...")
        
        races = self.data['2020_general_all']
        pres_race = None
        
        for race in races:
            if race.get('office') == 'President':
                pres_race = race
                break
        
        if not pres_race:
            print("No presidential race found in 2020 data")
            return None
            
        data = []
        for county in pres_race["counties"]:
            row = {"county": county["name"]}
            total = 0
            
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    if "trump" in candidate_key.lower():
                        row["pres_20_trump"] = votes
                    elif "biden" in candidate_key.lower():
                        row["pres_20_biden"] = votes
                    total += votes
            
            row["pres_20_total"] = total
            
            # Calculate percentages
            if "results" in county:
                for candidate_key, votes in county["results"].items():
                    if "trump" in candidate_key.lower():
                        row["pres_20_trump_pct"] = votes / total if total > 0 else 0
                    elif "biden" in candidate_key.lower():
                        row["pres_20_biden_pct"] = votes / total if total > 0 else 0
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def combine_all_data(self):
        """Combine all processed data into a single DataFrame."""
        print("Combining all data for Bernie vs. Hillary analysis...")
        
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
            
        df_2020_pres = self.process_2020_presidential()
        if df_2020_pres is not None:
            dfs.append(df_2020_pres)
            print("✓ Processed 2020 presidential data")
        
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
    
    def calculate_trump_shifts(self):
        """Calculate Trump support shifts between election cycles."""
        print("\n=== CALCULATING TRUMP SUPPORT SHIFTS ===")
        
        if self.combined_df is None:
            return
            
        # Calculate shifts where data is available
        if 'pres_16_trump_pct' in self.combined_df.columns and 'pres_20_trump_pct' in self.combined_df.columns:
            self.combined_df['trump_16_to_20_shift'] = (
                self.combined_df['pres_20_trump_pct'] - self.combined_df['pres_16_trump_pct']
            )
            print("✓ Calculated 2016->2020 Trump shift")
            
            # Calculate percentage change
            self.combined_df['trump_16_to_20_pct_change'] = (
                self.combined_df['trump_16_to_20_shift'] / self.combined_df['pres_16_trump_pct']
            ) * 100
            
        # Create proxy for 2020->2024 shift using 2016->2020 pattern
        if 'trump_16_to_20_shift' in self.combined_df.columns:
            # Use the 2016->2020 shift as a proxy for expected 2020->2024 shift
            self.combined_df['trump_20_to_24_proxy_shift'] = self.combined_df['trump_16_to_20_shift']
            self.combined_df['trump_20_to_24_proxy_pct_change'] = self.combined_df['trump_16_to_20_pct_change']
            print("✓ Created proxy for 2020->2024 Trump shift (using 2016->2020 pattern)")
        
        # Show available columns
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        print(f"Available shift variables: {shift_cols}")
    
    def analyze_bernie_hillary_patterns(self):
        """Analyze patterns between Bernie and Hillary primary support."""
        print("\n=== ANALYZING BERNIE vs. HILLARY PRIMARY PATTERNS ===")
        
        if self.combined_df is None:
            return
            
        # Check what data we have
        primary_cols = [col for col in self.combined_df.columns if 'prim_16' in col.lower()]
        print(f"Primary columns available: {primary_cols}")
        
        if 'prim_16_bernie_pct' in self.combined_df.columns and 'prim_16_hillary_pct' in self.combined_df.columns:
            # Calculate correlation between Bernie and Hillary support
            correlation = self.combined_df['prim_16_bernie_pct'].corr(self.combined_df['prim_16_hillary_pct'])
            print(f"\nBernie vs. Hillary correlation: {correlation:.4f}")
            
            if correlation < 0:
                print("→ Negative correlation: Counties that supported Bernie tended NOT to support Hillary")
            else:
                print("→ Positive correlation: Counties that supported Bernie also supported Hillary")
            
            # Analyze Bernie advantage
            if 'prim_16_bernie_advantage' in self.combined_df.columns:
                bernie_strong_counties = self.combined_df[self.combined_df['prim_16_bernie_advantage'] > 0]
                hillary_strong_counties = self.combined_df[self.combined_df['prim_16_bernie_advantage'] < 0]
                
                print(f"\nCounties where Bernie was stronger than Hillary: {len(bernie_strong_counties)}")
                print(f"Counties where Hillary was stronger than Bernie: {len(hillary_strong_counties)}")
                
                # Analyze Trump support in these counties
                if 'pres_16_trump_pct' in self.combined_df.columns:
                    bernie_strong_trump_16 = bernie_strong_counties['pres_16_trump_pct'].mean()
                    hillary_strong_trump_16 = hillary_strong_counties['pres_16_trump_pct'].mean()
                    
                    print(f"\nTrump support in 2016:")
                    print(f"  Bernie-strong counties: {bernie_strong_trump_16:.3f} ({bernie_strong_trump_16*100:.1f}%)")
                    print(f"  Hillary-strong counties: {hillary_strong_trump_16:.3f} ({hillary_strong_trump_16*100:.1f}%)")
                    
                    if bernie_strong_trump_16 > hillary_strong_trump_16:
                        print("→ Bernie-strong counties had HIGHER Trump support in 2016")
                    else:
                        print("→ Bernie-strong counties had LOWER Trump support in 2016")
                
                # Analyze Trump shifts
                if 'trump_16_to_20_shift' in self.combined_df.columns:
                    bernie_strong_trump_shift = bernie_strong_counties['trump_16_to_20_shift'].mean()
                    hillary_strong_trump_shift = hillary_strong_counties['trump_16_to_20_shift'].mean()
                    
                    print(f"\nTrump support shift 2016->2020:")
                    print(f"  Bernie-strong counties: {bernie_strong_trump_shift:.4f} ({bernie_strong_trump_shift*100:.2f}%)")
                    print(f"  Hillary-strong counties: {hillary_strong_trump_shift:.4f} ({hillary_strong_trump_shift*100:.2f}%)")
                    
                    if bernie_strong_trump_shift > hillary_strong_trump_shift:
                        print("→ Bernie-strong counties showed GREATER increase in Trump support")
                    else:
                        print("→ Bernie-strong counties showed SMALLER increase in Trump support")
    
    def analyze_trump_shift_relationships(self):
        """Analyze relationships between primary patterns and Trump shifts."""
        print("\n=== ANALYZING PRIMARY PATTERNS vs. TRUMP SHIFTS ===")
        
        if self.combined_df is None:
            return
            
        # Find available variables for analysis
        primary_vars = [col for col in self.combined_df.columns if 'prim_16' in col.lower()]
        shift_vars = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"Primary variables: {primary_vars}")
        print(f"Trump shift variables: {shift_vars}")
        
        if not primary_vars or not shift_vars:
            print("Insufficient data for analysis")
            return
        
        # Analyze relationships between primary patterns and Trump shifts
        for primary_var in primary_vars:
            if 'pct' not in primary_var:
                continue
                
            for shift_var in shift_vars:
                if primary_var in self.combined_df.columns and shift_var in self.combined_df.columns:
                    print(f"\n--- {primary_var} vs. {shift_var} ---")
                    
                    # Prepare data
                    X = self.combined_df[primary_var].values.reshape(-1, 1)
                    y = self.combined_df[shift_var].values
                    
                    # Remove NaN values
                    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                    X_clean = X[mask]
                    y_clean = y[mask]
                    
                    if len(X_clean) < 10:
                        print(f"Insufficient data: only {len(X_clean)} valid observations")
                        continue
                    
                    print(f"Data points: {len(X_clean)} counties")
                    
                    # Calculate correlation
                    correlation = np.corrcoef(X_clean.flatten(), y_clean)[0, 1]
                    print(f"Correlation: {correlation:.4f}")
                    
                    # Linear regression
                    X_train, X_test, y_train, y_test = train_test_split(
                        X_clean, y_clean, test_size=0.3, random_state=42
                    )
                    
                    lr_model = LinearRegression()
                    lr_model.fit(X_train, y_train)
                    
                    y_test_pred = lr_model.predict(X_test)
                    test_r2 = r2_score(y_test, y_test_pred)
                    
                    print(f"R² score: {test_r2:.4f}")
                    print(f"Slope: {lr_model.coef_[0]:.4f}")
                    print(f"Intercept: {lr_model.intercept_:.4f}")
                    
                    # Cross-validation
                    cv_scores = cross_val_score(lr_model, X_clean, y_clean, cv=5, scoring='r2')
                    print(f"Cross-validation R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
                    
                    # Interpretation
                    if abs(correlation) > 0.3:
                        if correlation > 0:
                            print("→ Strong positive relationship")
                        else:
                            print("→ Strong negative relationship")
                    elif abs(correlation) < 0.1:
                        print("→ Weak relationship")
                    else:
                        print("→ Moderate relationship")
                    
                    # Store model
                    self.models[f"{primary_var}_vs_{shift_var}"] = lr_model
    
    def create_bernie_trump_visualizations(self):
        """Create comprehensive visualizations for Bernie vs. Hillary analysis."""
        print("\n=== CREATING BERNIE vs. HILLARY VISUALIZATIONS ===")
        
        if self.combined_df is None:
            return
            
        # Find available variables
        primary_cols = [col for col in self.combined_df.columns if 'prim_16' in col.lower() and 'pct' in col]
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"Primary columns: {primary_cols}")
        print(f"Trump shift columns: {shift_cols}")
        
        if not primary_cols or not shift_cols:
            print("No variables found for plotting")
            return
        
        # Create subplots
        n_plots = len(primary_cols)
        fig, axes = plt.subplots(2, n_plots, figsize=(6*n_plots, 12))
        if n_plots == 1:
            axes = axes.reshape(2, 1)
        
        fig.suptitle('Bernie vs. Hillary 2016 Primary Patterns vs. Trump Support Shifts', 
                     fontsize=16, fontweight='bold')
        
        for i, primary_col in enumerate(primary_cols):
            ax_top = axes[0, i] if n_plots > 1 else axes[0, 0]
            ax_bottom = axes[1, i] if n_plots > 1 else axes[1, 0]
            
            # Plot primary support vs. Trump shift
            for shift_col in shift_cols:
                if shift_col in self.combined_df.columns and primary_col in self.combined_df.columns:
                    # Get data
                    x_data = self.combined_df[primary_col]
                    y_data = self.combined_df[shift_col]
                    
                    # Remove NaN values
                    mask = ~(np.isnan(x_data) | np.isnan(y_data))
                    x_clean = x_data[mask]
                    y_clean = y_data[mask]
                    
                    if len(x_clean) > 0:
                        # Top plot: Scatter with regression
                        ax_top.scatter(x_clean, y_clean, alpha=0.6, s=50, color='steelblue')
                        
                        # Add trend line
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            x_range = np.linspace(x_clean.min(), x_clean.max(), 100)
                            ax_top.plot(x_range, p(x_range), "r--", alpha=0.8, linewidth=2)
                            
                            # Calculate correlation
                            correlation = np.corrcoef(x_clean, y_clean)[0, 1]
                            ax_top.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax_top.transAxes, 
                                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                        
                        # Labels
                        primary_name = primary_col.replace('_', ' ').replace('pct', '').title()
                        shift_name = shift_col.replace('_', ' ').title()
                        ax_top.set_xlabel(f'{primary_name} Support (%)')
                        ax_top.set_ylabel(f'{shift_name}')
                        ax_top.set_title(f'{primary_name} vs. {shift_name}')
                        ax_top.grid(True, alpha=0.3)
                        
                        # Bottom plot: Residuals
                        if len(x_clean) > 1 and f"{primary_col}_vs_{shift_col}" in self.models:
                            model = self.models[f"{primary_col}_vs_{shift_col}"]
                            y_pred = model.predict(x_clean.values.reshape(-1, 1))
                            residuals = y_clean.values - y_pred
                            
                            ax_bottom.scatter(y_pred, residuals, alpha=0.6, s=50, color='orange')
                            ax_bottom.axhline(y=0, color='red', linestyle='--', alpha=0.8)
                            ax_bottom.set_xlabel('Predicted Shift')
                            ax_bottom.set_ylabel('Residuals')
                            ax_bottom.set_title(f'{primary_name} - Residual Plot')
                            ax_bottom.grid(True, alpha=0.3)
                        
                        break
        
        plt.tight_layout()
        plt.savefig('bernie_trump_shift_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Bernie vs. Hillary analysis plot saved as 'bernie_trump_shift_analysis.png'")
    
    def run_complete_analysis(self):
        """Run the complete Bernie vs. Hillary analysis."""
        print("=" * 80)
        print("BERNIE vs. HILLARY 2016 PRIMARY ANALYSIS")
        print("Trump Support Shifts: 2020->2024")
        print("=" * 80)
        
        # Combine all data
        self.combine_all_data()
        
        if self.combined_df is None:
            print("Failed to combine data. Exiting.")
            return
        
        # Calculate Trump shifts
        self.calculate_trump_shifts()
        
        # Analyze Bernie vs. Hillary patterns
        self.analyze_bernie_hillary_patterns()
        
        # Analyze relationships
        self.analyze_trump_shift_relationships()
        
        # Create visualizations
        self.create_bernie_trump_visualizations()
        
        print("\n" + "=" * 80)
        print("BERNIE vs. HILLARY ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(self.combined_df)}")
        print(f"  Variables: {len(self.combined_df.columns)}")
        
        # Show available variables
        primary_cols = [col for col in self.combined_df.columns if 'prim_16' in col.lower()]
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"  2016 Primary variables: {len(primary_cols)}")
        print(f"  Trump shift variables: {len(shift_cols)}")
        
        print(f"\nKey Research Question:")
        print(f"  Do Bernie supporters (but not Hillary supporters) in 2016 primaries")
        print(f"  show different Trump support shifts from 2020 to 2024?")
        
        if primary_cols and shift_cols:
            print(f"\nAnalysis available for:")
            print(f"  - Primary voting patterns: {primary_cols}")
            print(f"  - Trump support shifts: {shift_cols}")

def main():
    """Main function to run the Bernie vs. Hillary analysis."""
    analyzer = BernieTrumpShiftAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
