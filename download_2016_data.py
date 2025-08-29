#!/usr/bin/env python3
"""
Download 2016 Michigan Election Data

This script downloads the 2016 election results from the NYTimes interactive page
and saves them in JSON format for processing.

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import requests
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_via_api(election_type: str) -> Optional[Dict[str, Any]]:
    """Try to download data via the NYTimes API endpoint."""
    urls = {
        'general': "https://static01.nyt.com/elections-assets/2016/data/2016-11-08/results-michigan-president.json",
        'primary': "https://static01.nyt.com/elections-assets/2016/data/2016-03-08/results-michigan-democratic-primary.json"
    }
    
    url = urls.get(election_type)
    if not url:
        logger.error(f"Unknown election type: {election_type}")
        return None
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully downloaded 2016 {election_type} data via API")
            return data
        else:
            logger.warning(f"API request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading via API: {e}")
        return None


def download_via_selenium(election_type: str) -> Optional[Dict[str, Any]]:
    """Download data by scraping the interactive page."""
    urls = {
        'general': "https://www.nytimes.com/elections/2016/results/michigan/president",
        'primary': "https://www.nytimes.com/elections/2016/results/michigan/democratic-primary"
    }
    
    url = urls.get(election_type)
    if not url:
        logger.error(f"Unknown election type: {election_type}")
        return None
    
    # Set up Firefox options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        with webdriver.Firefox(options=options) as browser:
            logger.info(f"Loading page: {url}")
            browser.get(url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Try to extract election data
            try:
                # Try to get election data from various sources
                for var_name in ['electionData', 'resultsData', 'raceData', 'eln_races']:
                    data = browser.execute_script(f"return window.{var_name}")
                    if data:
                        logger.info(f"Found {var_name} variable")
                        return data
                
                # Try to extract data from the DOM
                logger.info("Attempting to extract data from DOM elements")
                return extract_data_from_dom(browser, election_type)
                
            except Exception as e:
                logger.error(f"Error extracting data: {e}")
                return None
                
    except Exception as e:
        logger.error(f"Error with Selenium: {e}")
        return None


def extract_data_from_dom(browser, election_type: str) -> Optional[Dict[str, Any]]:
    """Extract election data from DOM elements."""
    try:
        # Look for the results table
        results_table = browser.find_element(By.CSS_SELECTOR, "table")
        if results_table:
            logger.info("Found results table")
            
            # Extract candidate data
            candidates = []
            rows = results_table.find_elements(By.CSS_SELECTOR, "tr")
            
            for row in rows[1:]:  # Skip header row
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                if len(cells) >= 3:
                    candidate_name = cells[0].text.strip()
                    party = cells[1].text.strip()
                    votes = cells[2].text.strip().replace(',', '')
                    
                    try:
                        vote_count = int(votes)
                    except ValueError:
                        vote_count = 0
                    
                    candidates.append({
                        'name': candidate_name,
                        'party': party,
                        'votes': vote_count
                    })
            
            # Create basic data structure
            data = {
                'election_type': election_type,
                'year': 2016,
                'state': 'Michigan',
                'candidates': candidates,
                'source': 'NYTimes DOM extraction'
            }
            
            return data
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting data from DOM: {e}")
        return None


def create_fallback_data(election_type: str) -> Dict[str, Any]:
    """Create fallback data structure if download fails."""
    logger.warning(f"Creating fallback data for 2016 {election_type} election")
    
    if election_type == 'general':
        return {
            'election_type': 'general',
            'year': 2016,
            'state': 'Michigan',
            'race': 'President',
            'candidates': [
                {
                    'name': 'Donald J. Trump',
                    'party': 'Republican',
                    'votes': 2279543,
                    'percentage': 47.5,
                    'winner': True
                },
                {
                    'name': 'Hillary Clinton',
                    'party': 'Democrat',
                    'votes': 2268839,
                    'percentage': 47.3,
                    'winner': False
                }
            ],
            'source': 'Fallback data - manual entry required'
        }
    elif election_type == 'primary':
        return {
            'election_type': 'primary',
            'year': 2016,
            'state': 'Michigan',
            'race': 'Democratic Primary',
            'candidates': [
                {
                    'name': 'Bernie Sanders',
                    'party': 'Democrat',
                    'votes': 598943,
                    'percentage': 49.8,
                    'winner': True
                },
                {
                    'name': 'Hillary Clinton',
                    'party': 'Democrat',
                    'votes': 576795,
                    'percentage': 47.9,
                    'winner': False
                }
            ],
            'source': 'Fallback data - manual entry required'
        }
    else:
        return {
            'election_type': election_type,
            'year': 2016,
            'state': 'Michigan',
            'error': 'Unknown election type',
            'source': 'Fallback data - manual entry required'
        }


def main():
    """Main function to download 2016 election data."""
    parser = argparse.ArgumentParser(description='Download 2016 Michigan election data')
    parser.add_argument('--type', choices=['general', 'primary'], required=True,
                       help='Type of election to download')
    parser.add_argument('--output', type=str, default=None,
                       help='Output filename (default: 2016.{type}.json)')
    
    args = parser.parse_args()
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        output_file = f"2016.{args.type}.json"
    
    logger.info(f"Starting download of 2016 {args.type} election data")
    
    # Try API first
    data = download_via_api(args.type)
    
    # If API fails, try Selenium
    if not data:
        logger.info("API download failed, trying Selenium...")
        data = download_via_selenium(args.type)
    
    # If both fail, create fallback data
    if not data:
        logger.warning("Both download methods failed, creating fallback data")
        data = create_fallback_data(args.type)
    
    # Save data to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved data to {output_file}")
    except Exception as e:
        logger.error(f"Error saving data to {output_file}: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
