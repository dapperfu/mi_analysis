#!/usr/bin/env python3
"""
Election Data Normalization Script

This script normalizes NYTimes election JSON files from different years into a consistent format.
It preserves all major data while standardizing the structure for easier analysis.

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ElectionDataNormalizer:
    """Normalizes election JSON data into a consistent format."""
    
    def __init__(self, output_dir: str = "normalized_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Standard field mappings for different formats
        self.field_mappings = {
            '2016': {
                'candidate_id': 'nyt_id',
                'candidate_key': 'candidate_key',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'name_display': 'display_name',
                'party_id': 'party_id',
                'votes': 'votes',
                'percent': 'vote_percentage',
                'winner': 'winner'
            },
            '2020': {
                'candidate_id': 'nyt_id',
                'candidate_key': 'candidate_key',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'name_display': 'display_name',
                'party_id': 'party_id',
                'votes': 'votes',
                'percent': 'vote_percentage',
                'winner': 'winner'
            },
            '2022': {
                'nyt_id': 'nyt_id',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'party': 'party_info',
                'votes': 'votes'
            }
        }
    
    def detect_format(self, data: Any) -> str:
        """Detect the format/version of the election data."""
        if isinstance(data, list):
            # Check if it's a 2016-style format in a list
            if len(data) > 0 and isinstance(data[0], dict):
                if 'candidates' in data[0] and 'counties' in data[0]:
                    if 'absentee_votes' in data[0].get('candidates', [{}])[0]:
                        return '2020'
                    else:
                        return '2016'
                elif 'candidate_metadata' in data[0]:
                    return '2022'
            return '2022'
        elif isinstance(data, dict):
            if 'candidate_metadata' in data:
                return '2022'
            elif 'candidates' in data and 'counties' in data:
                if 'absentee_votes' in data.get('candidates', [{}])[0]:
                    return '2020'
                else:
                    return '2016'
        return 'unknown'
    
    def normalize_candidate(self, candidate: Dict[str, Any], format_type: str) -> Dict[str, Any]:
        """Normalize candidate data to standard format."""
        normalized = {
            'nyt_id': None,
            'candidate_key': None,
            'first_name': None,
            'last_name': None,
            'display_name': None,
            'party_id': None,
            'party_name': None,
            'party_abbreviation': None,
            'votes': 0,
            'vote_percentage': 0.0,
            'winner': False,
            'incumbent': False,
            'electoral_votes': 0,
            'img_url': None,
            'order': 0,
            'ballot_order': 0,
            'suffix': None
        }
        
        if format_type == '2016':
            normalized.update({
                'nyt_id': candidate.get('candidate_id'),
                'candidate_key': candidate.get('candidate_key'),
                'first_name': candidate.get('first_name'),
                'last_name': candidate.get('last_name'),
                'display_name': candidate.get('name_display'),
                'party_id': candidate.get('party_id'),
                'votes': candidate.get('votes', 0),
                'vote_percentage': candidate.get('percent', 0.0),
                'winner': candidate.get('winner', False),
                'electoral_votes': candidate.get('electoral_votes', 0),
                'order': candidate.get('order', 0)
            })
            
        elif format_type == '2020':
            normalized.update({
                'nyt_id': candidate.get('candidate_id'),
                'candidate_key': candidate.get('candidate_key'),
                'first_name': candidate.get('first_name'),
                'last_name': candidate.get('last_name'),
                'display_name': candidate.get('name_display'),
                'party_id': candidate.get('party_id'),
                'votes': candidate.get('votes', 0),
                'vote_percentage': candidate.get('percent', 0.0),
                'winner': candidate.get('winner', False),
                'incumbent': candidate.get('incumbent', False),
                'electoral_votes': candidate.get('electoral_votes', 0),
                'img_url': candidate.get('img_url'),
                'order': candidate.get('order', 0),
                'absentee_votes': candidate.get('absentee_votes', 0),
                'absentee_percent': candidate.get('absentee_percent', 0.0)
            })
            
        elif format_type == '2022':
            # Handle 2022 format which has candidate_metadata and reporting_units
            normalized.update({
                'nyt_id': candidate.get('nyt_id'),
                'first_name': candidate.get('first_name'),
                'last_name': candidate.get('last_name'),
                'display_name': f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
                'party_name': candidate.get('party', {}).get('name'),
                'party_abbreviation': candidate.get('party', {}).get('abbreviation'),
                'party_id': candidate.get('party', {}).get('nyt_id'),
                'votes': candidate.get('votes', {}).get('total', 0),
                'winner': candidate.get('leader', False),
                'incumbent': candidate.get('incumbent', False),
                'img_url': candidate.get('img_url'),
                'order': candidate.get('order', 0),
                'ballot_order': candidate.get('ballot_order', 0),
                'suffix': candidate.get('suffix')
            })
            
            # Handle different vote structures
            if isinstance(candidate.get('votes'), dict):
                vote_data = candidate['votes']
                normalized.update({
                    'advance_votes': vote_data.get('advance', 0),
                    'absentee_mail_votes': vote_data.get('absentee_mail', 0),
                    'early_in_person_votes': vote_data.get('early_in_person', 0),
                    'election_day_votes': vote_data.get('election_day_in_person', 0)
                })
        
        return normalized
    
    def normalize_county(self, county: Dict[str, Any], format_type: str) -> Dict[str, Any]:
        """Normalize county data to standard format."""
        normalized = {
            'fips': None,
            'name': None,
            'precincts_total': 0,
            'precincts_reporting': 0,
            'total_votes': 0,
            'expected_votes': 0,
            'eevp': 0,
            'eevp_display': None,
            'reporting_percentage': 0.0,
            'results': {},
            'absentee_results': {},
            'historical_margins': {},
            'last_updated': None,
            'data_source': None
        }
        
        if format_type in ['2016', '2020']:
            normalized.update({
                'fips': county.get('fips'),
                'name': county.get('name'),
                'precincts_total': county.get('precincts', 0),
                'precincts_reporting': county.get('reporting', 0),
                'total_votes': county.get('votes', 0),
                'expected_votes': county.get('tot_exp_vote', 0),
                'eevp': county.get('eevp', 0),
                'eevp_display': county.get('eevp_display'),
                'reporting_percentage': (county.get('reporting', 0) / county.get('precincts', 1)) * 100 if county.get('precincts', 0) > 0 else 0,
                'results': county.get('results', {}),
                'absentee_results': county.get('results_absentee', {}),
                'last_updated': county.get('last_updated'),
                'data_source': county.get('county_data_source', 'edison')
            })
            
            # Historical margins
            if format_type == '2020':
                normalized['historical_margins'] = {
                    '2012': county.get('margin2012'),
                    '2016': county.get('margin2016'),
                    '2020': county.get('margin2020')
                }
                
        elif format_type == '2022':
            normalized.update({
                'fips': county.get('fips_county'),
                'name': county.get('name'),
                'precincts_total': county.get('precincts_total', 0),
                'precincts_reporting': county.get('precincts_reporting', 0),
                'total_votes': county.get('total_votes', 0),
                'expected_votes': county.get('total_expected_vote', 0),
                'eevp': county.get('eevp', 0),
                'eevp_display': f"{county.get('eevp', 0)}%",
                'reporting_percentage': (county.get('precincts_reporting', 0) / county.get('precincts_total', 1)) * 100 if county.get('precincts_total', 0) > 0 else 0,
                'data_source': 'ap'
            })
            
            # Extract results from candidates
            results = {}
            for candidate in county.get('candidates', []):
                candidate_id = candidate.get('nyt_id')
                if candidate_id:
                    results[candidate_id] = candidate.get('votes', {}).get('total', 0)
            normalized['results'] = results
        
        return normalized
    
    def normalize_race_metadata(self, data: Any, format_type: str) -> Dict[str, Any]:
        """Normalize race-level metadata to standard format."""
        normalized = {
            'race_id': None,
            'race_name': None,
            'race_type': None,
            'election_date': None,
            'state': None,
            'state_postal': None,
            'electoral_votes': 0,
            'total_precincts': 0,
            'precincts_reporting': 0,
            'total_votes': 0,
            'expected_votes': 0,
            'eevp': 0,
            'eevp_display': None,
            'reporting_percentage': 0.0,
            'winner': None,
            'margin': None,
            'margin_display': None,
            'data_source': None,
            'last_updated': None,
            'certified': False
        }
        
        if format_type in ['2016', '2020']:
            if isinstance(data, dict):
                normalized.update({
                    'race_id': data.get('race_id'),
                    'race_name': data.get('race_name'),
                    'race_type': data.get('race_type'),
                    'election_date': data.get('election_date'),
                    'state': data.get('state_name'),
                    'state_postal': data.get('state_id'),
                    'electoral_votes': data.get('electoral_votes', 0),
                    'total_precincts': data.get('precincts_total', 0),
                    'precincts_reporting': data.get('precincts_reporting', 0),
                    'total_votes': sum(c.get('votes', 0) for c in data.get('candidates', [])),
                    'eevp': data.get('eevp', 0),
                    'eevp_display': data.get('eevp_display'),
                    'reporting_percentage': (data.get('precincts_reporting', 0) / data.get('precincts_total', 1)) * 100 if data.get('precincts_total', 0) > 0 else 0,
                    'winner': next((c.get('name_display') for c in data.get('candidates', []) if c.get('winner')), None),
                    'margin': data.get('leader_margin_value'),
                    'margin_display': data.get('leader_margin_display'),
                    'data_source': data.get('county_data_source', 'edison'),
                    'last_updated': data.get('last_updated'),
                    'certified': data.get('edison_certified', False)
                })
                
        elif format_type == '2022':
            if isinstance(data, list) and len(data) > 0:
                race_data = data[0]  # First race in the list
                normalized.update({
                    'race_id': race_data.get('race_id'),
                    'race_name': race_data.get('race_titles', {}).get('default_title'),
                    'race_type': race_data.get('race_type_id'),
                    'election_date': race_data.get('election_date'),
                    'state': 'Michigan',
                    'state_postal': 'MI',
                    'total_precincts': race_data.get('reporting_units', [{}])[0].get('precincts_total', 0),
                    'precincts_reporting': race_data.get('reporting_units', [{}])[0].get('precincts_reporting', 0),
                    'total_votes': race_data.get('reporting_units', [{}])[0].get('total_votes', 0),
                    'expected_votes': race_data.get('reporting_units', [{}])[0].get('total_expected_vote', 0),
                    'eevp': race_data.get('reporting_units', [{}])[0].get('eevp', 0),
                    'eevp_display': f"{race_data.get('reporting_units', [{}])[0].get('eevp', 0)}%",
                    'reporting_percentage': (race_data.get('reporting_units', [{}])[0].get('precincts_reporting', 0) / race_data.get('reporting_units', [{}])[0].get('precincts_total', 1)) * 100 if race_data.get('reporting_units', [{}])[0].get('precincts_total', 0) > 0 else 0,
                    'data_source': 'ap'
                })
        
        return normalized
    
    def normalize_file(self, file_path: Path) -> Dict[str, Any]:
        """Normalize a single election JSON file."""
        logger.info(f"Normalizing {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return {}
        
        # Detect format
        format_type = self.detect_format(data)
        logger.info(f"Detected format: {format_type}")
        
        # Normalize race metadata
        race_metadata = self.normalize_race_metadata(data, format_type)
        
        # Normalize candidates
        normalized_candidates = []
        if format_type in ['2016', '2020']:
            candidates = data.get('candidates', [])
            for candidate in candidates:
                normalized_candidates.append(self.normalize_candidate(candidate, format_type))
        elif format_type == '2022':
            if isinstance(data, list) and len(data) > 0:
                candidate_metadata = data[0].get('candidate_metadata', {})
                for candidate_id, candidate_data in candidate_metadata.items():
                    normalized_candidates.append(self.normalize_candidate(candidate_data, format_type))
        
        # Normalize counties
        normalized_counties = []
        if format_type in ['2016', '2020']:
            counties = data.get('counties', [])
            for county in counties:
                normalized_counties.append(self.normalize_county(county, format_type))
        elif format_type == '2022':
            if isinstance(data, list) and len(data) > 0:
                reporting_units = data[0].get('reporting_units', [])
                for unit in reporting_units:
                    if unit.get('level') == 'county':
                        normalized_counties.append(self.normalize_county(unit, format_type))
        
        # Create normalized structure
        normalized_data = {
            'metadata': {
                'original_file': str(file_path),
                'format_type': format_type,
                'normalization_timestamp': datetime.now().isoformat(),
                'normalizer_version': '1.0.0'
            },
            'race': race_metadata,
            'candidates': normalized_candidates,
            'counties': normalized_counties,
            'summary': {
                'total_candidates': len(normalized_candidates),
                'total_counties': len(normalized_counties),
                'total_votes': sum(c.get('votes', 0) for c in normalized_candidates),
                'reporting_percentage': race_metadata.get('reporting_percentage', 0)
            }
        }
        
        return normalized_data
    
    def normalize_all_files(self, input_dir: str = ".") -> None:
        """Normalize all election JSON files in the input directory."""
        input_path = Path(input_dir)
        json_files = list(input_path.glob("*.json"))
        
        logger.info(f"Found {len(json_files)} JSON files to normalize")
        
        for json_file in json_files:
            if 'normalized' not in json_file.name:  # Skip already normalized files
                try:
                    normalized_data = self.normalize_file(json_file)
                    if normalized_data:
                        # Create output filename
                        output_filename = f"normalized_{json_file.stem}.json"
                        output_path = self.output_dir / output_filename
                        
                        # Save normalized data
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(normalized_data, f, indent=2, ensure_ascii=False)
                        
                        logger.info(f"Saved normalized data to {output_path}")
                        
                except Exception as e:
                    logger.error(f"Error normalizing {json_file}: {e}")
    
    def create_summary_report(self) -> None:
        """Create a summary report of all normalized files."""
        summary = {
            'normalization_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_files_processed': 0,
                'files_by_format': {},
                'total_counties': 0,
                'total_candidates': 0,
                'total_votes': 0
            },
            'file_details': []
        }
        
        normalized_files = list(self.output_dir.glob("normalized_*.json"))
        
        for file_path in normalized_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_info = {
                    'filename': file_path.name,
                    'original_file': data['metadata']['original_file'],
                    'format_type': data['metadata']['format_type'],
                    'race_name': data['race']['race_name'],
                    'election_date': data['race']['election_date'],
                    'counties': len(data['counties']),
                    'candidates': len(data['candidates']),
                    'total_votes': data['summary']['total_votes']
                }
                
                summary['file_details'].append(file_info)
                summary['normalization_summary']['total_files_processed'] += 1
                summary['normalization_summary']['total_counties'] += file_info['counties']
                summary['normalization_summary']['total_candidates'] += file_info['candidates']
                summary['normalization_summary']['total_votes'] += file_info['total_votes']
                
                # Count by format
                format_type = file_info['format_type']
                summary['normalization_summary']['files_by_format'][format_type] = summary['normalization_summary']['files_by_format'].get(format_type, 0) + 1
                
            except Exception as e:
                logger.error(f"Error processing {file_path} for summary: {e}")
        
        # Save summary report
        summary_path = self.output_dir / "normalization_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Summary report saved to {summary_path}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("NORMALIZATION SUMMARY")
        print("="*60)
        print(f"Total files processed: {summary['normalization_summary']['total_files_processed']}")
        print(f"Files by format:")
        for format_type, count in summary['normalization_summary']['files_by_format'].items():
            print(f"  {format_type}: {count}")
        print(f"Total counties: {summary['normalization_summary']['total_counties']}")
        print(f"Total candidates: {summary['normalization_summary']['total_candidates']}")
        print(f"Total votes: {summary['normalization_summary']['total_votes']:,}")
        print("="*60)


def main():
    """Main function to run the normalization process."""
    print("Election Data Normalizer")
    print("=" * 40)
    
    # Initialize normalizer
    normalizer = ElectionDataNormalizer()
    
    # Normalize all files
    normalizer.normalize_all_files()
    
    # Create summary report
    normalizer.create_summary_report()
    
    print(f"\nNormalized files saved to: {normalizer.output_dir}")
    print("Process complete!")


if __name__ == "__main__":
    main()
