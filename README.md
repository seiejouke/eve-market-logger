# EVE Market Logger

EVE Market Logger is a data analysis project focused on station trading at Jita 4-4 in EVE Online. It uses the EVE Swagger Interface (ESI) API to fetch market data, stores it in a PostgreSQL database, and analyzes trade performance using Python and Jupyter.

This project simulates the operations of a solo trader managing a 1 billion ISK bankroll through a personal corporation.

## Objectives

- Fetch and log market data using the ESI API
- Store buy/sell orders in PostgreSQL
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
2. Insert market orders into a Postgres and CSV for ease of method
3. Analyze with Jupyter notebooks:  
   - Liquidity  
   - Profit margins  
   - ISK velocity  
   - Inventory aging  
   - Capital allocation

 ## Automate Market Data

 1. Retrieve Last 24 hours
 2. Sanitize and Merge
 3. Update types    

## Next Steps

- Interactive widget analysis notebook
- Create summary dashboards and reports  
- Add error logging and runtime validation  

## References

- EVE ESI API: https://esi.evetech.net/ui/  

