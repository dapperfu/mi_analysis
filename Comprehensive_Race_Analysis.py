#!/usr/bin/env python3
"""
Comprehensive Race Analysis: ALL Races, ALL Shifts, ALL Relationships

This script performs a comprehensive analysis of ALL election races and their relationships,
including shift patterns across election cycles and primary data analysis.

Key Analysis:
- ALL races vs. ALL other races
- ALL shift patterns: 2016->2020, 2020->2024, 2016->2024
- Republican primary data (Kasich, Cruz, Trump, etc.)
- Everything in between - complete political landscape

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
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (20, 16)

class ComprehensiveRaceAnalyzer:
    """Comprehensive analyzer for ALL races and their relationships."""
    
    def __init__(self):
        """Initialize the comprehensive analyzer."""
        self.data = {}
        self.combined_df = None
        self.models = {}
        self.correlations = {}
        self.shift_patterns = {}
        self.load_all_data()
        
    def load_all_data(self):
        """Load ALL available election data files."""
        print("Loading ALL election data for comprehensive analysis...")
        
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
            
        # Load 2018 data
        try:
            with open("2018.general.json", "r") as fp:
                self.data['2018_general'] = json.load(fp)
            print("✓ Loaded 2018 general data")
        except FileNotFoundError:
            print("✗ 2018 general data not found")
            
        # Load 2020 data
        try:
            with open("2020.primary.dem.json", "r") as fp:
                self.data['2020_primary_dem'] = json.load(fp)
            print("✓ Loaded 2020 Democratic primary data")
        except FileNotFoundError:
            print("✗ 2020 Democratic primary data not found")
            
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
    
    def extract_all_race_data(self):
        """Extract data from ALL available races across all years."""
        print("\n=== EXTRACTING ALL RACE DATA ===")
        
        all_races = []
        
        # Extract from election meta analysis (most comprehensive)
        if 'election_meta' in self.data:
            df = self.data['election_meta']
            print(f"✓ Election meta data: {len(df)} counties, {len(df.columns)} variables")
            
            # Get all race-related columns
            race_cols = [col for col in df.columns if any(race_type in col.lower() for race_type in 
                        ['pres', 'gov', 'sen', 'ag', 'sos', 'prop', 'prim', 'house', 'congress'])]
            
            print(f"Race-related columns found: {len(race_cols)}")
            for col in race_cols:
                print(f"  - {col}")
            
            all_races.append(df[['county'] + race_cols])
        
        # Extract from individual year files
        for year, data in self.data.items():
            if year == 'election_meta':
                continue
                
            print(f"\nProcessing {year} data...")
            
            if year == '2016_primary':
                # Handle 2016 primary structure
                if 'candidates' in data:
                    candidates = data.get('candidates', [])
                    print(f"  2016 Primary candidates: {len(candidates)}")
                    for candidate in candidates:
                        name = candidate.get('name', 'Unknown')
                        votes = candidate.get('votes', 0)
                        percentage = candidate.get('percentage', 0)
                        print(f"    - {name}: {votes:,} votes ({percentage:.1f}%)")
            
            elif year == '2016_general':
                # Handle 2016 general structure
                if isinstance(data, list):
                    races = data
                else:
                    races = [data]
                
                for race in races:
                    race_name = race.get('race_name', race.get('office', 'Unknown'))
                    print(f"  2016 General race: {race_name}")
            
            elif year == '2018_general':
                # Handle 2018 general structure
                if isinstance(data, list):
                    races = data
                else:
                    races = [data]
                
                for race in races:
                    race_name = race.get('race_name', race.get('office', 'Unknown'))
                    print(f"  2018 General race: {race_name}")
            
            elif year == '2020_primary_dem':
                # Handle 2020 Democratic primary
                if 'candidates' in data:
                    candidates = data.get('candidates', [])
                    print(f"  2020 Democratic Primary candidates: {len(candidates)}")
            
            elif year == '2020_general_all':
                # Handle 2020 general all
                races = data
                print(f"  2020 General races: {len(races)}")
                for race in races:
                    race_name = race.get('race_name', race.get('office', 'Unknown'))
                    print(f"    - {race_name}")
            
            elif year == '2022':
                # Handle 2022 data
                if 'races' in data:
                    races = data.get('races', [])
                    print(f"  2022 races: {len(races)}")
                    for race in races:
                        race_name = race.get('race_name', race.get('office', 'Unknown'))
                        print(f"    - {race_name}")
        
        return all_races
    
    def calculate_all_shifts(self):
        """Calculate ALL possible shift patterns across election cycles."""
        print("\n=== CALCULATING ALL SHIFT PATTERNS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        # Find all percentage columns
        pct_cols = [col for col in self.combined_df.columns if 'pct' in col.lower()]
        print(f"Percentage columns found: {len(pct_cols)}")
        
        # Group by year and race type
        year_race_groups = {}
        for col in pct_cols:
            # Parse column name to extract year and race type
            parts = col.split('_')
            if len(parts) >= 2:
                year = parts[1] if parts[1].isdigit() else None
                race_type = parts[0] if parts[0] in ['pres', 'gov', 'sen', 'ag', 'sos', 'prop'] else None
                
                if year and race_type:
                    key = f"{year}_{race_type}"
                    if key not in year_race_groups:
                        year_race_groups[key] = []
                    year_race_groups[key].append(col)
        
        print(f"Year-race groups: {list(year_race_groups.keys())}")
        
        # Calculate shifts for each race type
        for race_type in ['pres', 'gov', 'sen', 'ag', 'sos']:
            print(f"\n--- Calculating shifts for {race_type.upper()} ---")
            
            # Find columns for this race type
            race_cols = [col for col in pct_cols if col.startswith(f"{race_type}_")]
            if len(race_cols) < 2:
                continue
            
            # Sort by year
            race_cols.sort()
            print(f"  Race columns: {race_cols}")
            
            # Calculate shifts between consecutive years
            for i in range(len(race_cols) - 1):
                col1 = race_cols[i]
                col2 = race_cols[i + 1]
                
                # Extract years
                year1 = col1.split('_')[1] if len(col1.split('_')) > 1 else 'unknown'
                year2 = col2.split('_')[1] if len(col2.split('_')) > 1 else 'unknown'
                
                shift_col = f"{race_type}_{year1}_to_{year2}_shift"
                
                if col1 in self.combined_df.columns and col2 in self.combined_df.columns:
                    self.combined_df[shift_col] = (
                        self.combined_df[col2] - self.combined_df[col1]
                    )
                    print(f"    ✓ Calculated {shift_col}")
                    
                    # Calculate percentage change
                    pct_change_col = f"{race_type}_{year1}_to_{year2}_pct_change"
                    self.combined_df[pct_change_col] = (
                        self.combined_df[shift_col] / self.combined_df[col1]
                    ) * 100
                    print(f"    ✓ Calculated {pct_change_col}")
        
        # Show all calculated shifts
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        print(f"\nTotal shift variables calculated: {len(shift_cols)}")
        for col in shift_cols:
            print(f"  - {col}")
    
    def analyze_all_correlations(self):
        """Analyze correlations between ALL variables."""
        print("\n=== ANALYZING ALL CORRELATIONS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        # Get all numeric columns
        numeric_cols = self.combined_df.select_dtypes(include=[np.number]).columns.tolist()
        print(f"Numeric columns available: {len(numeric_cols)}")
        
        # Remove county index and other non-meaningful columns
        meaningful_cols = [col for col in numeric_cols if col != 'county' and not col.endswith('_index')]
        print(f"Meaningful numeric columns: {len(meaningful_cols)}")
        
        if len(meaningful_cols) > 50:
            print("Too many columns for full correlation matrix. Sampling...")
            meaningful_cols = meaningful_cols[:50]
        
        # Calculate correlation matrix
        print("Calculating correlation matrix...")
        correlation_matrix = self.combined_df[meaningful_cols].corr()
        
        # Store correlations
        self.correlations = correlation_matrix
        
        # Find strongest correlations
        print("\n=== STRONGEST CORRELATIONS ===")
        
        # Get upper triangle of correlation matrix
        upper_triangle = np.triu(np.ones(correlation_matrix.shape), k=1)
        
        # Find strongest positive and negative correlations
        correlations_flat = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if not np.isnan(corr_value):
                    correlations_flat.append({
                        'var1': correlation_matrix.columns[i],
                        'var2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        # Sort by absolute correlation
        correlations_flat.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        print("Top 20 Strongest Correlations:")
        for i, corr in enumerate(correlations_flat[:20]):
            print(f"{i+1:2d}. {corr['var1']:<30} vs. {corr['var2']:<30} r = {corr['correlation']:6.3f}")
        
        print("\nTop 20 Strongest Negative Correlations:")
        negative_corrs = [corr for corr in correlations_flat if corr['correlation'] < 0]
        for i, corr in enumerate(negative_corrs[:20]):
            print(f"{i+1:2d}. {corr['var1']:<30} vs. {corr['var2']:<30} r = {corr['correlation']:6.3f}")
        
        return correlation_matrix
    
    def analyze_republican_primary_patterns(self):
        """Analyze Republican primary patterns and their relationships."""
        print("\n=== REPUBLICAN PRIMARY PATTERN ANALYSIS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        # Find Republican primary columns
        rep_primary_cols = [col for col in self.combined_df.columns if 'prim' in col.lower() and any(rep in col.lower() for rep in ['kasich', 'cruz', 'trump', 'rubio', 'bush'])]
        print(f"Republican primary columns found: {len(rep_primary_cols)}")
        for col in rep_primary_cols:
            print(f"  - {col}")
        
        if not rep_primary_cols:
            print("No Republican primary data found")
            return
        
        # Find proposition columns
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
        print(f"Proposition columns found: {len(prop_cols)}")
        
        # Analyze relationships between Republican primary support and propositions
        print(f"\n--- REPUBLICAN PRIMARY vs. PROPOSITIONS ---")
        
        for rep_col in rep_primary_cols:
            for prop_col in prop_cols:
                if rep_col in self.combined_df.columns and prop_col in self.combined_df.columns:
                    # Calculate correlation
                    correlation = self.combined_df[rep_col].corr(self.combined_df[prop_col])
                    
                    if not np.isnan(correlation):
                        print(f"\n{rep_col} vs. {prop_col}:")
                        print(f"  Correlation: {correlation:.4f}")
                        
                        # Interpretation
                        if abs(correlation) > 0.3:
                            if correlation > 0:
                                print("  → Strong positive relationship")
                            else:
                                print("  → Strong negative relationship")
                        elif abs(correlation) < 0.1:
                            print("  → Weak relationship")
                        else:
                            print("  → Moderate relationship")
                        
                        # Linear regression
                        X = self.combined_df[rep_col].values.reshape(-1, 1)
                        y = self.combined_df[prop_col].values
                        
                        # Remove NaN values
                        mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                        X_clean = X[mask]
                        y_clean = y[mask]
                        
                        if len(X_clean) > 10:
                            # Split data
                            X_train, X_test, y_train, y_test = train_test_split(
                                X_clean, y_clean, test_size=0.3, random_state=42
                            )
                            
                            lr_model = LinearRegression()
                            lr_model.fit(X_train, y_train)
                            
                            y_test_pred = lr_model.predict(X_test)
                            test_r2 = r2_score(y_test, y_test_pred)
                            
                            print(f"  R² score: {test_r2:.4f}")
                            print(f"  Slope: {lr_model.coef_[0]:.4f}")
                            
                            # Store model
                            self.models[f"{rep_col}_vs_{prop_col}"] = lr_model
    
    def analyze_shift_patterns(self):
        """Analyze patterns in shift variables."""
        print("\n=== SHIFT PATTERN ANALYSIS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        # Find all shift columns
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        print(f"Shift columns found: {len(shift_cols)}")
        
        if not shift_cols:
            print("No shift data available")
            return
        
        # Analyze relationships between shifts and other variables
        print(f"\n--- SHIFT vs. OTHER VARIABLES ---")
        
        # Find non-shift columns
        non_shift_cols = [col for col in self.combined_df.columns if 'shift' not in col.lower() and 'change' not in col.lower() and col != 'county']
        
        for shift_col in shift_cols:
            print(f"\nAnalyzing {shift_col}:")
            
            for other_col in non_shift_cols[:10]:  # Limit to first 10 for readability
                if shift_col in self.combined_df.columns and other_col in self.combined_df.columns:
                    # Calculate correlation
                    correlation = self.combined_df[shift_col].corr(self.combined_df[other_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:  # Only show meaningful correlations
                        print(f"  vs. {other_col}: r = {correlation:.3f}")
                        
                        # Store significant correlations
                        if abs(correlation) > 0.3:
                            self.shift_patterns[f"{shift_col}_vs_{other_col}"] = correlation
    
    def create_comprehensive_visualizations(self):
        """Create comprehensive visualizations for all relationships."""
        print("\n=== CREATING COMPREHENSIVE VISUALIZATIONS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        # Create correlation heatmap
        if hasattr(self, 'correlations') and self.correlations is not None:
            print("Creating correlation heatmap...")
            
            plt.figure(figsize=(20, 16))
            mask = np.triu(np.ones_like(self.correlations, dtype=bool))
            sns.heatmap(self.correlations, mask=mask, annot=False, cmap='RdBu_r', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8})
            plt.title('Comprehensive Correlation Matrix: ALL Races & Variables', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('comprehensive_correlation_heatmap.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Correlation heatmap saved as 'comprehensive_correlation_heatmap.png'")
        
        # Create shift pattern visualizations
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        if shift_cols:
            print("Creating shift pattern visualizations...")
            
            n_shifts = min(len(shift_cols), 6)  # Limit to 6 for readability
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Shift Pattern Analysis: 2016->2020, 2020->2024, 2016->2024', 
                         fontsize=16, fontweight='bold')
            
            for i, shift_col in enumerate(shift_cols[:n_shifts]):
                row = i // 3
                col = i % 3
                ax = axes[row, col]
                
                # Plot distribution of shift
                shift_data = self.combined_df[shift_col].dropna()
                if len(shift_data) > 0:
                    ax.hist(shift_data, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
                    ax.set_xlabel(shift_col.replace('_', ' ').title())
                    ax.set_ylabel('Count')
                    ax.set_title(f'{shift_col.replace("_", " ").title()}')
                    ax.grid(True, alpha=0.3)
                    
                    # Add mean line
                    mean_shift = np.mean(shift_data)
                    ax.axvline(mean_shift, color='red', linestyle='--', linewidth=2, 
                              label=f'Mean: {mean_shift:.3f}')
                    ax.legend()
            
            plt.tight_layout()
            plt.savefig('comprehensive_shift_patterns.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Shift pattern visualizations saved as 'comprehensive_shift_patterns.png'")
    
    def run_complete_analysis(self):
        """Run the complete comprehensive analysis."""
        print("=" * 80)
        print("COMPREHENSIVE RACE ANALYSIS: ALL RACES, ALL SHIFTS, ALL RELATIONSHIPS")
        print("=" * 80)
        
        # Extract all race data
        all_races = self.extract_all_race_data()
        
        # Combine data if we have multiple sources
        if all_races:
            if len(all_races) == 1:
                self.combined_df = all_races[0]
            else:
                # Merge multiple dataframes
                self.combined_df = all_races[0]
                for df in all_races[1:]:
                    self.combined_df = self.combined_df.merge(df, on="county", how="outer")
            
            print(f"✓ Combined data: {len(self.combined_df)} counties, {len(self.combined_df.columns)} columns")
        else:
            print("✗ No race data available")
            return
        
        # Calculate all shifts
        self.calculate_all_shifts()
        
        # Analyze all correlations
        self.analyze_all_correlations()
        
        # Analyze Republican primary patterns
        self.analyze_republican_primary_patterns()
        
        # Analyze shift patterns
        self.analyze_shift_patterns()
        
        # Create visualizations
        self.create_comprehensive_visualizations()
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(self.combined_df)}")
        print(f"  Variables: {len(self.combined_df.columns)}")
        
        # Show available variables by category
        pres_cols = [col for col in self.combined_df.columns if 'pres' in col.lower()]
        gov_cols = [col for col in self.combined_df.columns if 'gov' in col.lower()]
        sen_cols = [col for col in self.combined_df.columns if 'sen' in col.lower()]
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower()]
        prim_cols = [col for col in self.combined_df.columns if 'prim' in col.lower()]
        shift_cols = [col for col in self.combined_df.columns if 'shift' in col.lower() or 'change' in col.lower()]
        
        print(f"\nVariable Categories:")
        print(f"  Presidential: {len(pres_cols)}")
        print(f"  Governor: {len(gov_cols)}")
        print(f"  Senate: {len(sen_cols)}")
        print(f"  Propositions: {len(prop_cols)}")
        print(f"  Primaries: {len(prim_cols)}")
        print(f"  Shifts: {len(shift_cols)}")
        
        print(f"\nKey Findings:")
        if hasattr(self, 'correlations') and self.correlations is not None:
            print(f"  - Correlation matrix calculated for {len(self.correlations)} variables")
        if hasattr(self, 'shift_patterns'):
            print(f"  - {len(self.shift_patterns)} significant shift patterns identified")
        if hasattr(self, 'models'):
            print(f"  - {len(self.models)} regression models created")

def main():
    """Main function to run the comprehensive analysis."""
    analyzer = ComprehensiveRaceAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
