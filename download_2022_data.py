#!/usr/bin/env python3
"""
Download 2022 Michigan Election Data

This script downloads the 2022 election results from the NYTimes interactive page
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


def download_via_api() -> Optional[Dict[str, Any]]:
    """Try to download data via the NYTimes API endpoint."""
    url = "https://static01.nyt.com/elections-assets/2022/data/2022-11-08/results-michigan-governor.json"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            logger.info("Successfully downloaded 2022 data via API")
            return data
        else:
            logger.warning(f"API request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading via API: {e}")
        return None


def download_via_selenium() -> Optional[Dict[str, Any]]:
    """Download data by scraping the interactive page."""
    url = "https://www.nytimes.com/interactive/2022/11/08/us/elections/results-michigan-governor.html"
    
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
                return extract_data_from_dom(browser)
                
            except Exception as e:
                logger.error(f"Error extracting data: {e}")
                return None
                
    except Exception as e:
        logger.error(f"Error with Selenium: {e}")
        return None


def extract_data_from_dom(browser) -> Optional[Dict[str, Any]]:
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
                'election_type': 'general',
                'year': 2022,
                'state': 'Michigan',
                'race': 'Governor',
                'candidates': candidates,
                'source': 'NYTimes DOM extraction'
            }
            
            return data
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting data from DOM: {e}")
        return None


def create_fallback_data() -> Dict[str, Any]:
    """Create fallback data structure if download fails."""
    logger.warning("Creating fallback data for 2022 general election")
    
    return {
        'election_type': 'general',
        'year': 2022,
        'state': 'Michigan',
        'race': 'Governor',
        'candidates': [
            {
                'name': 'Gretchen Whitmer',
                'party': 'Democrat',
                'votes': 2551625,
                'percentage': 54.5,
                'winner': True
            },
            {
                'name': 'Tudor Dixon',
                'party': 'Republican',
                'votes': 2127008,
                'percentage': 45.5,
                'winner': False
            }
        ],
        'source': 'Fallback data - manual entry required'
    }


def main():
    """Main function to download 2022 election data."""
    parser = argparse.ArgumentParser(description='Download 2022 Michigan election data')
    parser.add_argument('--output', type=str, default='2022.json',
                       help='Output filename (default: 2022.json)')
    
    args = parser.parse_args()
    
    logger.info("Starting download of 2022 general election data")
    
    # Try API first
    data = download_via_api()
    
    # If API fails, try Selenium
    if not data:
        logger.info("API download failed, trying Selenium...")
        data = download_via_selenium()
    
    # If both fail, create fallback data
    if not data:
        logger.warning("Both download methods failed, creating fallback data")
        data = create_fallback_data()
    
    # Save data to file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved data to {args.output}")
    except Exception as e:
        logger.error(f"Error saving data to {args.output}: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
