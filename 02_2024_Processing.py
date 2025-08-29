#!/usr/bin/env python3
"""
2024 Presidential Election Data Processing Script

This script processes the 2024 presidential election data from NYTimes API
and converts it to a standardized format for analysis.

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Election2024Processor:
    """Processes 2024 presidential election data."""
    
    def __init__(self):
        self.data_file = "2024.president.json"
        self.output_file = "2024.ft"
        self.counties_file = "michigan_counties.csv"
        
    def load_2024_data(self) -> Optional[Dict[str, Any]]:
        """Load 2024 presidential election data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
            logger.info(f"Loaded 2024 presidential data from {self.data_file}")
            return data
        except FileNotFoundError:
            logger.warning(f"{self.data_file} not found. 2024 election data not yet available.")
            return None
        except Exception as e:
            logger.error(f"Error loading {self.data_file}: {e}")
            return None
    
    def create_county_list(self) -> pd.DataFrame:
        """Create a list of Michigan counties for reference."""
        counties = [
            "Alcona", "Alger", "Allegan", "Alpena", "Antrim", "Arenac", "Baraga", "Barry", "Bay", "Benzie",
            "Berrien", "Branch", "Calhoun", "Cass", "Charlevoix", "Cheboygan", "Chippewa", "Clare", "Clinton",
            "Crawford", "Delta", "Dickinson", "Eaton", "Emmet", "Genesee", "Gladwin", "Gogebic", "Grand Traverse",
            "Gratiot", "Hillsdale", "Houghton", "Huron", "Ingham", "Ionia", "Iosco", "Iron", "Isabella", "Jackson",
            "Kalamazoo", "Kalkaska", "Keweenaw", "Lake", "Lapeer", "Leelanau", "Lenawee", "Livingston", "Luce",
            "Mackinac", "Macomb", "Manistee", "Marquette", "Mason", "Mecosta", "Menominee", "Midland", "Missaukee",
            "Monroe", "Montcalm", "Montmorency", "Muskegon", "Newaygo", "Oakland", "Oceana", "Ogemaw", "Ontonagon",
            "Osceola", "Oscoda", "Otsego", "Ottawa", "Presque Isle", "Roscommon", "Saginaw", "Sanilac", "Schoolcraft",
            "Shiawassee", "St. Clair", "St. Joseph", "Tuscola", "Van Buren", "Washtenaw", "Wayne", "Wexford"
        ]
        
        df = pd.DataFrame({
            'county': counties,
            'county_id': range(1, len(counties) + 1)
        })
        
        return df
    
    def process_2024_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Process 2024 election data into a standardized DataFrame."""
        logger.info("Processing 2024 presidential election data...")
        
        # Initialize with county list
        df = self.create_county_list()
        
        # Extract race information
        race_info = data.get('race', {})
        election_date = race_info.get('election_date', '2024-11-05')
        
        # Process candidates
        candidates = data.get('candidates', [])
        candidate_mapping = {}
        
        for candidate in candidates:
            candidate_id = candidate.get('nyt_id', '')
            candidate_key = candidate.get('candidate_key', '')
            display_name = candidate.get('display_name', '')
            
            if candidate_id and candidate_key:
                candidate_mapping[candidate_key] = {
                    'id': candidate_id,
                    'name': display_name
                }
        
        # Process county results
        counties_data = data.get('counties', [])
        
        for county_data in counties_data:
            county_name = county_data.get('name', '')
            county_fips = county_data.get('fips', '')
            
            # Find matching county in our DataFrame
            county_mask = df['county'].str.lower() == county_name.lower()
            
            if county_mask.any():
                county_idx = county_mask.idxmax()
                
                # Add FIPS code
                df.loc[county_idx, 'fips'] = county_fips
                
                # Add precinct information
                df.loc[county_idx, 'precincts_total'] = county_data.get('precincts_total', 0)
                df.loc[county_idx, 'precincts_reporting'] = county_data.get('precincts_reporting', 0)
                
                # Add vote totals
                df.loc[county_idx, 'pres_24_total'] = county_data.get('total_votes', 0)
                df.loc[county_idx, 'pres_24_expected'] = county_data.get('expected_votes', 0)
                
                # Process candidate results
                results = county_data.get('results', {})
                
                for candidate_key, vote_count in results.items():
                    if candidate_key in candidate_mapping:
                        candidate_name = candidate_mapping[candidate_key]['name'].lower().replace(' ', '_')
                        
                        # Add vote count
                        df.loc[county_idx, f'pres_24_{candidate_name}'] = vote_count
                        
                        # Calculate percentage
                        total_votes = county_data.get('total_votes', 1)
                        if total_votes > 0:
                            percentage = (vote_count / total_votes) * 100
                            df.loc[county_idx, f'pres_24_{candidate_name}_pct'] = percentage / 100  # Store as decimal
        
        # Fill missing values
        df = df.fillna(0)
        
        # Add metadata columns
        df['election_date'] = election_date
        df['data_source'] = 'nytimes'
        
        logger.info(f"Processed data for {len(df)} counties")
        return df
    
    def save_to_feather(self, df: pd.DataFrame) -> None:
        """Save processed data to Feather format."""
        try:
            df.to_feather(self.output_file)
            logger.info(f"Saved 2024 data to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving to {self.output_file}: {e}")
    
    def save_to_json(self, df: pd.DataFrame) -> None:
        """Save processed data to JSON format for consistency."""
        try:
            json_file = "2024.json"
            df.to_json(json_file, orient='records', indent=2)
            logger.info(f"Saved 2024 data to {json_file}")
        except Exception as e:
            logger.error(f"Error saving to {json_file}: {e}")
    
    def run_processing(self) -> Optional[pd.DataFrame]:
        """Main processing pipeline."""
        logger.info("Starting 2024 election data processing...")
        
        # Load data
        data = self.load_2024_data()
        
        if data is None:
            logger.info("No 2024 data available yet. Creating placeholder structure.")
            # Create placeholder DataFrame for future use
            df = self.create_county_list()
            df['election_date'] = '2024-11-05'
            df['data_source'] = 'placeholder'
            df['pres_24_total'] = 0
            df['pres_24_expected'] = 0
            df['precincts_total'] = 0
            df['precincts_reporting'] = 0
            df['fips'] = ''
            
            # Add placeholder columns for expected candidates
            placeholder_candidates = ['harris', 'trump', 'other']
            for candidate in placeholder_candidates:
                df[f'pres_24_{candidate}'] = 0
                df[f'pres_24_{candidate}_pct'] = 0.0
            
            self.save_to_feather(df)
            self.save_to_json(df)
            return df
        
        # Process data
        df = self.process_2024_data(data)
        
        # Save to both Feather and JSON formats
        self.save_to_feather(df)
        self.save_to_json(df)
        
        return df
    
    def generate_summary(self, df: pd.DataFrame) -> None:
        """Generate summary statistics for the processed data."""
        if df is None or df.empty:
            logger.warning("No data to summarize")
            return
        
        logger.info("Generating 2024 election summary...")
        
        # Basic statistics
        total_votes = df['pres_24_total'].sum()
        total_counties = len(df)
        
        print(f"\n2024 Presidential Election Summary")
        print("=" * 50)
        print(f"Total votes cast: {total_votes:,}")
        print(f"Number of counties: {total_counties}")
        
        # Candidate analysis
        candidate_cols = [col for col in df.columns if 'pres_24_' in col and 'pct' in col and 'total' not in col]
        
        if candidate_cols:
            print(f"\nCandidate Results:")
            for col in candidate_cols:
                candidate_name = col.replace('pres_24_', '').replace('_pct', '')
                vote_col = col.replace('_pct', '')
                
                if vote_col in df.columns:
                    total_votes_candidate = df[vote_col].sum()
                    percentage = (total_votes_candidate / total_votes * 100) if total_votes > 0 else 0
                    print(f"  {candidate_name.title()}: {total_votes_candidate:,} votes ({percentage:.1f}%)")
        
        # County analysis
        if 'pres_24_total' in df.columns:
            top_counties = df.nlargest(5, 'pres_24_total')[['county', 'pres_24_total']]
            print(f"\nTop 5 counties by turnout:")
            for _, row in top_counties.iterrows():
                print(f"  {row['county']}: {row['pres_24_total']:,} votes")


def main():
    """Main function to run the 2024 election processing."""
    print("2024 Presidential Election Data Processor")
    print("=" * 50)
    
    processor = Election2024Processor()
    
    # Run processing
    df = processor.run_processing()
    
    # Generate summary
    processor.generate_summary(df)
    
    print(f"\nProcessing complete!")
    if df is not None:
        print(f"Data shape: {df.shape}")
        print(f"Output file: {processor.output_file}")


if __name__ == "__main__":
    main()
