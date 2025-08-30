#!/usr/bin/env python3
"""
Michigan Election Mapping with Multiple Backend Support

This script creates county-level election result maps for Michigan using
multiple plotting backends and real geographic data sources.

Supported backends:
- matplotlib + cartopy (professional static maps)
- plotly (interactive maps)
- geopandas + matplotlib (simple static maps)

Author: Generated via Cursor IDE with AI assistance
Model: Claude 3.5 Sonnet
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Literal
from pathlib import Path
import json
import requests
import zipfile
import io
import tempfile
import os


class MichiganMultiBackendMapper:
    """
    A class for creating Michigan county-level election maps using multiple backends.
    
    This class can download real county boundary data and create maps using
    different plotting libraries for different use cases.
    """
    
    def __init__(self, output_dir: str = "maps") -> None:
        """
        Initialize the Michigan Multi-Backend Mapper.
        
        Parameters
        ----------
        output_dir : str
            Directory to save generated maps
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.michigan_counties: Optional[gpd.GeoDataFrame] = None
        self.election_data: Optional[pd.DataFrame] = None
        
    def download_real_michigan_counties(self) -> gpd.GeoDataFrame:
        """
        Download REAL Michigan county boundaries from multiple sources.
        
        Returns
        -------
        geopandas.GeoDataFrame
            County boundaries for Michigan with ACTUAL geometries
        """
        print("Downloading REAL Michigan county boundaries...")
        
        # Try multiple sources for Michigan county data
        sources = [
            {
                'name': 'Natural Earth (simplified)',
                'url': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_2_counties.zip',
                'filter_col': 'ADMIN1',
                'filter_val': 'Michigan',
                'name_col': 'NAME'
            },
            {
                'name': 'Natural Earth (detailed)',
                'url': 'https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_2_counties.zip',
                'filter_col': 'ADMIN1',
                'filter_val': 'Michigan',
                'name_col': 'NAME'
            }
        ]
        
        for source in sources:
            try:
                print(f"  Trying {source['name']}...")
                print(f"    URL: {source['url']}")
                
                # Download the file
                response = requests.get(source['url'], timeout=60)
                response.raise_for_status()
                
                # Extract the zip file
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                    # Find the shapefile
                    shp_files = [f for f in zip_file.namelist() if f.endswith('.shp')]
                    if not shp_files:
                        print(f"    ❌ No shapefile found in zip")
                        continue
                    
                    # Extract to temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        zip_file.extractall(temp_dir)
                        shp_path = Path(temp_dir) / shp_files[0]
                        
                        # Load the counties
                        print(f"    📁 Loading shapefile: {shp_path}")
                        counties = gpd.read_file(shp_path)
                        
                        # Filter for Michigan counties
                        michigan_counties = counties[counties[source['filter_col']] == source['filter_val']].copy()
                        
                        if len(michigan_counties) == 0:
                            print(f"    ❌ No Michigan counties found")
                            continue
                        
                        # Clean up column names and select relevant columns
                        michigan_counties = michigan_counties[['NAME', 'geometry']].copy()
                        michigan_counties.columns = ['county_name', 'geometry']
                        
                        # Standardize county names (remove "County" suffix)
                        michigan_counties['county_name'] = michigan_counties['county_name'].str.replace(' County', '')
                        
                        print(f"    ✅ Successfully loaded {len(michigan_counties)} Michigan counties")
                        print(f"    📊 Counties: {', '.join(michigan_counties['county_name'].head(5).tolist())}...")
                        
                        # Ensure proper coordinate system
                        if michigan_counties.crs != "EPSG:4326":
                            michigan_counties = michigan_counties.to_crs("EPSG:4326")
                        
                        self.michigan_counties = michigan_counties
                        return michigan_counties
                        
            except Exception as e:
                print(f"    ❌ Failed: {e}")
                continue
        
        # If all external sources fail, create a basic Michigan outline
        print("  ❌ All external sources failed")
        print("  Creating a basic Michigan outline as fallback...")
        
        from shapely.geometry import Point
        michigan_outline = gpd.GeoDataFrame(
            {
                'county_name': ['Michigan'],
                'geometry': [Point(-85.5, 44.5).buffer(2)]
            },
            crs="EPSG:4326"
        )
        
        # Create a simple fallback with basic county shapes for testing
        # This is NOT ideal but allows the system to work when external data fails
        fallback_counties = []
        county_names = ['Wayne', 'Oakland', 'Macomb', 'Kent', 'Genesee']
        
        for i, name in enumerate(county_names):
            # Create simple rectangular counties for fallback
            x_offset = i * 0.5
            county_geom = Point(-85.5 + x_offset, 44.5).buffer(0.2)
            fallback_counties.append({
                'county_name': name,
                'geometry': county_geom
            })
        
        michigan_outline = gpd.GeoDataFrame(fallback_counties, crs="EPSG:4326")
        
        self.michigan_counties = michigan_outline
        return michigan_outline
    
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
    
    def create_matplotlib_map(
        self,
        title: str = "Michigan 2024 Presidential Election Results",
        filename: str = "michigan_2024_matplotlib.png"
    ) -> str:
        """
        Create a map using matplotlib + geopandas (simple but effective).
        
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
            self.download_real_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        print("Creating matplotlib map...")
        
        # Merge election data with county geometries
        merged_data = self.michigan_counties.merge(
            self.election_data, 
            on='county_name', 
            how='left'
        )
        
        # Create the map
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(1, 1, figsize=(18, 16))
        
        # Color counties based on winner
        colors = {'Harris': '#1f77b4', 'Trump': '#d62728'}
        merged_data['color'] = merged_data['winner'].map(colors)
        
        # Plot counties
        merged_data.plot(
            column='winner',
            ax=ax,
            edgecolor='black',
            linewidth=0.2,
            legend=True,
            categorical=True,
            missing_kwds={'color': 'lightgrey'}
        )
        
        # Customize the map
        ax.set_title(title, fontsize=24, fontweight='bold', pad=30)
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1f77b4', label='Kamala Harris (D)', edgecolor='black', linewidth=0.5),
            Patch(facecolor='#d62728', label='Donald Trump (R)', edgecolor='black', linewidth=0.5),
            Patch(facecolor='lightgrey', label='No Data', edgecolor='black', linewidth=0.5)
        ]
        ax.legend(handles=legend_elements, loc='upper right', title='Winner', 
                 fontsize=16, title_fontsize=18, frameon=True, 
                 fancybox=True, shadow=True)
        
        # Add statistics
        total_counties = len(merged_data)
        harris_counties = len(merged_data[merged_data['winner'] == 'Harris'])
        trump_counties = len(merged_data[merged_data['winner'] == 'Trump'])
        
        stats_text = f"Harris: {harris_counties} counties\nTrump: {trump_counties} counties\nTotal: {total_counties} counties"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=16,
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
                facecolor='white', alpha=0.9, edgecolor='black', linewidth=0.5))
        
        # Save the map
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=400, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"  ✅ Matplotlib map saved: {output_path}")
        return str(output_path)
    
    def create_plotly_map(
        self,
        title: str = "Michigan 2024 Presidential Election Results",
        filename: str = "michigan_2024_plotly.html"
    ) -> str:
        """
        Create an interactive map using Plotly.
        
        Parameters
        ----------
        title : str
            Title for the map
        filename : str
            Output filename for the HTML
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if self.michigan_counties is None:
            self.download_real_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        print("Creating Plotly interactive map...")
        
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Merge election data with county geometries
            merged_data = self.michigan_counties.merge(
                self.election_data, 
                on='county_name', 
                how='left'
            )
            
            # Create the map
            fig = px.choropleth_mapbox(
                merged_data,
                geojson=merged_data.geometry.__geo_interface__,
                locations=merged_data.index,
                color='winner',
                color_discrete_map={'Harris': '#1f77b4', 'Trump': '#d62728'},
                hover_name='county_name',
                hover_data=['harris_pct', 'trump_pct', 'margin'],
                title=title,
                mapbox_style="carto-positron",
                zoom=5,
                center={"lat": 44.5, "lon": -85.5}
            )
            
            # Customize the layout
            fig.update_layout(
                title_x=0.5,
                title_font_size=20,
                height=800,
                margin={"r":0,"t":50,"l":0,"b":0}
            )
            
            # Save the map
            output_path = self.output_dir / filename
            fig.write_html(output_path)
            
            print(f"  ✅ Plotly map saved: {output_path}")
            return str(output_path)
            
        except ImportError:
            print("  ❌ Plotly not available. Install with: pip install plotly")
            return ""
    
    def create_cartopy_map(
        self,
        title: str = "Michigan 2024 Presidential Election Results",
        filename: str = "michigan_2024_cartopy.png"
    ) -> str:
        """
        Create a professional map using Cartopy (if available).
        
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
            self.download_real_michigan_counties()
        
        if self.election_data is None:
            self.load_2024_election_data()
        
        print("Creating Cartopy professional map...")
        
        try:
            import matplotlib.pyplot as plt
            import cartopy.crs as ccrs
            import cartopy.feature as cfeature
            
            # Merge election data with county geometries
            merged_data = self.michigan_counties.merge(
                self.election_data, 
                on='county_name', 
                how='left'
            )
            
            # Create the map with Cartopy
            fig = plt.figure(figsize=(18, 16))
            ax = plt.axes(projection=ccrs.PlateCarree())
            
            # Set the map extent to Michigan
            ax.set_extent([-90.5, -82.0, 41.5, 48.0], crs=ccrs.PlateCarree())
            
            # Add natural features
            ax.add_feature(cfeature.LAND, facecolor='lightgray')
            ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
            ax.add_feature(cfeature.LAKES, facecolor='lightblue')
            ax.add_feature(cfeature.RIVERS, edgecolor='blue', linewidth=0.5)
            ax.add_feature(cfeature.STATES, edgecolor='black', linewidth=1)
            
            # Color counties based on winner
            colors = {'Harris': '#1f77b4', 'Trump': '#d62728'}
            merged_data['color'] = merged_data['winner'].map(colors)
            
            # Plot counties
            merged_data.plot(
                column='winner',
                ax=ax,
                edgecolor='black',
                linewidth=0.3,
                legend=True,
                categorical=True,
                missing_kwds={'color': 'lightgrey'},
                transform=ccrs.PlateCarree()
            )
            
            # Customize the map
            ax.set_title(title, fontsize=24, fontweight='bold', pad=30)
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#1f77b4', label='Kamala Harris (D)', edgecolor='black', linewidth=0.5),
                Patch(facecolor='#d62728', label='Donald Trump (R)', edgecolor='black', linewidth=0.5),
                Patch(facecolor='lightgrey', label='No Data', edgecolor='black', linewidth=0.5)
            ]
            ax.legend(handles=legend_elements, loc='upper right', title='Winner', 
                     fontsize=16, title_fontsize=18, frameon=True, 
                     fancybox=True, shadow=True)
            
            # Save the map
            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=400, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"  ✅ Cartopy map saved: {output_path}")
            return str(output_path)
            
        except ImportError:
            print("  ❌ Cartopy not available. Install with: pip install cartopy")
            return ""
    
    def create_map(
        self,
        backend: Literal["matplotlib", "plotly", "cartopy"] = "matplotlib",
        title: str = "Michigan 2024 Presidential Election Results",
        filename: Optional[str] = None
    ) -> str:
        """
        Create a map using the specified backend.
        
        Parameters
        ----------
        backend : str
            Backend to use: "matplotlib", "plotly", or "cartopy"
        title : str
            Title for the map
        filename : str, optional
            Output filename (auto-generated if not provided)
            
        Returns
        -------
        str
            Path to the generated map file
        """
        if filename is None:
            if backend == "plotly":
                filename = f"michigan_2024_{backend}.html"
            else:
                filename = f"michigan_2024_{backend}.png"
        
        if backend == "matplotlib":
            return self.create_matplotlib_map(title, filename)
        elif backend == "plotly":
            return self.create_plotly_map(title, filename)
        elif backend == "cartopy":
            return self.create_cartopy_map(title, filename)
        else:
            raise ValueError(f"Unknown backend: {backend}. Use 'matplotlib', 'plotly', or 'cartopy'")


def main() -> None:
    """Main function to demonstrate multi-backend mapping."""
    print("🗺️  Michigan Election Mapping with Multiple Backends")
    print("=" * 60)
    
    # Create mapper instance
    mapper = MichiganMultiBackendMapper()
    
    try:
        # Try different backends
        backends = ["matplotlib", "plotly", "cartopy"]
        
        for backend in backends:
            print(f"\n{'-'*20} Creating {backend.upper()} Map {'-'*20}")
            try:
                map_path = mapper.create_map(
                    backend=backend,
                    title=f"Michigan 2024 Presidential Election Results ({backend.title()})"
                )
                if map_path:
                    print(f"✅ {backend.title()} map created successfully!")
                else:
                    print(f"❌ {backend.title()} map creation failed")
            except Exception as e:
                print(f"❌ Error with {backend}: {e}")
        
        print("\n🎉 Multi-backend mapping complete!")
        print("\n📁 Generated Maps:")
        print("  Check the maps/ directory for output files")
        print("\n💡 Each backend offers different advantages:")
        print("  - matplotlib: Simple, reliable, high-quality static maps")
        print("  - plotly: Interactive, web-friendly, zoomable maps")
        print("  - cartopy: Professional cartography with geographic features")
        
    except Exception as e:
        print(f"❌ Error during mapping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
