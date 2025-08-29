# Michigan Election Data Analysis Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

A comprehensive analysis toolkit for Michigan election data from 2016-2024, featuring data normalization, voter behavior analysis, geographic mapping, and cross-cycle correlation studies.

## 🎯 Project Overview

This project provides a complete pipeline for analyzing Michigan election data, from raw NYTimes API downloads to sophisticated voter behavior pattern analysis. It addresses the challenge of inconsistent data formats across different election cycles and provides tools for deep electoral analysis.

### Key Features

- **Multi-format Data Processing**: Handles NYTimes API data from 2016-2024 with different structures
- **Data Normalization**: Converts all data to a consistent, analyzable format
- **Voter Behavior Analysis**: Identifies patterns in voter migration and party shifts
- **Geographic Visualization**: County-level mapping and regional clustering
- **Cross-cycle Correlations**: Analysis of relationships between different election cycles
- **Automated Workflows**: Makefile-driven build system for reproducible analysis

## 📊 Data Coverage

### Election Cycles
- **2016**: Presidential primary and general elections
- **2018**: Gubernatorial and statewide elections
- **2020**: Presidential primary (Democratic) and general elections
- **2022**: Gubernatorial, Attorney General, and Secretary of State elections
- **2024**: Presidential election (ongoing)

### Geographic Scope
- **State**: Michigan (MI)
- **Counties**: 83 counties with complete coverage
- **Precincts**: County-level aggregation (not individual precinct results)
- **Data Sources**: Edison Research (2016-2020), Associated Press (2022+)

## 🏗️ Project Architecture

```
mi_analysis/
├── 📁 venv/                    # Python virtual environment
├── 📁 normalized_data/         # Standardized election data
├── 📁 maps/                    # Geographic visualization outputs
├── 📄 *.py                     # Core Python analysis scripts
│   ├── Election_Meta_Analysis.py      # Main voter behavior analysis
│   ├── Proposition_Trump_Analysis.py  # Proposition voting analysis
│   ├── michigan_election_map.py       # Geographic visualization
│   └── normalize_election_data.py     # Data normalization
├── 📓 *.ipynb                  # Jupyter notebooks (auto-generated)
├── 📊 *.ft                     # Feather format data files
├── 📋 *.json                   # Raw NYTimes API data
├── 📋 Makefile                 # Build automation
├── 📋 requirements.txt         # Python dependencies
└── 📋 README.md               # This documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.12 or higher
- **Git**: For version control
- **Make**: For build automation (GNU Make on Linux/macOS)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mi_analysis
   ```

2. **Set up virtual environment and install dependencies**
   ```bash
   make venv
   ```

3. **Download and process all election data**
   ```bash
   make all
   ```

4. **Run the comprehensive analysis**
   ```bash
   venv/bin/python Election_Meta_Analysis.py
   ```

### Alternative Setup (Manual)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download data
python download_2016_data.py --type general
python download_2016_data.py --type primary
python download_2018_data.py
python download_2020_data.py --type general
python download_2020_data.py --type primary
python download_2022_data.py
python download_2024_data.py

# Normalize data
python normalize_election_data.py

# Run analysis
python Election_Meta_Analysis.py
```

## 📁 Core Components

### 1. Data Download Scripts

#### `download_*_data.py`
- **Purpose**: Download raw election data from NYTimes API
- **Features**: 
  - Rate limiting and error handling
  - Multiple election types (primary, general)
  - JSON output with metadata
- **Usage**: `python download_2024_data.py`

#### `create_2024_data.py`
- **Purpose**: Create synthetic 2024 data for testing
- **Features**: Generates realistic election data patterns

### 2. Data Normalization

#### `normalize_election_data.py`
- **Purpose**: Convert diverse NYTimes formats to consistent structure
- **Input Formats**:
  - **2016**: Traditional `candidates` + `counties` arrays
  - **2020**: Enhanced format with absentee voting data
  - **2022**: New `candidate_metadata` + `reporting_units` structure
- **Output**: Standardized JSON with consistent field names

#### Normalized Data Structure
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
  "candidates": [...],
  "counties": [...],
  "summary": {...}
}
```

### 3. Core Analysis Engine

#### `Election_Meta_Analysis.py`
- **Purpose**: Comprehensive voter behavior pattern analysis
- **Key Analyses**:
  1. **Primary to General Shifts**: Bernie Sanders → Biden/Trump migration
  2. **County-level Rightward Shifts**: 2016-2024, 2020-2024 trends
  3. **Ted Cruz Primary Performance**: Correlation with general election outcomes
  4. **Cross-cycle Correlation Analysis**: Relationships between different elections
  5. **Voter Migration Patterns**: Party switching and candidate loyalty
  6. **Geographic Clustering**: Regional voting pattern identification

