# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\automated_portfolio.csv"
df = pd.read_csv(csv_path)
df = df.sort_values('final_alloc_value', ascending=False)

# --- TOP 20 CHART ONLY ---
df_top20 = df.head(20)
top20_height = 28 * len(df_top20)

story_top20 = pynarrative.Story(df_top20, height=top20_height)
story_top20 = story_top20.mark_bar(size=20).encode(
    y=alt.Y('Item:N', sort='-x', title='Item',
            axis=alt.Axis(labelFontSize=12, labelLimit=340),
            scale=alt.Scale(paddingInner=0.5, paddingOuter=0.4)),
    x=alt.X('final_alloc_value:Q', title='Final Allocated Value (ISK)'),
    color=alt.value('#2687C9'),
    tooltip=[
        alt.Tooltip('Item:N'),
        alt.Tooltip('final_alloc_value:Q', format=",.0f", title='Final Value (ISK)'),
        alt.Tooltip('Trades:Q', title='Trades'),
        alt.Tooltip('Avg ROI/Trade (%):Q', format=".2f", title='Avg ROI/Trade (%)'),
        alt.Tooltip('avg_daily_isk_flow:Q', format=",.0f", title='Avg Daily ISK Flow')
    ]
)
story_top20 = story_top20.add_title(
    "Top 20 Portfolio Items by Value",
    subtitle="A focused look at your 20 most valuable trades. Hover for details."
)
story_top20 = story_top20.add_source("Source: automated_portfolio.csv")

# --- DISPLAY ONLY THE TOP 20 CHART ---
display(Markdown("## Portfolio Summary: Top 20 Trades"))
display(story_top20.render())

import pandas as pd

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\automated_portfolio.csv"
df = pd.read_csv(csv_path)

# Display the suspicious row and a few others for context
print(df[df['Item'] == 'Compressed Mercoxit'])
print("\nOther top ROIs:")
print(df[['Item', 'Trades', 'Avg ROI/Trade (%)']].sort_values('Avg ROI/Trade (%)', ascending=False).head(10))


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\automated_portfolio.csv"
df = pd.read_csv(csv_path)

# Filter out extreme ROI values above 1000%
df = df[df['Avg ROI/Trade (%)'] < 1000]

df = df.sort_values('final_alloc_value', ascending=False)

# Top 20 chart example (after filtering)
df_top20 = df.head(20)
top20_height = 28 * len(df_top20)

story_top20 = pynarrative.Story(df_top20, height=top20_height)
story_top20 = story_top20.mark_bar(size=20).encode(
    y=alt.Y('Item:N', sort='-x', title='Item',
            axis=alt.Axis(labelFontSize=12, labelLimit=340),
            scale=alt.Scale(paddingInner=0.5, paddingOuter=0.4)),
    x=alt.X('final_alloc_value:Q', title='Final Allocated Value (ISK)'),
    color=alt.value('#2687C9'),
    tooltip=[
        alt.Tooltip('Item:N'),
        alt.Tooltip('final_alloc_value:Q', format=",.0f", title='Final Value (ISK)'),
        alt.Tooltip('Trades:Q', title='Trades'),
        alt.Tooltip('Avg ROI/Trade (%):Q', format=".2f", title='Avg ROI/Trade (%)'),
        alt.Tooltip('avg_daily_isk_flow:Q', format=",.0f", title='Avg Daily ISK Flow')
    ]
)
story_top20 = story_top20.add_title(
    "Top 20 Portfolio Items by Value (ROI filtered)",
    subtitle="This chart excludes ROI values above 1000% to avoid data anomalies."
)
story_top20 = story_top20.add_source("Source: automated_portfolio.csv")

display(Markdown("## Portfolio Summary: Top 20 Trades (Filtered)"))
display(story_top20.render())


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\candidate_isk_flow_full.csv"
df = pd.read_csv(csv_path)

# Filter positive values just in case
df = df[df['avg_daily_isk_flow'] > 0]

# Sort descending by avg_daily_isk_flow
df = df.sort_values('avg_daily_isk_flow', ascending=False)

