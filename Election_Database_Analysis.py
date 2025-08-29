#!/usr/bin/env python3
"""
Election Database Analysis: Advanced Analysis Using SQLite and PonyORM

This script performs comprehensive analysis of election data stored in a SQLite database,
providing better querying capabilities, data integrity, and performance than .ft files.

Key Features:
1. Relational queries across elections, counties, and candidates
2. Advanced voter behavior analysis
3. Geographic clustering and pattern recognition
4. Cross-election cycle correlations
5. Voter migration tracking

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats
import warnings
from typing import Dict, List, Any, Optional, Tuple
from pony.orm import *
import sqlite3

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Import database models
from election_database import db, County, Election, Candidate, Result

class ElectionDatabaseAnalyzer:
    """Advanced election data analyzer using SQLite database with PonyORM."""
    
    def __init__(self, db_path: str = "elections.db"):
        """Initialize the analyzer with database connection."""
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self) -> None:
        """Set up the database connection."""
        db.bind(provider='sqlite', filename=self.db_path)
        db.generate_mapping()
        print(f"✓ Connected to database: {self.db_path}")
    
    def get_county_summary(self) -> pd.DataFrame:
        """Get summary statistics for all counties."""
        print("Getting county summary...")
        
        with db_session:
            # Get all counties with their result counts
            counties = select((c.name, c.fips_code, count(r)) 
                            for c in County 
                            for r in c.results).order_by(desc(count(r)))
            
            county_data = []
            for county_name, fips_code, result_count in counties:
                county_data.append({
                    'county': county_name,
                    'fips_code': fips_code,
                    'total_results': result_count
                })
        
        df = pd.DataFrame(county_data)
        print(f"✓ Found {len(df)} counties")
        return df
    
    def get_election_summary(self) -> pd.DataFrame:
        """Get summary of all elections in the database."""
        print("Getting election summary...")
        
        with db_session:
            elections = select((e.year, e.election_type, e.office, e.party, 
                              e.election_date, count(r)) 
                             for e in Election 
                             for r in e.results).order_by(desc(e.year), e.election_type)
            
            election_data = []
            for year, election_type, office, party, election_date, result_count in elections:
                election_data.append({
                    'year': year,
                    'election_type': election_type,
                    'office': office,
                    'party': party,
                    'election_date': election_date,
                    'total_results': result_count
                })
        
        df = pd.DataFrame(election_data)
        print(f"✓ Found {len(df)} elections")
        return df
    
    def get_candidate_performance(self, candidate_name: str, 
                                 election_year: Optional[int] = None) -> pd.DataFrame:
        """Get performance data for a specific candidate."""
        print(f"Getting performance data for {candidate_name}...")
        
        with db_session:
            query = select((r.county.name, r.election.year, r.election.election_type,
                           r.election.office, r.votes, r.percentage, r.winner)
                          for r in Result 
                          for c in r.candidate 
                          if c.name == candidate_name)
            
            if election_year:
                query = query.filter(lambda r: r.election.year == election_year)
            
            results = []
            for county_name, year, election_type, office, votes, percentage, winner in query:
                results.append({
                    'county': county_name,
                    'year': year,
                    'election_type': election_type,
                    'office': office,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        df = pd.DataFrame(results)
        print(f"✓ Found {len(df)} results for {candidate_name}")
        return df
    
    def analyze_bernie_sanders_patterns(self) -> Dict[str, Any]:
        """Analyze Bernie Sanders performance patterns across elections."""
        print("\n=== BERNIE SANDERS PATTERN ANALYSIS ===")
        
        # Get Bernie's primary performance
        bernie_primary = self.get_candidate_performance("Bernie Sanders")
        
        if bernie_primary.empty:
            print("No Bernie Sanders data found")
            return {}
        
        # Get Biden's general performance in same counties
        biden_general = self.get_candidate_performance("Joe Biden")
        
        analysis = {}
        
        if not biden_general.empty:
            # Merge on county and year to find correlations
            merged = bernie_primary.merge(
                biden_general, 
                on=['county', 'year'], 
                suffixes=('_bernie', '_biden')
            )
            
            if not merged.empty:
                # Calculate correlation between Bernie primary and Biden general
                correlation = merged['percentage_bernie'].corr(merged['percentage_biden'])
                analysis['bernie_biden_correlation'] = correlation
                print(f"Bernie primary → Biden general correlation: {correlation:.4f}")
                
                # Find counties where Bernie was strong but Biden underperformed
                bernie_median = merged['percentage_bernie'].median()
                biden_median = merged['percentage_biden'].median()
                
                underperformers = merged[
                    (merged['percentage_bernie'] > bernie_median) & 
                    (merged['percentage_biden'] < biden_median)
                ]
                
                analysis['underperforming_counties'] = len(underperformers)
                print(f"Counties where Bernie was strong but Biden underperformed: {len(underperformers)}")
        
        return analysis
    
    def analyze_ted_cruz_patterns(self) -> Dict[str, Any]:
        """Analyze Ted Cruz primary performance patterns."""
        print("\n=== TED CRUZ PATTERN ANALYSIS ===")
        
        # Get Cruz's primary performance
        cruz_primary = self.get_candidate_performance("Ted Cruz")
        
        if cruz_primary.empty:
            print("No Ted Cruz data found")
            return {}
        
        # Get Trump's general performance in same counties
        trump_general = self.get_candidate_performance("Donald J. Trump")
        
        analysis = {}
        
        if not trump_general.empty:
            # Merge on county and year to find correlations
            merged = cruz_primary.merge(
                trump_general, 
                on=['county', 'year'], 
                suffixes=('_cruz', '_trump')
            )
            
            if not merged.empty:
                # Calculate correlation between Cruz primary and Trump general
                correlation = merged['percentage_cruz'].corr(merged['percentage_trump'])
                analysis['cruz_trump_correlation'] = correlation
                print(f"Cruz primary → Trump general correlation: {correlation:.4f}")
                
                # Find counties where Cruz was strong but Trump underperformed
                cruz_median = merged['percentage_cruz'].median()
                trump_median = merged['percentage_trump'].median()
                
                underperformers = merged[
                    (merged['percentage_cruz'] > cruz_median) & 
                    (merged['percentage_trump'] < trump_median)
                ]
                
                analysis['underperforming_counties'] = len(underperformers)
                print(f"Counties where Cruz was strong but Trump underperformed: {len(underperformers)}")
        
        return analysis
    
    def analyze_voter_shifts(self, year1: int, year2: int, 
                           candidate1: str, candidate2: str) -> pd.DataFrame:
        """Analyze voter shifts between two elections for specific candidates."""
        print(f"\n=== VOTER SHIFT ANALYSIS: {candidate1} ({year1}) → {candidate2} ({year2}) ===")
        
        # Get performance data for both candidates
        candidate1_data = self.get_candidate_performance(candidate1, year1)
        candidate2_data = self.get_candidate_performance(candidate2, year2)
        
        if candidate1_data.empty or candidate2_data.empty:
            print(f"Insufficient data for shift analysis")
            return pd.DataFrame()
        
        # Merge on county
        merged = candidate1_data.merge(
            candidate2_data, 
            on='county', 
            suffixes=('_1', '_2')
        )
        
        if merged.empty:
            print("No matching counties found")
            return pd.DataFrame()
        
        # Calculate shifts
        merged['vote_shift'] = merged['votes_2'] - merged['votes_1']
        merged['percentage_shift'] = merged['percentage_2'] - merged['percentage_1']
        merged['vote_change_pct'] = (merged['vote_shift'] / merged['votes_1'] * 100)
        
        # Sort by biggest shifts
        merged = merged.sort_values('percentage_shift', ascending=False)
        
        print(f"✓ Analyzed shifts for {len(merged)} counties")
        print(f"Biggest gainers:")
        for _, row in merged.head(5).iterrows():
            print(f"  {row['county']}: {row['percentage_shift']:.2f}%")
        
        print(f"Biggest losers:")
        for _, row in merged.tail(5).iterrows():
            print(f"  {row['county']}: {row['percentage_shift']:.2f}%")
        
        return merged
    
    def get_election_results_matrix(self, year: int, office: str) -> pd.DataFrame:
        """Get a matrix of election results for a specific year and office."""
        print(f"Getting results matrix for {year} {office}...")
        
        with db_session:
            # Get all results for the specified election
            results = select((r.county.name, r.candidate.name, r.candidate.party, 
                            r.votes, r.percentage, r.winner)
                           for r in Result 
                           for e in r.election 
                           if e.year == year and e.office == office)
            
            results_data = []
            for county_name, candidate_name, party, votes, percentage, winner in results:
                results_data.append({
                    'county': county_name,
                    'candidate': candidate_name,
                    'party': party,
                    'votes': votes,
                    'percentage': percentage,
                    'winner': winner
                })
        
        if not results_data:
            print(f"No results found for {year} {office}")
            return pd.DataFrame()
        
        df = pd.DataFrame(results_data)
        
        # Pivot to create a matrix
        matrix = df.pivot(index='county', columns='candidate', values='percentage')
        matrix = matrix.fillna(0)
        
        print(f"✓ Created results matrix: {matrix.shape}")
        return matrix
    
    def perform_geographic_clustering(self, year: int, office: str, n_clusters: int = 5) -> pd.DataFrame:
        """Perform geographic clustering analysis on election results."""
        print(f"\n=== GEOGRAPHIC CLUSTERING: {year} {office} ===")
        
        # Get results matrix
        matrix = self.get_election_results_matrix(year, office)
        
        if matrix.empty:
            print("No data available for clustering")
            return pd.DataFrame()
        
        # Prepare data for clustering
        cluster_data = matrix.fillna(0)
        
        # Standardize the data
        scaler = StandardScaler()
        cluster_data_scaled = scaler.fit_transform(cluster_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(cluster_data_scaled)
        
        # Add cluster labels to the matrix
        matrix_with_clusters = matrix.copy()
        matrix_with_clusters['cluster'] = cluster_labels
        
        # Analyze clusters
        print(f"Created {n_clusters} geographic clusters")
        
        for cluster_id in range(n_clusters):
            cluster_counties = matrix_with_clusters[matrix_with_clusters['cluster'] == cluster_id]
            print(f"\nCluster {cluster_id}: {len(cluster_counties)} counties")
            
            # Show sample counties
            sample_counties = cluster_counties.index.tolist()[:5]
            print(f"Sample counties: {', '.join(sample_counties)}")
            
            # Show cluster characteristics (average percentages)
            cluster_means = cluster_counties.drop('cluster', axis=1).mean()
            top_characteristics = cluster_means.nlargest(3)
            print("Top characteristics:")
            for candidate, mean_val in top_characteristics.items():
                print(f"  {candidate}: {mean_val:.2f}%")
        
        return matrix_with_clusters
    
    def analyze_cross_election_correlations(self) -> pd.DataFrame:
        """Analyze correlations between different elections."""
        print("\n=== CROSS-ELECTION CORRELATION ANALYSIS ===")
        
        # Get all elections
        elections = self.get_election_summary()
        
        if elections.empty:
            print("No election data available")
            return pd.DataFrame()
        
        # Focus on general elections for comparison
        general_elections = elections[elections['election_type'] == 'general']
        
        correlations = []
        
        # Compare different years for same office
        for office in general_elections['office'].unique():
            office_elections = general_elections[general_elections['office'] == office]
            
            if len(office_elections) >= 2:
                years = sorted(office_elections['year'].tolist())
                
                for i in range(len(years)):
                    for j in range(i+1, len(years)):
                        year1, year2 = years[i], years[j]
                        
                        # Get results matrices for both years
                        matrix1 = self.get_election_results_matrix(year1, office)
                        matrix2 = self.get_election_results_matrix(year2, office)
                        
                        if not matrix1.empty and not matrix2.empty:
                            # Find common candidates
                            common_candidates = set(matrix1.columns) & set(matrix2.columns)
                            
                            for candidate in common_candidates:
                                if candidate in matrix1.columns and candidate in matrix2.columns:
                                    # Calculate correlation
                                    correlation = matrix1[candidate].corr(matrix2[candidate])
                                    
                                    if not pd.isna(correlation):
                                        correlations.append({
                                            'office': office,
                                            'year1': year1,
                                            'year2': year2,
                                            'candidate': candidate,
                                            'correlation': correlation,
                                            'abs_correlation': abs(correlation)
                                        })
        
        if correlations:
            correlations_df = pd.DataFrame(correlations)
            correlations_df = correlations_df.sort_values('abs_correlation', ascending=False)
            
            print(f"✓ Found {len(correlations_df)} correlations")
            print("\nTop 10 strongest correlations:")
            print(correlations_df.head(10))
            
            return correlations_df
        else:
            print("No correlations found")
            return pd.DataFrame()
    
    def generate_summary_report(self) -> None:
        """Generate a comprehensive summary report."""
        print("\n" + "=" * 60)
        print("ELECTION DATABASE ANALYSIS SUMMARY REPORT")
        print("=" * 60)
        
        # Database overview
        county_summary = self.get_county_summary()
        election_summary = self.get_election_summary()
        
        print(f"\nDATABASE OVERVIEW:")
        print(f"  Total Counties: {len(county_summary)}")
        print(f"  Total Elections: {len(election_summary)}")
        print(f"  Data Years: {sorted(election_summary['year'].unique())}")
        print(f"  Offices: {sorted(election_summary['office'].unique())}")
        
        # Analysis results
        print(f"\nANALYSIS RESULTS:")
        
        # Bernie analysis
        bernie_analysis = self.analyze_bernie_sanders_patterns()
        if bernie_analysis:
            print(f"  Bernie Sanders Analysis: ✓")
        
        # Cruz analysis
        cruz_analysis = self.analyze_ted_cruz_patterns()
        if cruz_analysis:
            print(f"  Ted Cruz Analysis: ✓")
        
        # Voter shifts
        print(f"\nVOTER SHIFT ANALYSES:")
        
        # Trump 2016-2020
        trump_shifts = self.analyze_voter_shifts(2016, 2020, "Donald J. Trump", "Donald J. Trump")
        if not trump_shifts.empty:
            print(f"  Trump 2016→2020: ✓")
        
        # Governor 2018-2022
        gov_shifts = self.analyze_voter_shifts(2018, 2022, "Bill Schuette", "Tudor Dixon")
        if not gov_shifts.empty:
            print(f"  Governor 2018→2022: ✓")
        
        # Geographic clustering
        print(f"\nGEOGRAPHIC ANALYSIS:")
        clustering_2022 = self.perform_geographic_clustering(2022, "Governor")
        if not clustering_2022.empty:
            print(f"  2022 Governor Clustering: ✓")
        
        # Cross-election correlations
        print(f"\nCORRELATION ANALYSIS:")
        correlations = self.analyze_cross_election_correlations()
        if not correlations.empty:
            print(f"  Cross-election Correlations: ✓")
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

def main():
    """Main function to run the database analysis."""
    analyzer = ElectionDatabaseAnalyzer()
    analyzer.generate_summary_report()

if __name__ == "__main__":
    main()
