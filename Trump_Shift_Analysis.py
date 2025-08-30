#!/usr/bin/env python3
"""
Trump Support Shift Analysis: 2016->2020->2024 vs. Secretary of State & Propositions

This script analyzes the relationship between Trump support shifts across election cycles
and support for Secretary of State candidates and progressive propositions.

Key Analysis:
- Trump support shifts: 2016->2020->2024 (using available data)
- Secretary of State support patterns
- Proposition support correlations
- Voter behavior shift analysis

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (18, 14)

class TrumpShiftAnalyzer:
    """Analyzer for Trump support shifts and their relationships."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.data = {}
        self.combined_df = None
        self.models = {}
        self.load_all_data()
        
    def load_all_data(self):
        """Load all available election data files."""
        print("Loading election data for Trump shift analysis...")
        
        # Load 2016 data
        try:
            with open("2016.general.json", "r") as fp:
                self.data['2016_general'] = json.load(fp)
            print("✓ Loaded 2016 general election data")
        except FileNotFoundError:
            print("✗ 2016 general election data not found")
            
        # Load 2020 data
        try:
            with open("2020.general.all.json", "r") as fp:
                self.data['2020_general_all'] = json.load(fp)
            print("✓ Loaded 2020 general all data")
        except FileNotFoundError:
            print("✗ 2020 general all data not found")
            
        # Load 2022 data
        try:
            with open("2022.json", "r") as fp:
                self.data['2022'] = json.load(fp)
            print("✓ Loaded 2022 data")
        except FileNotFoundError:
            print("✗ 2022 data not found")
            
        # Load existing feather files for additional data
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
    
    def process_2016_presidential(self):
        """Process 2016 presidential election data."""
        if '2016_general' not in self.data:
            return None
            
        print("Processing 2016 presidential data...")
        
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
            print("No presidential race found in 2016 data")
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
    
    def process_2020_proposals(self):
        """Process 2020 proposals (Props 1 & 2)."""
        if '2020_general_all' not in self.data:
            return None
            
        print("Processing 2020 proposals data...")
        
        races = self.data['2020_general_all']
        proposals = [race for race in races if race.get('office') == 'Proposal']
        
        data = []
        for proposal in proposals:
            prop_num = proposal.get('race_name', '').split(':')[0].split()[-1]
            print(f"Processing {proposal.get('race_name', 'Unknown')}")
            
            for county in proposal["counties"]:
                row = {"county": county["name"]}
                total = 0
                
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        if "yes" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_yes_pct"] = votes / county.get("total_votes", votes) if county.get("total_votes", 0) > 0 else 0
                        elif "no" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_no_pct"] = votes / county.get("total_votes", votes) if county.get("total_votes", 0) > 0 else 0
                
                data.append(row)
        
        return pd.DataFrame(data)
    
    def extract_secretary_of_state_data(self):
        """Extract Secretary of State data from existing files."""
        print("Extracting Secretary of State data...")
        
        sos_data = None
        
        # Check election meta analysis for SOS data
        if 'election_meta' in self.data:
            df = self.data['election_meta']
            sos_cols = [col for col in df.columns if 'sos' in col.lower() and 'benson' in col.lower()]
            if sos_cols:
                print(f"Found SOS columns in election meta data: {sos_cols}")
                sos_data = df[['county'] + sos_cols].copy()
                return sos_data
        
        # If no SOS data found, create placeholder
        print("No Secretary of State data found in existing files")
        print("Note: Jocelyn Benson (D) was Secretary of State in 2022")
        print("This data would be valuable for analysis but is not currently available")
        
        return None
    
    def extract_prop3_data(self):
        """Extract Prop 3 data from existing files."""
        print("Extracting Prop 3 data...")
        
        prop3_data = None
        
        # Check election meta analysis for Prop 3 data
        if 'election_meta' in self.data:
            df = self.data['election_meta']
            prop3_cols = [col for col in df.columns if 'prop3' in col.lower()]
            if prop3_cols:
                print(f"Found Prop 3 columns in election meta data: {prop3_cols}")
                prop3_data = df[['county'] + prop3_cols].copy()
                return prop3_data
        
        print("No Prop 3 data found in existing files")
        return None
    
    def combine_all_data(self):
        """Combine all processed data into a single DataFrame."""
        print("Combining all data for Trump shift analysis...")
        
        dfs = []
        
        # Process each dataset
        df_2016_pres = self.process_2016_presidential()
        if df_2016_pres is not None:
            dfs.append(df_2016_pres)
            print("✓ Processed 2016 presidential data")
            
        df_2020_pres = self.process_2020_presidential()
        if df_2020_pres is not None:
            dfs.append(df_2020_pres)
            print("✓ Processed 2020 presidential data")
            
        df_2020_props = self.process_2020_proposals()
        if df_2020_props is not None:
            dfs.append(df_2020_props)
            print("✓ Processed 2020 proposals data")
            
        df_sos = self.extract_secretary_of_state_data()
        if df_sos is not None:
            dfs.append(df_sos)
            print("✓ Processed Secretary of State data")
            
        df_prop3 = self.extract_prop3_data()
        if df_prop3 is not None:
            dfs.append(df_prop3)
            print("✓ Processed Prop 3 data")
        
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
            # This assumes similar voter behavior patterns
            self.combined_df['trump_20_to_24_proxy_shift'] = self.combined_df['trump_16_to_20_shift']
            self.combined_df['trump_20_to_24_proxy_pct_change'] = self.combined_df['trump_16_to_20_pct_change']
            print("✓ Created proxy for 2020->2024 Trump shift (using 2016->2020 pattern)")
        
        # Show available columns
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        print(f"Available shift variables: {shift_cols}")
    
    def analyze_trump_shift_relationships(self):
        """Analyze relationships between Trump shifts and other variables."""
        print("\n=== ANALYZING TRUMP SHIFT RELATIONSHIPS ===")
        
        if self.combined_df is None:
            return
            
        # Find all available variables for analysis
        analysis_vars = []
        
        # Proposition variables
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
        analysis_vars.extend(prop_cols)
        
        # Secretary of State variables
        sos_cols = [col for col in self.combined_df.columns if 'sos' in col.lower() and 'pct' in col]
        analysis_vars.extend(sos_cols)
        
        # Trump shift variables
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        analysis_vars.extend(shift_cols)
        
        print(f"Variables available for analysis: {analysis_vars}")
        
        if not analysis_vars:
            print("No variables found for analysis")
            return
        
        # Analyze relationships between Trump shifts and other variables
        for shift_var in shift_cols:
            print(f"\n{'='*60}")
            print(f"ANALYZING: {shift_var}")
            print(f"{'='*60}")
            
            for analysis_var in analysis_vars:
                if analysis_var == shift_var:
                    continue
                    
                if shift_var in self.combined_df.columns and analysis_var in self.combined_df.columns:
                    # Prepare data
                    X = self.combined_df[analysis_var].values.reshape(-1, 1)
                    y = self.combined_df[shift_var].values
                    
                    # Remove NaN values
                    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                    X_clean = X[mask]
                    y_clean = y[mask]
                    
                    if len(X_clean) < 10:
                        continue
                    
                    print(f"\n--- {analysis_var} vs. {shift_var} ---")
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
                    self.models[f"{analysis_var}_vs_{shift_var}"] = lr_model
    
    def create_trump_shift_visualizations(self):
        """Create comprehensive visualizations for Trump shift analysis."""
        print("\n=== CREATING TRUMP SHIFT VISUALIZATIONS ===")
        
        if self.combined_df is None:
            return
            
        # Find available variables
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
        sos_cols = [col for col in self.combined_df.columns if 'sos' in col.lower() and 'pct' in col]
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"Proposition variables: {prop_cols}")
        print(f"Secretary of State variables: {sos_cols}")
        print(f"Trump shift variables: {shift_cols}")
        
        if not shift_cols:
            print("No Trump shift variables found for plotting")
            return
        
        # Create subplots
        n_plots = len(prop_cols) + len(sos_cols)
        if n_plots == 0:
            print("No variables found for plotting")
            return
            
        fig, axes = plt.subplots(2, max(1, n_plots//2), figsize=(6*max(1, n_plots//2), 12))
        if n_plots == 1:
            axes = axes.reshape(2, 1)
        elif n_plots <= 2:
            axes = axes.reshape(2, 1)
        
        fig.suptitle('Trump Support Shifts vs. Secretary of State & Proposition Support', 
                     fontsize=16, fontweight='bold')
        
        plot_idx = 0
        
        # Plot proposition relationships
        for prop_col in prop_cols:
            if plot_idx >= n_plots:
                break
                
            for shift_col in shift_cols:
                if shift_col in self.combined_df.columns and prop_col in self.combined_df.columns:
                    # Get data
                    x_data = self.combined_df[prop_col]
                    y_data = self.combined_df[shift_col]
                    
                    # Remove NaN values
                    mask = ~(np.isnan(x_data) | np.isnan(y_data))
                    x_clean = x_data[mask]
                    y_clean = y_data[mask]
                    
                    if len(x_clean) > 0:
                        # Top plot: Scatter with regression
                        ax_top = axes[0, plot_idx % (n_plots//2)] if n_plots > 2 else axes[0, 0]
                        
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
                        prop_name = prop_col.replace('_', ' ').replace('pct', '').title()
                        shift_name = shift_col.replace('_', ' ').title()
                        ax_top.set_xlabel(f'{prop_name} Support (%)')
                        ax_top.set_ylabel(f'{shift_name}')
                        ax_top.set_title(f'{prop_name} vs. {shift_name}')
                        ax_top.grid(True, alpha=0.3)
                        
                        # Bottom plot: Residuals
                        ax_bottom = axes[1, plot_idx % (n_plots//2)] if n_plots > 2 else axes[1, 0]
                        
                        if len(x_clean) > 1 and f"{prop_col}_vs_{shift_col}" in self.models:
                            model = self.models[f"{prop_col}_vs_{shift_col}"]
                            y_pred = model.predict(x_clean.values.reshape(-1, 1))
                            residuals = y_clean.values - y_pred
                            
                            ax_bottom.scatter(y_pred, residuals, alpha=0.6, s=50, color='orange')
                            ax_bottom.axhline(y=0, color='red', linestyle='--', alpha=0.8)
                            ax_bottom.set_xlabel('Predicted Shift')
                            ax_bottom.set_ylabel('Residuals')
                            ax_bottom.set_title(f'{prop_name} - Residual Plot')
                            ax_bottom.grid(True, alpha=0.3)
                        
                        plot_idx += 1
                        break
        
        # Plot Secretary of State relationships
        for sos_col in sos_cols:
            if plot_idx >= n_plots:
                break
                
            for shift_col in shift_cols:
                if shift_col in self.combined_df.columns and sos_col in self.combined_df.columns:
                    # Similar plotting logic for SOS
                    x_data = self.combined_df[sos_col]
                    y_data = self.combined_df[shift_col]
                    
                    mask = ~(np.isnan(x_data) | np.isnan(y_data))
                    x_clean = x_data[mask]
                    y_clean = y_data[mask]
                    
                    if len(x_clean) > 0:
                        ax_top = axes[0, plot_idx % (n_plots//2)] if n_plots > 2 else axes[0, 0]
                        
                        ax_top.scatter(x_clean, y_clean, alpha=0.6, s=50, color='green')
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            x_range = np.linspace(x_clean.min(), x_clean.max(), 100)
                            ax_top.plot(x_range, p(x_range), "r--", alpha=0.8, linewidth=2)
                            
                            correlation = np.corrcoef(x_clean, y_clean)[0, 1]
                            ax_top.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax_top.transAxes, 
                                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                        
                        sos_name = sos_col.replace('_', ' ').replace('pct', '').title()
                        shift_name = shift_col.replace('_', ' ').title()
                        ax_top.set_xlabel(f'{sos_name} Support (%)')
                        ax_top.set_ylabel(f'{shift_name}')
                        ax_top.set_title(f'{sos_name} vs. {shift_name}')
                        ax_top.grid(True, alpha=0.3)
                        
                        plot_idx += 1
                        break
        
        plt.tight_layout()
        plt.savefig('trump_shift_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Trump shift analysis plot saved as 'trump_shift_analysis.png'")
    
    def run_complete_analysis(self):
        """Run the complete Trump shift analysis."""
        print("=" * 80)
        print("TRUMP SUPPORT SHIFT ANALYSIS: 2016->2020->2024")
        print("vs. Secretary of State & Proposition Support")
        print("=" * 80)
        
        # Combine all data
        self.combine_all_data()
        
        if self.combined_df is None:
            print("Failed to combine data. Exiting.")
            return
        
        # Calculate Trump shifts
        self.calculate_trump_shifts()
        
        # Analyze relationships
        self.analyze_trump_shift_relationships()
        
        # Create visualizations
        self.create_trump_shift_visualizations()
        
        print("\n" + "=" * 80)
        print("TRUMP SHIFT ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(self.combined_df)}")
        print(f"  Variables: {len(self.combined_df.columns)}")
        
        # Show available variables
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower()]
        sos_cols = [col for col in self.combined_df.columns if 'sos' in col.lower()]
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"  Proposition variables: {len(prop_cols)}")
        print(f"  Secretary of State variables: {len(sos_cols)}")
        print(f"  Trump shift variables: {len(shift_cols)}")
        
        print(f"\nKey Findings:")
        if shift_cols:
            print(f"  - Trump support shifts calculated: {shift_cols}")
        if prop_cols:
            print(f"  - Proposition support available: {prop_cols}")
        if sos_cols:
            print(f"  - Secretary of State data available: {sos_cols}")

def main():
    """Main function to run the Trump shift analysis."""
    analyzer = TrumpShiftAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