# Top 3 items
df_top3 = df.head(3).copy()
df_top3.loc[:, 'Item_short'] = df_top3['Item'].str.slice(0, 30) + '...'
height_top3 = 28 * len(df_top3)

story_top3 = pynarrative.Story(df_top3, height=height_top3)
story_top3 = story_top3.mark_bar(size=30).encode(
    y=alt.Y('Item_short:N', sort='-x', title='Item',
            axis=alt.Axis(labelFontSize=14, labelLimit=350),
            scale=alt.Scale(paddingInner=0.6, paddingOuter=0.4)),
    x=alt.X('avg_daily_isk_flow:Q', title='Average Daily ISK Flow'),
    color=alt.value('#D9534F'),  # red color for emphasis
    tooltip=[alt.Tooltip('Item:N'), alt.Tooltip('avg_daily_isk_flow:Q', format=",.0f", title='Avg Daily ISK Flow')]
)
story_top3 = story_top3.add_title(
    "Top 3 Candidate Items by Average Daily ISK Flow",
    subtitle="The major market movers"
)
story_top3 = story_top3.add_source("Source: candidate_isk_flow_full.csv")

# Top 20 excluding top 3
df_rest = df.iloc[3:23].copy()
df_rest.loc[:, 'Item_short'] = df_rest['Item'].str.slice(0, 30) + '...'
height_rest = 28 * len(df_rest)

story_rest = pynarrative.Story(df_rest, height=height_rest)
story_rest = story_rest.mark_bar(size=20).encode(
    y=alt.Y('Item_short:N', sort='-x', title='Item',
            axis=alt.Axis(labelFontSize=12, labelLimit=350),
            scale=alt.Scale(paddingInner=0.5, paddingOuter=0.4)),
    x=alt.X('avg_daily_isk_flow:Q', title='Average Daily ISK Flow'),
    color=alt.value('#5A9BD4'),
    tooltip=[alt.Tooltip('Item:N'), alt.Tooltip('avg_daily_isk_flow:Q', format=",.0f", title='Avg Daily ISK Flow')]
)
story_rest = story_rest.add_title(
    "Next 20 Candidate Items by Average Daily ISK Flow",
    subtitle="Smaller, but still significant ISK flows"
)
story_rest = story_rest.add_source("Source: candidate_isk_flow_full.csv")

# Display both charts
display(Markdown("## Candidate Items ISK Flow"))
display(story_top3.render())
display(story_rest.render())


# %%
from IPython.display import Markdown, display

display(Markdown("""
# EVE Online RSI Grid Sweep Overview

**Exploring RSI window sizes and buy/sell thresholds for optimal trading performance**

This dataset represents a comprehensive grid sweep exploring various RSI parameter combinations,
including different window sizes (`win`), buy thresholds (`buy_th`), and sell thresholds (`sell_th`).
Each parameter combination was backtested to evaluate its profitability both in-sample (training phase)
and out-of-sample (validation phase).

The goal is to identify robust RSI settings that maximize return on investment (ROI) while maintaining
consistent performance outside the training period. This analysis aids in tuning the trading algorithm
to adapt effectively to EVE Onlineâ€™s dynamic market conditions.

---

### Potential Next Steps

- Visualize IS and OOS ROI across parameter ranges.
- Identify parameter sets with highest and most stable ROI.
- Compare trade volume to ROI for strategy robustness.
- Perform sensitivity analysis on RSI window sizes.

---

*Source: eve_rsi_gridsearch_all_results.csv*
"""))


# %%
import altair as alt
alt.data_transformers.enable("vegafusion")

import pandas as pd
import pynarrative
from IPython.display import display, Markdown

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\MA_EMA_RV_roi_results.csv"
df = pd.read_csv(csv_path)

df_filtered = df[df['trades'] >= 10].copy()

df_filtered['strategy_label'] = (
    df_filtered['strategy'] + " (MAw=" +
    df_filtered['ma_window'].astype(str) + ", Volw=" +
    df_filtered['vol_window'].astype(str) + ")"
)

df_top20 = df_filtered.sort_values('roi', ascending=False).head(20)
chart_height = 30 * len(df_top20)

