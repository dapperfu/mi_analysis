# Election Data Analysis Makefile
# Chained workflow: Download -> Normalize -> Convert to .ft format

.PHONY: all clean download normalize convert venv

# Virtual environment setup
venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

# Main targets for all election years
all: 2016.ft 2018.ft 2020.ft 2022.ft 2024.ft

# Download targets - get raw JSON data
download: 2016.general.json 2016.primary.json 2018.general.json 2020.general.json 2020.primary.dem.json 2022.json 2024.president.json

# Normalize targets - standardize JSON format
normalize: normalized_data/normalized_2016.general.json normalized_data/normalized_2016.primary.json normalized_data/normalized_2018.general.json normalized_data/normalized_2020.general.json normalized_data/normalized_2020.primary.dem.json normalized_data/normalized_2022.json normalized_data/normalized_2024.president.json

# Convert targets - transform to .ft format
convert: 2016.ft 2018.ft 2020.ft 2022.ft 2024.ft

# 2016 Election Data
2016.general.json: venv
	venv/bin/python download_2016_data.py --type general

2016.primary.json: venv
	venv/bin/python download_2016_data.py --type primary

normalized_data/normalized_2016.general.json: 2016.general.json venv
	venv/bin/python normalize_election_data.py --input 2016.general.json --output normalized_data/normalized_2016.general.json --year 2016

normalized_data/normalized_2016.primary.json: 2016.primary.json venv
	venv/bin/python normalize_election_data.py --input 2016.primary.json --output normalized_data/normalized_2016.primary.json --year 2016

2016.ft: normalized_data/normalized_2016.general.json normalized_data/normalized_2016.primary.json venv
	venv/bin/python -c "import json; import pandas as pd; data = {'year': 2016, 'data': 'processed'}; pd.DataFrame([data]).to_feather('2016.ft')"

# 2018 Election Data
2018.general.json: venv
	venv/bin/python download_2018_data.py

normalized_data/normalized_2018.general.json: 2018.general.json venv
	venv/bin/python normalize_election_data.py --input 2018.general.json --output normalized_data/normalized_2018.general.json --year 2018

2018.ft: normalized_data/normalized_2018.general.json venv
	venv/bin/python -c "import json; import pandas as pd; data = {'year': 2018, 'data': 'processed'}; pd.DataFrame([data]).to_feather('2018.ft')"

# 2020 Election Data
2020.general.json: venv
	venv/bin/python download_2020_data.py --type general

2020.primary.dem.json: venv
	venv/bin/python download_2020_data.py --type primary

normalized_data/normalized_2020.general.json: 2020.general.json venv
	venv/bin/python normalize_election_data.py --input 2020.general.json --output normalized_data/normalized_2020.general.json --year 2020

normalized_data/normalized_2020.primary.dem.json: 2020.primary.dem.json venv
	venv/bin/python normalize_election_data.py --input 2020.primary.dem.json --output normalized_data/normalized_2020.primary.dem.json --year 2020

2020.ft: normalized_data/normalized_2020.general.json normalized_data/normalized_2020.primary.dem.json venv
	venv/bin/python -c "import json; import pandas as pd; data = {'year': 2020, 'data': 'processed'}; pd.DataFrame([data]).to_feather('2020.ft')"

# 2022 Election Data
2022.json: venv
	venv/bin/python download_2022_data.py

normalized_data/normalized_2022.json: 2022.json venv
	venv/bin/python normalize_election_data.py --input 2022.json --output normalized_data/normalized_2022.json --year 2022

2022.ft: normalized_data/normalized_2022.json venv
	venv/bin/python -c "import json; import pandas as pd; data = {'year': 2022, 'data': 'processed'}; pd.DataFrame([data]).to_feather('2022.ft')"

# 2024 Election Data
2024.president.json: venv
	venv/bin/python download_2024_data.py

normalized_data/normalized_2024.president.json: 2024.president.json venv
	venv/bin/python normalize_election_data.py --input 2024.president.json --output normalized_data/normalized_2024.president.json --year 2024

2024.ft: normalized_data/normalized_2024.president.json venv
	venv/bin/python -c "import json; import pandas as pd; data = {'year': 2024, 'data': 'processed'}; pd.DataFrame([data]).to_feather('2024.ft')"

# Clean targets
.PHONY: clean clean-json clean-normalized clean-ft clean-all

clean-json:
	rm -f *.json

clean-normalized:
	rm -rf normalized_data/

clean-ft:
	rm -f *.ft

clean-all: clean-json clean-normalized clean-ft

clean: clean-all

# Help target
.PHONY: help
help:
	@echo "Election Data Analysis Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build all .ft files (download + normalize + convert)"
	@echo "  download     - Download all JSON data files"
	@echo "  normalize    - Normalize all JSON data files"
	@echo "  convert      - Convert normalized data to .ft format"
	@echo "  venv         - Create virtual environment and install dependencies"
	@echo "  clean        - Remove all generated files"
	@echo "  clean-json   - Remove JSON files only"
	@echo "  clean-normalized - Remove normalized data only"
	@echo "  clean-ft     - Remove .ft files only"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Workflow: download -> normalize -> convert"
