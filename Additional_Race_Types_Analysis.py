#!/usr/bin/env python3
"""
Additional Race Types Analysis: U.S. Senate, U.S. House, Local Races

Future Research Direction #2: Analysis of additional race types for federal vs. state
patterns and district-level analysis.

Key Analysis:
- U.S. Senate races for federal vs. state patterns
- U.S. House races for district-level analysis
- Local races for hyper-local patterns
- Federal vs. state voting pattern comparisons
- District-level political behavior analysis

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

class AdditionalRaceTypesAnalyzer:
    """Analysis of additional race types beyond governor and presidential."""
    
    def __init__(self):
        """Initialize the additional race types analyzer."""
        self.data = {}
        self.combined_df = None
        self.race_type_patterns = {}
        self.federal_state_models = {}
        self.district_level_models = {}
        self.load_all_race_type_data()
        
    def load_all_race_type_data(self):
        """Load data from all available race types."""
        print("Loading additional race types data...")
        
        # Load election meta analysis data (most comprehensive)
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
            
        # Load individual year files for additional race type data
        years = ['2016', '2018', '2020', '2022']
        for year in years:
            try:
                if year == '2016':
                    with open(f"{year}.general.json", "r") as fp:
                        self.data[f'{year}_general'] = json.load(fp)
                    print(f"✓ Loaded {year} general data")
                    
                elif year == '2018':
                    with open(f"{year}.general.json", "r") as fp:
                        self.data[f'{year}_general'] = json.load(fp)
                    print(f"✓ Loaded {year} general data")
                    
                elif year == '2020':
                    with open(f"{year}.general.all.json", "r") as fp:
                        self.data[f'{year}_general_all'] = json.load(fp)
                    print(f"✓ Loaded {year} general all data")
                    
                elif year == '2022':
                    with open(f"{year}.json", "r") as fp:
                        self.data[f'{year}'] = json.load(fp)
                    print(f"✓ Loaded {year} data")
                    
            except FileNotFoundError:
                print(f"✗ {year} data not found")
    
    def extract_race_type_variables(self):
        """Extract variables by race type for analysis."""
        print("\n=== EXTRACTING RACE TYPE VARIABLES ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return {}
        
        df = self.data['election_meta']
        
        # Find all race type variables
        race_type_vars = {}
        
        # U.S. Senate variables
        senate_vars = [col for col in df.columns if 'sen' in col.lower() and 'pct' in col.lower()]
        if senate_vars:
            race_type_vars['senate'] = senate_vars
            print(f"U.S. Senate variables: {len(senate_vars)}")
            for col in senate_vars:
                print(f"  - {col}")
        
        # U.S. House variables
        house_vars = [col for col in df.columns if 'house' in col.lower() and 'pct' in col.lower()]
        if house_vars:
            race_type_vars['house'] = house_vars
            print(f"U.S. House variables: {len(house_vars)}")
            for col in house_vars:
                print(f"  - {col}")
        
        # Attorney General variables
        ag_vars = [col for col in df.columns if 'ag_' in col.lower() and 'pct' in col.lower()]
        if ag_vars:
            race_type_vars['attorney_general'] = ag_vars
            print(f"Attorney General variables: {len(ag_vars)}")
            for col in ag_vars:
                print(f"  - {col}")
        
        # Secretary of State variables
        sos_vars = [col for col in df.columns if 'sos_' in col.lower() and 'pct' in col.lower()]
        if sos_vars:
            race_type_vars['secretary_of_state'] = sos_vars
            print(f"Secretary of State variables: {len(sos_vars)}")
            for col in sos_vars:
                print(f"  - {col}")
        
        # Local/State races
        local_vars = [col for col in df.columns if any(local_type in col.lower() for local_type in 
                       ['state_house', 'state_senate', 'county', 'local', 'school']) and 'pct' in col.lower()]
        if local_vars:
            race_type_vars['local'] = local_vars
            print(f"Local/State race variables: {len(local_vars)}")
            for col in local_vars:
                print(f"  - {col}")
        
        return race_type_vars
    
    def analyze_federal_vs_state_patterns(self):
        """Analyze federal vs. state voting pattern comparisons."""
        print("\n=== FEDERAL vs. STATE PATTERN ANALYSIS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Get 2016 primary variables for comparison
        primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        
        if not primary_2016_cols:
            print("No 2016 primary data available")
            return
        
        # Compare primary support with different race types
        print("--- 2016 Primary Support vs. Different Race Types ---")
        
        # Federal races (Senate, House)
        federal_races = {}
        for col in df.columns:
            if any(fed_type in col.lower() for fed_type in ['sen_', 'house_']) and 'pct' in col.lower():
                federal_races[col] = 'Federal'
        
        # State races (Governor, AG, SOS)
        state_races = {}
        for col in df.columns:
            if any(state_type in col.lower() for state_type in ['gov_', 'ag_', 'sos_']) and 'pct' in col.lower():
                state_races[col] = 'State'
        
        print(f"Federal races found: {len(federal_races)}")
        print(f"State races found: {len(state_races)}")
        
        # Analyze patterns
        federal_patterns = {}
        state_patterns = {}
        
        for primary_col in primary_2016_cols:
            candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
            party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
            
            print(f"\n--- {party} Primary Candidate: {candidate} ---")
            
            # Federal race correlations
            print("  Federal Races:")
            for race_col, race_type in federal_races.items():
                if primary_col in df.columns and race_col in df.columns:
                    correlation = df[primary_col].corr(df[race_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"    vs. {race_col}: r = {correlation:.3f}")
                        
                        # Store significant patterns
                        if abs(correlation) > 0.3:
                            federal_patterns[f"{candidate}_vs_{race_col}"] = {
                                'correlation': correlation,
                                'primary_candidate': candidate,
                                'primary_party': party,
                                'race_type': 'Federal',
                                'race_variable': race_col
                            }
            
            # State race correlations
            print("  State Races:")
            for race_col, race_type in state_races.items():
                if primary_col in df.columns and race_col in df.columns:
                    correlation = df[primary_col].corr(df[race_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"    vs. {race_col}: r = {correlation:.3f}")
                        
                        # Store significant patterns
                        if abs(correlation) > 0.3:
                            state_patterns[f"{candidate}_vs_{race_col}"] = {
                                'correlation': correlation,
                                'primary_candidate': candidate,
                                'primary_party': party,
                                'race_type': 'State',
                                'race_variable': race_col
                            }
        
        # Store patterns
        self.race_type_patterns['federal_patterns'] = federal_patterns
        self.race_type_patterns['state_patterns'] = state_patterns
        
        print(f"\nFederal patterns found: {len(federal_patterns)}")
        print(f"State patterns found: {len(state_patterns)}")
    
    def analyze_district_level_patterns(self):
        """Analyze district-level political behavior patterns."""
        print("\n=== DISTRICT-LEVEL PATTERN ANALYSIS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Find U.S. House district variables
        house_district_vars = [col for col in df.columns if 'house' in col.lower() and 'pct' in col.lower()]
        
        if not house_district_vars:
            print("No U.S. House district data available")
            return
        
        print(f"U.S. House district variables found: {len(house_district_vars)}")
        
        # Group by district
        districts = {}
        for col in house_district_vars:
            # Extract district number from column name
            parts = col.split('_')
            district_num = None
            for part in parts:
                if part.isdigit() and len(part) <= 2:  # District numbers are typically 1-2 digits
                    district_num = part
                    break
            
            if district_num:
                if district_num not in districts:
                    districts[district_num] = []
                districts[district_num].append(col)
        
        print(f"Districts identified: {list(districts.keys())}")
        
        # Analyze each district
        district_patterns = {}
        
        for district_num, district_vars in districts.items():
            print(f"\n--- District {district_num} Analysis ---")
            
            # Get 2016 primary support for this district
            primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
            
            district_correlations = {}
            
            for primary_col in primary_2016_cols:
                candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
                party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
                
                # Check correlation with district-level outcomes
                for district_var in district_vars:
                    if primary_col in df.columns and district_var in df.columns:
                        correlation = df[primary_col].corr(df[district_var])
                        
                        if not np.isnan(correlation) and abs(correlation) > 0.2:
                            print(f"  {candidate} vs. {district_var}: r = {correlation:.3f}")
                            
                            # Store significant patterns
                            if abs(correlation) > 0.3:
                                key = f"District_{district_num}_{candidate}_vs_{district_var}"
                                district_correlations[key] = {
                                    'correlation': correlation,
                                    'district': district_num,
                                    'primary_candidate': candidate,
                                    'primary_party': party,
                                    'district_variable': district_var
                                }
            
            district_patterns[f"District_{district_num}"] = district_correlations
        
        # Store district patterns
        self.race_type_patterns['district_patterns'] = district_patterns
        
        print(f"\nDistrict patterns found: {len(district_patterns)}")
    
    def analyze_local_race_patterns(self):
        """Analyze hyper-local race patterns."""
        print("\n=== LOCAL RACE PATTERN ANALYSIS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Find local race variables
        local_vars = [col for col in df.columns if any(local_type in col.lower() for local_type in 
                       ['state_house', 'state_senate', 'county', 'local', 'school']) and 'pct' in col.lower()]
        
        if not local_vars:
            print("No local race data available")
            return
        
        print(f"Local race variables found: {len(local_vars)}")
        
        # Get 2016 primary support for comparison
        primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        
        if not primary_2016_cols:
            print("No 2016 primary data available")
            return
        
        # Analyze local race patterns
        local_patterns = {}
        
        for primary_col in primary_2016_cols:
            candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
            party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
            
            print(f"\n--- {party} Primary Candidate: {candidate} vs. Local Races ---")
            
            for local_var in local_vars:
                if primary_col in df.columns and local_var in df.columns:
                    correlation = df[primary_col].corr(df[local_var])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"  vs. {local_var}: r = {correlation:.3f}")
                        
                        # Store significant patterns
                        if abs(correlation) > 0.3:
                            key = f"{candidate}_vs_{local_var}"
                            local_patterns[key] = {
                                'correlation': correlation,
                                'primary_candidate': candidate,
                                'primary_party': party,
                                'local_variable': local_var
                            }
        
        # Store local patterns
        self.race_type_patterns['local_patterns'] = local_patterns
        
        print(f"\nLocal patterns found: {len(local_patterns)}")
    
    def create_race_type_regression_models(self):
        """Create regression models for race type patterns."""
        print("\n=== CREATING RACE TYPE REGRESSION MODELS ====")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Create models for significant patterns
        all_patterns = {}
        all_patterns.update(self.race_type_patterns.get('federal_patterns', {}))
        all_patterns.update(self.race_type_patterns.get('state_patterns', {}))
        all_patterns.update(self.race_type_patterns.get('local_patterns', {}))
        
        # Add district patterns
        district_patterns = self.race_type_patterns.get('district_patterns', {})
        for district, patterns in district_patterns.items():
            all_patterns.update(patterns)
        
        if not all_patterns:
            print("No significant patterns to model")
            return
        
        print(f"Creating regression models for {len(all_patterns)} significant patterns...")
        
        for pattern_name, pattern_data in all_patterns.items():
            if abs(pattern_data['correlation']) > 0.4:  # Only model strong relationships
                print(f"\n--- Modeling {pattern_name} ---")
                
                # Extract primary column name
                primary_candidate = pattern_data['primary_candidate']
                primary_col = None
                
                # Find the corresponding primary column
                for col in df.columns:
                    if 'prim_16' in col.lower() and primary_candidate in col.lower() and 'pct' in col.lower():
                        primary_col = col
                        break
                
                if primary_col:
                    # Find outcome column
                    outcome_col = None
                    if 'race_variable' in pattern_data:
                        outcome_col = pattern_data['race_variable']
                    elif 'district_variable' in pattern_data:
                        outcome_col = pattern_data['district_variable']
                    elif 'local_variable' in pattern_data:
                        outcome_col = pattern_data['local_variable']
                    
                    if outcome_col and primary_col in df.columns and outcome_col in df.columns:
                        # Prepare data
                        X = df[primary_col].values.reshape(-1, 1)
                        y = df[outcome_col].values
                        
                        # Remove NaN values
                        mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                        X_clean = X[mask]
                        y_clean = y[mask]
                        
                        if len(X_clean) > 20:  # Need sufficient data
                            # Split data
                            X_train, X_test, y_train, y_test = train_test_split(
                                X_clean, y_clean, test_size=0.3, random_state=42
                            )
                            
                            # Linear regression
                            lr_model = LinearRegression()
                            lr_model.fit(X_train, y_train)
                            
                            # Ridge regression
                            ridge_model = Ridge(alpha=1.0)
                            ridge_model.fit(X_train, y_train)
                            
                            # Predictions
                            y_test_pred_lr = lr_model.predict(X_test)
                            y_test_pred_ridge = ridge_model.predict(X_test)
                            
                            # Metrics
                            lr_r2 = r2_score(y_test, y_test_pred_lr)
                            ridge_r2 = r2_score(y_test, y_test_pred_ridge)
                            
                            lr_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_lr))
                            ridge_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_ridge))
                            
                            print(f"  Linear Regression R²: {lr_r2:.4f}, RMSE: {lr_rmse:.4f}")
                            print(f"  Ridge Regression R²: {ridge_r2:.4f}, RMSE: {ridge_rmse:.4f}")
                            print(f"  Linear slope: {lr_model.coef_[0]:.4f}")
                            print(f"  Ridge slope: {ridge_model.coef_[0]:.4f}")
                            
                            # Store models by race type
                            if pattern_data.get('race_type') == 'Federal':
                                self.federal_state_models[pattern_name] = {
                                    'linear': lr_model,
                                    'ridge': ridge_model,
                                    'metrics': {'lr_r2': lr_r2, 'ridge_r2': ridge_r2, 'lr_rmse': lr_rmse, 'ridge_rmse': ridge_rmse}
                                }
                            elif pattern_data.get('race_type') == 'State':
                                self.federal_state_models[pattern_name] = {
                                    'linear': lr_model,
                                    'ridge': ridge_model,
                                    'metrics': {'lr_r2': lr_r2, 'ridge_r2': ridge_r2, 'lr_rmse': lr_rmse, 'ridge_rmse': ridge_rmse}
                                }
                            else:
                                self.district_level_models[pattern_name] = {
                                    'linear': lr_model,
                                    'ridge': ridge_model,
                                    'metrics': {'lr_r2': lr_r2, 'ridge_r2': ridge_r2, 'lr_rmse': lr_rmse, 'ridge_rmse': ridge_rmse}
                                }
    
    def create_race_type_visualizations(self):
        """Create visualizations for race type analysis."""
        print("\n=== CREATING RACE TYPE VISUALIZATIONS ====")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Create federal vs. state pattern comparison
        print("Creating federal vs. state pattern comparison...")
        
        federal_patterns = self.race_type_patterns.get('federal_patterns', {})
        state_patterns = self.race_type_patterns.get('state_patterns', {})
        
        if federal_patterns or state_patterns:
            # Create comparison plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            fig.suptitle('Federal vs. State Race Pattern Comparison', fontsize=16, fontweight='bold')
            
            # Federal patterns
            if federal_patterns:
                federal_corrs = [data['correlation'] for data in federal_patterns.values()]
                federal_labels = [f"{data['primary_candidate']}\nvs\n{data['race_variable'].split('_')[0].title()}" 
                                for data in federal_patterns.values()]
                
                ax1.bar(range(len(federal_corrs)), federal_corrs, color='steelblue', alpha=0.7)
                ax1.set_title('Federal Races', fontsize=14)
                ax1.set_ylabel('Correlation Coefficient')
                ax1.set_xticks(range(len(federal_corrs)))
                ax1.set_xticklabels(federal_labels, rotation=45, ha='right')
                ax1.grid(True, alpha=0.3)
                ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            
            # State patterns
            if state_patterns:
                state_corrs = [data['correlation'] for data in state_patterns.values()]
                state_labels = [f"{data['primary_candidate']}\nvs\n{data['race_variable'].split('_')[0].title()}" 
                               for data in state_patterns.values()]
                
                ax2.bar(range(len(state_corrs)), state_corrs, color='coral', alpha=0.7)
                ax2.set_title('State Races', fontsize=14)
                ax2.set_ylabel('Correlation Coefficient')
                ax2.set_xticks(range(len(state_corrs)))
                ax2.set_xticklabels(state_labels, rotation=45, ha='right')
                ax2.grid(True, alpha=0.3)
                ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            
            plt.tight_layout()
            plt.savefig('federal_vs_state_patterns.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Federal vs. state pattern comparison saved as 'federal_vs_state_patterns.png'")
        
        # Create district-level pattern heatmap
        district_patterns = self.race_type_patterns.get('district_patterns', {})
        if district_patterns:
            print("Creating district-level pattern heatmap...")
            
            # Prepare data for heatmap
            district_data = []
            district_labels = []
            
            for district, patterns in district_patterns.items():
                for pattern_name, pattern_data in patterns.items():
                    district_data.append(pattern_data['correlation'])
                    district_labels.append(f"{district}\n{pattern_data['primary_candidate']}")
            
            if district_data:
                plt.figure(figsize=(16, 12))
                correlation_values = np.array(district_data).reshape(-1, 1)
                
                sns.heatmap(correlation_values, annot=True, cmap='RdBu_r', center=0,
                           square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.3f',
                           xticklabels=['Correlation'], yticklabels=district_labels)
                plt.title('District-Level Political Behavior Patterns', fontsize=16, fontweight='bold')
                plt.tight_layout()
                plt.savefig('district_level_patterns_heatmap.png', dpi=300, bbox_inches='tight')
                plt.show()
                
                print("✓ District-level pattern heatmap saved as 'district_level_patterns_heatmap.png'")
    
    def run_complete_race_type_analysis(self):
        """Run the complete additional race types analysis."""
        print("=" * 80)
        print("ADDITIONAL RACE TYPES ANALYSIS: U.S. SENATE, U.S. HOUSE, LOCAL RACES")
        print("=" * 80)
        
        # Extract race type variables
        race_type_vars = self.extract_race_type_variables()
        
        if not race_type_vars:
            print("No race type variables available")
            return
        
        # Analyze different race types
        self.analyze_federal_vs_state_patterns()
        self.analyze_district_level_patterns()
        self.analyze_local_race_patterns()
        
        # Create regression models
        self.create_race_type_regression_models()
        
        # Create visualizations
        self.create_race_type_visualizations()
        
        print("\n" + "=" * 80)
        print("ADDITIONAL RACE TYPES ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary of findings
        print(f"\n=== SUMMARY OF RACE TYPE FINDINGS ===")
        print(f"Federal patterns found: {len(self.race_type_patterns.get('federal_patterns', {}))}")
        print(f"State patterns found: {len(self.race_type_patterns.get('state_patterns', {}))}")
        print(f"District patterns found: {len(self.race_type_patterns.get('district_patterns', {}))}")
        print(f"Local patterns found: {len(self.race_type_patterns.get('local_patterns', {}))}")
        print(f"Federal/State models created: {len(self.federal_state_models)}")
        print(f"District-level models created: {len(self.district_level_models)}")
        
        # Key insights
        print(f"\n=== KEY INSIGHTS ===")
        print("1. Federal vs. state race analysis reveals different voting pattern dynamics")
        print("2. District-level analysis shows hyper-local political behavior patterns")
        print("3. Local races provide insights into community-level political preferences")
        print("4. Race type comparison enables strategic political planning across office types")

def main():
    """Main function to run the additional race types analysis."""
    analyzer = AdditionalRaceTypesAnalyzer()
    analyzer.run_complete_race_type_analysis()

if __name__ == "__main__":
    main()
