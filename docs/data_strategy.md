# 📊 EVE Online Market Analysis – Data Strategy

---

## 🎯 Vision & Objectives

**Primary Goal:**  
To analyze item liquidity, volume trends, and pricing behaviors to support profitable station trading strategies in EVE Online.

**Strategic Sub-goals:**

- Identify high-liquidity, high-margin items for active or passive trading.
- Track short- and mid-term market cycles to detect price floors, pumps, or panics.
- Simulate strategies like flipping, margin trading, and "buy-and-hold" investing.
- Build dashboards and visualizations to aid intuitive decision-making.

---

## 🧱 Data Architecture

| Layer               | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Data Sources**     | EVE ESI API endpoints (market history, orders, item metadata)              |
| **Storage Layer**    | PostgreSQL 17.5 (schema: `market_history`, `item_meta`)                    |
| **Ingestion Tools**  | Python scripts using `requests`, batched CSV output with sleep timer       |
| **Processing Layer** | `pandas` and `IPython` for analysis; Jupyter notebooks for experiments     |
| **Output/Export**    | Daily/weekly CSVs saved to `output/market_history/`, PostgreSQL exports    |

---

## 🔄 Data Lifecycle & Management

| Stage         | Strategy                                                                 |
|---------------|--------------------------------------------------------------------------|
| **Ingestion** | Fetch all item history in The Forge via ESI, using sleep to avoid throttle |
| **Validation**| Check for response failures, zero volumes, corrupted/missing fields       |
| **Cleaning**  | Deduplicate, convert timestamps to UTC, fill missing values where feasible |
| **Storage**   | Save raw and cleaned versions separately; sync key items to PostgreSQL    |
| **Versioning**| Timestamped batch files (`YYYY-MM-DD_batch_001.csv`, etc)                 |
| **Backup**    | Zip and store weekly backups of CSVs and PostgreSQL database dumps        |

---

## 🕵️‍♂️ Data Governance & Quality

| Policy              | Practice                                                                |
|---------------------|-------------------------------------------------------------------------|
| **Ownership**        | Single-developer managed (Jouke Seinstra)                              |
| **Validation**       | Enforce constraints (e.g., `volume ≥ 0`, `avg_price > 0`)              |
| **Reproducibility**  | All scripts versioned via Git; use `.env` or config files for constants |
| **Documentation**    | Markdown summaries per script; schema diagram for DB (optional future) |
| **Logging**          | Logs include item IDs, batch index, fetch status, and API errors       |

---

## 📈 Data Analytics & Insights

| Analysis Type           | Method / Tool                                                     |
|--------------------------|-------------------------------------------------------------------|
| **Liquidity Analysis**    | Group by item ID and region, aggregate daily volume using SQL/pandas |
| **Price Trend Detection** | Rolling averages, Bollinger bands, outlier detection              |
| **Strategy Simulation**   | Scripted backtests comparing historical buy/sell decisions         |
| **Visualization**         | matplotlib / seaborn charts; optional: Plotly/Dash in future       |
| **Indicators**            | Daily vol
