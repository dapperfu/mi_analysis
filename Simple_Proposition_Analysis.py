#!/usr/bin/env python3
"""
Simplified Proposition vs. Trump Performance Analysis

This script analyzes the relationship between 2020 proposition voting patterns and
Trump's performance, using existing processed data.

Propositions analyzed:
- Prop 1 (2020): Change How Parks Revenue Can Be Spent
- Prop 2 (2020): Require Warrant for Electronic Data

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
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 10)

def analyze_propositions_vs_trump():
    """Analyze 2020 propositions vs. Trump performance."""
    
    print("=== PROPOSITION vs. TRUMP PERFORMANCE ANALYSIS ===")
    
    # Load 2020 proposal data
    try:
        with open("2020.general.all.json", "r") as fp:
            data_2020 = json.load(fp)
        print("✓ Loaded 2020 general all data")
    except FileNotFoundError:
        print("✗ 2020 general all data not found")
        return
    
    # Find proposals
    proposals = [race for race in data_2020 if race.get('office') == 'Proposal']
    print(f"Found {len(proposals)} proposals:")
    for prop in proposals:
        print(f"  - {prop.get('race_name', 'Unknown')}")
    
    # Find presidential race
    pres_race = None
    for race in data_2020:
        if race.get('office') == 'President':
            pres_race = race
            break
    
    if not pres_race:
        print("No presidential race found")
        return
    
    # Process proposal data
    prop_data = []
    for proposal in proposals:
        prop_num = proposal.get('race_name', '').split(':')[0].split()[-1]
        print(f"\nProcessing {proposal.get('race_name', 'Unknown')}")
        
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
            
            prop_data.append(row)
    
    df_props = pd.DataFrame(prop_data)
    print(f"✓ Processed proposal data: {len(df_props)} counties")
    
    # Process presidential data
    pres_data = []
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
        
        pres_data.append(row)
    
    df_pres = pd.DataFrame(pres_data)
    print(f"✓ Processed presidential data: {len(df_pres)} counties")
    
    # Merge data
    df_combined = df_props.merge(df_pres, on="county", how="outer")
    print(f"✓ Combined data: {len(df_combined)} counties, {len(df_combined.columns)} columns")
    
    # Show available columns
    prop_cols = [col for col in df_combined.columns if 'prop' in col.lower() and 'pct' in col and 'yes' in col]
    print(f"\nProposition columns: {prop_cols}")
    
    # Analyze relationships
    print("\n=== PROPOSITION vs. TRUMP PERFORMANCE ANALYSIS ===")
    
    for prop_col in prop_cols:
        print(f"\n--- Analyzing {prop_col} ---")
        
        if prop_col in df_combined.columns and 'pres_20_trump_pct' in df_combined.columns:
            # Calculate correlation
            correlation = df_combined[prop_col].corr(df_combined['pres_20_trump_pct'])
            print(f"Correlation with Trump 2020 performance: {correlation:.4f}")
            
            # Linear regression
            X = df_combined[prop_col].values.reshape(-1, 1)
            y = df_combined['pres_20_trump_pct'].values
            
            # Remove NaN values
            mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
            X_clean = X[mask]
            y_clean = y[mask]
            
            if len(X_clean) > 0:
                reg = LinearRegression().fit(X_clean, y_clean)
                r2 = r2_score(y_clean, reg.predict(X_clean))
                print(f"R² score: {r2:.4f}")
                print(f"Slope: {reg.coef_[0]:.4f}")
                print(f"Intercept: {reg.intercept_:.4f}")
                
                # Interpretation
                if correlation > 0.3:
                    print("→ Strong positive relationship: Higher proposition support correlates with higher Trump support")
                elif correlation < -0.3:
                    print("→ Strong negative relationship: Higher proposition support correlates with lower Trump support")
                elif abs(correlation) < 0.1:
                    print("→ Weak relationship: Little correlation between proposition support and Trump performance")
                else:
                    print("→ Moderate relationship: Some correlation between proposition support and Trump performance")
    
    # Create visualization
    create_proposition_trump_plot(df_combined, prop_cols)
    
    return df_combined

def create_proposition_trump_plot(df, prop_cols):
    """Create the main plot showing proposition support vs. Trump performance."""
    print("\n=== CREATING PROPOSITION vs. TRUMP PERFORMANCE PLOT ===")
    
    if not prop_cols:
        print("No proposition data found for plotting")
        return
    
    # Create subplots
    fig, axes = plt.subplots(1, len(prop_cols), figsize=(5*len(prop_cols), 8))
    if len(prop_cols) == 1:
        axes = [axes]
    
    fig.suptitle('Proposition Support vs. Trump 2020 Performance', fontsize=16, fontweight='bold')
    
    for i, prop_col in enumerate(prop_cols):
        ax = axes[i]
        
        # Get data for this proposition
        x_data = df[prop_col]
        y_data = df['pres_20_trump_pct']
        
        # Remove NaN values
        mask = ~(np.isnan(x_data) | np.isnan(y_data))
        x_clean = x_data[mask]
        y_clean = y_data[mask]
        
        if len(x_clean) > 0:
            # Scatter plot
            ax.scatter(x_clean, y_clean, alpha=0.6, s=50)
            
            # Add trend line
            if len(x_clean) > 1:
                z = np.polyfit(x_clean, y_clean, 1)
                p = np.poly1d(z)
                ax.plot(x_clean, p(x_clean), "r--", alpha=0.8, linewidth=2)
                
                # Calculate correlation
                correlation = np.corrcoef(x_clean, y_clean)[0, 1]
                ax.text(0.05, 0.95, f'r = {correlation:.3f}', transform=ax.transAxes, 
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Labels and title
            prop_name = prop_col.replace('_', ' ').replace('pct', '').title()
            ax.set_xlabel(f'{prop_name} Support (%)')
            ax.set_ylabel('Trump 2020 Performance (%)')
            ax.set_title(f'{prop_name} vs. Trump 2020')
            ax.grid(True, alpha=0.3)
            
            # Add horizontal line at y=0.5 (50% Trump support)
            ax.axhline(y=0.5, color='black', linestyle='-', alpha=0.3)
            
            # Add vertical line at x=0.5 (50% proposition support)
            ax.axvline(x=0.5, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('proposition_trump_analysis_2020.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✓ Plot saved as 'proposition_trump_analysis_2020.png'")

def analyze_cannabis_connection():
    """Analyze potential cannabis voting connection."""
    print("\n=== CANNABIS VOTING CONNECTION ANALYSIS ===")
    
    print("Note: Cannabis legalization in Michigan was passed via ballot initiative in 2018")
    print("This analysis focuses on Props 1, 2, and 3 from 2020-2022")
    print("\nCannabis legalization voting patterns:")
    print("- 2018: Proposal 1 (Recreational Marijuana) - PASSED with 56.1%")
    print("- This suggests cannabis-friendly voters may have different political preferences")
    print("\nTo analyze cannabis voting vs. Trump support:")
    print("1. We'd need 2018 cannabis legalization data by county")
    print("2. Compare with 2020 Trump performance")
    print("3. Look for negative correlation (cannabis support vs. Trump support)")

def main():
    """Main function to run the analysis."""
    print("=" * 70)
    print("PROPOSITION vs. TRUMP PERFORMANCE ANALYSIS (2020)")
    print("=" * 70)
    
    # Run the main analysis
    df = analyze_propositions_vs_trump()
    
    if df is not None:
        # Analyze cannabis connection
        analyze_cannabis_connection()
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        
        # Summary statistics
        print(f"\nDataset Summary:")
        print(f"  Counties: {len(df)}")
        print(f"  Variables: {len(df.columns)}")
        
        # Show available proposition data
        prop_cols = [col for col in df.columns if 'prop' in col.lower()]
        print(f"  Proposition variables: {len(prop_cols)}")
        for col in prop_cols:
            print(f"    - {col}")

if __name__ == "__main__":
    main()
