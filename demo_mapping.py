#!/usr/bin/env python3
"""
Michigan Election Mapping Demonstration Script

This script demonstrates various mapping capabilities including:
- Custom county data mapping
- Different color schemes
- Multiple map types
- Interactive data exploration

Author: Generated via Cursor IDE with AI assistance
Model: Claude 3.5 Sonnet
"""

from michigan_election_map import MichiganElectionMapper
from michigan_2024_election_map import Michigan2024ElectionMapper
import pandas as pd


def demonstrate_custom_mapping() -> None:
    """Demonstrate custom county data mapping."""
    print("🗺️  Demonstrating Custom County Mapping...")
    
    # Create mapper instance
    mapper = MichiganElectionMapper()
    
    # Create custom data for demonstration
    # This could be turnout, demographics, or any county-level metric
    custom_county_data = {
        'Wayne': 85.2,      # High value
        'Oakland': 72.1,    # Medium-high value
        'Macomb': 58.9,     # Medium value
        'Kent': 45.3,       # Medium-low value
        'Genesee': 78.6,    # High value
        'Washtenaw': 89.4,  # Very high value
        'Ingham': 76.8,     # High value
        'Saginaw': 62.3,    # Medium value
        'Ottawa': 41.7,     # Low value
        'Kalamazoo': 68.9   # Medium-high value
    }
    
    # Create custom map with different colormap
    print("  Creating custom county values map...")
    custom_map_path = mapper.create_custom_map(
        county_values=custom_county_data,
        value_column="custom_metric",
        title="Michigan Custom County Metric (Sample Data)",
        filename="michigan_custom_demo.png",
        colormap="viridis"  # Different colormap for variety
    )
    print(f"  ✅ Custom map created: {custom_map_path}")
    
    # Create another map with different colormap
    print("  Creating alternative colormap map...")
    alt_map_path = mapper.create_custom_map(
        county_values=custom_county_data,
        value_column="custom_metric",
        title="Michigan Custom County Metric - Alternative View",
        filename="michigan_custom_alt.png",
        colormap="plasma"  # Another colormap option
    )
    print(f"  ✅ Alternative map created: {alt_map_path}")


def demonstrate_2024_data_analysis() -> None:
    """Demonstrate 2024 election data analysis and mapping."""
    print("\n🗳️  Demonstrating 2024 Election Data Analysis...")
    
    # Create 2024 mapper instance
    mapper = Michigan2024ElectionMapper()
    
    # Load the actual 2024 election data
    print("  Loading 2024 election data...")
    election_data = mapper.load_2024_election_data()
    
    # Show some data statistics
    print(f"  📊 Data loaded: {len(election_data)} counties")
    print(f"  🏆 Harris won: {len(election_data[election_data['winner'] == 'Harris'])} counties")
    print(f"  🏆 Trump won: {len(election_data[election_data['winner'] == 'Trump'])} counties")
    
    # Show margin statistics
    avg_margin = election_data['margin'].mean()
    max_margin = election_data['margin'].max()
    print(f"  📈 Average margin: {avg_margin:.1%}")
    print(f"  📈 Maximum margin: {max_margin:.1%}")
    
    # Create the main election map
    print("  Creating 2024 election results map...")
    election_map_path = mapper.create_2024_election_map(
        title="Michigan 2024 Presidential Election - Live Results",
        filename="michigan_2024_live_demo.png"
    )
    print(f"  ✅ Election map created: {election_map_path}")
    
    # Create margin of victory map
    print("  Creating margin of victory map...")
    margin_map_path = mapper.create_margin_map(
        title="Michigan 2024 Presidential Election - Margin Analysis",
        filename="michigan_2024_margin_demo.png"
    )
    print(f"  ✅ Margin map created: {margin_map_path}")


def demonstrate_data_exploration() -> None:
    """Demonstrate data exploration capabilities."""
    print("\n🔍 Demonstrating Data Exploration...")
    
    # Load 2024 data for analysis
    mapper = Michigan2024ElectionMapper()
    election_data = mapper.load_2024_election_data()
    
    # Find closest races (smallest margins)
    print("  📊 Top 5 Closest Races:")
    closest_races = election_data.nsmallest(5, 'margin')[['county', 'winner', 'margin']]
    for _, race in closest_races.iterrows():
        print(f"    {race['county']}: {race['winner']} by {race['margin']:.1%}")
    
    # Find biggest landslides
    print("  📊 Top 5 Biggest Landslides:")
    biggest_landslides = election_data.nlargest(5, 'margin')[['county', 'winner', 'margin']]
    for _, race in biggest_landslides.iterrows():
        print(f"    {race['county']}: {race['winner']} by {race['margin']:.1%}")
    
    # County count by winner
    winner_counts = election_data['winner'].value_counts()
    print(f"  🏆 County Count by Winner:")
    for winner, count in winner_counts.items():
        print(f"    {winner}: {count} counties")


def main() -> None:
    """Main demonstration function."""
    print("🚀 Michigan Election Mapping System - Full Demonstration")
    print("=" * 60)
    
    try:
        # Demonstrate custom mapping
        demonstrate_custom_mapping()
        
        # Demonstrate 2024 data analysis
        demonstrate_2024_data_analysis()
        
        # Demonstrate data exploration
        demonstrate_data_exploration()
        
        print("\n🎉 Demonstration Complete!")
        print("\n📁 Generated Maps:")
        print("  - michigan_custom_demo.png (Custom county data)")
        print("  - michigan_custom_alt.png (Alternative colormap)")
        print("  - michigan_2024_live_demo.png (2024 election results)")
        print("  - michigan_2024_margin_demo.png (2024 margin analysis)")
        print("\n💡 You can now use these maps for:")
        print("  - Presentations and reports")
        print("  - Social media and communications")
        print("  - Academic research and analysis")
        print("  - News articles and publications")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("Please check that all dependencies are installed and data files are available.")


if __name__ == "__main__":
    main()
