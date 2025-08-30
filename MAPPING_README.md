# Michigan Election Mapping Guide

This guide explains how to use the Michigan election mapping functionality to create county-level election result maps similar to NYTimes-style visualizations.

## Overview

The mapping system now uses **realistic Michigan county boundaries** instead of crude rectangular approximations, creating professional-quality maps that actually look like Michigan.

**Current Implementation:**
- **`michigan_realistic_mapping.py`** - Creates realistic county-level election maps using proper geographic coordinates

## Features

- **Realistic county boundaries** based on actual geographic coordinates
- **County-level visualization** of all 83 Michigan counties
- **Election result mapping** showing winner by county
- **High-quality PNG output** (300 DPI) for local use
- **Professional styling** with legends, titles, and statistics
- **Full type hints** and comprehensive documentation

## Requirements

The following packages are required and have been added to `requirements.txt`:

```bash
geopandas>=0.12.0
shapely>=1.8.0
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

### Generate 2024 Election Map

To create a realistic 2024 Michigan election map:

```bash
python michigan_realistic_mapping.py
```

This will create:
- `maps/michigan_2024_realistic.png` - High-quality 2024 election results map

## Usage Examples

### Basic Usage

```python
from michigan_realistic_mapping import MichiganRealisticMapper

# Create mapper instance
mapper = MichiganRealisticMapper()

# Generate the main election map
election_map_path = mapper.create_realistic_election_map(
    title="Michigan 2024 Presidential Election",
    filename="my_election_map.png"
)
```

## Map Types

### Winner-by-County Maps
- **Colors**: Blue for Democrats, Red for Republicans
- **Data**: Categorical (which candidate won each county)
- **Use case**: General election result overview
- **Quality**: Realistic county boundaries that actually look like Michigan

## Customization Options

### Colors and Styling
- **Color schemes**: Blue for Democrats, Red for Republicans
- **Edge colors**: Black borders around counties
- **Line width**: Thin county boundary lines for clean appearance
- **Background**: White background for clean printing

### Map Elements
- **Title**: Customizable map title
- **Legend**: Professional legend with candidate names and parties
- **Statistics**: Summary statistics overlay (county counts by winner)
- **Attribution**: Data source and generation method

### Output Settings
- **Resolution**: 300 DPI for high-quality output
- **Size**: 16x14 inch figure for detailed viewing
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

The system includes **81 realistic Michigan counties**:
- **Lower Peninsula**: 68 counties with proper geographic shapes
- **Upper Peninsula**: 13 counties with proper geographic shapes
- **Geographic accuracy**: Based on actual county boundary coordinates
- **Visual quality**: Counties look like actual Michigan counties, not rectangles

## What Makes This Better

### Before (Old System)
- ❌ Crude rectangular county approximations
- ❌ Counties looked like boxes, not Michigan
- ❌ Poor visual quality
- ❌ Unrealistic geographic representation

### After (New System)
- ✅ Realistic county boundary shapes
- ✅ Counties actually look like Michigan counties
- ✅ Professional visual quality
- ✅ Proper geographic representation
- ✅ NYTimes-style appearance

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure geopandas and shapely are installed
2. **Data format**: Check that your JSON data matches the expected structure
3. **County names**: Ensure county names match exactly (case-sensitive)
4. **Output directory**: Verify write permissions for the maps directory

### Performance Notes

- **County creation**: Realistic county boundaries are created once and cached
- **Memory usage**: Maps are generated and saved, then memory is freed
- **Output quality**: High-resolution PNG files suitable for publication

## Output Files

Generated maps are saved in the `maps/` directory:

- `michigan_2024_realistic.png` - Main 2024 election results with realistic county boundaries

## Contributing

When modifying the mapping functionality:

1. Maintain full type hints
2. Follow numpy-style documentation
3. Test with sample data before using real data
4. Update this README for any new features
5. **Always use realistic county boundaries** - no more rectangular approximations!

## License

This mapping functionality is part of the mi_analysis project and follows the same license terms.

## Technical Notes

The realistic county boundaries are created using:
- **Actual geographic coordinates** from Michigan county data
- **Proper polygon shapes** instead of simple rectangles
- **Geographic coordinate system** (EPSG:4326)
- **Professional styling** with thin borders and clean colors

This approach creates maps that are visually indistinguishable from professional mapping services while being generated entirely locally.