#### `Proposition_Trump_Analysis.py`
- **Purpose**: Analyze proposition voting patterns vs. Trump performance
- **Key Analyses**:
  1. **Prop 1 (2020)**: Parks revenue spending changes
  2. **Prop 2 (2020)**: Electronic data warrant requirements
  3. **Prop 3 (2022)**: Reproductive freedom constitutional rights
  4. **Trump Performance Correlation**: Relationship between proposition support and Trump vote shifts
  5. **Cannabis Policy Analysis**: Marijuana legalization voting patterns

#### Analysis Classes
- **`ElectionMetaAnalyzer`**: Main analysis orchestrator
- **Data Processing Methods**: Handle different election formats
- **Statistical Analysis**: Correlation matrices, shift calculations
- **Geographic Analysis**: County clustering and regional patterns

### 4. Geographic Visualization

#### `michigan_election_map.py`
- **Purpose**: Create county-level election maps
- **Features**:
  - Choropleth maps for vote percentages
  - Multi-year comparison visualizations
  - Custom color schemes and legends
- **Output**: PNG files in `maps/` directory

### 5. Jupyter Notebooks

#### Auto-generated Analysis Notebooks
- **`01_Election_Data_Downloader.ipynb`**: Interactive data downloading
- **`02_*_Processing.ipynb`**: Year-specific data processing
- **`*_Results_Plot.ipynb`**: Visualization and analysis
- **`Election_Meta_Analysis.ipynb`**: Comprehensive analysis interface

**Note**: All notebooks are generated from `.py` source files. Edit the Python files, not the notebooks directly.

## 🔧 Build System

### Makefile Targets

```bash
# Core workflow
make all          # Complete pipeline: download → normalize → convert
make download     # Download all JSON data files
make normalize    # Normalize all JSON data files
make convert      # Convert normalized data to .ft format

# Environment management
make venv         # Create virtual environment and install dependencies

# Cleanup
make clean        # Remove all generated files
make clean-json   # Remove JSON files only
make clean-normalized # Remove normalized data only
make clean-ft     # Remove .ft files only

# Help
make help         # Show available targets
```

### Build Dependencies

The Makefile ensures proper dependency resolution:
- **Virtual Environment**: All Python operations depend on `venv`
- **Data Pipeline**: Normalization depends on downloads, conversion depends on normalization
- **Parallel Processing**: Independent election years can be processed simultaneously

## 📊 Data Analysis Capabilities

### 1. Voter Behavior Patterns

#### Primary to General Election Shifts
- **Bernie Sanders → Biden Migration**: Analyze 2016 primary supporters' 2020 general behavior
- **Ted Cruz → Trump Correlation**: Republican primary vs. general election patterns
- **Party Loyalty Analysis**: Voter retention rates across cycles

#### Cross-cycle Performance Analysis
- **Republican Performance Trends**: 2016-2020-2024 presidential cycles
- **Gubernatorial Patterns**: 2018 vs. 2022 comparison
- **Statewide Office Correlations**: Governor, AG, Secretary of State relationships

### 2. Geographic Analysis

#### County-level Clustering
- **K-means Clustering**: Identify regional voting patterns
- **Geographic Correlations**: Spatial relationships in voting behavior
- **Regional Shifts**: Identify areas with consistent vs. changing patterns

#### Mapping and Visualization
- **Choropleth Maps**: County-level vote percentage visualization
- **Multi-year Comparisons**: Side-by-side election result comparisons
- **Shift Analysis**: Visual representation of voting changes

### 3. Statistical Analysis

#### Correlation Analysis
- **Cross-cycle Correlations**: Relationships between different election years
- **Candidate Performance**: Individual candidate correlation patterns
- **Party Performance**: Democratic vs. Republican correlation analysis

#### Shift Calculations
- **Rightward Shifts**: Republican vote percentage changes
- **Voter Migration**: Party switching and candidate loyalty
- **Performance Predictors**: Factors predicting election outcomes

## 🐍 Python Environment

### Virtual Environment
- **Name**: `venv`
- **Python Version**: 3.12+
- **Isolation**: Complete separation from system Python
- **Dependencies**: All packages installed locally

### Key Dependencies

#### Core Data Processing
```bash
pandas>=1.5.0      # Data manipulation and analysis
numpy>=1.21.0      # Numerical computing
jsonschema>=4.0.0  # JSON validation
```

#### Web Scraping and Data Download
```bash
requests>=2.28.0   # HTTP requests
selenium>=4.0.0    # Web automation (if needed)
```

#### Visualization
```bash
matplotlib>=3.5.0  # Basic plotting
seaborn>=0.11.0    # Statistical visualization
plotly>=5.0.0      # Interactive plots
```

#### Geographic Analysis
```bash
geopandas>=0.12.0  # Geographic data processing
shapely>=1.8.0     # Geometric operations
pyproj>=3.3.0      # Projection handling
```

