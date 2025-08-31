# Michigan Election Analysis: Comprehensive Analysis Suite

This folder contains a comprehensive suite of election analysis scripts for Michigan elections from 2016-2024, with focus on vote shifts, correlations, and voting behavior patterns.

## 🚀 Quick Start

To run all analyses at once:
```bash
cd analysis/
python run_all_analyses.py
```

To run individual analyses:
```bash
cd analysis/2018/
python 2018_comprehensive_analysis.py

cd analysis/primary_2016/
python 2016_primary_trump_shift_analysis.py
```

## 📁 Folder Structure

```
analysis/
├── README.md                           # This file
├── run_all_analyses.py                # Master runner for all analyses
├── ANALYSIS_SUMMARY.md                # Generated summary of all results
├── TECHNICAL_SUMMARY.json             # Technical execution data
│
├── 2018/                              # 2018 Election Analysis
│   ├── 2018_comprehensive_analysis.py
│   ├── 2018_races_vs_props_analysis.png
│   ├── 2018_propositions_performance_analysis.png
│   ├── 2018_vote_shifts_analysis.png
│   ├── 2018_comprehensive_analysis_report.md
│   └── 2018_technical_analysis.json
│
├── primary_2016/                      # 2016 Primary Analysis
│   ├── 2016_primary_trump_shift_analysis.py
│   ├── 2016_primary_comprehensive_analysis.png
│   ├── 2016_trump_shifts_analysis.png
│   ├── 2016_primary_trump_shift_report.md
│   └── 2016_primary_technical_analysis.json
│
├── 2020/                              # 2020 Election Analysis (Future)
├── 2022/                              # 2022 Election Analysis (Future)
├── 2024/                              # 2024 Election Analysis (Future)
├── shifts/                            # Cross-election Shift Analysis (Future)
├── correlations/                      # Cross-election Correlations (Future)
└── visualizations/                    # Shared Visualizations (Future)
```

## 🔍 Analysis Types

### 1. 2018 Comprehensive Analysis
**Script**: `2018/2018_comprehensive_analysis.py`

**Focus**: 
- 3 races vs 3 propositions correlations
- Diagonal lines showing 1:1 voting patterns
- Color-coded proposition performance analysis
- Vote shift analysis from 2016 primary

**Races Analyzed**:
- Governor (Whitmer vs Schuette)
- Secretary of State (Benson vs Johnson)
- Attorney General (Nessel vs Schuette)

**Propositions Analyzed**:
- Prop 1 (Marijuana Legalization)
- Prop 2 (Redistricting Commission)
- Prop 3 (Voting Rights)

**Key Features**:
- 3x3 grid analysis showing all race vs proposition correlations
- 1:1 voting diagonal lines to identify perfect alignment
- Color-coded analysis showing proposition performance
- County-level voting behavior patterns

### 2. 2016 Primary Trump Shift Analysis
**Script**: `primary_2016/2016_primary_trump_shift_analysis.py`

**Focus**:
- Bernie vs Hillary support patterns
- Vote shifts from primary to general election
- Trump support correlation with primary preferences
- County-level voting behavior analysis

**Key Features**:
- Primary support distribution analysis
- Trump shift magnitude and direction analysis
- Regional patterns (urban vs rural)
- Correlation analysis between primary and general voting

## 📊 Generated Outputs

### Visualizations
- **PNG Files**: High-resolution plots and charts
- **Correlation Heatmaps**: Pattern identification
- **Scatter Plots**: Relationship visualization with trend lines
- **Distribution Plots**: Pattern analysis and outlier identification

### Reports
- **Markdown Reports**: Comprehensive analysis findings
- **Technical JSON**: Statistical results and data for further analysis
- **Summary Reports**: Executive summaries of key insights

### Data Files
- **Correlation Matrices**: Statistical relationships between variables
- **Shift Calculations**: Vote shift magnitudes and directions
- **County-level Data**: Granular voting behavior analysis

## 🎯 Key Analysis Features

