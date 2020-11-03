# Singapore's Data Science Job Market Analysis

This is an attempt to **understand the data-science job market in Singapore**. The main objective is to address worries and questions faced by budding data scientists or business analysts. We will follow through with some conclusions supported by real-world data. 

The <u>workflow</u> is as follows:

1. Web-scrape all November 2019 job postings from *Glassdoor*, under the search terms: [gd_scraper.py](https://github.com/longwind48/glassdoor-data-analysis/blob/master/src/data/gd_scraper.py)
   - Data Scientist
   - Business Analyst
   - Data Analyst
2. Conduct Exploratory Data Analysis [gd_data_jobs_analysis_clean.ipynb](https://nbviewer.jupyter.org/github/longwind48/glassdoor_data_analysis/blob/master/notebooks/gd_data_jobs_analysis_clean.ipynb)


## Set Up

Requirements:

- Git
- Python3


```shell
$ git clone https://github.com/longwind48/glassdoor-data-analysis.git
$ cd glassdoor-data-analysis

$ pip install -r requirements.txt

# Visit localhost:9999 and input token to access jupyter notebook
```

## Future Work

- [ ] Add tests for scraper
- [ ] Add docstrings for all functions
- [ ] Write analysis in README
- [X] Add requirements.txt

