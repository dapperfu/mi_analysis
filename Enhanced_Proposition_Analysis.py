#!/usr/bin/env python3
"""
Enhanced Proposition vs. Trump Performance Analysis

This script uses sklearn for robust linear regression analysis of the relationship
between proposition voting patterns and Trump's performance.

Propositions analyzed:
- Prop 1 (2020): Change How Parks Revenue Can Be Spent
- Prop 2 (2020): Require Warrant for Electronic Data
- Prop 3 (2022): Constitutional Right to Reproductive Freedom (abortion rights)

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 12)

class EnhancedPropositionAnalyzer:
    """Enhanced analyzer using sklearn for robust regression analysis."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.data = {}
        self.combined_df = None
        self.models = {}
        self.load_all_data()
        
    def load_all_data(self):
        """Load all available election data files."""
        print("Loading election data...")
        
        # Load 2020 data for Props 1 & 2
        try:
            with open("2020.general.all.json", "r") as fp:
                self.data['2020_general_all'] = json.load(fp)
            print("✓ Loaded 2020 general all data")
        except FileNotFoundError:
            print("✗ 2020 general all data not found")
            
        # Load 2022 data for Prop 3
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
    
    def process_2020_proposals(self):
        """Process 2020 proposals (Props 1 & 2)."""
        if '2020_general_all' not in self.data:
            return None
            
        races = self.data['2020_general_all']
        proposals = [race for race in races if race.get('office') == 'Proposal']
        
        data = []
        for proposal in proposals:
            prop_num = proposal.get('race_name', '').split(':')[0].split()[-1]
            print(f"Processing {proposal.get('race_name', 'Unknown')}")
            
            for county in proposal["counties"]:
                row = {"county": county["name"]}
                total = 0
                
                # Handle the results structure
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        if "yes" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_yes"] = votes
                            total += votes
                        elif "no" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_no"] = votes
                            total += votes
                
                row[f"prop_{prop_num}_20_total"] = total
                
                # Calculate percentages
                if "results" in county:
                    for candidate_key, votes in county["results"].items():
                        if "yes" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_yes_pct"] = votes / total if total > 0 else 0
                        elif "no" in candidate_key.lower():
                            row[f"prop_{prop_num}_20_no_pct"] = votes / total if total > 0 else 0
                
                data.append(row)
        
        return pd.DataFrame(data)
    
    def process_2020_presidential(self):
        """Process 2020 presidential election data."""
        if '2020_general_all' not in self.data:
            return None
            
        races = self.data['2020_general_all']
        # Find the presidential race
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
    
    def extract_prop3_data(self):
        """Extract Prop 3 data from existing feather files or notebooks."""
        print("Attempting to extract Prop 3 data...")
        
        # Try to find Prop 3 data in existing files
        prop3_data = None
        
        # Check if we have it in the election meta analysis
        if 'election_meta' in self.data:
            df = self.data['election_meta']
            prop3_cols = [col for col in df.columns if 'prop3' in col.lower()]
            if prop3_cols:
                print(f"Found Prop 3 columns in election meta data: {prop3_cols}")
                # Extract county and Prop 3 data
                prop3_data = df[['county'] + prop3_cols].copy()
                return prop3_data
        
        # If no Prop 3 data found, create a placeholder
        print("No Prop 3 data found in existing files")
        print("Note: Prop 3 (2022) was about constitutional right to reproductive freedom")
        print("This data would be valuable for analysis but is not currently available")
        
        return None
    
    def combine_all_data(self):
        """Combine all processed data into a single DataFrame."""
        print("Combining all data...")
        
        dfs = []
        
        # Process each dataset
        df_2020_props = self.process_2020_proposals()
        if df_2020_props is not None:
            dfs.append(df_2020_props)
            print("✓ Processed 2020 proposals data")
            
        df_2020_pres = self.process_2020_presidential()
        if df_2020_pres is not None:
            dfs.append(df_2020_pres)
            print("✓ Processed 2020 presidential data")
            
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
    
    def run_enhanced_regression_analysis(self):
        """Run enhanced regression analysis using sklearn."""
        print("\n=== ENHANCED REGRESSION ANALYSIS ===")
        
        if self.combined_df is None:
            return
            
        # Find proposition columns
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
        print(f"Found {len(prop_cols)} proposition yes percentage columns: {prop_cols}")
        
        if not prop_cols:
            print("No proposition data found for analysis")
            return
        
        # Analyze each proposition with multiple regression models
        for prop_col in prop_cols:
            print(f"\n{'='*60}")
            print(f"ANALYZING: {prop_col}")
            print(f"{'='*60}")
            
            if prop_col in self.combined_df.columns and 'pres_20_trump_pct' in self.combined_df.columns:
                # Prepare data
                X = self.combined_df[prop_col].values.reshape(-1, 1)
                y = self.combined_df['pres_20_trump_pct'].values
                
                # Remove NaN values
                mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                X_clean = X[mask]
                y_clean = y[mask]
                
                if len(X_clean) < 10:
                    print(f"Insufficient data for {prop_col}: only {len(X_clean)} valid observations")
                    continue
                
                print(f"Data points: {len(X_clean)} counties")
                
                # Split data for validation
                X_train, X_test, y_train, y_test = train_test_split(
                    X_clean, y_clean, test_size=0.3, random_state=42
                )
                
                # 1. Linear Regression
                print("\n1. LINEAR REGRESSION:")
                lr_model = LinearRegression()
                lr_model.fit(X_train, y_train)
                
                # Training metrics
                y_train_pred = lr_model.predict(X_train)
                train_r2 = r2_score(y_train, y_train_pred)
                train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
                train_mae = mean_absolute_error(y_train, y_train_pred)
                
                # Test metrics
                y_test_pred = lr_model.predict(X_test)
                test_r2 = r2_score(y_test, y_test_pred)
                test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
                test_mae = mean_absolute_error(y_test, y_test_pred)
                
                print(f"  Training R²: {train_r2:.4f}")
                print(f"  Training RMSE: {train_rmse:.4f}")
                print(f"  Training MAE: {train_mae:.4f}")
                print(f"  Test R²: {test_r2:.4f}")
                print(f"  Test RMSE: {test_rmse:.4f}")
                print(f"  Test MAE: {test_mae:.4f}")
                print(f"  Slope: {lr_model.coef_[0]:.4f}")
                print(f"  Intercept: {lr_model.intercept_:.4f}")
                
                # Cross-validation
                cv_scores = cross_val_score(lr_model, X_clean, y_clean, cv=5, scoring='r2')
                print(f"  Cross-validation R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
                
                # 2. Ridge Regression
                print("\n2. RIDGE REGRESSION:")
                ridge_model = Ridge(alpha=1.0)
                ridge_model.fit(X_train, y_train)
                
                y_test_pred_ridge = ridge_model.predict(X_test)
                test_r2_ridge = r2_score(y_test, y_test_pred_ridge)
                print(f"  Test R²: {test_r2_ridge:.4f}")
                print(f"  Slope: {ridge_model.coef_[0]:.4f}")
                
                # 3. Random Forest
                print("\n3. RANDOM FOREST:")
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                rf_model.fit(X_train, y_train)
                
                y_test_pred_rf = rf_model.predict(X_test)
                test_r2_rf = r2_score(y_test, y_test_pred_rf)
                print(f"  Test R²: {test_r2_rf:.4f}")
                print(f"  Feature importance: {rf_model.feature_importances_[0]:.4f}")
                
                # Store best model
                models = {
                    'Linear': (lr_model, test_r2),
                    'Ridge': (ridge_model, test_r2_ridge),
                    'RandomForest': (rf_model, test_r2_rf)
                }
                best_model_name = max(models, key=lambda k: models[k][1])
                best_model = models[best_model_name][0]
                self.models[prop_col] = best_model
                
                print(f"\n  BEST MODEL: {best_model_name} (R² = {models[best_model_name][1]:.4f})")
                
                # Correlation analysis
                correlation = np.corrcoef(X_clean.flatten(), y_clean)[0, 1]
                print(f"\n  CORRELATION ANALYSIS:")
                print(f"  Pearson correlation: {correlation:.4f}")
                print(f"  Correlation squared: {correlation**2:.4f}")
                
                # Interpretation
                if correlation > 0.3:
                    print("  → Strong positive relationship: Higher proposition support correlates with higher Trump support")
                elif correlation < -0.3:
                    print("  → Strong negative relationship: Higher proposition support correlates with lower Trump support")
                elif abs(correlation) < 0.1:
                    print("  → Weak relationship: Little correlation between proposition support and Trump performance")
                else:
                    print("  → Moderate relationship: Some correlation between proposition support and Trump performance")
    
    def create_enhanced_visualizations(self):
        """Create enhanced visualizations with regression lines and confidence intervals."""
        print("\n=== CREATING ENHANCED VISUALIZATIONS ===")
        
        if self.combined_df is None:
            return
            
        # Find proposition columns
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
        
        if not prop_cols:
            print("No proposition data found for plotting")
            return
        
        # Create subplots
        n_props = len(prop_cols)
        fig, axes = plt.subplots(2, n_props, figsize=(5*n_props, 12))
        if n_props == 1:
            axes = axes.reshape(2, 1)
        
        fig.suptitle('Enhanced Proposition vs. Trump Performance Analysis', fontsize=16, fontweight='bold')
        
        for i, prop_col in enumerate(prop_cols):
            # Get data for this proposition
            x_data = self.combined_df[prop_col]
            y_data = self.combined_df['pres_20_trump_pct']
            
            # Remove NaN values
            mask = ~(np.isnan(x_data) | np.isnan(y_data))
            x_clean = x_data[mask]
            y_clean = y_data[mask]
            
            if len(x_clean) > 0:
                # Top plot: Scatter with regression line
                ax_top = axes[0, i]
                
                # Scatter plot
                ax_top.scatter(x_clean, y_clean, alpha=0.6, s=50, color='steelblue')
                
                # Add trend line
                if len(x_clean) > 1:
                    z = np.polyfit(x_clean, y_clean, 1)
                    p = np.poly1d(z)
                    x_range = np.linspace(x_clean.min(), x_clean.max(), 100)
                    ax_top.plot(x_range, p(x_range), "r--", alpha=0.8, linewidth=2, label='Linear Trend')
                    
                    # Calculate correlation
                    correlation = np.corrcoef(x_clean, y_clean)[0, 1]
                    ax_top.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax_top.transAxes, 
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                    
                    # Add R²
                    r2 = correlation**2
                    ax_top.text(0.05, 0.88, f'R² = {r2:.3f}', transform=ax_top.transAxes, 
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                
                # Labels and title
                prop_name = prop_col.replace('_', ' ').replace('pct', '').title()
                ax_top.set_xlabel(f'{prop_name} Support (%)')
                ax_top.set_ylabel('Trump 2020 Performance (%)')
                ax_top.set_title(f'{prop_name} vs. Trump 2020')
                ax_top.grid(True, alpha=0.3)
                ax_top.legend()
                
                # Add reference lines
                ax_top.axhline(y=0.5, color='black', linestyle='-', alpha=0.3)
                ax_top.axvline(x=0.5, color='black', linestyle='-', alpha=0.3)
                
                # Bottom plot: Residuals
                ax_bottom = axes[1, i]
                
                if len(x_clean) > 1 and prop_col in self.models:
                    model = self.models[prop_col]
                    y_pred = model.predict(x_clean.values.reshape(-1, 1))
                    residuals = y_clean.values - y_pred
                    
                    ax_bottom.scatter(y_pred, residuals, alpha=0.6, s=50, color='orange')
                    ax_bottom.axhline(y=0, color='red', linestyle='--', alpha=0.8)
                    ax_bottom.set_xlabel('Predicted Trump Performance (%)')
                    ax_bottom.set_ylabel('Residuals')
                    ax_bottom.set_title(f'{prop_name} - Residual Plot')
                    ax_bottom.grid(True, alpha=0.3)
                    
                    # Add residual statistics
                    residual_std = np.std(residuals)
                    ax_bottom.text(0.05, 0.95, f'σ = {residual_std:.3f}', transform=ax_bottom.transAxes, 
                                  bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('enhanced_proposition_trump_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Enhanced plot saved as 'enhanced_proposition_trump_analysis.png'")
    
    def run_complete_analysis(self):
        """Run the complete enhanced analysis."""
        print("=" * 80)
        print("ENHANCED PROPOSITION vs. TRUMP PERFORMANCE ANALYSIS")
        print("=" * 80)
        
        # Combine all data
        self.combine_all_data()
        
        if self.combined_df is None:
            print("Failed to combine data. Exiting.")
            return
        
        # Run enhanced regression analysis
        self.run_enhanced_regression_analysis()
        
        # Create enhanced visualizations
        self.create_enhanced_visualizations()
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(self.combined_df)}")
        print(f"  Variables: {len(self.combined_df.columns)}")
        
        # Show available proposition data
        prop_cols = [col for col in self.combined_df.columns if 'prop' in col.lower()]
        print(f"  Proposition variables: {len(prop_cols)}")
        for col in prop_cols:
            print(f"    - {col}")

def main():
    """Main function to run the enhanced analysis."""
    analyzer = EnhancedPropositionAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
