#!/usr/bin/env python3
"""
Michigan 2024 Presidential Election Map Generator

This script creates a county-level map of Michigan showing the 2024 presidential
election results, using actual data from the 2024.json file.

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
from shapely.geometry import Polygon


class Michigan2024ElectionMapper:
    """
    A class for creating the 2024 Michigan presidential election result map.
    
    This class creates a county-level map showing which candidate won each county
    and the margin of victory, similar to NYTimes-style election maps.
    """
    
    def __init__(self, output_dir: str = "maps") -> None:
        """
        Initialize the Michigan 2024 Election Mapper.
        
        Parameters
        ----------
        output_dir : str
            Directory to save generated maps
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.michigan_counties: Optional[gpd.GeoDataFrame] = None
        self.election_data: Optional[pd.DataFrame] = None
        
    def create_michigan_counties(self) -> gpd.GeoDataFrame:
        """
        Create Michigan county boundaries manually.
        
        Returns
        -------
        geopandas.GeoDataFrame
            County boundaries for Michigan with county names and geometries
        """
        # Define Michigan counties with approximate coordinates
        michigan_counties_data = [
            ('Alcona', [(-83.8, 44.5), (-83.3, 44.5), (-83.3, 45.0), (-83.8, 45.0)]),
            ('Alger', [(-87.0, 46.0), (-86.5, 46.0), (-86.5, 46.5), (-87.0, 46.5)]),
            ('Allegan', [(-86.0, 42.5), (-85.5, 42.5), (-85.5, 43.0), (-86.0, 43.0)]),
            ('Alpena', [(-83.8, 45.0), (-83.3, 45.0), (-83.3, 45.5), (-83.8, 45.5)]),
            ('Antrim', [(-85.5, 44.5), (-85.0, 44.5), (-85.0, 45.0), (-85.5, 45.0)]),
            ('Arenac', [(-84.0, 44.0), (-83.5, 44.0), (-83.5, 44.5), (-84.0, 44.5)]),
            ('Baraga', [(-88.5, 46.5), (-88.0, 46.5), (-88.0, 47.0), (-88.5, 47.0)]),
            ('Barry', [(-85.5, 42.5), (-85.0, 42.5), (-85.0, 43.0), (-85.5, 43.0)]),
            ('Bay', [(-84.2, 43.5), (-83.7, 43.5), (-83.7, 44.0), (-84.2, 44.0)]),
            ('Benzie', [(-86.8, 44.5), (-86.3, 44.5), (-86.3, 45.0), (-86.8, 45.0)]),
            ('Berrien', [(-86.5, 41.5), (-86.0, 41.5), (-86.0, 42.0), (-86.5, 42.0)]),
            ('Branch', [(-85.3, 41.5), (-84.8, 41.5), (-84.8, 42.0), (-85.3, 42.0)]),
            ('Calhoun', [(-85.2, 42.0), (-84.8, 42.0), (-84.8, 42.5), (-85.2, 42.5)]),
            ('Cass', [(-86.0, 41.5), (-85.5, 41.5), (-85.5, 42.0), (-86.0, 42.0)]),
            ('Charlevoix', [(-85.3, 45.0), (-84.8, 45.0), (-84.8, 45.5), (-85.3, 45.5)]),
            ('Cheboygan', [(-84.8, 45.0), (-84.3, 45.0), (-84.3, 45.5), (-84.8, 45.5)]),
            ('Chippewa', [(-85.0, 46.0), (-84.5, 46.0), (-84.5, 46.5), (-85.0, 46.5)]),
            ('Clare', [(-85.0, 44.0), (-84.5, 44.0), (-84.5, 44.5), (-85.0, 44.5)]),
            ('Clinton', [(-84.8, 42.5), (-84.3, 42.5), (-84.3, 43.0), (-84.8, 43.0)]),
            ('Crawford', [(-84.8, 44.5), (-84.3, 44.5), (-84.3, 45.0), (-84.8, 45.0)]),
            ('Delta', [(-87.0, 45.5), (-86.5, 45.5), (-86.5, 46.0), (-87.0, 46.0)]),
            ('Dickinson', [(-88.0, 45.5), (-87.5, 45.5), (-87.5, 46.0), (-88.0, 46.0)]),
            ('Eaton', [(-85.0, 42.5), (-84.5, 42.5), (-84.5, 43.0), (-85.0, 43.0)]),
            ('Emmet', [(-85.0, 45.0), (-84.5, 45.0), (-84.5, 45.5), (-85.0, 45.5)]),
            ('Genesee', [(-83.8, 42.8), (-83.2, 42.8), (-83.2, 43.2), (-83.8, 43.2)]),
            ('Gladwin', [(-84.8, 44.0), (-84.3, 44.0), (-84.3, 44.5), (-84.8, 44.5)]),
            ('Gogebic', [(-90.0, 46.0), (-89.5, 46.0), (-89.5, 46.5), (-90.0, 46.5)]),
            ('Grand Traverse', [(-85.8, 44.5), (-85.3, 44.5), (-85.3, 45.0), (-85.8, 45.0)]),
            ('Gratiot', [(-84.8, 43.0), (-84.3, 43.0), (-84.3, 43.5), (-84.8, 43.5)]),
            ('Hillsdale', [(-84.8, 41.5), (-84.3, 41.5), (-84.3, 42.0), (-84.8, 42.0)]),
            ('Houghton', [(-89.0, 46.5), (-88.5, 46.5), (-88.5, 47.0), (-89.0, 47.0)]),
            ('Huron', [(-83.5, 43.5), (-83.0, 43.5), (-83.0, 44.0), (-83.5, 44.0)]),
            ('Ingham', [(-84.5, 42.5), (-84.0, 42.5), (-84.0, 43.0), (-84.5, 43.0)]),
            ('Ionia', [(-85.3, 42.5), (-84.8, 42.5), (-84.8, 43.0), (-85.3, 43.0)]),
            ('Iosco', [(-83.8, 44.0), (-83.3, 44.0), (-83.3, 44.5), (-83.8, 44.5)]),
            ('Iron', [(-88.5, 46.0), (-88.0, 46.0), (-88.0, 46.5), (-88.5, 46.5)]),
            ('Isabella', [(-85.3, 43.5), (-84.8, 43.5), (-84.8, 44.0), (-85.3, 44.0)]),
            ('Jackson', [(-84.5, 42.0), (-84.0, 42.0), (-84.0, 42.5), (-84.5, 42.5)]),
            ('Kalamazoo', [(-85.8, 42.0), (-85.2, 42.0), (-85.2, 42.5), (-85.8, 42.5)]),
            ('Kalkaska', [(-85.3, 44.5), (-84.8, 44.5), (-84.8, 45.0), (-85.3, 45.0)]),
            ('Kent', [(-85.8, 42.8), (-85.2, 42.8), (-85.2, 43.2), (-85.8, 43.2)]),
            ('Keweenaw', [(-88.5, 47.0), (-88.0, 47.0), (-88.0, 47.5), (-88.5, 47.5)]),
            ('Lake', [(-85.8, 43.5), (-85.3, 43.5), (-85.3, 44.0), (-85.8, 44.0)]),
            ('Lapeer', [(-83.5, 42.5), (-83.0, 42.5), (-83.0, 43.0), (-83.5, 43.0)]),
            ('Leelanau', [(-86.0, 44.5), (-85.5, 44.5), (-85.5, 45.0), (-86.0, 45.0)]),
            ('Lenawee', [(-84.0, 41.5), (-83.5, 41.5), (-83.5, 42.0), (-84.0, 42.0)]),
            ('Livingston', [(-84.0, 42.5), (-83.5, 42.5), (-83.5, 43.0), (-84.0, 43.0)]),
            ('Luce', [(-85.5, 46.0), (-85.0, 46.0), (-85.0, 46.5), (-85.5, 46.5)]),
            ('Mackinac', [(-85.5, 45.5), (-85.0, 45.5), (-85.0, 46.0), (-85.5, 46.0)]),
            ('Macomb', [(-83.0, 42.5), (-82.5, 42.5), (-82.5, 43.0), (-83.0, 43.0)]),
            ('Manistee', [(-86.8, 44.0), (-86.3, 44.0), (-86.3, 44.5), (-86.8, 44.5)]),
            ('Marquette', [(-87.5, 46.0), (-87.0, 46.0), (-87.0, 46.5), (-87.5, 46.5)]),
            ('Mason', [(-86.5, 44.0), (-86.0, 44.0), (-86.0, 44.5), (-86.5, 44.5)]),
            ('Mecosta', [(-85.8, 43.0), (-85.3, 43.0), (-85.3, 43.5), (-85.8, 43.5)]),
            ('Menominee', [(-87.5, 45.0), (-87.0, 45.0), (-87.0, 45.5), (-87.5, 45.5)]),
            ('Midland', [(-84.5, 43.5), (-84.0, 43.5), (-84.0, 44.0), (-84.5, 44.0)]),
            ('Missaukee', [(-85.5, 44.0), (-85.0, 44.0), (-85.0, 44.5), (-85.5, 44.5)]),
            ('Monroe', [(-83.5, 41.5), (-83.0, 41.5), (-83.0, 42.0), (-83.5, 42.0)]),
            ('Montcalm', [(-85.5, 43.0), (-85.0, 43.0), (-85.0, 43.5), (-85.5, 43.5)]),
            ('Muskegon', [(-86.5, 43.0), (-86.0, 43.0), (-86.0, 43.5), (-86.5, 43.5)]),
            ('Newaygo', [(-86.0, 43.0), (-85.5, 43.0), (-85.5, 43.5), (-86.0, 43.5)]),
            ('Oakland', [(-83.5, 42.5), (-82.8, 42.5), (-82.8, 43.0), (-83.5, 43.0)]),
            ('Oceana', [(-86.5, 43.5), (-86.0, 43.5), (-86.0, 44.0), (-86.5, 44.0)]),
            ('Ogemaw', [(-84.3, 44.0), (-83.8, 44.0), (-83.8, 44.5), (-84.3, 44.5)]),
            ('Ontonagon', [(-89.5, 46.5), (-89.0, 46.5), (-89.0, 47.0), (-89.5, 47.0)]),
            ('Osceola', [(-85.5, 43.5), (-85.0, 43.5), (-85.0, 44.0), (-85.5, 44.0)]),
            ('Oscoda', [(-84.5, 44.5), (-84.0, 44.5), (-84.0, 45.0), (-84.5, 45.0)]),
            ('Otsego', [(-84.8, 44.5), (-84.3, 44.5), (-84.3, 45.0), (-84.8, 45.0)]),
            ('Ottawa', [(-86.2, 42.5), (-85.8, 42.5), (-85.8, 43.0), (-86.2, 43.0)]),
            ('Presque Isle', [(-84.3, 45.0), (-83.8, 45.0), (-83.8, 45.5), (-84.3, 45.5)]),
            ('Roscommon', [(-84.8, 44.0), (-84.3, 44.0), (-84.3, 44.5), (-84.8, 44.5)]),
            ('Saginaw', [(-84.2, 43.0), (-83.8, 43.0), (-83.8, 43.5), (-84.2, 43.5)]),
            ('Sanilac', [(-83.0, 43.0), (-82.5, 43.0), (-82.5, 43.5), (-83.0, 43.5)]),
            ('Schoolcraft', [(-86.5, 45.5), (-86.0, 45.5), (-86.0, 46.0), (-86.5, 46.0)]),
            ('Shiawassee', [(-84.5, 42.5), (-84.0, 42.5), (-84.0, 43.0), (-84.5, 43.0)]),
            ('St. Clair', [(-82.8, 42.5), (-82.3, 42.5), (-82.3, 43.0), (-82.8, 43.0)]),
            ('St. Joseph', [(-85.8, 41.5), (-85.3, 41.5), (-85.3, 42.0), (-85.8, 42.0)]),
            ('Tuscola', [(-83.8, 43.0), (-83.3, 43.0), (-83.3, 43.5), (-83.8, 43.5)]),
            ('Van Buren', [(-86.2, 42.0), (-85.8, 42.0), (-85.8, 42.5), (-86.2, 42.5)]),
            ('Washtenaw', [(-84.0, 42.0), (-83.5, 42.0), (-83.5, 42.5), (-84.0, 42.5)]),
            ('Wayne', [(-83.5, 42.0), (-82.8, 42.0), (-82.8, 42.5), (-83.5, 42.5)]),
            ('Wexford', [(-85.8, 44.0), (-85.3, 44.0), (-85.3, 44.5), (-85.8, 44.5)])
        ]
        
        # Create GeoDataFrame
        counties_list = []
        for county_name, coords in michigan_counties_data:
            # Create a polygon from the coordinates
            polygon = Polygon(coords)
            counties_list.append({
                'county_name': county_name,
                'geometry': polygon
            })
        
        michigan_counties = gpd.GeoDataFrame(counties_list, crs="EPSG:4326")
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
        
        self.election_data = df
        return df
    
    def create_2024_election_map(
        self,
        title: str = "Michigan 2024 Presidential Election Results",
        filename: str = "michigan_2024_election_map.png"
    ) -> str:
        """
        Create the 2024 Michigan presidential election result map.
        
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
            self.create_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        # Merge election data with county geometries
        merged_data = self.michigan_counties.merge(
            self.election_data, 
            on='county_name', 
            how='left'
        )
        
        # Create the map
        fig, ax = plt.subplots(1, 1, figsize=(14, 12))
        
        # Color counties based on winner
        colors = {'Harris': '#1f77b4', 'Trump': '#d62728'}
        merged_data['color'] = merged_data['winner'].map(colors)
        
        # Plot counties
        merged_data.plot(
            column='winner',
            ax=ax,
            edgecolor='black',
            linewidth=0.5,
            legend=True,
            categorical=True,
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1f77b4', label='Kamala Harris (D)'),
            Patch(facecolor='#d62728', label='Donald Trump (R)'),
            Patch(facecolor='lightgrey', label='No Data')
        ]
        ax.legend(handles=legend_elements, loc='upper right', title='Winner', fontsize=12)
        
        # Add summary statistics
        total_counties = len(merged_data)
        harris_counties = len(merged_data[merged_data['winner'] == 'Harris'])
        trump_counties = len(merged_data[merged_data['winner'] == 'Trump'])
        
        stats_text = f"Harris: {harris_counties} counties\nTrump: {trump_counties} counties\nTotal: {total_counties} counties"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(output_path)
    
    def create_margin_map(
        self,
        title: str = "Michigan 2024 Presidential Election Margin of Victory",
        filename: str = "michigan_2024_margin_map.png"
    ) -> str:
        """
        Create a map showing the margin of victory for each county.
        
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
            self.create_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        # Merge election data with county geometries
        merged_data = self.michigan_counties.merge(
            self.election_data, 
            on='county_name', 
            how='left'
        )
        
        # Create the map
        fig, ax = plt.subplots(1, 1, figsize=(14, 12))
        
        # Plot counties with continuous color scale based on margin
        merged_data.plot(
            column='margin',
            ax=ax,
            edgecolor='black',
            linewidth=0.5,
            legend=True,
            cmap='RdBu_r',
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Add summary statistics
        avg_margin = merged_data['margin'].mean()
        max_margin = merged_data['margin'].max()
        
        stats_text = f"Average Margin: {avg_margin:.1%}\nMax Margin: {max_margin:.1%}"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(output_path)


def main() -> None:
    """Main function to create the 2024 Michigan election maps."""
    # Create mapper instance
    mapper = Michigan2024ElectionMapper()
    
    # Create the main election result map
    print("Creating 2024 Michigan presidential election map...")
    election_map_path = mapper.create_2024_election_map()
    print(f"Election map created: {election_map_path}")
    
    # Create the margin of victory map
    print("Creating margin of victory map...")
    margin_map_path = mapper.create_margin_map()
    print(f"Margin map created: {margin_map_path}")
    
    print("Map generation complete!")
    print(f"\nFiles created:")
    print(f"  - {election_map_path}")
    print(f"  - {margin_map_path}")


if __name__ == "__main__":
    main()
