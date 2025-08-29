# Election Database System

This project now uses a **SQLite database with PonyORM** instead of `.ft` files for storing and analyzing election data. This provides better data integrity, querying capabilities, and performance.

## Why SQLite + PonyORM is Better Than .ft Files

### Advantages:
1. **Proper Relational Structure** - Enforces data relationships and integrity
2. **Better Querying** - SQL queries are more powerful than file-based lookups
3. **Data Consistency** - Referential integrity prevents orphaned records
4. **Scalability** - Better performance as data grows
5. **Standard Tooling** - Can use any SQLite browser or analysis tool
6. **ACID Compliance** - Database transactions ensure data reliability
7. **Indexing** - Faster searches and joins
8. **Multi-user Support** - Multiple processes can access data simultaneously

### Database Schema

```
Counties (1) ←→ (Many) Results (Many) ←→ (1) Elections
                    ↓
                (Many) ←→ (1) Candidates
```

- **Counties**: Master list of Michigan counties
- **Elections**: Election metadata (year, type, office, party)
- **Candidates**: Candidate information (name, party, NYT ID)
- **Results**: County-level election results (votes, percentages, winners)

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate

# Install database dependencies
pip install -r requirements_db.txt
```

### 2. Run the Migration

The migration script will convert your existing JSON data to the database:

```bash
python election_database.py
```

This will:
- Create `elections.db` SQLite database
- Create all necessary tables
- Migrate data from your JSON files
- Show migration progress and summary

### 3. Verify the Database

Check that the migration was successful:

```bash
python election_query_tool.py stats
```

## Usage

### Interactive Query Tool

The easiest way to explore your data:

```bash
python election_query_tool.py
```

**Available Commands:**
- `stats` - Show database statistics
- `top <year> <office> [limit]` - Show top performers
- `county <name>` - Show county performance
- `candidate <name>` - Show candidate summary
- `compare <candidate1> <candidate2> <year> <office>` - Compare candidates
- `turnout <year> <office>` - Show turnout data
- `search <term>` - Search for candidates
- `help` - Show help
- `quit` - Exit

**Examples:**
```bash
# Show top performers in 2022 Governor race
top 2022 Governor 5

# Compare Whitmer vs Dixon in 2022
compare Gretchen Whitmer Tudor Dixon 2022 Governor

# Show performance for Wayne County
county Wayne

# Search for candidates with "Trump" in name
search Trump
```

### Command Line Usage

You can also run queries directly from the command line:

```bash
# Show database stats
python election_query_tool.py stats

# Show top 10 performers in 2020 President race
python election_query_tool.py "top 2020 President 10"
```

### Advanced Analysis

For comprehensive analysis using the database:

```bash
python Election_Database_Analysis.py
```

This script provides:
- Voter behavior pattern analysis
- Geographic clustering
- Cross-election correlations
- Voter migration tracking
- Advanced statistical analysis

## Database Queries

### Basic Queries

```python
from election_database import db, County, Election, Candidate, Result
from pony.orm import *

# Get all counties
with db_session:
    counties = select(c for c in County)[:]

# Get 2022 Governor election results
with db_session:
    results = select(r for r in Result 
                    for e in r.election 
                    if e.year == 2022 and e.office == "Governor")[:]

# Get candidate performance summary
with db_session:
    candidate_summary = select((r.candidate.name, r.election.year, 
                               r.election.office, sum(r.votes))
                              for r in Result
                              ).group_by(r.candidate.name, r.election.year, r.election.office)
```

### Advanced Queries

```python
# Find counties where Bernie Sanders was strong but Biden underperformed
with db_session:
    bernie_strong = select(r for r in Result 
                          for c in r.candidate 
                          if c.name == "Bernie Sanders" 
                          and r.percentage > 50)[:]
    
    biden_weak = select(r for r in Result 
                        for c in r.candidate 
                        if c.name == "Joe Biden" 
                        and r.percentage < 30)[:]

# Analyze voter shifts between elections
with db_session:
    trump_2016 = select(r for r in Result 
                        for c in r.candidate 
                        for e in r.election 
                        if c.name == "Donald J. Trump" 
                        and e.year == 2016)[:]
    
    trump_2020 = select(r for r in Result 
                        for c in r.candidate 
                        for e in r.election 
                        if c.name == "Donald J. Trump" 
                        and e.year == 2020)[:]
```

## Data Migration Notes

### What Gets Migrated

The migration script handles:
- **2016 Primary**: Republican and Democratic presidential primaries
- **2016 General**: Presidential election
- **2018 General**: Governor election
- **2020 Primary**: Democratic presidential primary
- **2020 General**: Presidential election
- **2022 General**: Governor, Attorney General, Secretary of State

### Data Structure Changes

- **Before**: Flat JSON files with nested county/candidate structures
- **After**: Normalized relational database with proper foreign keys

### Handling Missing Data

- Counties are created automatically as needed
- Candidates are matched by name and party
- Elections are created with metadata
- Results include votes, percentages, and winner flags

## Performance Benefits

### Query Performance
- **Before**: Loading entire JSON files into memory
- **After**: Indexed database queries, only load needed data

### Memory Usage
- **Before**: All data loaded at once
- **After**: Stream data as needed, efficient memory usage

### Scalability
- **Before**: Performance degrades with file size
- **After**: Consistent performance regardless of data size

## Troubleshooting

### Common Issues

1. **Database not found**: Run the migration script first
2. **Import errors**: Make sure PonyORM is installed
3. **Data missing**: Check that JSON files exist and are readable
4. **Permission errors**: Ensure write access to create database

### Debugging

Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Data Validation

Check data integrity:
```bash
python election_query_tool.py stats
```

This will show counts and verify all data was migrated correctly.

## Future Enhancements

### Planned Features
- **Geographic coordinates** for counties
- **Demographic data** integration
- **Real-time updates** from election sources
- **Advanced analytics** dashboard
- **Export capabilities** to various formats

### Database Upgrades
- **PostgreSQL** support for larger datasets
- **Read replicas** for analysis workloads
- **Automated backups** and recovery
- **Data versioning** and change tracking

## Migration from .ft Files

If you have existing `.ft` files:

1. **Backup** your current data
2. **Run migration** to create database
3. **Verify** data integrity
4. **Update** your analysis scripts to use database
5. **Archive** old `.ft` files

The database provides the same data but in a much more robust and queryable format.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the database schema
3. Test with the query tool
4. Check migration logs for errors

The new database system provides a solid foundation for advanced election analysis and will scale much better than the previous file-based approach.