story = pynarrative.Story(df_top20, height=chart_height)

story = story.add_title(
    "Compare ROI by Strategy",
    subtitle="Each strategyâ€™s moving average and volume windows shown. Hover bars to see profit and trades."
)

story = story.mark_bar(size=20).encode(
    y=alt.Y('strategy_label:N', sort='-x', title='Strategy and Window Sizes',
            axis=alt.Axis(labelFontSize=12, labelLimit=300)),
    x=alt.X('roi:Q', title='Return on Investment (ROI)', axis=alt.Axis(format='%')),
    color=alt.Color('roi:Q', scale=alt.Scale(scheme='greenblue')),
    tooltip=[
        alt.Tooltip('item:N', title='Item'),
        alt.Tooltip('strategy:N', title='Strategy'),
        alt.Tooltip('ma_window:Q', title='MA Window'),
        alt.Tooltip('vol_window:Q', title='Volume Window'),
        alt.Tooltip('profit:Q', format=',.0f', title='Profit (ISK)'),
        alt.Tooltip('roi:Q', format='.2%', title='ROI'),
        alt.Tooltip('trades:Q', title='Trades')
    ]
)

story = story.add_source("Source: MA_EMA_RV_roi_results.csv")

# Display warning and context above chart using Markdown
display(Markdown("âš ï¸ **Note:** These trades are likely not robust and may be overfitted to historical data."))

display(Markdown("This chart compares ROI for the top 20 trading strategies with at least 10 trades."))

# Display chart heading and chart
display(Markdown("## Trading Strategy ROI Overview (Top 20, â‰¥10 Trades)"))
display(story.render())


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Battleship_2025-07-14_18-58.csv"
df = pd.read_csv(csv_path, parse_dates=['date'])

df_raven = df[df['type_name'] == 'Raven']

price_chart = alt.Chart(df_raven).mark_line(color='blue').encode(
    x='date:T',
    y=alt.Y('average:Q', title='Average Price (ISK)'),
    tooltip=['date:T', 'average:Q', 'lowest:Q', 'highest:Q']
)

price_band = alt.Chart(df_raven).mark_area(opacity=0.2, color='blue').encode(
    x='date:T',
    y='lowest:Q',
    y2='highest:Q'
)

price_layered = price_band + price_chart
price_layered = price_layered.properties(width=700, height=300)

story = pynarrative.Story(df_raven, width=700, height=300)
story = story.add_title("Raven Battleship Market History (2024-07)")
story = story.add_context(
    "This chart shows daily average price trends for Raven battleship only.",
    position='top'  # context text above chart
)
story.chart = price_layered
story = story.add_source("Source: EVE Online Market API (Raw)")

display(Markdown("## Raven Battleship Market History Overview"))
display(story.render())


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

# Load Ice Product market history CSV
csv_path_ice = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Ice_Product_2025-07-14_14-46.csv"
df_ice = pd.read_csv(csv_path_ice, parse_dates=['date'])

# Filter to top item: Heavy Water
df_heavy_water = df_ice[df_ice['type_name'] == 'Heavy Water']

# Create price line and price band charts
price_chart_ice = alt.Chart(df_heavy_water).mark_line(color='darkcyan').encode(
    x='date:T',
    y=alt.Y('average:Q', title='Average Price (ISK)'),
    tooltip=['date:T', 'average:Q', 'lowest:Q', 'highest:Q']
)

price_band_ice = alt.Chart(df_heavy_water).mark_area(opacity=0.2, color='darkcyan').encode(
    x='date:T',
    y='lowest:Q',
    y2='highest:Q'
)

price_layered_ice = price_band_ice + price_chart_ice
price_layered_ice = price_layered_ice.properties(width=700, height=300)

# Create PyNarrative story for Heavy Water
story_ice = pynarrative.Story(df_heavy_water, width=700, height=300)
story_ice = story_ice.add_title("Heavy Water Market History (2024-07)")
story_ice = story_ice.add_context(
    "This chart shows daily average price trends for Heavy Water, the top ice product.",
    position='top'
)
story_ice.chart = price_layered_ice
story_ice = story_ice.add_source("Source: EVE Online Market API (Raw)")

