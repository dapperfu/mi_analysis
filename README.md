# Michigan Election Data Analysis

This repository contains normalized election data from the New York Times API for Michigan elections from 2016-2024, along with analysis tools and notebooks.

## Data Structure

### Original Data Format
The NYTimes API provides election data in different formats across different years:
- **2016**: Traditional format with `candidates` and `counties` arrays
- **2020**: Enhanced format with additional absentee voting data
- **2022**: New format with `candidate_metadata` and `reporting_units` structure

### Normalized Data Format
All data is normalized to a consistent structure with the following key sections:

```json
{
  "metadata": {
    "original_file": "source_file.json",
    "format_type": "2016|2020|2022",
    "normalization_timestamp": "ISO timestamp",
    "normalizer_version": "1.0.0"
  },
  "race": {
    "race_id": "unique_race_identifier",
    "race_name": "President|Governor|etc.",
    "election_date": "YYYY-MM-DD",
    "state": "Michigan",
    "state_postal": "MI",
    "total_precincts": 4974,
    "precincts_reporting": 4974,
    "total_votes": 5530000,
    "reporting_percentage": 100.0,
    "winner": "Candidate Name",
    "margin": 2.78,
    "margin_display": "D+3"
  },
  "candidates": [
    {
      "nyt_id": "candidate-identifier",
      "candidate_key": "short_key",
      "first_name": "First",
      "last_name": "Last",
      "display_name": "Full Display Name",
      "party_id": "democrat|republican|etc.",
      "party_name": "Democratic Party",
      "party_abbreviation": "Dem.",
      "votes": 2804040,
      "vote_percentage": 50.6,
      "winner": true,
      "incumbent": false,
      "electoral_votes": 16
    }
  ],
  "counties": [
    {
      "fips": "26001",
      "name": "Alcona",
      "precincts_total": 12,
      "precincts_reporting": 12,
      "total_votes": 7064,
      "expected_votes": 7064,
      "eevp": 100,
      "reporting_percentage": 100.0,
      "results": {
        "bidenj": 2142,
        "trumpd": 4848
      },
      "data_source": "edison|ap"
    }
  ],
  "summary": {
    "total_candidates": 6,
    "total_counties": 83,
    "total_votes": 5530000,
    "reporting_percentage": 100.0
  }
}
```

## Key Features

### Data Granularity
- **Smallest Unit**: County-level reporting (not individual precincts or polling locations)
- **Precinct Counts**: Available as totals per county, but not individual precinct results
- **Vote Types**: Includes total votes, absentee votes (where available), and breakdowns by voting method

### Consistent Fields
- All candidates have standardized fields regardless of original format
- County data is normalized with consistent field names
- Historical margins preserved where available
- Data source attribution maintained

## Usage

### Normalization Script
```bash
# Run the normalization script to convert all JSON files
python normalize_election_data.py

# This will create a 'normalized_data' directory with:
# - normalized_2016.general.json
# - normalized_2020.general.json  
# - normalized_2022.json
# - normalization_summary.json
```

### Analysis Notebooks
- `01_Election_Data_Downloader.ipynb`: Download fresh data from NYTimes API
- `02_*_Processing.ipynb`: Process and analyze specific election years
- `*_Results_Plot.ipynb`: Generate visualizations and comparisons
- `Election_Meta_Analysis.py`: Comprehensive analysis script

## Data Sources

- **2016-2020**: Edison Research (via NYTimes)
- **2022+**: Associated Press (via NYTimes)
- **Coverage**: Michigan statewide elections (President, Governor, Senate, etc.)

## Requirements

```bash
pip install -r requirements.txt
```

## Notes

- All data is at the county level (83 Michigan counties)
- Precinct counts are totals, not individual results
- Historical margins available for 2020 data
- Absentee voting data available for 2020+ elections
- Data is certified and final (not real-time)

## Contributing

When making changes:
1. Update the source `.py` files (not the `.ipynb` files directly)
2. Regenerate notebooks using the source scripts
3. Follow the commit message format specified in the rules
4. Ensure all data is properly normalized before analysis
