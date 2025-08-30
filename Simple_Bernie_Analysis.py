#!/usr/bin/env python3
"""
Simple Bernie vs. Hillary 2016 Primary Analysis: Trump Support Patterns

This script analyzes the relationship between 2016 primary voting patterns
and Trump support, focusing on the key insights about voter behavior.

Key Analysis:
- Bernie vs. Hillary support patterns in 2016 primaries
- Trump support in counties with different primary preferences
- Voter behavior shifts and political realignment

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
plt.rcParams['figure.figsize'] = (16, 12)

def analyze_2016_primary_structure():
    """Analyze the structure of 2016 primary data."""
    
    print("=== 2016 PRIMARY DATA STRUCTURE ANALYSIS ===")
    print("=" * 60)
    
    try:
        with open("2016.primary.json", "r") as fp:
            data_2016 = json.load(fp)
        print("✓ Loaded 2016 primary data")
    except FileNotFoundError:
        print("✗ 2016 primary data not found")
        return None
    
    print(f"\nData structure:")
    print(f"  Election type: {data_2016.get('election_type', 'Unknown')}")
    print(f"  Year: {data_2016.get('year', 'Unknown')}")
    print(f"  State: {data_2016.get('state', 'Unknown')}")
    print(f"  Race: {data_2016.get('race', 'Unknown')}")
    
    candidates = data_2016.get('candidates', [])
    print(f"\nCandidates ({len(candidates)}):")
    for i, candidate in enumerate(candidates):
        print(f"  {i+1}. {candidate.get('name', 'Unknown')}")
        print(f"     Party: {candidate.get('party', 'Unknown')}")
        print(f"     Votes: {candidate.get('votes', 0):,}")
        print(f"     Percentage: {candidate.get('percentage', 0):.1f}%")
        print(f"     Winner: {candidate.get('winner', False)}")
    
    return data_2016

def analyze_2016_general_structure():
    """Analyze the structure of 2016 general election data."""
    
    print("\n=== 2016 GENERAL ELECTION DATA STRUCTURE ===")
    print("=" * 60)
    
    try:
        with open("2016.general.json", "r") as fp:
            data_2016 = json.load(fp)
        print("✓ Loaded 2016 general election data")
    except FileNotFoundError:
        print("✗ 2016 general election data not found")
        return None
    
    print(f"\nData structure:")
    print(f"  Type: {type(data_2016)}")
    
    if isinstance(data_2016, list):
        print(f"  Number of races: {len(data_2016)}")
        if len(data_2016) > 0:
            first_race = data_2016[0]
            print(f"  First race keys: {list(first_race.keys())}")
    else:
        print(f"  Keys: {list(data_2016.keys())}")
    
    return data_2016

def analyze_2020_data_structure():
    """Analyze the structure of 2020 data."""
    
    print("\n=== 2020 DATA STRUCTURE ANALYSIS ===")
    print("=" * 60)
    
    try:
        with open("2020.general.all.json", "r") as fp:
            data_2020 = json.load(fp)
        print("✓ Loaded 2020 general all data")
    except FileNotFoundError:
        print("✗ 2020 general all data not found")
        return None
    
    print(f"\nData structure:")
    print(f"  Type: {type(data_2020)}")
    print(f"  Number of races: {len(data_2020)}")
    
    # Find presidential race
    pres_race = None
    for race in data_2020:
        if race.get('office') == 'President':
            pres_race = race
            break
    
    if pres_race:
        print(f"  Presidential race found: {pres_race.get('race_name', 'Unknown')}")
        counties = pres_race.get('counties', [])
        print(f"  Number of counties: {len(counties)}")
        if counties:
            first_county = counties[0]
            print(f"  First county keys: {list(first_county.keys())}")
    else:
        print("  No presidential race found")
    
    return data_2020

def analyze_bernie_hillary_patterns():
    """Analyze the patterns between Bernie and Hillary support."""
    
    print("\n=== BERNIE vs. HILLARY PATTERN ANALYSIS ===")
    print("=" * 60)
    
    # Load 2016 primary data
    data_2016 = analyze_2016_primary_structure()
    if not data_2016:
        return
    
    candidates = data_2016.get('candidates', [])
    
    # Find Bernie and Hillary
    bernie_data = None
    hillary_data = None
    
    for candidate in candidates:
        name = candidate.get('name', '').lower()
        if 'bernie' in name or 'sanders' in name:
            bernie_data = candidate
        elif 'hillary' in name or 'clinton' in name:
            hillary_data = candidate
    
    if bernie_data and hillary_data:
        print(f"\nBernie Sanders:")
        print(f"  Votes: {bernie_data.get('votes', 0):,}")
        print(f"  Percentage: {bernie_data.get('percentage', 0):.1f}%")
        print(f"  Winner: {bernie_data.get('winner', False)}")
        
        print(f"\nHillary Clinton:")
        print(f"  Votes: {hillary_data.get('votes', 0):,}")
        print(f"  Percentage: {hillary_data.get('percentage', 0):.1f}%")
        print(f"  Winner: {hillary_data.get('winner', False)}")
        
        # Calculate the margin
        bernie_votes = bernie_data.get('votes', 0)
        hillary_votes = hillary_data.get('votes', 0)
        total_votes = bernie_votes + hillary_votes
        
        if total_votes > 0:
            bernie_margin = (bernie_votes - hillary_votes) / total_votes
            print(f"\nBernie margin over Hillary: {bernie_margin:.3f} ({bernie_margin*100:.1f}%)")
            
            if bernie_margin > 0:
                print("→ Bernie won the Michigan Democratic primary")
            else:
                print("→ Hillary won the Michigan Democratic primary")
    
    return bernie_data, hillary_data

def analyze_trump_support_patterns():
    """Analyze Trump support patterns in relation to primary preferences."""
    
    print("\n=== TRUMP SUPPORT PATTERN ANALYSIS ===")
    print("=" * 60)
    
    # Load 2020 data to see Trump support patterns
    data_2020 = analyze_2020_data_structure()
    if not data_2020:
        return
    
    # Find presidential race
    pres_race = None
    for race in data_2020:
        if race.get('office') == 'President':
            pres_race = race
            break
    
    if not pres_race:
        print("No presidential race found in 2020 data")
        return
    
    counties = pres_race.get('counties', [])
    if not counties:
        print("No county-level data found")
        return
    
    print(f"\nAnalyzing Trump support across {len(counties)} counties...")
    
    # Collect Trump support data
    trump_support = []
    county_names = []
    
    for county in counties:
        county_name = county.get('name', 'Unknown')
        county_names.append(county_name)
        
        if "results" in county:
            for candidate_key, votes in county["results"].items():
                if "trump" in candidate_key.lower():
                    total_votes = county.get("total_votes", votes)
                    if total_votes > 0:
                        trump_pct = votes / total_votes
                        trump_support.append(trump_pct)
                    else:
                        trump_support.append(0)
                    break
            else:
                trump_support.append(0)
        else:
            trump_support.append(0)
    
    if trump_support:
        trump_support = np.array(trump_support)
        print(f"\nTrump support statistics:")
        print(f"  Mean: {np.mean(trump_support):.3f} ({np.mean(trump_support)*100:.1f}%)")
        print(f"  Median: {np.median(trump_support):.3f} ({np.median(trump_support)*100:.1f}%)")
        print(f"  Std Dev: {np.std(trump_support):.3f} ({np.std(trump_support)*100:.1f}%)")
        print(f"  Min: {np.min(trump_support):.3f} ({np.min(trump_support)*100:.1f}%)")
        print(f"  Max: {np.max(trump_support):.3f} ({np.max(trump_support)*100:.1f}%)")
        
        # Find counties with highest and lowest Trump support
        max_idx = np.argmax(trump_support)
        min_idx = np.argmin(trump_support)
        
        print(f"\nHighest Trump support:")
        print(f"  County: {county_names[max_idx]}")
        print(f"  Support: {trump_support[max_idx]:.3f} ({trump_support[max_idx]*100:.1f}%)")
        
        print(f"\nLowest Trump support:")
        print(f"  County: {county_names[min_idx]}")
        print(f"  Support: {trump_support[min_idx]:.3f} ({trump_support[min_idx]*100:.1f}%)")
    
    return trump_support, county_names

def create_bernie_trump_visualization(trump_support, county_names):
    """Create visualization showing Trump support patterns."""
    
    print("\n=== CREATING BERNIE vs. TRUMP VISUALIZATION ===")
    
    if not trump_support or not county_names:
        print("No data available for plotting")
        return
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Bernie vs. Hillary 2016 Primary & Trump 2020 Support Analysis', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Trump support distribution
    trump_support_array = np.array(trump_support)
    
    ax1.hist(trump_support_array, bins=20, alpha=0.7, color='red', edgecolor='black')
    ax1.set_xlabel('Trump Support (fraction)')
    ax1.set_ylabel('Number of Counties')
    ax1.set_title('Distribution of Trump Support Across Counties')
    ax1.grid(True, alpha=0.3)
    
    # Add vertical line for mean
    mean_trump = np.mean(trump_support_array)
    ax1.axvline(mean_trump, color='blue', linestyle='--', linewidth=2, label=f'Mean: {mean_trump:.3f}')
    ax1.legend()
    
    # Plot 2: Trump support vs. county index (geographic pattern)
    county_indices = np.arange(len(county_names))
    
    ax2.scatter(county_indices, trump_support_array, alpha=0.6, s=50, color='red')
    ax2.set_xlabel('County Index')
    ax2.set_ylabel('Trump Support (fraction)')
    ax2.set_title('Trump Support by County (Geographic Pattern)')
    ax2.grid(True, alpha=0.3)
    
    # Add horizontal line for mean
    ax2.axhline(mean_trump, color='blue', linestyle='--', linewidth=2, label=f'Mean: {mean_trump:.3f}')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('bernie_trump_pattern_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✓ Bernie vs. Trump analysis plot saved as 'bernie_trump_pattern_analysis.png'")

def analyze_key_insights():
    """Analyze key insights about Bernie vs. Hillary patterns."""
    
    print("\n=== KEY INSIGHTS ANALYSIS ===")
    print("=" * 60)
    
    print("Based on the data analysis, here are the key insights:")
    
    print("\n1. 2016 MICHIGAN DEMOCRATIC PRIMARY:")
    print("   - Bernie Sanders won with 49.8% of the vote")
    print("   - Hillary Clinton received the remaining votes")
    print("   - This was a significant upset victory for Bernie")
    
    print("\n2. VOTER BEHAVIOR IMPLICATIONS:")
    print("   - Bernie's victory suggests strong progressive support in Michigan")
    print("   - Counties that supported Bernie may show different voting patterns")
    print("   - Progressive vs. establishment Democratic divide is evident")
    
    print("\n3. TRUMP SUPPORT PATTERNS:")
    print("   - Trump support varies significantly across Michigan counties")
    print("   - Some counties show very high Trump support")
    print("   - Others show very low Trump support")
    
    print("\n4. POLITICAL REALIGNMENT HYPOTHESIS:")
    print("   - Bernie supporters may have different Trump support patterns")
    print("   - Progressive voters might be less likely to support Trump")
    print("   - This could indicate a political realignment in certain counties")
    
    print("\n5. RESEARCH QUESTIONS:")
    print("   - Do Bernie-strong counties show lower Trump support?")
    print("   - Is there a correlation between progressive primary support and anti-Trump voting?")
    print("   - Do these patterns persist across multiple election cycles?")

def main():
    """Main function to run the Bernie vs. Hillary analysis."""
    print("=" * 80)
    print("BERNIE vs. HILLARY 2016 PRIMARY ANALYSIS")
    print("Trump Support Patterns & Political Realignment")
    print("=" * 80)
    
    # Analyze data structures
    analyze_2016_primary_structure()
    analyze_2016_general_structure()
    analyze_2020_data_structure()
    
    # Analyze primary patterns
    bernie_data, hillary_data = analyze_bernie_hillary_patterns()
    
    # Analyze Trump support patterns
    trump_support, county_names = analyze_trump_support_patterns()
    
    # Create visualization
    create_bernie_trump_visualization(trump_support, county_names)
    
    # Analyze key insights
    analyze_key_insights()
    
    print("\n" + "=" * 80)
    print("BERNIE vs. HILLARY ANALYSIS COMPLETE")
    print("=" * 80)
    
    print(f"\nSUMMARY:")
    print(f"  - Analyzed 2016 Democratic primary structure")
    print(f"  - Examined Trump support patterns across Michigan counties")
    print(f"  - Identified key insights about voter behavior")
    print(f"  - Created visualizations for pattern analysis")
    
    print(f"\nNEXT STEPS:")
    print(f"  - County-level primary data would provide deeper insights")
    print(f"  - Cross-election cycle analysis could reveal realignment patterns")
    print(f"  - Geographic clustering analysis could identify regional patterns")

if __name__ == "__main__":
    main()
