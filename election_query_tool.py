#!/usr/bin/env python3
"""
Election Database Query Tool

A simple interactive tool for querying the election database and exploring
voter behavior patterns across different elections and counties.

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from pony.orm import *
from election_database import db, County, Election, Candidate, Result

class ElectionQueryTool:
    """Interactive query tool for the election database."""
    
    def __init__(self, db_path: str = "elections_enhanced.db"):
        """Initialize the query tool."""
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self) -> None:
        """Set up the database connection."""
        db.bind(provider='sqlite', filename=self.db_path)
        db.generate_mapping()
        print(f"✓ Connected to database: {self.db_path}")
    
    def get_top_performers(self, year: int, office: str, limit: int = 10) -> pd.DataFrame:
        """Get top performing candidates for a specific election."""
        print(f"Getting top performers for {year} {office}...")
        
        with db_session:
            results = select((r.candidate.name, r.candidate.party, r.county.name, 
                            r.votes, r.percentage, r.winner)
                           for r in Result 
                           for e in r.election 
                           if e.year == year and e.office == office
                           ).order_by(desc(4)).limit(limit)
            
            data = []
            for candidate_name, party, county_name, votes, percentage, winner in results:
                data.append({
                    'candidate': candidate_name,
                    'party': party,
                    'county': county_name,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            print(f"✓ Found {len(df)} top performers")
            print(df.to_string(index=False))
        else:
            print(f"No results found for {year} {office}")
        
        return df
    
    def get_county_performance(self, county_name: str) -> pd.DataFrame:
        """Get all election results for a specific county."""
        print(f"Getting performance data for {county_name}...")
        
        with db_session:
            results = select((r.election.year, r.election.election_type, r.election.office,
                            r.candidate.name, r.candidate.party, r.votes, r.percentage, r.winner)
                           for r in Result 
                           for c in r.county 
                           if c.name == county_name
                           ).order_by(desc(r.election.year), r.election.election_type)
            
            data = []
            for year, election_type, office, candidate_name, party, votes, percentage, winner in results:
                data.append({
                    'year': year,
                    'election_type': election_type,
                    'office': office,
                    'candidate': candidate_name,
                    'party': party,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            print(f"✓ Found {len(df)} results for {county_name}")
            print(df.to_string(index=False))
        else:
            print(f"No results found for {county_name}")
        
        return df
    
    def get_candidate_summary(self, candidate_name: str) -> pd.DataFrame:
        """Get summary statistics for a specific candidate."""
        print(f"Getting summary for {candidate_name}...")
        
        with db_session:
            results = select((r.election.year, r.election.election_type, r.election.office,
                            r.county.name, r.votes, r.percentage, r.winner)
                           for r in Result 
                           for c in r.candidate 
                           if c.name == candidate_name
                           ).order_by(desc(1), 2)
            
            data = []
            for year, election_type, office, county_name, votes, percentage, winner in results:
                data.append({
                    'year': year,
                    'election_type': election_type,
                    'office': office,
                    'county': county_name,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            print(f"✓ Found {len(df)} results for {candidate_name}")
            
            # Calculate summary statistics
            summary = df.groupby(['year', 'election_type', 'office']).agg({
                'votes': ['sum', 'mean', 'max'],
                'percentage': ['mean', 'max'],
                'winner': 'sum'
            }).round(2)
            
            print("\nSummary by Election:")
            print(summary)
            
            # Show top 5 performances
            print(f"\nTop 5 Performances:")
            top_performances = df.nlargest(5, 'percentage')[['county', 'year', 'office', 'percentage']]
            print(top_performances.to_string(index=False))
        else:
            print(f"No results found for {candidate_name}")
        
        return df
    
    def compare_candidates(self, candidate1: str, candidate2: str, year: int, office: str) -> pd.DataFrame:
        """Compare two candidates in the same election."""
        print(f"Comparing {candidate1} vs {candidate2} in {year} {office}...")
        
        with db_session:
            results = select((r.county.name, r.candidate.name, r.votes, r.percentage, r.winner)
                           for r in Result 
                           for e in r.election 
                           for c in r.candidate
                           if e.year == year and e.office == office 
                           and c.name in [candidate1, candidate2])
            
            data = []
            for county_name, candidate_name, votes, percentage, winner in results:
                data.append({
                    'county': county_name,
                    'candidate': candidate_name,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            # Pivot to compare side by side
            comparison = df.pivot(index='county', columns='candidate', values='percentage')
            comparison = comparison.fillna(0)
            
            # Calculate vote difference
            if candidate1 in comparison.columns and candidate2 in comparison.columns:
                comparison['difference'] = comparison[candidate1] - comparison[candidate2]
                comparison = comparison.sort_values('difference', ascending=False)
                
                print(f"✓ Comparison for {len(comparison)} counties:")
                print(comparison.round(2))
                
                # Summary statistics
                print(f"\nSummary:")
                print(f"  {candidate1} wins: {(comparison['difference'] > 0).sum()} counties")
                print(f"  {candidate2} wins: {(comparison['difference'] < 0).sum()} counties")
                print(f"  Ties: {(comparison['difference'] == 0).sum()} counties")
                
                print(f"\nBiggest {candidate1} wins:")
                print(comparison.head(5)[['difference']].round(2))
                
                print(f"\nBiggest {candidate2} wins:")
                print(comparison.tail(5)[['difference']].round(2))
            else:
                print("Both candidates not found in this election")
        else:
            print(f"No results found for comparison")
        
        return df
    
    def get_election_turnout(self, year: int, office: str) -> pd.DataFrame:
        """Get turnout statistics for a specific election."""
        print(f"Getting turnout data for {year} {office}...")
        
        with db_session:
            # Get total votes by county
            county_totals = select((r.county.name, sum(r.votes))
                                 for r in Result 
                                 for e in r.election 
                                 if e.year == year and e.office == office
                                 ).group_by(r.county.name)
            
            data = []
            for county_name, total_votes in county_totals:
                data.append({
                    'county': county_name,
                    'total_votes': total_votes
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values('total_votes', ascending=False)
            
            print(f"✓ Turnout for {len(df)} counties:")
            print(df.to_string(index=False))
            
            # Summary statistics
            print(f"\nTurnout Summary:")
            print(f"  Total votes: {df['total_votes'].sum():,}")
            print(f"  Average per county: {df['total_votes'].mean():,.0f}")
            print(f"  Highest turnout: {df.iloc[0]['county']} ({df.iloc[0]['total_votes']:,})")
            print(f"  Lowest turnout: {df.iloc[-1]['county']} ({df.iloc[-1]['total_votes']:,})")
        else:
            print(f"No turnout data found for {year} {office}")
        
        return df
    
    def search_candidates(self, search_term: str) -> pd.DataFrame:
        """Search for candidates by name."""
        print(f"Searching for candidates matching '{search_term}'...")
        
        with db_session:
            candidates = select((c.name, c.party, c.nyt_id, count(r))
                              for c in Candidate 
                              for r in c.results
                              if search_term.lower() in c.name.lower())
            
            data = []
            for name, party, nyt_id, result_count in candidates:
                data.append({
                    'name': name,
                    'party': party,
                    'nyt_id': nyt_id,
                    'total_results': result_count
                })
        
        df = pd.DataFrame(data)
        if not df.empty:
            print(f"✓ Found {len(df)} matching candidates:")
            print(df.to_string(index=False))
        else:
            print(f"No candidates found matching '{search_term}'")
        
        return df
    
    def get_database_stats(self) -> None:
        """Get overall database statistics."""
        print("Getting database statistics...")
        
        with db_session:
            county_count = select(count(c) for c in County).get()
            election_count = select(count(e) for e in Election).get()
            candidate_count = select(count(c) for c in Candidate).get()
            result_count = select(count(r) for r in Result).get()
            
            # Get year range
            years = select(e.year for e in Election).distinct()
            year_list = sorted([year for year in years])
            
            # Get offices
            offices = select(e.office for e in Election).distinct()
            office_list = sorted([office for office in offices])
            
            print(f"\nDatabase Statistics:")
            print(f"  Counties: {county_count}")
            print(f"  Elections: {election_count}")
            print(f"  Candidates: {candidate_count}")
            print(f"  Results: {result_count}")
            print(f"  Year Range: {year_list[0]} - {year_list[-1]}")
            print(f"  Offices: {', '.join(office_list)}")
            
            # Show elections by year
            print(f"\nElections by Year:")
            for year in year_list:
                year_elections = select((e.election_type, e.office, e.party)
                                      for e in Election 
                                      if e.year == year)
                
                election_list = []
                for election_type, office, party in year_elections:
                    if party:
                        election_list.append(f"{election_type} {office} ({party})")
                    else:
                        election_list.append(f"{election_type} {office}")
                
                print(f"  {year}: {', '.join(election_list)}")
    
    def interactive_mode(self) -> None:
        """Run the tool in interactive mode."""
        print("\n" + "=" * 60)
        print("ELECTION DATABASE QUERY TOOL")
        print("=" * 60)
        print("Available commands:")
        print("  1. stats - Show database statistics")
        print("  2. top <year> <office> [limit] - Show top performers")
        print("  3. county <name> - Show county performance")
        print("  4. candidate <name> - Show candidate summary")
        print("  5. compare <candidate1> <candidate2> <year> <office> - Compare candidates")
        print("  6. turnout <year> <office> - Show turnout data")
        print("  7. search <term> - Search for candidates")
        print("  8. help - Show this help")
        print("  9. quit - Exit")
        print("=" * 60)
        
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("Goodbye!")
                    break
                elif command == 'help':
                    print("Available commands:")
                    print("  1. stats - Show database statistics")
                    print("  2. top <year> <office> [limit] - Show top performers")
                    print("  3. county <name> - Show county performance")
                    print("  4. candidate <name> - Show candidate summary")
                    print("  5. compare <candidate1> <candidate2> <year> <office> - Compare candidates")
                    print("  6. turnout <year> <office> - Show turnout data")
                    print("  7. search <term> - Search for candidates")
                    print("  8. help - Show this help")
                    print("  9. quit - Exit")
                elif command == 'stats':
                    self.get_database_stats()
                elif command.startswith('top '):
                    parts = command.split()
                    if len(parts) >= 3:
                        year = int(parts[1])
                        office = ' '.join(parts[2:-1]) if len(parts) > 3 else parts[2]
                        limit = int(parts[-1]) if len(parts) > 3 and parts[-1].isdigit() else 10
                        self.get_top_performers(year, office, limit)
                    else:
                        print("Usage: top <year> <office> [limit]")
                elif command.startswith('county '):
                    county_name = command[7:]
                    self.get_county_performance(county_name)
                elif command.startswith('candidate '):
                    candidate_name = command[10:]
                    self.get_candidate_summary(candidate_name)
                elif command.startswith('compare '):
                    parts = command.split()
                    if len(parts) >= 5:
                        candidate1 = parts[1]
                        candidate2 = parts[2]
                        year = int(parts[3])
                        office = ' '.join(parts[4:])
                        self.compare_candidates(candidate1, candidate2, year, office)
                    else:
                        print("Usage: compare <candidate1> <candidate2> <year> <office>")
                elif command.startswith('turnout '):
                    parts = command.split()
                    if len(parts) >= 3:
                        year = int(parts[1])
                        office = ' '.join(parts[2:])
                        self.get_election_turnout(year, office)
                    else:
                        print("Usage: turnout <year> <office>")
                elif command.startswith('search '):
                    search_term = command[7:]
                    self.search_candidates(search_term)
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Type 'help' for available commands.")

def main():
    """Main function to run the query tool."""
    tool = ElectionQueryTool()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = ' '.join(sys.argv[1:])
        if command == 'stats':
            tool.get_database_stats()
        elif command.startswith('top '):
            parts = command.split()
            if len(parts) >= 3:
                year = int(parts[1])
                office = ' '.join(parts[2:-1]) if len(parts) > 3 else parts[2]
                limit = int(parts[-1]) if len(parts) > 3 and parts[-1].isdigit() else 10
                tool.get_top_performers(year, office, limit)
        elif command.startswith('search '):
            search_term = command[7:]
            tool.search_candidates(search_term)
        elif command.startswith('candidate '):
            candidate_name = command[10:]
            tool.get_candidate_summary(candidate_name)
        else:
            print("Unknown command. Run without arguments for interactive mode.")
    else:
        # Interactive mode
        tool.interactive_mode()

if __name__ == "__main__":
    import sys
    main()