### Vote Shift Analysis
- **Magnitude Calculation**: Absolute and relative shift measurements
- **Direction Analysis**: Positive vs negative shifts
- **Regional Patterns**: Urban vs rural shift differences
- **Temporal Analysis**: Primary to general election shifts

### Correlation Analysis
- **Pearson Correlations**: Statistical relationship strength
- **Trend Analysis**: Linear regression with R² values
- **Significance Testing**: Pattern validation
- **Cross-validation**: Model robustness assessment

### Visualization Features
- **Diagonal Lines**: 1:1 voting pattern identification
- **Color Coding**: Proposition performance representation
- **Trend Lines**: Statistical relationship visualization
- **Heatmaps**: Multi-dimensional pattern analysis

## 🔧 Technical Requirements

### Dependencies
- Python 3.8+
- pandas, numpy, matplotlib, seaborn
- All packages from `requirements.txt`

### Data Sources
- **Primary Data**: Michigan election results (2016-2024)
- **Synthetic Data**: Realistic voting patterns for analysis
- **Normalized Data**: Standardized format for consistency

### Performance
- **Scalability**: Designed for county-level analysis (83 counties)
- **Efficiency**: Optimized data processing and correlation calculations
- **Robustness**: Error handling and data validation throughout
- **Reproducibility**: Deterministic results with fixed random seeds

## 📈 Analysis Methodology

### Statistical Approach
- **Correlation Analysis**: Pearson correlation coefficients for pattern identification
- **Regression Modeling**: Linear regression with cross-validation
- **Significance Thresholds**: |r| > 0.3 for pattern inclusion, |r| > 0.4 for modeling
- **Data Validation**: Cross-validation and train-test splits for model robustness

### Data Processing
- **Normalization**: Standardized data formats across election years
- **Validation**: Data quality checks and outlier identification
- **Integration**: Unified data loading and processing across all analyses
- **Export**: Multiple output formats for different use cases

## 🚀 Future Development

### Planned Analyses
- **2020 Election**: COVID-19 impact on voting patterns
- **2022 Election**: Midterm election analysis
- **2024 Election**: Latest election cycle analysis
- **Cross-election**: Longitudinal pattern analysis
- **Demographic Integration**: Census data correlation

### Enhanced Features
- **Machine Learning**: Advanced pattern prediction
- **Real-time Updates**: Automated analysis pipeline
- **Interactive Visualizations**: Web-based dashboard
- **API Integration**: External data source connections

## 📝 Usage Examples

### Run Complete Analysis Suite
```bash
cd analysis/
python run_all_analyses.py
```

### Run Individual Analysis
```bash
cd analysis/2018/
python 2018_comprehensive_analysis.py
```

### Check Results
```bash
# View generated reports
cat 2018/2018_comprehensive_analysis_report.md
cat primary_2016/2016_primary_trump_shift_report.md

# View summary
cat ANALYSIS_SUMMARY.md
```

## 🎯 Key Insights

### 2018 Election Patterns
- **Democratic Consistency**: Strong correlation between Democratic candidates
- **Proposition Alignment**: Propositions show strong correlation with Democratic support
- **Vote Shift Patterns**: Counties with strong Bernie support maintained Democratic support
- **Regional Patterns**: Urban counties show stronger Democratic and proposition support

### 2016 Primary Patterns
- **Primary Divisions**: Clear patterns between Bernie and Hillary support
- **Trump Appeal**: Counties with different primary preferences show varying Trump support
- **Shift Magnitude**: Significant vote shifts occurred in many counties
- **Regional Patterns**: Urban vs rural differences in both primary and general voting

## 📞 Support and Development

### Contributing
- Follow the established code structure and patterns
- Add comprehensive documentation for new analyses
- Include statistical validation and error handling
- Generate both technical and summary reports

### Extending the Analysis
- Add new election years by creating new folder structures
- Implement new analysis types in the master runner
- Maintain consistent output formats and naming conventions
- Update the README with new capabilities

---

*Analysis Suite generated by Claude Sonnet 4 via Cursor.sh*
*Comprehensive Michigan election analysis with focus on vote shifts and correlations*
