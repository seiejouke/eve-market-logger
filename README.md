![Description of screenshot](images/Market_Overview1.png)

[![Build Status](https://img.shields.io/github/actions/workflow/status/seiejouke/eve-market-logger/main.yml?branch=main)](https://github.com/seiejouke/eve-market-logger/actions)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/release/python-3120/)




# EVE Market Logger

EVE Market Logger is a data analysis project focused on station trading at Jita 4-4 in EVE Online. It uses the EVE Swagger Interface (ESI) API to fetch market data, stores it in a PostgreSQL database, and analyzes trade performance using Python and Jupyter.

This project simulates the operations of an investment trader.

## Objectives

- Automate and merge market data using the ESI API
- Analyze trade performance, liquidity, and market behavior
- Apply real data analyst practices in a game economy

## Tech Stack

- Python 3.12  
- PostgreSQL 17.5  
- pandas, psycopg2, matplotlib  
- Jupyter Notebooks  
- EVE Swagger Interface (ESI API)  
- VS Code on Windows 11 with PowerShell


## Data Workflow

1. Use Python scripts to query the ESI API  
2. Analyze with Jupyter notebooks:  
   - Liquidity  
   - Profit margins  
   - ISK velocity  
   - Inventory aging  
   - Capital allocation

## Next Steps

Interactive widget analysis notebook
  - Descriptive analysis
  - Trend analysis 
- Create summary dashboards and reports(BI/Streamlit)  
- Automate backlog, item types, sanitation, and merge logic
- Import market orders into a Postgres and CSV for ease of method
- Scale conclusion to Postgres


## References

- EVE ESI API: https://esi.evetech.net/ui/