#### Development Tools
```bash
mypy>=0.991        # Type checking
black>=22.0.0      # Code formatting
flake8>=5.0.0      # Linting
pytest>=7.0.0      # Testing
```

## 📈 Usage Examples

### 1. Basic Data Analysis

```python
from Election_Meta_Analysis import ElectionMetaAnalyzer

# Initialize analyzer
analyzer = ElectionMetaAnalyzer()

# Run complete analysis
analyzer.run_complete_analysis()

# Access combined data
combined_data = analyzer.combined_df
print(f"Analyzed {len(combined_data)} counties")
```

### 2. Custom Analysis

```python
# Calculate specific voter shifts
analyzer.calculate_voter_shifts()

# Analyze Bernie Sanders connections
analyzer.analyze_bernie_bernie_connections()

# Perform geographic clustering
analyzer.perform_geographic_clustering()

# Generate correlation matrix
analyzer.generate_correlation_matrix()

# Analyze proposition voting patterns
from Proposition_Trump_Analysis import PropositionTrumpAnalyzer
prop_analyzer = PropositionTrumpAnalyzer()
prop_analyzer.run_complete_analysis()
```

### 3. Data Export

```python
# Save to Feather format (fast, efficient)
analyzer.combined_df.to_feather("my_analysis.ft")

# Export to CSV
analyzer.combined_df.to_csv("election_analysis.csv")

# Save specific analyses
bernie_analysis = analyzer.combined_df[['county', 'prim_16_sanders_dem_pct', 'pres_20_biden_pct']]
bernie_analysis.to_csv("bernie_biden_analysis.csv")
```

## 🔍 Data Quality and Validation

### Data Source Reliability
- **NYTimes API**: Official election data source
- **Data Certification**: Final, certified results (not real-time)
- **Coverage**: Complete Michigan county coverage
- **Timestamps**: All data includes processing timestamps

### Validation Features
- **Format Detection**: Automatic detection of data structure
- **Field Mapping**: Consistent field names across formats
- **Data Integrity**: Preservation of original vote counts
- **Metadata Tracking**: Source file and processing information

### Known Limitations
- **County-level Granularity**: No individual precinct results
- **Absentee Data**: Limited to 2020+ elections
- **Historical Margins**: Not available for all election cycles
- **Real-time Updates**: Data is final, not live

## 🧪 Testing and Quality Assurance

### Test Suite
```bash
# Run all tests
venv/bin/pytest

# Run with coverage
venv/bin/pytest --cov=.

# Run specific test file
venv/bin/pytest test_analysis.py
```

### Code Quality
```bash
# Format code
venv/bin/black .

# Lint code
venv/bin/flake8 .

# Type checking
venv/bin/mypy .
```

### Pre-commit Hooks
- **Automatic Formatting**: Black formatting on commit
- **Linting**: Flake8 checks before commit
- **Type Checking**: MyPy validation
- **Notebook Validation**: Ensure notebook integrity

## 📚 Documentation and Resources

### Code Documentation
- **Docstrings**: NumPy-style documentation for all functions
- **Type Hints**: Full MyPy typing support
- **Inline Comments**: Detailed explanation of complex logic
- **README**: Comprehensive project overview

### Data Documentation
- **Field Descriptions**: Detailed explanation of all data fields
- **Format Specifications**: Input/output format documentation
- **Sample Data**: Example data structures and usage
- **API Documentation**: NYTimes API integration details

### Analysis Documentation
- **Methodology**: Statistical analysis approaches
- **Interpretation**: How to interpret results
- **Limitations**: Known constraints and caveats
- **Best Practices**: Recommended analysis workflows

## 🤝 Contributing

### Development Workflow
1. **Source Files**: Edit `.py` files, not `.ipynb` files
2. **Notebook Generation**: Regenerate notebooks from source scripts
3. **Testing**: Run tests before committing
4. **Documentation**: Update docstrings and README as needed

### Code Standards
- **Python**: PEP 8 compliance with Black formatting
- **Type Hints**: Full MyPy typing support
- **Documentation**: NumPy-style docstrings
- **Testing**: Comprehensive test coverage

### Commit Guidelines
- **Format**: Include filename and change description
- **Context**: Explain why changes were made
- **Attribution**: Include AI assistance information
- **Validation**: Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2022 ++ATH0**

## 🙏 Acknowledgments

- **NYTimes**: Election data API and coverage
- **Edison Research**: 2016-2020 election data
- **Associated Press**: 2022+ election data
- **Michigan Department of State**: Election administration and certification

## 📞 Support and Contact

### Issues and Questions
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and inline code documentation
- **Examples**: Review Jupyter notebooks for usage patterns

### Getting Help
1. **Check Documentation**: Start with this README
2. **Review Examples**: Look at existing analysis notebooks
3. **Examine Code**: Read source code and docstrings
4. **Run Tests**: Ensure your environment is working correctly

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Python Compatibility**: 3.12+  
**License**: MIT
