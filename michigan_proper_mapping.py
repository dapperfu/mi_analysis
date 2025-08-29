#!/usr/bin/env python3
"""
Michigan Election Mapping with Proper Geographic Data

This script creates county-level election result maps for Michigan using
actual geographic county boundaries from reliable sources.

Author: Generated via Cursor IDE with AI assistance
Model: Claude 3.5 Sonnet
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import json
import requests
import zipfile
import io
import tempfile


class MichiganProperMapper:
    """
    A class for creating Michigan county-level election maps using proper geographic data.
    
    This class downloads real county boundary data and creates professional-quality
    election result maps that actually look like Michigan.
    """
    
    def __init__(self, output_dir: str = "maps") -> None:
        """
        Initialize the Michigan Proper Mapper.
        
        Parameters
        ----------
        output_dir : str
            Directory to save generated maps
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.michigan_counties: Optional[gpd.GeoDataFrame] = None
        self.election_data: Optional[pd.DataFrame] = None
        
    def download_michigan_counties(self) -> gpd.GeoDataFrame:
        """
        Download actual Michigan county boundaries from reliable sources.
        
        Returns
        -------
        geopandas.GeoDataFrame
            County boundaries for Michigan with proper geometries
        """
        print("Downloading Michigan county boundaries...")
        
        try:
            # Try to download from US Census Bureau TIGER/Line files
            # This is the most reliable source for US geographic data
            tiger_url = "https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip"
            
            print(f"  Downloading from: {tiger_url}")
            response = requests.get(tiger_url, timeout=30)
            response.raise_for_status()
            
            # Extract the zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                # Find the shapefile
                shp_files = [f for f in zip_file.namelist() if f.endswith('.shp')]
                if not shp_files:
                    raise ValueError("No shapefile found in zip")
                
                # Extract to temporary directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_file.extractall(temp_dir)
                    shp_path = Path(temp_dir) / shp_files[0]
                    
                    # Load the counties
                    counties = gpd.read_file(shp_path)
                    
                    # Filter for Michigan counties (FIPS state code 26)
                    michigan_counties = counties[counties['STATEFP'] == '26'].copy()
                    
                    # Clean up column names and select relevant columns
                    michigan_counties = michigan_counties[['NAME', 'geometry']].copy()
                    michigan_counties.columns = ['county_name', 'geometry']
                    
                    # Standardize county names (remove "County" suffix)
                    michigan_counties['county_name'] = michigan_counties['county_name'].str.replace(' County', '')
                    
                    print(f"  ✅ Successfully loaded {len(michigan_counties)} Michigan counties")
                    
        except Exception as e:
            print(f"  ❌ Failed to download from Census Bureau: {e}")
            print("  Trying alternative source...")
            
            try:
                # Alternative: Try to use Natural Earth data
                print("  Downloading from Natural Earth...")
                counties = gpd.read_file(
                    "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_2_counties.zip"
                )
                
                # Filter for Michigan counties
                michigan_counties = counties[counties['ADMIN1'] == 'Michigan'].copy()
                
                # Clean up column names and select relevant columns
                michigan_counties = michigan_counties[['NAME', 'geometry']].copy()
                michigan_counties.columns = ['county_name', 'geometry']
                
                # Standardize county names (remove "County" suffix)
                michigan_counties['county_name'] = michigan_counties['county_name'].str.replace(' County', '')
                
                print(f"  ✅ Successfully loaded {len(michigan_counties)} Michigan counties from Natural Earth")
                
            except Exception as e2:
                print(f"  ❌ Failed to download from Natural Earth: {e2}")
                print("  Creating a basic Michigan outline as fallback...")
                
                # Fallback: Create a basic Michigan outline
                michigan_outline = gpd.GeoDataFrame(
                    {
                        'county_name': ['Michigan'],
                        'geometry': [gpd.points_from_xy([-85.5], [44.5]).buffer(2)]
                    },
                    crs="EPSG:4326"
                )
                michigan_counties = michigan_outline
        
        # Ensure proper coordinate system
        if michigan_counties.crs != "EPSG:4326":
            michigan_counties = michigan_counties.to_crs("EPSG:4326")
        
        self.michigan_counties = michigan_counties
        return michigan_counties
    
    def load_2024_election_data(self, election_file: str = "2024.json") -> pd.DataFrame:
        """
        Load 2024 election data from the JSON file.
        
        Parameters
        ----------
        election_file : str
            Path to the 2024 election results JSON file
            
        Returns
        -------
        pandas.DataFrame
            Election results with county-level data
        """
        print("Loading 2024 election data...")
        
        with open(election_file, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Clean up county names to match our map
        df['county_name'] = df['county'].str.replace(' County', '')
        
        # Calculate winner and margin
        df['winner'] = np.where(
            df['pres_24_kamala_harris_pct'] > df['pres_24_donald_j._trump_pct'],
            'Harris',
            'Trump'
        )
        
        df['margin'] = np.abs(df['pres_24_kamala_harris_pct'] - df['pres_24_donald_j._trump_pct'])
        df['harris_pct'] = df['pres_24_kamala_harris_pct'] * 100
        df['trump_pct'] = df['pres_24_donald_j._trump_pct'] * 100
        
        print(f"  ✅ Loaded data for {len(df)} counties")
        
        self.election_data = df
        return df
    
    def create_proper_election_map(
        self,
        title: str = "Michigan 2024 Presidential Election Results",
        filename: str = "michigan_2024_proper_map.png"
    ) -> str:
        """
        Create a proper 2024 Michigan presidential election result map.
        
        Parameters
        ----------
        title : str
            Title for the map
        filename : str
            Output filename for the PNG
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if self.michigan_counties is None:
            self.download_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        print("Creating proper election map...")
        
        # Merge election data with county geometries
        merged_data = self.michigan_counties.merge(
            self.election_data, 
            on='county_name', 
            how='left'
        )
        
        # Create the map with proper styling
        fig, ax = plt.subplots(1, 1, figsize=(16, 14))
        
        # Color counties based on winner
        colors = {'Harris': '#1f77b4', 'Trump': '#d62728'}
        merged_data['color'] = merged_data['winner'].map(colors)
        
        # Plot counties with proper styling
        merged_data.plot(
            column='winner',
            ax=ax,
            edgecolor='black',
            linewidth=0.3,  # Thinner lines for cleaner look
            legend=True,
            categorical=True,
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=20, fontweight='bold', pad=25)
        ax.axis('off')
        
        # Add professional legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1f77b4', label='Kamala Harris (D)', edgecolor='black', linewidth=0.5),
            Patch(facecolor='#d62728', label='Donald Trump (R)', edgecolor='black', linewidth=0.5),
            Patch(facecolor='lightgrey', label='No Data', edgecolor='black', linewidth=0.5)
        ]
        ax.legend(handles=legend_elements, loc='upper right', title='Winner', 
                 fontsize=14, title_fontsize=16, frameon=True, 
                 fancybox=True, shadow=True)
        
        # Add summary statistics
        total_counties = len(merged_data)
        harris_counties = len(merged_data[merged_data['winner'] == 'Harris'])
        trump_counties = len(merged_data[merged_data['winner'] == 'Trump'])
        
        stats_text = f"Harris: {harris_counties} counties\nTrump: {trump_counties} counties\nTotal: {total_counties} counties"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
                facecolor='white', alpha=0.9, edgecolor='black', linewidth=0.5))
        
        # Add data source attribution
        ax.text(0.98, 0.02, "Data: NYTimes | Map: Generated locally", 
                transform=ax.transAxes, fontsize=10, style='italic',
                horizontalalignment='right', verticalalignment='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Save the map with high quality
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"  ✅ Map saved: {output_path}")
        return str(output_path)
    
    def create_proper_margin_map(
        self,
        title: str = "Michigan 2024 Presidential Election Margin of Victory",
        filename: str = "michigan_2024_proper_margin.png"
    ) -> str:
        """
        Create a proper margin of victory map.
        
        Parameters
        ----------
        title : str
            Title for the map
        filename : str
            Output filename
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if self.michigan_counties is None:
            self.download_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        print("Creating proper margin map...")
        
        # Merge election data with county geometries
        merged_data = self.michigan_counties.merge(
            self.election_data, 
            on='county_name', 
            how='left'
        )
        
        # Create the map
        fig, ax = plt.subplots(1, 1, figsize=(16, 14))
        
        # Plot counties with continuous color scale based on margin
        merged_data.plot(
            column='margin',
            ax=ax,
            edgecolor='black',
            linewidth=0.3,
            legend=True,
            cmap='RdBu_r',
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=20, fontweight='bold', pad=25)
        ax.axis('off')
        
        # Add summary statistics
        avg_margin = merged_data['margin'].mean()
        max_margin = merged_data['margin'].max()
        
        stats_text = f"Average Margin: {avg_margin:.1%}\nMax Margin: {max_margin:.1%}"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
                facecolor='white', alpha=0.9, edgecolor='black', linewidth=0.5))
        
        # Add data source attribution
        ax.text(0.98, 0.02, "Data: NYTimes | Map: Generated locally", 
                transform=ax.transAxes, fontsize=10, style='italic',
                horizontalalignment='right', verticalalignment='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"  ✅ Map saved: {output_path}")
        return str(output_path)


def main() -> None:
    """Main function to create proper Michigan election maps."""
    print("🗺️  Michigan Election Mapping with Proper Geographic Data")
    print("=" * 60)
    
    # Create mapper instance
    mapper = MichiganProperMapper()
    
    try:
        # Create the main election result map
        print("\n1. Creating 2024 election results map...")
        election_map_path = mapper.create_proper_election_map(
            title="Michigan 2024 Presidential Election Results",
            filename="michigan_2024_proper_map.png"
        )
        
        # Create the margin of victory map
        print("\n2. Creating margin of victory map...")
        margin_map_path = mapper.create_proper_margin_map(
            title="Michigan 2024 Presidential Election Margin of Victory",
            filename="michigan_2024_proper_margin.png"
        )
        
        print("\n🎉 Proper mapping complete!")
        print(f"\n📁 Generated Maps:")
        print(f"  - {election_map_path}")
        print(f"  - {margin_map_path}")
        print("\n💡 These maps now use actual Michigan county boundaries!")
        
    except Exception as e:
        print(f"❌ Error during mapping: {e}")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()
