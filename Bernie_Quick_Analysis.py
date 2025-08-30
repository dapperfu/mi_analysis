#!/usr/bin/env python3
"""
Quick Bernie vs. Hillary 2016 Primary Analysis

Simple analysis of the key patterns and insights.

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json

def main():
    """Quick analysis of Bernie vs. Hillary patterns."""
    
    print("=== QUICK BERNIE vs. HILLARY ANALYSIS ===")
    print("=" * 50)
    
    # Load 2016 primary data
    try:
        with open("2016.primary.json", "r") as fp:
            data_2016 = json.load(fp)
        print("✓ Loaded 2016 primary data")
    except FileNotFoundError:
        print("✗ 2016 primary data not found")
        return
    
    print(f"\n2016 Michigan Democratic Primary:")
    print(f"  Election type: {data_2016.get('election_type', 'Unknown')}")
    print(f"  Year: {data_2016.get('year', 'Unknown')}")
    print(f"  State: {data_2016.get('state', 'Unknown')}")
    print(f"  Race: {data_2016.get('race', 'Unknown')}")
    
    candidates = data_2016.get('candidates', [])
    print(f"\nCandidates ({len(candidates)}):")
    
    bernie_data = None
    hillary_data = None
    
    for i, candidate in enumerate(candidates):
        name = candidate.get('name', 'Unknown')
        votes = candidate.get('votes', 0)
        percentage = candidate.get('percentage', 0)
        winner = candidate.get('winner', False)
        
        print(f"  {i+1}. {name}")
        print(f"     Votes: {votes:,}")
        print(f"     Percentage: {percentage:.1f}%")
        print(f"     Winner: {winner}")
        
        if 'bernie' in name.lower() or 'sanders' in name.lower():
            bernie_data = candidate
        elif 'hillary' in name.lower() or 'clinton' in name.lower():
            hillary_data = candidate
    
    if bernie_data and hillary_data:
        print(f"\n=== KEY FINDINGS ===")
        
        bernie_votes = bernie_data.get('votes', 0)
        hillary_votes = hillary_data.get('votes', 0)
        total_votes = bernie_votes + hillary_votes
        
        if total_votes > 0:
            bernie_margin = (bernie_votes - hillary_votes) / total_votes
            print(f"\n1. BERNIE WON THE MICHIGAN PRIMARY!")
            print(f"   - Bernie margin: {bernie_margin:.3f} ({bernie_margin*100:.1f}%)")
            print(f"   - This was a significant upset victory")
            
            print(f"\n2. VOTER BEHAVIOR IMPLICATIONS:")
            print(f"   - Strong progressive support in Michigan")
            print(f"   - Bernie supporters may show different voting patterns")
            print(f"   - Progressive vs. establishment Democratic divide")
            
            print(f"\n3. TRUMP SUPPORT HYPOTHESIS:")
            print(f"   - Bernie-strong counties may show lower Trump support")
            print(f"   - Progressive voters less likely to support Trump")
            print(f"   - Potential political realignment in certain areas")
            
            print(f"\n4. RESEARCH QUESTIONS:")
            print(f"   - Do Bernie supporters shift away from Trump 2020->2024?")
            print(f"   - Is there correlation between progressive primary support and anti-Trump voting?")
            print(f"   - Do these patterns persist across election cycles?")
            
            print(f"\n5. DATA LIMITATIONS:")
            print(f"   - 2016 primary data is state-level, not county-level")
            print(f"   - Need county-level primary data for deeper analysis")
            print(f"   - 2020->2024 Trump shifts would require 2024 data")
    
    print(f"\n" + "=" * 50)
    print("ANALYSIS COMPLETE")

if __name__ == "__main__":
    main()