# Display narrative heading and story
display(Markdown("## Heavy Water Market History Overview"))
display(story_ice.render())


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

# Load Mineral market history CSV
csv_path_mineral = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Mineral_2025-07-14_17-10.csv"
df_mineral = pd.read_csv(csv_path_mineral, parse_dates=['date'])

# Filter to Tritanium only
df_tritanium = df_mineral[df_mineral['type_name'] == 'Tritanium']

# Create price line and band charts
price_chart_min = alt.Chart(df_tritanium).mark_line(color='orange').encode(
    x='date:T',
    y=alt.Y('average:Q', title='Average Price (ISK)'),
    tooltip=['date:T', 'average:Q', 'lowest:Q', 'highest:Q']
)

price_band_min = alt.Chart(df_tritanium).mark_area(opacity=0.2, color='orange').encode(
    x='date:T',
    y='lowest:Q',
    y2='highest:Q'
)

price_layered_min = price_band_min + price_chart_min
price_layered_min = price_layered_min.properties(width=700, height=300)

# Create PyNarrative story for Tritanium
story_min = pynarrative.Story(df_tritanium, width=700, height=300)
story_min = story_min.add_title("Tritanium Market History (2024-07)")
story_min = story_min.add_context(
    "This chart shows daily average price trends for Tritanium, a key mineral.",
    position='top'
)
story_min.chart = price_layered_min
story_min = story_min.add_source("Source: EVE Online Market API (Raw)")

# Display narrative heading and story
display(Markdown("## Tritanium Market History Overview"))
display(story_min.render())


# %%
import pandas as pd
import pynarrative
import altair as alt
from IPython.display import display, Markdown

# Load CSV
csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\robust_OOS_strategies_top.csv"
df = pd.read_csv(csv_path)

df_sorted = df.sort_values(by='test_roi', ascending=False)
df_sorted['item_window'] = df_sorted['item'] + " (w=" + df_sorted['window'].astype(str) + ")"

df_melt = df_sorted.melt(
    id_vars=['item_window', 'train_trades', 'test_trades', 'train_profit', 'test_profit'],
    value_vars=['train_roi', 'test_roi'],
    var_name='dataset',
    value_name='ROI'
)

df_melt['dataset'] = df_melt['dataset'].map({
    'train_roi': 'Train ROI',
    'test_roi': 'Test ROI'
})

chart = alt.Chart(df_melt).mark_bar(size=18).encode(
    y=alt.Y('item_window:N', sort='-x', title='Item (Window Size)', axis=alt.Axis(labelFontSize=12)),
    x=alt.X('ROI:Q', title='Return on Investment (ROI)', axis=alt.Axis(format=".2f")),
    color=alt.Color('dataset:N', scale=alt.Scale(domain=['Train ROI', 'Test ROI'], range=['#1f77b4', '#ff7f0e']), legend=alt.Legend(title="Dataset")),
    tooltip=[
        alt.Tooltip('item_window:N', title='Item (Window)'),
        alt.Tooltip('ROI:Q', format=".4f", title='ROI'),
        alt.Tooltip('dataset:N', title='Dataset'),
        alt.Tooltip('train_trades:Q', title='Train Trades'),
        alt.Tooltip('test_trades:Q', title='Test Trades'),
        alt.Tooltip('train_profit:Q', format=",.0f", title='Train Profit (ISK)'),
        alt.Tooltip('test_profit:Q', format=",.0f", title='Test Profit (ISK)')
    ]
).properties(width=700, height=600)

story = pynarrative.Story()
story.chart = chart

# Display the text above the chart explicitly as Markdown
display(Markdown("### This chart compares the in-sample (train) and out-of-sample (test) ROI of top RSI trading strategies across different window sizes. Higher test ROI suggests better strategy robustness. Hover over bars for detailed trades and profit info."))

# Now display the story chart
display(story.render())

# Add source info below
display(Markdown("_Source: robust_OOS_strategies_top.csv_"))




