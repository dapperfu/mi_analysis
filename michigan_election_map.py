#!/usr/bin/env python3
"""
Michigan Election County Map Generator

This module provides functionality to create county-level election result maps
for the state of Michigan, similar to NYTimes-style election maps.

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


class MichiganElectionMapper:
    """
    A class for creating county-level election result maps for Michigan.
    
    This class handles creating geographic data, processing election results,
    and generating styled maps with county-level coloring based on election outcomes.
    """
    
    def __init__(self, output_dir: str = "maps") -> None:
        """
        Initialize the Michigan Election Mapper.
        
        Parameters
        ----------
        output_dir : str
            Directory to save generated maps
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.michigan_counties: Optional[gpd.GeoDataFrame] = None
        
    def create_michigan_counties(self) -> gpd.GeoDataFrame:
        """
        Create Michigan county boundaries manually since external sources may be unreliable.
        
        Returns
        -------
        geopandas.GeoDataFrame
            County boundaries for Michigan with county names and geometries
        """
        # Define Michigan counties with approximate coordinates
        # This is a simplified representation - for production use, get actual county boundary files
        michigan_counties_data = [
            # Major counties with approximate bounding boxes
            ('Wayne', [(-83.5, 42.0), (-82.8, 42.0), (-82.8, 42.5), (-83.5, 42.5)]),
            ('Oakland', [(-83.5, 42.5), (-82.8, 42.5), (-82.8, 43.0), (-83.5, 43.0)]),
            ('Macomb', [(-83.0, 42.5), (-82.5, 42.5), (-82.5, 43.0), (-83.0, 43.0)]),
            ('Kent', [(-85.8, 42.8), (-85.2, 42.8), (-85.2, 43.2), (-85.8, 43.2)]),
            ('Genesee', [(-83.8, 42.8), (-83.2, 42.8), (-83.2, 43.2), (-83.8, 43.2)]),
            ('Washtenaw', [(-84.0, 42.0), (-83.5, 42.0), (-83.5, 42.5), (-84.0, 42.5)]),
            ('Ingham', [(-84.5, 42.5), (-84.0, 42.5), (-84.0, 43.0), (-84.5, 43.0)]),
            ('Saginaw', [(-84.2, 43.0), (-83.8, 43.0), (-83.8, 43.5), (-84.2, 43.5)]),
            ('Ottawa', [(-86.2, 42.5), (-85.8, 42.5), (-85.8, 43.0), (-86.2, 43.0)]),
            ('Kalamazoo', [(-85.8, 42.0), (-85.2, 42.0), (-85.2, 42.5), (-85.8, 42.5)]),
            ('Calhoun', [(-85.2, 42.0), (-84.8, 42.0), (-84.8, 42.5), (-85.2, 42.5)]),
            ('Jackson', [(-84.5, 42.0), (-84.0, 42.0), (-84.0, 42.5), (-84.5, 42.5)]),
            ('Lenawee', [(-84.0, 41.5), (-83.5, 41.5), (-83.5, 42.0), (-84.0, 42.0)]),
            ('Monroe', [(-83.5, 41.5), (-83.0, 41.5), (-83.0, 42.0), (-83.5, 42.0)]),
            ('St. Clair', [(-82.8, 42.5), (-82.3, 42.5), (-82.3, 43.0), (-82.8, 43.0)]),
            ('Livingston', [(-84.0, 42.5), (-83.5, 42.5), (-83.5, 43.0), (-84.0, 43.0)]),
            ('Shiawassee', [(-84.5, 42.5), (-84.0, 42.5), (-84.0, 43.0), (-84.5, 43.0)]),
            ('Clinton', [(-84.8, 42.5), (-84.3, 42.5), (-84.3, 43.0), (-84.8, 43.0)]),
            ('Eaton', [(-85.0, 42.5), (-84.5, 42.5), (-84.5, 43.0), (-85.0, 43.0)]),
            ('Barry', [(-85.5, 42.5), (-85.0, 42.5), (-85.0, 43.0), (-85.5, 43.0)]),
            ('Allegan', [(-86.0, 42.5), (-85.5, 42.5), (-85.5, 43.0), (-86.0, 43.0)]),
            ('Van Buren', [(-86.2, 42.0), (-85.8, 42.0), (-85.8, 42.5), (-86.2, 42.5)]),
            ('Berrien', [(-86.5, 41.5), (-86.0, 41.5), (-86.0, 42.0), (-86.5, 42.0)]),
            ('Cass', [(-86.0, 41.5), (-85.5, 41.5), (-85.5, 42.0), (-86.0, 42.0)]),
            ('St. Joseph', [(-85.8, 41.5), (-85.3, 41.5), (-85.3, 42.0), (-85.8, 42.0)]),
            ('Branch', [(-85.3, 41.5), (-84.8, 41.5), (-84.8, 42.0), (-85.3, 42.0)]),
            ('Hillsdale', [(-84.8, 41.5), (-84.3, 41.5), (-84.3, 42.0), (-84.8, 42.0)]),
            ('Ionia', [(-85.3, 42.5), (-84.8, 42.5), (-84.8, 43.0), (-85.3, 43.0)]),
            ('Montcalm', [(-85.5, 43.0), (-85.0, 43.0), (-85.0, 43.5), (-85.5, 43.5)]),
            ('Mecosta', [(-85.8, 43.0), (-85.3, 43.0), (-85.3, 43.5), (-85.8, 43.5)]),
            ('Newaygo', [(-86.0, 43.0), (-85.5, 43.0), (-85.5, 43.5), (-86.0, 43.5)]),
            ('Muskegon', [(-86.5, 43.0), (-86.0, 43.0), (-86.0, 43.5), (-86.5, 43.5)]),
            ('Oceana', [(-86.5, 43.5), (-86.0, 43.5), (-86.0, 44.0), (-86.5, 44.0)]),
            ('Mason', [(-86.5, 44.0), (-86.0, 44.0), (-86.0, 44.5), (-86.5, 44.5)]),
            ('Manistee', [(-86.8, 44.0), (-86.3, 44.0), (-86.3, 44.5), (-86.8, 44.5)]),
            ('Benzie', [(-86.8, 44.5), (-86.3, 44.5), (-86.3, 45.0), (-86.8, 45.0)]),
            ('Leelanau', [(-86.0, 44.5), (-85.5, 44.5), (-85.5, 45.0), (-86.0, 45.0)]),
            ('Grand Traverse', [(-85.8, 44.5), (-85.3, 44.5), (-85.3, 45.0), (-85.8, 45.0)]),
            ('Antrim', [(-85.5, 44.5), (-85.0, 44.5), (-85.0, 45.0), (-85.5, 45.0)]),
            ('Charlevoix', [(-85.3, 45.0), (-84.8, 45.0), (-84.8, 45.5), (-85.3, 45.5)]),
            ('Emmet', [(-85.0, 45.0), (-84.5, 45.0), (-84.5, 45.5), (-85.0, 45.5)]),
            ('Cheboygan', [(-84.8, 45.0), (-84.3, 45.0), (-84.3, 45.5), (-84.8, 45.5)]),
            ('Presque Isle', [(-84.3, 45.0), (-83.8, 45.0), (-83.8, 45.5), (-84.3, 45.5)]),
            ('Alpena', [(-83.8, 45.0), (-83.3, 45.0), (-83.3, 45.5), (-83.8, 45.5)]),
            ('Alcona', [(-83.8, 44.5), (-83.3, 44.5), (-83.3, 45.0), (-83.8, 45.0)]),
            ('Iosco', [(-83.8, 44.0), (-83.3, 44.0), (-83.3, 44.5), (-83.8, 44.5)]),
            ('Arenac', [(-84.0, 44.0), (-83.5, 44.0), (-83.5, 44.5), (-84.0, 44.5)]),
            ('Bay', [(-84.2, 43.5), (-83.7, 43.5), (-83.7, 44.0), (-84.2, 44.0)]),
            ('Midland', [(-84.5, 43.5), (-84.0, 43.5), (-84.0, 44.0), (-84.5, 44.0)]),
            ('Gladwin', [(-84.8, 44.0), (-84.3, 44.0), (-84.3, 44.5), (-84.8, 44.5)]),
            ('Clare', [(-85.0, 44.0), (-84.5, 44.0), (-84.5, 44.5), (-85.0, 44.5)]),
            ('Isabella', [(-85.3, 43.5), (-84.8, 43.5), (-84.8, 44.0), (-85.3, 44.0)]),
            ('Gratiot', [(-84.8, 43.0), (-84.3, 43.0), (-84.3, 43.5), (-84.8, 43.5)]),
            ('Saginaw', [(-84.2, 43.0), (-83.8, 43.0), (-83.8, 43.5), (-84.2, 43.5)]),
            ('Tuscola', [(-83.8, 43.0), (-83.3, 43.0), (-83.3, 43.5), (-83.8, 43.5)]),
            ('Huron', [(-83.5, 43.5), (-83.0, 43.5), (-83.0, 44.0), (-83.5, 44.0)]),
            ('Sanilac', [(-83.0, 43.0), (-82.5, 43.0), (-82.5, 43.5), (-83.0, 43.5)]),
            ('Lapeer', [(-83.5, 42.5), (-83.0, 42.5), (-83.0, 43.0), (-83.5, 43.0)]),
            ('Dickinson', [(-88.0, 45.5), (-87.5, 45.5), (-87.5, 46.0), (-88.0, 46.0)]),
            ('Iron', [(-88.5, 46.0), (-88.0, 46.0), (-88.0, 46.5), (-88.5, 46.5)]),
            ('Gogebic', [(-90.0, 46.0), (-89.5, 46.0), (-89.5, 46.5), (-90.0, 46.5)]),
            ('Ontonagon', [(-89.5, 46.5), (-89.0, 46.5), (-89.0, 47.0), (-89.5, 47.0)]),
            ('Houghton', [(-89.0, 46.5), (-88.5, 46.5), (-88.5, 47.0), (-89.0, 47.0)]),
            ('Keweenaw', [(-88.5, 47.0), (-88.0, 47.0), (-88.0, 47.5), (-88.5, 47.5)]),
            ('Marquette', [(-87.5, 46.0), (-87.0, 46.0), (-87.0, 46.5), (-87.5, 46.5)]),
            ('Alger', [(-87.0, 46.0), (-86.5, 46.0), (-86.5, 46.5), (-87.0, 46.5)]),
            ('Schoolcraft', [(-86.5, 45.5), (-86.0, 45.5), (-86.0, 46.0), (-86.5, 46.0)]),
            ('Mackinac', [(-85.5, 45.5), (-85.0, 45.5), (-85.0, 46.0), (-85.5, 46.0)]),
            ('Chippewa', [(-85.0, 46.0), (-84.5, 46.0), (-84.5, 46.5), (-85.0, 46.5)]),
            ('Luce', [(-85.5, 46.0), (-85.0, 46.0), (-85.0, 46.5), (-85.5, 46.5)]),
            ('Delta', [(-87.0, 45.5), (-86.5, 45.5), (-86.5, 46.0), (-87.0, 46.0)]),
            ('Menominee', [(-87.5, 45.0), (-87.0, 45.0), (-87.0, 45.5), (-87.5, 45.5)]),
            ('Delta', [(-87.0, 45.5), (-86.5, 45.5), (-86.5, 46.0), (-87.0, 46.0)])
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
    
    def load_election_data(self, election_file: str) -> pd.DataFrame:
        """
        Load election data from a JSON file.
        
        Parameters
        ----------
        election_file : str
            Path to the election results JSON file
            
        Returns
        -------
        pandas.DataFrame
            Election results with county-level data
        """
        with open(election_file, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame - adjust this based on your actual data structure
        # This is a placeholder - you'll need to adapt to your actual data format
        df = pd.DataFrame(data)
        return df
    
    def create_election_map(
        self,
        election_data: pd.DataFrame,
        title: str = "Michigan Presidential Election Results",
        filename: str = "michigan_election_map.png",
        color_scheme: str = "red_blue"
    ) -> str:
        """
        Create an election result map for Michigan counties.
        
        Parameters
        ----------
        election_data : pandas.DataFrame
            Election results data with county information
        title : str
            Title for the map
        filename : str
            Output filename for the PNG
        color_scheme : str
            Color scheme for the map ('red_blue', 'blue_red', or 'custom')
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if self.michigan_counties is None:
            self.create_michigan_counties()
        
        # Merge election data with county geometries
        # You'll need to adjust this based on your actual data structure
        merged_data = self.michigan_counties.copy()
        
        # Example: if you have county names and vote percentages
        # merged_data = merged_data.merge(
        #     election_data, 
        #     left_on='county_name', 
        #     right_on='county', 
        #     how='left'
        # )
        
        # For demonstration, create sample data
        np.random.seed(42)  # For reproducible results
        merged_data['dem_percentage'] = np.random.uniform(30, 70, len(merged_data))
        merged_data['rep_percentage'] = 100 - merged_data['dem_percentage']
        merged_data['winner'] = np.where(merged_data['dem_percentage'] > 50, 'Democrat', 'Republican')
        
        # Create the map
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Color counties based on winner
        colors = {'Democrat': '#1f77b4', 'Republican': '#d62728'}
        merged_data['color'] = merged_data['winner'].map(colors)
        
        # Plot counties
        merged_data.plot(
            column='winner',
            ax=ax,
            edgecolor='black',
            linewidth=0.5,
            legend=True,
            categorical=True
        )
        
        # Customize the map
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Add county labels (optional - can be crowded)
        # for idx, row in merged_data.iterrows():
        #     ax.annotate(
        #         text=row['county_name'],
        #         xy=row.geometry.centroid.coords[0],
        #         ha='center',
        #         va='center',
        #         fontsize=8
        #     )
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1f77b4', label='Democrat'),
            Patch(facecolor='#d62728', label='Republican')
        ]
        ax.legend(handles=legend_elements, loc='upper right', title='Winner')
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(output_path)
    
    def create_custom_map(
        self,
        county_values: Dict[str, float],
        value_column: str = "vote_percentage",
        title: str = "Michigan Custom Map",
        filename: str = "michigan_custom_map.png",
        colormap: str = "RdBu_r"
    ) -> str:
        """
        Create a custom map with continuous values for each county.
        
        Parameters
        ----------
        county_values : Dict[str, float]
            Dictionary mapping county names to values
        value_column : str
            Name for the value column
        title : str
            Title for the map
        filename : str
            Output filename
        colormap : str
            Matplotlib colormap name
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if self.michigan_counties is None:
            self.create_michigan_counties()
        
        # Create DataFrame from county values
        values_df = pd.DataFrame(list(county_values.items()), columns=['county_name', value_column])
        
        # Merge with county geometries
        merged_data = self.michigan_counties.merge(values_df, on='county_name', how='left')
        
        # Create the map
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Plot counties with continuous color scale
        merged_data.plot(
            column=value_column,
            ax=ax,
            edgecolor='black',
            linewidth=0.5,
            legend=True,
            cmap=colormap,
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(output_path)


def main() -> None:
    """Main function to demonstrate the Michigan Election Mapper."""
    # Create mapper instance
    mapper = MichiganElectionMapper()
    
    # Create a sample election map
    print("Creating sample Michigan election map...")
    sample_map_path = mapper.create_election_map(
        election_data=pd.DataFrame(),  # Empty for demo
        title="Michigan Presidential Election 2024 (Sample Data)",
        filename="michigan_election_2024_sample.png"
    )
    print(f"Sample map created: {sample_map_path}")
    
    # Create a custom map with sample data
    print("Creating custom Michigan map...")
    sample_values = {
        'Wayne': 75.2,
        'Oakland': 65.8,
        'Macomb': 45.3,
        'Kent': 52.1,
        'Genesee': 68.9,
        'Washtenaw': 78.4,
        'Ingham': 72.6,
        'Saginaw': 58.7,
        'Ottawa': 48.2,
        'Kalamazoo': 61.3
    }
    
    custom_map_path = mapper.create_custom_map(
        county_values=sample_values,
        value_column="dem_percentage",
        title="Michigan Democratic Vote Percentage (Sample)",
        filename="michigan_dem_percentage_sample.png",
        colormap="RdBu_r"
    )
    print(f"Custom map created: {custom_map_path}")
    
    print("Map generation complete!")


if __name__ == "__main__":
    main()
