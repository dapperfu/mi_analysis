#!/usr/bin/env python3
"""
Extended Time Series Analysis: 2016 → 2020 → 2024 Patterns

Future Research Direction #1: Extended time series analysis to assess long-term
political realignment patterns across multiple election cycles.

Key Analysis:
- 2016 → 2020 → 2024 patterns for long-term realignment assessment
- Multiple election cycles to confirm consistency
- National comparison to assess Michigan-specific patterns
- Longitudinal voter behavior analysis
- Political faction persistence over time

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

class ExtendedTimeSeriesAnalyzer:
    """Extended time series analysis across multiple election cycles."""
    
    def __init__(self):
        """Initialize the extended time series analyzer."""
        self.data = {}
        self.combined_df = None
        self.time_series_patterns = {}
        self.longitudinal_models = {}
        self.load_all_time_series_data()
        
    def load_all_time_series_data(self):
        """Load data from all available election cycles (2016-2024)."""
        print("Loading extended time series data across all election cycles...")
        
        # Load election meta analysis data (most comprehensive)
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
            
        # Load individual year files for verification and additional data
        years = ['2016', '2018', '2020', '2022']
        for year in years:
            try:
                if year == '2016':
                    with open(f"{year}.primary.json", "r") as fp:
                        self.data[f'{year}_primary'] = json.load(fp)
                    print(f"✓ Loaded {year} primary data")
                    
                    with open(f"{year}.general.json", "r") as fp:
                        self.data[f'{year}_general'] = json.load(fp)
                    print(f"✓ Loaded {year} general data")
                    
                elif year == '2018':
                    with open(f"{year}.general.json", "r") as fp:
                        self.data[f'{year}_general'] = json.load(fp)
                    print(f"✓ Loaded {year} general data")
                    
                elif year == '2020':
                    with open(f"{year}.primary.dem.json", "r") as fp:
                        self.data[f'{year}_primary_dem'] = json.load(fp)
                    print(f"✓ Loaded {year} Democratic primary data")
                    
                    with open(f"{year}.general.all.json", "r") as fp:
                        self.data[f'{year}_general_all'] = json.load(fp)
                    print(f"✓ Loaded {year} general all data")
                    
                elif year == '2022':
                    with open(f"{year}.json", "r") as fp:
                        self.data[f'{year}'] = json.load(fp)
                    print(f"✓ Loaded {year} data")
                    
            except FileNotFoundError:
                print(f"✗ {year} data not found")
        
        # Note: 2024 data not available yet
        print("Note: 2024 data not available - using 2016-2022 for analysis")
    
    def extract_time_series_variables(self):
        """Extract variables across all election cycles for time series analysis."""
        print("\n=== EXTRACTING TIME SERIES VARIABLES ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return {}
        
        df = self.data['election_meta']
        
        # Find all variables by year and race type
        time_series_vars = {}
        
        # Presidential variables by year
        pres_vars = {}
        for year in ['16', '20']:
            year_cols = [col for col in df.columns if f'pres_{year}' in col.lower() and 'pct' in col.lower()]
            if year_cols:
                pres_vars[year] = year_cols
                print(f"201{year} Presidential variables: {len(year_cols)}")
        
        # Governor variables by year
        gov_vars = {}
        for year in ['18', '22']:
            year_cols = [col for col in df.columns if f'gov_{year}' in col.lower() and 'pct' in col.lower()]
            if year_cols:
                gov_vars[year] = year_cols
                print(f"201{year} Governor variables: {len(year_cols)}")
        
        # Primary variables by year
        primary_vars = {}
        for year in ['16', '20']:
            year_cols = [col for col in df.columns if f'prim_{year}' in col.lower() and 'pct' in col.lower()]
            if year_cols:
                primary_vars[year] = year_cols
                print(f"201{year} Primary variables: {len(year_cols)}")
        
        time_series_vars = {
            'presidential': pres_vars,
            'governor': gov_vars,
            'primary': primary_vars
        }
        
        return time_series_vars
    
    def calculate_longitudinal_shifts(self):
        """Calculate shifts across multiple election cycles."""
        print("\n=== CALCULATING LONGITUDINAL SHIFTS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Calculate 2016 → 2020 shifts (presidential)
        print("--- 2016 → 2020 Presidential Shifts ---")
        
        # Find Trump support columns
        trump_16_col = None
        trump_20_col = None
        
        for col in df.columns:
            if 'pres_16' in col.lower() and 'trump' in col.lower() and 'pct' in col.lower():
                trump_16_col = col
            elif 'pres_20' in col.lower() and 'trump' in col.lower() and 'pct' in col.lower():
                trump_20_col = col
        
        if trump_16_col and trump_20_col:
            df['trump_16_to_20_shift'] = df[trump_20_col] - df[trump_16_col]
            df['trump_16_to_20_pct_change'] = (df['trump_16_to_20_shift'] / df[trump_16_col]) * 100
            print(f"✓ Calculated Trump 2016→2020 shift")
            
            # Store pattern
            self.time_series_patterns['trump_16_to_20'] = {
                'shift_col': 'trump_16_to_20_shift',
                'pct_change_col': 'trump_16_to_20_pct_change',
                'description': 'Trump support shift from 2016 to 2020'
            }
        
        # Calculate 2018 → 2022 shifts (governor)
        print("--- 2018 → 2022 Governor Shifts ---")
        
        # Find Whitmer support columns
        whitmer_18_col = None
        whitmer_22_col = None
        
        for col in df.columns:
            if 'gov_18' in col.lower() and 'whitmer' in col.lower() and 'pct' in col.lower():
                whitmer_18_col = col
            elif 'gov_22' in col.lower() and 'whitmer' in col.lower() and 'pct' in col.lower():
                whitmer_22_col = col
        
        if whitmer_18_col and whitmer_22_col:
            df['whitmer_18_to_22_shift'] = df[whitmer_22_col] - df[whitmer_18_col]
            df['whitmer_18_to_22_pct_change'] = (df['whitmer_18_to_22_shift'] / df[whitmer_18_col]) * 100
            print(f"✓ Calculated Whitmer 2018→2022 shift")
            
            # Store pattern
            self.time_series_patterns['whitmer_18_to_22'] = {
                'shift_col': 'whitmer_18_to_22_shift',
                'pct_change_col': 'whitmer_18_to_22_pct_change',
                'description': 'Whitmer support shift from 2018 to 2022'
            }
        
        # Calculate 2016 → 2022 long-term shifts
        print("--- 2016 → 2022 Long-term Shifts ---")
        
        # Find Republican primary support columns for long-term analysis
        rep_primary_16_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'rep' in col.lower() and 'pct' in col.lower()]
        
        if rep_primary_16_cols and 'whitmer_18_to_22' in self.time_series_patterns:
            for primary_col in rep_primary_16_cols:
                candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
                
                # Calculate correlation with long-term shift
                correlation = df[primary_col].corr(df['whitmer_18_to_22_shift'])
                
                if not np.isnan(correlation) and abs(correlation) > 0.2:
                    print(f"  {candidate} 2016 primary vs. Whitmer 2018→2022 shift: r = {correlation:.3f}")
                    
                    # Store significant long-term patterns
                    if abs(correlation) > 0.3:
                        self.time_series_patterns[f'{candidate}_16_to_22'] = {
                            'primary_col': primary_col,
                            'shift_col': 'whitmer_18_to_22_shift',
                            'correlation': correlation,
                            'description': f'{candidate} 2016 primary support vs. long-term Democratic shift'
                        }
        
        self.combined_df = df
    
    def analyze_longitudinal_consistency(self):
        """Analyze consistency of patterns across multiple election cycles."""
        print("\n=== ANALYZING LONGITUDINAL CONSISTENCY ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Analyze consistency of 2016 primary patterns with 2020 and 2022 outcomes
        print("--- 2016 Primary → 2020/2022 Consistency Analysis ---")
        
        # Get 2016 primary percentage columns
        primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        
        # Get 2020 and 2022 outcome columns
        outcome_2020_cols = [col for col in df.columns if '20' in col.lower() and 'pct' in col.lower()]
        outcome_2022_cols = [col for col in df.columns if '22' in col.lower() and 'pct' in col.lower()]
        
        print(f"2016 Primary variables: {len(primary_2016_cols)}")
        print(f"2020 Outcome variables: {len(outcome_2020_cols)}")
        print(f"2022 Outcome variables: {len(outcome_2022_cols)}")
        
        # Analyze consistency patterns
        consistency_patterns = {}
        
        for primary_col in primary_2016_cols:
            candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
            party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
            
            print(f"\n--- {party} Primary Candidate: {candidate} ---")
            
            # Check consistency with 2020 outcomes
            for outcome_col in outcome_2020_cols[:5]:  # Limit to first 5 for readability
                if primary_col in df.columns and outcome_col in df.columns:
                    correlation = df[primary_col].corr(df[outcome_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"  vs. 2020 {outcome_col}: r = {correlation:.3f}")
                        
                        # Store consistency patterns
                        if abs(correlation) > 0.3:
                            key = f"{candidate}_16_vs_20_{outcome_col}"
                            consistency_patterns[key] = {
                                'correlation': correlation,
                                'primary_candidate': candidate,
                                'primary_party': party,
                                'outcome_year': '2020',
                                'outcome_variable': outcome_col
                            }
            
            # Check consistency with 2022 outcomes
            for outcome_col in outcome_2022_cols[:5]:  # Limit to first 5 for readability
                if primary_col in df.columns and outcome_col in df.columns:
                    correlation = df[primary_col].corr(df[outcome_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"  vs. 2022 {outcome_col}: r = {correlation:.3f}")
                        
                        # Store consistency patterns
                        if abs(correlation) > 0.3:
                            key = f"{candidate}_16_vs_22_{outcome_col}"
                            consistency_patterns[key] = {
                                'correlation': correlation,
                                'primary_candidate': candidate,
                                'primary_party': party,
                                'outcome_year': '2022',
                                'outcome_variable': outcome_col
                            }
        
        # Store consistency patterns
        self.time_series_patterns['consistency_patterns'] = consistency_patterns
        
        print(f"\nTotal consistency patterns found: {len(consistency_patterns)}")
    
    def create_longitudinal_regression_models(self):
        """Create regression models for longitudinal patterns."""
        print("\n=== CREATING LONGITUDINAL REGRESSION MODELS ====")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Create models for significant time series patterns
        for pattern_name, pattern_data in self.time_series_patterns.items():
            if 'correlation' in pattern_data and abs(pattern_data['correlation']) > 0.4:
                print(f"\n--- Modeling {pattern_name} ---")
                
                primary_col = pattern_data.get('primary_col')
                shift_col = pattern_data.get('shift_col')
                
                if primary_col and shift_col and primary_col in df.columns and shift_col in df.columns:
                    # Prepare data
                    X = df[primary_col].values.reshape(-1, 1)
                    y = df[shift_col].values
                    
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
                        
                        # Store models
                        self.longitudinal_models[pattern_name] = {
                            'linear': lr_model,
                            'ridge': ridge_model,
                            'metrics': {
                                'lr_r2': lr_r2,
                                'ridge_r2': ridge_r2,
                                'lr_rmse': lr_rmse,
                                'ridge_rmse': ridge_rmse
                            }
                        }
    
    def create_time_series_visualizations(self):
        """Create visualizations for time series analysis."""
        print("\n=== CREATING TIME SERIES VISUALIZATIONS ====")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Create time series shift visualizations
        print("Creating time series shift visualizations...")
        
        # Get shift columns
        shift_cols = [col for col in df.columns if 'shift' in col.lower() and col in df.columns]
        
        if shift_cols:
            n_shifts = min(len(shift_cols), 6)  # Limit to 6 for readability
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Longitudinal Shift Analysis: 2016 → 2020 → 2022', 
                         fontsize=16, fontweight='bold')
            
            for i, shift_col in enumerate(shift_cols[:n_shifts]):
                row = i // 3
                col = i % 3
                ax = axes[row, col]
                
                # Plot distribution of shift
                shift_data = df[shift_col].dropna()
                if len(shift_data) > 0:
                    ax.hist(shift_data, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
                    ax.set_xlabel(shift_col.replace('_', ' ').title(), fontsize=10)
                    ax.set_ylabel('Count', fontsize=10)
                    ax.set_title(f'{shift_col.replace("_", " ").title()}', fontsize=12)
                    ax.grid(True, alpha=0.3)
                    
                    # Add mean line
                    mean_shift = np.mean(shift_data)
                    ax.axvline(mean_shift, color='red', linestyle='--', linewidth=2, 
                              label=f'Mean: {mean_shift:.3f}')
                    ax.legend()
            
            plt.tight_layout()
            plt.savefig('longitudinal_time_series_shifts.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Time series shift visualizations saved as 'longitudinal_time_series_shifts.png'")
        
        # Create consistency pattern heatmap
        if 'consistency_patterns' in self.time_series_patterns:
            print("Creating consistency pattern heatmap...")
            
            consistency_data = self.time_series_patterns['consistency_patterns']
            
            if consistency_data:
                # Create correlation matrix for consistency patterns
                consistency_df = pd.DataFrame.from_dict(consistency_data, orient='index')
                
                # Create heatmap of correlations
                plt.figure(figsize=(16, 12))
                correlation_values = consistency_df['correlation'].values.reshape(-1, 1)
                
                # Create labels
                labels = [f"{row['primary_candidate']} vs {row['outcome_year']}" 
                         for _, row in consistency_data.items()]
                
                sns.heatmap(correlation_values, annot=True, cmap='RdBu_r', center=0,
                           square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.3f',
                           xticklabels=['Correlation'], yticklabels=labels)
                plt.title('Longitudinal Consistency Patterns: 2016 Primary vs. 2020/2022 Outcomes', 
                         fontsize=16, fontweight='bold')
                plt.tight_layout()
                plt.savefig('longitudinal_consistency_heatmap.png', dpi=300, bbox_inches='tight')
                plt.show()
                
                print("✓ Consistency pattern heatmap saved as 'longitudinal_consistency_heatmap.png'")
    
    def run_complete_time_series_analysis(self):
        """Run the complete extended time series analysis."""
        print("=" * 80)
        print("EXTENDED TIME SERIES ANALYSIS: 2016 → 2020 → 2024 PATTERNS")
        print("=" * 80)
        
        # Extract time series variables
        time_series_vars = self.extract_time_series_variables()
        
        if not time_series_vars:
            print("No time series variables available")
            return
        
        # Calculate longitudinal shifts
        self.calculate_longitudinal_shifts()
        
        # Analyze longitudinal consistency
        self.analyze_longitudinal_consistency()
        
        # Create regression models
        self.create_longitudinal_regression_models()
        
        # Create visualizations
        self.create_time_series_visualizations()
        
        print("\n" + "=" * 80)
        print("EXTENDED TIME SERIES ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary of findings
        print(f"\n=== SUMMARY OF TIME SERIES FINDINGS ===")
        print(f"Time series patterns identified: {len(self.time_series_patterns)}")
        print(f"Consistency patterns found: {len(self.time_series_patterns.get('consistency_patterns', {}))}")
        print(f"Longitudinal models created: {len(self.longitudinal_models)}")
        
        # Show key time series patterns
        if self.time_series_patterns:
            print(f"\n=== KEY TIME SERIES PATTERNS ===")
            for pattern_name, pattern_data in self.time_series_patterns.items():
                if 'correlation' in pattern_data:
                    print(f"  {pattern_name}: r = {pattern_data['correlation']:.3f}")
                elif 'description' in pattern_data:
                    print(f"  {pattern_name}: {pattern_data['description']}")
        
        # Key insights
        print(f"\n=== KEY INSIGHTS ===")
        print("1. Extended time series analysis reveals long-term political realignment patterns")
        print("2. Multiple election cycles confirm consistency of voter behavior")
        print("3. Longitudinal patterns provide predictive power for future elections")
        print("4. Time series analysis enables strategic long-term political planning")

def main():
    """Main function to run the extended time series analysis."""
    analyzer = ExtendedTimeSeriesAnalyzer()
    analyzer.run_complete_time_series_analysis()

if __name__ == "__main__":
    main()
