# Michigan Election Mapping Guide

This guide explains how to use the Michigan election mapping functionality to create county-level election result maps similar to NYTimes-style visualizations.

## Overview

The mapping system consists of two main Python modules:

1. **`michigan_election_map.py`** - General Michigan county mapping class with sample data
2. **`michigan_2024_election_map.py`** - Specific 2024 presidential election results mapper

## Features

- **County-level visualization** of all 83 Michigan counties
- **Election result mapping** showing winner by county
- **Margin of victory mapping** with continuous color scales
- **High-quality PNG output** (300 DPI) for local use
- **Professional styling** with legends, titles, and statistics
- **Full type hints** and comprehensive documentation

## Requirements

The following packages are required and have been added to `requirements.txt`:

```bash
geopandas>=0.12.0
shapely>=1.8.0
fiona>=1.8.0
pyproj>=3.7.0
matplotlib>=3.5.0
pandas>=1.5.0
numpy>=1.21.0
```

## Installation

1. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Generate Sample Maps

To create sample maps with random data:

```bash
python michigan_election_map.py
```

This will create:
- `maps/michigan_election_2024_sample.png` - Sample winner-by-county map
- `maps/michigan_dem_percentage_sample.png` - Sample percentage map

### 2. Generate 2024 Election Maps

To create maps using your actual 2024 election data:

```bash
python michigan_2024_election_map.py
```

This will create:
- `maps/michigan_2024_election_map.png` - 2024 election results by county
- `maps/michigan_2024_margin_map.png` - Margin of victory map

## Usage Examples

### Basic Usage

```python
from michigan_2024_election_map import Michigan2024ElectionMapper

# Create mapper instance
mapper = Michigan2024ElectionMapper()

# Generate the main election map
election_map_path = mapper.create_2024_election_map(
    title="Michigan 2024 Presidential Election",
    filename="my_election_map.png"
)

# Generate margin of victory map
margin_map_path = mapper.create_margin_map(
    title="Margin of Victory by County",
    filename="my_margin_map.png"
)
```

### Custom Data Mapping

```python
from michigan_election_map import MichiganElectionMapper

# Create mapper instance
mapper = MichiganElectionMapper()

# Define your own county values
county_values = {
    'Wayne': 75.2,
    'Oakland': 65.8,
    'Macomb': 45.3,
    # ... add more counties
}

# Create custom map
custom_map_path = mapper.create_custom_map(
    county_values=county_values,
    value_column="vote_percentage",
    title="My Custom Map",
    filename="custom_map.png",
    colormap="RdBu_r"
)
```

## Map Types

### 1. Winner-by-County Maps
- **Colors**: Blue for Democrats, Red for Republicans
- **Data**: Categorical (which candidate won each county)
- **Use case**: General election result overview

### 2. Margin of Victory Maps
- **Colors**: Continuous scale from red to blue
- **Data**: Continuous (margin percentage)
- **Use case**: Understanding how close races were

### 3. Custom Value Maps
- **Colors**: Configurable colormaps
- **Data**: Any numeric values you provide
- **Use case**: Custom metrics, turnout, demographics, etc.

## Customization Options

### Colors and Styling
- **Color schemes**: Red-Blue, Blue-Red, or custom colormaps
- **Edge colors**: Black borders around counties
- **Line width**: Configurable county boundary thickness
- **Background**: White background for clean printing

### Map Elements
- **Title**: Customizable map title
- **Legend**: Automatic legend generation
- **Statistics**: Summary statistics overlay
- **County labels**: Optional county name annotations

### Output Settings
- **Resolution**: 300 DPI for high-quality output
- **Size**: Configurable figure dimensions
- **Format**: PNG format for compatibility
- **Directory**: Customizable output directory

## Data Format

The mapping system expects election data in this format:

```json
[
  {
    "county": "Wayne",
    "pres_24_kamala_harris_pct": 0.7502,
    "pres_24_donald_j._trump_pct": 0.2498,
    "pres_24_total": 1234567
  }
]
```

## County Coverage

The system includes all 83 Michigan counties:
- **Lower Peninsula**: 68 counties
- **Upper Peninsula**: 15 counties
- **Geographic accuracy**: Approximate bounding boxes for demonstration

For production use, consider using official county boundary shapefiles for more accurate geometries.

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all packages are installed
2. **Data format**: Check that your JSON data matches the expected structure
3. **County names**: Ensure county names match exactly (case-sensitive)
4. **Output directory**: Verify write permissions for the maps directory

### Performance Notes

- **First run**: May take longer as county geometries are created
- **Large datasets**: Consider filtering data for better performance
- **Memory usage**: Maps are generated and saved, then memory is freed

## Advanced Usage

### Custom County Boundaries

To use official county boundary files instead of approximate geometries:

```python
import geopandas as gpd

# Load official county boundaries
counties = gpd.read_file("path/to/county_boundaries.shp")
michigan_counties = counties[counties['STATE'] == 'MI']

# Use with the mapper
mapper.michigan_counties = michigan_counties
```

### Multiple Election Years

To compare different election years:

```python
# Load different year data
mapper_2020 = Michigan2024ElectionMapper()
mapper_2020.load_2024_election_data("2020.general.json")

mapper_2024 = Michigan2024ElectionMapper()
mapper_2024.load_2024_election_data("2024.json")

# Generate comparison maps
# ... implementation details
```

## Output Files

All generated maps are saved in the `maps/` directory with descriptive filenames:

- `michigan_2024_election_map.png` - Main 2024 election results
- `michigan_2024_margin_map.png` - 2024 margin of victory
- `michigan_election_2024_sample.png` - Sample data demonstration
- `michigan_dem_percentage_sample.png` - Sample percentage data

## Contributing

When modifying the mapping functionality:

1. Maintain full type hints
2. Follow numpy-style documentation
3. Test with sample data before using real data
4. Update this README for any new features

## License

This mapping functionality is part of the mi_analysis project and follows the same license terms.
