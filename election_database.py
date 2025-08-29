#!/usr/bin/env python3
"""
Election Database Schema and Migration Script

This script creates a SQLite database with PonyORM to store election data
in a proper relational structure, replacing the .ft files.

Database Schema:
- Counties: Master list of Michigan counties
- Elections: Election metadata (year, type, office)
- Candidates: Candidate information
- Results: County-level election results (one-to-many from counties)

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import os
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pony.orm import *

# Database setup
db = Database()

class County(db.Entity):
    """Michigan counties table."""
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    fips_code = Optional(str)  # Federal Information Processing Standards code
    results = Set("Result")
    
    def __repr__(self) -> str:
        return f"<County: {self.name}>"

class Election(db.Entity):
    """Election metadata table."""
    id = PrimaryKey(int, auto=True)
    year = Required(int)
    election_type = Required(str)  # 'primary', 'general', 'special'
    office = Required(str)  # 'President', 'Governor', 'Attorney General', etc.
    party = Optional(str)  # For primaries
    election_date = Optional(str)
    source = Optional(str)
    results = Set("Result")
    
    def __repr__(self) -> str:
        return f"<Election: {self.year} {self.election_type} {self.office}>"

class Candidate(db.Entity):
    """Candidate information table."""
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    party = Required(str)
    nyt_id = Optional(str, nullable=True)  # New York Times identifier
    results = Set("Result")
    
    def __repr__(self) -> str:
        return f"<Candidate: {self.name} ({self.party})>"

class Result(db.Entity):
    """County-level election results table."""
    id = PrimaryKey(int, auto=True)
    county = Required(County)
    election = Required(Election)
    candidate = Required(Candidate)
    votes = Required(int)
    percentage = Optional(float)
    winner = Optional(bool)
    
    def __repr__(self) -> str:
        return f"<Result: {self.county.name} - {self.candidate.name} ({self.votes})>"

class ElectionDataMigrator:
    """Migrates election data from JSON files to the database."""
    
    def __init__(self, db_path: str = "elections.db"):
        """Initialize the migrator with database path."""
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self) -> None:
        """Set up the database connection and create tables."""
        db.bind(provider='sqlite', filename=self.db_path, create_db=True)
        db.generate_mapping(create_tables=True)
        print(f"✓ Database setup complete: {self.db_path}")
    
    def get_or_create_county(self, county_name: str) -> County:
        """Get existing county or create new one."""
        county = County.get(name=county_name)
        if county is None:
            county = County(name=county_name)
        return county
    
    def get_or_create_candidate(self, name: str, party: str, nyt_id: Union[str, None] = None) -> Candidate:
        """Get existing candidate or create new one."""
        # Try to find by name and party first
        candidate = Candidate.get(name=name, party=party)
        if candidate is None:
            candidate = Candidate(name=name, party=party, nyt_id=nyt_id)
        elif nyt_id and not candidate.nyt_id:
            candidate.nyt_id = nyt_id
        return candidate
    
    def get_or_create_election(self, year: int, election_type: str, office: str, 
                              party: Union[str, None] = None, election_date: Union[str, None] = None,
                              source: Union[str, None] = None) -> Election:
        """Get existing election or create new one."""
        # For primaries, include party in the lookup
        if election_type == 'primary':
            election = Election.get(year=year, election_type=election_type, 
                                  office=office, party=party)
        else:
            election = Election.get(year=year, election_type=election_type, 
                                  office=office, party=None)
        
        if election is None:
            election = Election(year=year, election_type=election_type, office=office,
                              party=party, election_date=election_date, source=source)
        return election
    
    def migrate_2016_data(self) -> None:
        """Migrate 2016 election data."""
        print("Migrating 2016 data...")
        
        # Migrate 2016 primary - create election record even without county data
        try:
            with open("normalized_data/normalized_2016.primary.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2016, "primary", office, 
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Create candidates from normalized data
                for candidate_data in data['candidates']:
                    first_name = candidate_data.get('first_name', '') or ""
                    last_name = candidate_data.get('last_name', '') or ""
                    candidate_name = candidate_data.get('display_name') or f"{first_name} {last_name}".strip()
                    if candidate_name:
                        party = candidate_data.get('party_id', 'Unknown').title()
                        candidate = self.get_or_create_candidate(candidate_name, party)
                        
                        # Create a placeholder result for the state total
                        # We'll need to create a "State" county for this
                        state_county = self.get_or_create_county("Michigan (State Total)")
                        
                        votes = candidate_data.get('votes', 0)
                        percentage = candidate_data.get('vote_percentage', 0)
                        winner = candidate_data.get('winner', False)
                        
                        existing_result = Result.get(county=state_county, election=election, candidate=candidate)
                        if existing_result is None:
                            Result(county=state_county, election=election, candidate=candidate, 
                                   votes=votes, percentage=percentage, winner=winner)
                
                print("✓ Migrated 2016 primary data (state totals only)")
            else:
                print("⚠️  2016 primary data doesn't have race information - skipping")
            
        except FileNotFoundError:
            print("✗ 2016 primary normalized data not found")
        
        # Migrate 2016 general - create election record even without county data
        try:
            with open("normalized_data/normalized_2016.general.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2016, "general", office, 
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Create candidates from normalized data
                for candidate_data in data['candidates']:
                    first_name = candidate_data.get('first_name', '') or ""
                    last_name = candidate_data.get('last_name', '') or ""
                    candidate_name = candidate_data.get('display_name') or f"{first_name} {last_name}".strip()
                    if candidate_name:
                        party = candidate_data.get('party_id', 'Unknown').title()
                        candidate = self.get_or_create_candidate(candidate_name, party)
                        
                        # Create a placeholder result for the state total
                        state_county = self.get_or_create_county("Michigan (State Total)")
                        
                        votes = candidate_data.get('votes', 0)
                        percentage = candidate_data.get('vote_percentage', 0)
                        winner = candidate_data.get('winner', False)
                        
                        existing_result = Result.get(county=state_county, election=election, candidate=candidate)
                        if existing_result is None:
                            Result(county=state_county, election=election, candidate=candidate, 
                                   votes=votes, percentage=percentage, winner=winner)
                
                print("✓ Migrated 2016 general data (state totals only)")
            else:
                print("⚠️  2016 general data doesn't have race information - skipping")
            
        except FileNotFoundError:
            print("✗ 2016 general normalized data not found")
    
    def migrate_2020_data(self) -> None:
        """Migrate 2020 election data."""
        print("Migrating 2020 data...")
        
        # Migrate 2020 Democratic primary - this has county-level data
        try:
            with open("normalized_data/normalized_2020.primary.dem.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2020, "primary", office, "Democrat",
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Process county-level results
                for county_data in data["counties"]:
                    county = self.get_or_create_county(county_data["name"])
                    
                    if "results" in county_data:
                        for candidate_key, votes in county_data["results"].items():
                            # Find candidate by key
                            candidate = None
                            for candidate_info in data["candidates"]:
                                if candidate_info.get("candidate_key") == candidate_key:
                                    first_name = candidate_info.get("first_name", "") or ""
                                    last_name = candidate_info.get("last_name", "") or ""
                                    candidate_name = candidate_info.get("display_name") or f"{first_name} {last_name}".strip()
                                    if candidate_name:
                                        candidate = self.get_or_create_candidate(candidate_name, "Democrat")
                                    break
                            
                            if candidate:
                                total_votes = sum(county_data["results"].values())
                                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                                
                                existing_result = Result.get(county=county, election=election, candidate=candidate)
                                if existing_result is None:
                                    Result(county=county, election=election, candidate=candidate, 
                                           votes=votes, percentage=percentage)
                
                print("✓ Migrated 2020 Democratic primary data (with county results)")
            else:
                print("⚠️  2020 primary data doesn't have race information - skipping")
            
        except FileNotFoundError:
            print("✗ 2020 Democratic primary normalized data not found")
        
        # Migrate 2020 general - create election record even without county data
        try:
            with open("normalized_data/normalized_2020.general.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2020, "general", office, 
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Create candidates from normalized data
                for candidate_data in data['candidates']:
                    first_name = candidate_data.get('first_name', '') or ""
                    last_name = candidate_data.get('last_name', '') or ""
                    candidate_name = candidate_data.get('display_name') or f"{first_name} {last_name}".strip()
                    if candidate_name:
                        party = candidate_data.get('party_id', 'Unknown').title()
                        candidate = self.get_or_create_candidate(candidate_name, party)
                        
                        # Create a placeholder result for the state total
                        state_county = self.get_or_create_county("Michigan (State Total)")
                        
                        votes = candidate_data.get('votes', 0)
                        percentage = candidate_data.get('vote_percentage', 0)
                        winner = candidate_data.get('winner', False)
                        
                        existing_result = Result.get(county=state_county, election=election, candidate=candidate)
                        if existing_result is None:
                            Result(county=state_county, election=election, candidate=candidate, 
                                   votes=votes, percentage=percentage, winner=winner)
                
                print("✓ Migrated 2020 general data (state totals only)")
            else:
                print("⚠️  2020 general data doesn't have race information - skipping")
            
        except FileNotFoundError:
            print("✗ 2020 general normalized data not found")
    
    def migrate_2022_data(self) -> None:
        """Migrate 2022 election data."""
        print("Migrating 2022 data...")
        
        try:
            with open("normalized_data/normalized_2022.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2022, "general", office, 
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Create candidates from normalized data
                for candidate_data in data['candidates']:
                    first_name = candidate_data.get('first_name', '') or ""
                    last_name = candidate_data.get('last_name', '') or ""
                    candidate_name = candidate_data.get('display_name') or f"{first_name} {last_name}".strip()
                    if candidate_name:
                        party = candidate_data.get('party_id', 'Unknown').title()
                        candidate = self.get_or_create_candidate(candidate_name, party)
                        
                        # Create a placeholder result for the state total
                        state_county = self.get_or_create_county("Michigan (State Total)")
                        
                        votes = candidate_data.get('votes', 0)
                        percentage = candidate_data.get('vote_percentage', 0)
                        winner = candidate_data.get('winner', False)
                        
                        existing_result = Result.get(county=state_county, election=election, candidate=candidate)
                        if existing_result is None:
                            Result(county=state_county, election=election, candidate=candidate, 
                                   votes=votes, percentage=percentage, winner=winner)
                
                print("✓ Migrated 2022 data (state totals only)")
            else:
                print("⚠️  2022 data doesn't have race information - skipping")
            
        except FileNotFoundError:
            print("✗ 2022 normalized data not found")
    
    def _determine_party_from_nyt_id(self, nyt_id: str) -> str:
        """Determine party from NYT ID based on known patterns."""
        # This is a simplified mapping - you may need to expand this
        if "whitmer" in nyt_id or "nessel" in nyt_id or "benson" in nyt_id:
            return "Democrat"
        elif "dixon" in nyt_id or "deperno" in nyt_id or "karamo" in nyt_id:
            return "Republican"
        else:
            return "Unknown"
    
    def migrate_2018_data(self) -> None:
        """Migrate 2018 election data."""
        print("Migrating 2018 data...")
        
        try:
            with open("normalized_data/normalized_2018.general.json", "r") as fp:
                data = json.load(fp)
            
            if data['race']['race_name']:
                office = data['race']['race_name']
                election = self.get_or_create_election(2018, "general", office, 
                                                      election_date=data['race']['election_date'],
                                                      source="normalized")
                
                # Create candidates from normalized data
                for candidate_data in data['candidates']:
                    first_name = candidate_data.get('first_name', '') or ""
                    last_name = candidate_data.get('last_name', '') or ""
                    candidate_name = candidate_data.get('display_name') or f"{first_name} {last_name}".strip()
                    if candidate_name:
                        party = candidate_data.get('party_id', 'Unknown').title()
                        candidate = self.get_or_create_candidate(candidate_name, party)
                        
                        # Create a placeholder result for the state total
                        state_county = self.get_or_create_county("Michigan (State Total)")
                        
                        votes = candidate_data.get('votes', 0)
                        percentage = candidate_data.get('vote_percentage', 0)
                        winner = candidate_data.get('winner', False)
                        
                        existing_result = Result.get(county=state_county, election=election, candidate=candidate)
                        if existing_result is None:
                            Result(county=state_county, election=election, candidate=candidate, 
                                   votes=votes, percentage=percentage, winner=winner)
                
                print("✓ Migrated 2018 data (state totals only)")
            else:
                print("⚠️  2018 data doesn't have race information - skipping")
                
        except FileNotFoundError:
            print("✗ 2018 normalized data not found")
    
    def run_migration(self) -> None:
        """Run the complete migration process."""
        print("=" * 60)
        print("ELECTION DATA MIGRATION TO SQLITE DATABASE")
        print("=" * 60)
        
        with db_session:
            # Migrate all available data
            self.migrate_2016_data()
            self.migrate_2018_data()
            self.migrate_2020_data()
            self.migrate_2022_data()
            
            # Commit all changes
            commit()
        
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print("=" * 60)
        
        # Print summary statistics
        with db_session:
            county_count = select(count(c) for c in County).get()
            election_count = select(count(e) for e in Election).get()
            candidate_count = select(count(c) for c in Candidate).get()
            result_count = select(count(r) for r in Result).get()
            
            print(f"\nDatabase Summary:")
            print(f"  Counties: {county_count}")
            print(f"  Elections: {election_count}")
            print(f"  Candidates: {candidate_count}")
            print(f"  Results: {result_count}")

def main():
    """Main function to run the migration."""
    migrator = ElectionDataMigrator()
    migrator.run_migration()

if __name__ == "__main__":
    main()
