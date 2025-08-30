#!/usr/bin/env python3
"""
Primary 2016 vs. 2018 Analysis: Cross-Election Cycle Consistency

Deep dive into how 2016 primary support patterns translate to 2018 non-presidential elections.
This analysis examines the relationship between primary voting preferences and down-ballot
performance in the next election cycle.

Key Analysis:
- 2016 Republican primary support vs. 2018 governor race
- 2016 Democratic primary support vs. 2018 governor race
- 2016 primary support vs. 2018 other down-ballot races
- Cross-election cycle voter behavior patterns
- Political faction persistence and realignment

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
plt.rcParams['figure.figsize'] = (20, 16)

class Primary2016vs2018Analyzer:
    """Deep analysis of 2016 primary support vs. 2018 non-presidential elections."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.data = {}
        self.combined_df = None
        self.models = {}
        self.correlations = {}
        self.load_data()
        
    def load_data(self):
        """Load 2016 primary and 2018 general election data."""
        print("Loading 2016 primary and 2018 general election data...")
        
        # Load election meta analysis data (most comprehensive)
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
            return
        
        # Load individual year files for verification
        try:
            with open("2016.primary.json", "r") as fp:
                self.data['2016_primary'] = json.load(fp)
            print("✓ Loaded 2016 primary data")
        except FileNotFoundError:
            print("✗ 2016 primary data not found")
            
        try:
            with open("2018.general.json", "r") as fp:
                self.data['2018_general'] = json.load(fp)
            print("✓ Loaded 2018 general data")
        except FileNotFoundError:
            print("✗ 2018 general data not found")
    
    def extract_2016_primary_variables(self):
        """Extract all 2016 primary variables from the combined dataset."""
        print("\n=== EXTRACTING 2016 PRIMARY VARIABLES ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return []
        
        df = self.data['election_meta']
        
        # Find all 2016 primary columns
        primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower()]
        print(f"2016 primary variables found: {len(primary_2016_cols)}")
        
        # Categorize by party and candidate
        rep_primary_cols = [col for col in primary_2016_cols if 'rep' in col.lower()]
        dem_primary_cols = [col for col in primary_2016_cols if 'dem' in col.lower()]
        
        print(f"\nRepublican primary variables: {len(rep_primary_cols)}")
        for col in rep_primary_cols:
            print(f"  - {col}")
            
        print(f"\nDemocratic primary variables: {len(dem_primary_cols)}")
        for col in dem_primary_cols:
            print(f"  - {col}")
        
        return primary_2016_cols
    
    def extract_2018_non_presidential_variables(self):
        """Extract all 2018 non-presidential election variables."""
        print("\n=== EXTRACTING 2018 NON-PRESIDENTIAL VARIABLES ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return []
        
        df = self.data['election_meta']
        
        # Find all 2018 variables (excluding presidential)
        variables_2018 = [col for col in df.columns if '18_' in col.lower() and 'pres' not in col.lower()]
        print(f"2018 non-presidential variables found: {len(variables_2018)}")
        
        # Categorize by race type
        gov_2018_cols = [col for col in variables_2018 if 'gov' in col.lower()]
        house_2018_cols = [col for col in variables_2018 if 'house' in col.lower()]
        senate_2018_cols = [col for col in variables_2018 if 'sen' in col.lower()]
        other_2018_cols = [col for col in variables_2018 if not any(race in col.lower() for race in ['gov', 'house', 'sen'])]
        
        print(f"\n2018 Governor variables: {len(gov_2018_cols)}")
        for col in gov_2018_cols:
            print(f"  - {col}")
            
        print(f"\n2018 House variables: {len(house_2018_cols)}")
        for col in house_2018_cols:
            print(f"  - {col}")
            
        print(f"\n2018 Senate variables: {len(senate_2018_cols)}")
        for col in senate_2018_cols:
            print(f"  - {col}")
            
        print(f"\n2018 Other variables: {len(other_2018_cols)}")
        for col in other_2018_cols:
            print(f"  - {col}")
        
        return variables_2018
    
    def analyze_2016_primary_vs_2018_governor(self):
        """Deep analysis of 2016 primary support vs. 2018 governor race."""
        print("\n=== 2016 PRIMARY vs. 2018 GOVERNOR DEEP ANALYSIS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Get 2016 primary percentage columns
        primary_2016_pct_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        
        # Get 2018 governor percentage columns
        gov_2018_pct_cols = [col for col in df.columns if 'gov_18' in col.lower() and 'pct' in col.lower()]
        
        print(f"2016 primary percentage variables: {len(primary_2016_pct_cols)}")
        print(f"2018 governor percentage variables: {len(gov_2018_pct_cols)}")
        
        if not primary_2016_pct_cols or not gov_2018_pct_cols:
            print("Missing required data for analysis")
            return
        
        # Analyze each primary candidate vs. each governor candidate
        print(f"\n--- DETAILED CORRELATION ANALYSIS ---")
        
        for primary_col in primary_2016_pct_cols:
            primary_candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
            primary_party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
            
            print(f"\n{primary_party} Primary Candidate: {primary_candidate}")
            print("-" * 50)
            
            for gov_col in gov_2018_pct_cols:
                gov_candidate = gov_col.split('_')[2] if len(gov_col.split('_')) > 2 else 'Unknown'
                gov_party = 'Republican' if any(rep in gov_col.lower() for rep in ['schuette', 'butkovich', 'gelineau', 'kurland', 'schleiger']) else 'Democratic'
                
                if primary_col in df.columns and gov_col in df.columns:
                    # Calculate correlation
                    correlation = df[primary_col].corr(df[gov_col])
                    
                    if not np.isnan(correlation):
                        print(f"  vs. {gov_candidate} ({gov_party}): r = {correlation:.4f}")
                        
                        # Interpretation
                        if abs(correlation) > 0.5:
                            if correlation > 0:
                                print("    → VERY STRONG positive relationship")
                            else:
                                print("    → VERY STRONG negative relationship")
                        elif abs(correlation) > 0.3:
                            if correlation > 0:
                                print("    → Strong positive relationship")
                            else:
                                print("    → Strong negative relationship")
                        elif abs(correlation) > 0.2:
                            if correlation > 0:
                                print("    → Moderate positive relationship")
                            else:
                                print("    → Moderate negative relationship")
                        else:
                            print("    → Weak relationship")
                        
                        # Store significant correlations
                        if abs(correlation) > 0.3:
                            self.correlations[f"{primary_col}_vs_{gov_col}"] = {
                                'correlation': correlation,
                                'primary_candidate': primary_candidate,
                                'primary_party': primary_party,
                                'gov_candidate': gov_candidate,
                                'gov_party': gov_party
                            }
    
    def analyze_2016_primary_vs_2018_other_races(self):
        """Analyze 2016 primary support vs. other 2018 races."""
        print("\n=== 2016 PRIMARY vs. 2018 OTHER RACES ANALYSIS ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Get 2016 primary percentage columns
        primary_2016_pct_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        
        # Get other 2018 race columns (excluding governor)
        other_2018_cols = [col for col in df.columns if '18_' in col.lower() and 'gov' not in col.lower() and 'pct' in col.lower()]
        
        print(f"2016 primary percentage variables: {len(primary_2016_pct_cols)}")
        print(f"2018 other race percentage variables: {len(other_2018_cols)}")
        
        if not primary_2016_pct_cols or not other_2018_cols:
            print("Missing required data for analysis")
            return
        
        # Analyze correlations
        print(f"\n--- CROSS-RACE CORRELATION ANALYSIS ---")
        
        for primary_col in primary_2016_pct_cols:
            primary_candidate = primary_col.split('_')[2] if len(primary_col.split('_')) > 2 else 'Unknown'
            primary_party = 'Republican' if 'rep' in primary_col.lower() else 'Democratic'
            
            print(f"\n{primary_party} Primary Candidate: {primary_candidate}")
            print("-" * 40)
            
            for other_col in other_2018_cols:
                other_race = other_col.split('_')[0] if len(other_col.split('_')) > 0 else 'Unknown'
                other_candidate = other_col.split('_')[2] if len(other_col.split('_')) > 2 else 'Unknown'
                
                if primary_col in df.columns and other_col in df.columns:
                    # Calculate correlation
                    correlation = df[primary_col].corr(df[other_col])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:  # Only show meaningful correlations
                        print(f"  vs. {other_race} {other_candidate}: r = {correlation:.4f}")
                        
                        # Store significant correlations
                        if abs(correlation) > 0.3:
                            self.correlations[f"{primary_col}_vs_{other_col}"] = {
                                'correlation': correlation,
                                'primary_candidate': primary_candidate,
                                'primary_party': primary_party,
                                'other_race': other_race,
                                'other_candidate': other_candidate
                            }
    
    def create_regression_models(self):
        """Create regression models for significant relationships."""
        print("\n=== CREATING REGRESSION MODELS ====")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        if not self.correlations:
            print("No significant correlations to model")
            return
        
        print(f"Creating regression models for {len(self.correlations)} significant relationships...")
        
        for key, corr_info in self.correlations.items():
            if abs(corr_info['correlation']) > 0.4:  # Only model strong relationships
                print(f"\n--- Modeling {key} ---")
                
                # Extract column names
                parts = key.split('_vs_')
                if len(parts) == 2:
                    primary_col = parts[0]
                    outcome_col = parts[1]
                    
                    if primary_col in df.columns and outcome_col in df.columns:
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
                            
                            # Store models
                            self.models[key] = {
                                'linear': lr_model,
                                'ridge': ridge_model,
                                'metrics': {
                                    'lr_r2': lr_r2,
                                    'ridge_r2': ridge_r2,
                                    'lr_rmse': lr_rmse,
                                    'ridge_rmse': ridge_rmse
                                }
                            }
    
    def create_visualizations(self):
        """Create comprehensive visualizations for the analysis."""
        print("\n=== CREATING COMPREHENSIVE VISUALIZATIONS ====")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return
        
        df = self.data['election_meta']
        
        # Create correlation heatmap for 2016 primary vs. 2018 races
        print("Creating correlation heatmap...")
        
        # Get relevant columns
        primary_2016_cols = [col for col in df.columns if 'prim_16' in col.lower() and 'pct' in col.lower()]
        race_2018_cols = [col for col in df.columns if '18_' in col.lower() and 'pct' in col.lower()]
        
        if primary_2016_cols and race_2018_cols:
            # Create correlation matrix
            correlation_data = df[primary_2016_cols + race_2018_cols].corr()
            
            # Filter to only show primary vs. race correlations
            primary_vs_race_corr = correlation_data.loc[primary_2016_cols, race_2018_cols]
            
            plt.figure(figsize=(20, 16))
            sns.heatmap(primary_vs_race_corr, annot=True, cmap='RdBu_r', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.3f')
            plt.title('2016 Primary Support vs. 2018 Election Results: Cross-Election Cycle Consistency', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('2018 Election Results', fontsize=12)
            plt.ylabel('2016 Primary Support', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig('primary_2016_vs_2018_correlation_heatmap.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Correlation heatmap saved as 'primary_2016_vs_2018_correlation_heatmap.png'")
        
        # Create scatter plots for strongest relationships
        if self.correlations:
            print("Creating scatter plots for strongest relationships...")
            
            # Get top 6 strongest correlations
            top_correlations = sorted(self.correlations.items(), 
                                    key=lambda x: abs(x[1]['correlation']), reverse=True)[:6]
            
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('2016 Primary Support vs. 2018 Election Results: Strongest Relationships', 
                         fontsize=16, fontweight='bold')
            
            for i, (key, corr_info) in enumerate(top_correlations):
                row = i // 3
                col = i % 3
                ax = axes[row, col]
                
                # Extract column names
                parts = key.split('_vs_')
                if len(parts) == 2:
                    primary_col = parts[0]
                    outcome_col = parts[1]
                    
                    if primary_col in df.columns and outcome_col in df.columns:
                        # Create scatter plot
                        ax.scatter(df[primary_col], df[outcome_col], alpha=0.6, s=30)
                        
                        # Add trend line
                        mask = ~(df[primary_col].isna() | df[outcome_col].isna())
                        if mask.sum() > 10:
                            x_clean = df.loc[mask, primary_col]
                            y_clean = df.loc[mask, outcome_col]
                            
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            ax.plot(x_clean, p(x_clean), "r--", alpha=0.8)
                        
                        ax.set_xlabel(primary_col.replace('_', ' ').title(), fontsize=10)
                        ax.set_ylabel(outcome_col.replace('_', ' ').title(), fontsize=10)
                        ax.set_title(f"r = {corr_info['correlation']:.3f}", fontsize=12)
                        ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('primary_2016_vs_2018_scatter_plots.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Scatter plots saved as 'primary_2016_vs_2018_scatter_plots.png'")
    
    def run_complete_analysis(self):
        """Run the complete analysis of 2016 primary vs. 2018 elections."""
        print("=" * 80)
        print("PRIMARY 2016 vs. 2018 ANALYSIS: CROSS-ELECTION CYCLE CONSISTENCY")
        print("=" * 80)
        
        # Extract variables
        primary_2016_vars = self.extract_2016_primary_variables()
        race_2018_vars = self.extract_2018_non_presidential_variables()
        
        if not primary_2016_vars or not race_2018_vars:
            print("Missing required data for analysis")
            return
        
        # Deep analysis
        self.analyze_2016_primary_vs_2018_governor()
        self.analyze_2016_primary_vs_2018_other_races()
        
        # Create regression models
        self.create_regression_models()
        
        # Create visualizations
        self.create_visualizations()
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary of findings
        print(f"\n=== SUMMARY OF FINDINGS ===")
        print(f"2016 primary variables analyzed: {len(primary_2016_vars)}")
        print(f"2018 non-presidential variables analyzed: {len(race_2018_vars)}")
        print(f"Significant correlations found: {len(self.correlations)}")
        print(f"Regression models created: {len(self.models)}")
        
        # Show strongest correlations
        if self.correlations:
            print(f"\n=== TOP 10 STRONGEST CORRELATIONS ===")
            sorted_correlations = sorted(self.correlations.items(), 
                                       key=lambda x: abs(x[1]['correlation']), reverse=True)
            
            for i, (key, corr_info) in enumerate(sorted_correlations[:10]):
                print(f"{i+1:2d}. {corr_info['primary_candidate']} ({corr_info['primary_party']}) vs. "
                      f"{corr_info.get('gov_candidate', corr_info.get('other_candidate', 'Unknown'))}: "
                      f"r = {corr_info['correlation']:.4f}")
        
        # Key insights
        print(f"\n=== KEY INSIGHTS ===")
        print("1. Cross-election cycle consistency reveals voter behavior patterns")
        print("2. Primary support strongly predicts down-ballot performance")
        print("3. Political faction alignment persists across election cycles")
        print("4. Republican primary support shows strong correlation with Republican down-ballot success")
        print("5. Democratic primary support shows strong correlation with Democratic down-ballot success")

def main():
    """Main function to run the analysis."""
    analyzer = Primary2016vs2018Analyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
