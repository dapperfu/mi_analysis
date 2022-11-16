.PHONY: all
all: 2022.ft

2022.json: 01_Election_Data_Downloader.ipynb
	jupyter-execute ${^}

2022.ft: 2022.json
	jupyter-execute 2022_Processing.ipynb

.PHONY: clean
clean:
	rm -rf *.json
