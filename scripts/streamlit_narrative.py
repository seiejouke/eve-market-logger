import streamlit as st
import pandas as pd
import pynarrative
import altair as alt

st.set_page_config(page_title="EVE Online Market Narrative Dashboard", layout="wide")

st.title("EVE Online Market Narrative Dashboard")
st.caption("All charts are fully interactive. Hover for tooltips, zoom, and click to explore!")

# ---- 1. Portfolio Summary: Top 20 Trades ----
st.header("Portfolio Summary: Top 20 Trades")

csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\automated_portfolio.csv"
df = pd.read_csv(csv_path)
df = df.sort_values('final_alloc_value', ascending=False)

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

st.altair_chart(story_top20.chart, use_container_width=True)

# ---- 2. Portfolio Summary: Top 20 Trades (Filtered) ----
st.header("Portfolio Summary: Top 20 Trades (Filtered)")

df_filtered = pd.read_csv(csv_path)
df_filtered = df_filtered[df_filtered['Avg ROI/Trade (%)'] < 1000]
df_filtered = df_filtered.sort_values('final_alloc_value', ascending=False)
df_top20f = df_filtered.head(20)
top20_height_f = 28 * len(df_top20f)

story_top20f = pynarrative.Story(df_top20f, height=top20_height_f)
story_top20f = story_top20f.mark_bar(size=20).encode(
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
story_top20f = story_top20f.add_title(
    "Top 20 Portfolio Items by Value (ROI filtered)",
    subtitle="This chart excludes ROI values above 1000% to avoid data anomalies."
)
story_top20f = story_top20f.add_source("Source: automated_portfolio.csv")

st.altair_chart(story_top20f.chart, use_container_width=True)

# ---- 3. Candidate Items ISK Flow ----
st.header("Candidate Items ISK Flow")

csv_path2 = r"C:\Users\Jouke\Documents\evedata-logger\output\candidate_isk_flow_full.csv"
df2 = pd.read_csv(csv_path2)
df2 = df2[df2['avg_daily_isk_flow'] > 0]
df2 = df2.sort_values('avg_daily_isk_flow', ascending=False)

df_top3 = df2.head(3).copy()
df_top3.loc[:, 'Item_short'] = df_top3['Item'].str.slice(0, 30) + '...'
height_top3 = 28 * len(df_top3)
story_top3 = pynarrative.Story(df_top3, height=height_top3)
story_top3 = story_top3.mark_bar(size=30).encode(
    y=alt.Y('Item_short:N', sort='-x', title='Item',
            axis=alt.Axis(labelFontSize=14, labelLimit=350),
            scale=alt.Scale(paddingInner=0.6, paddingOuter=0.4)),
    x=alt.X('avg_daily_isk_flow:Q', title='Average Daily ISK Flow'),
    color=alt.value('#D9534F'),
    tooltip=[alt.Tooltip('Item:N'), alt.Tooltip('avg_daily_isk_flow:Q', format=",.0f", title='Avg Daily ISK Flow')]
)
story_top3 = story_top3.add_title(
    "Top 3 Candidate Items by Average Daily ISK Flow",
    subtitle="The major market movers"
)
story_top3 = story_top3.add_source("Source: candidate_isk_flow_full.csv")

st.altair_chart(story_top3.chart, use_container_width=True)

df_rest = df2.iloc[3:23].copy()
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

st.altair_chart(story_rest.chart, use_container_width=True)

# ---- 4. RSI Grid Sweep Narrative ----
st.header("EVE Online RSI Grid Sweep Overview")

st.markdown("""
**Exploring RSI window sizes and buy/sell thresholds for optimal trading performance**

This dataset represents a comprehensive grid sweep exploring various RSI parameter combinations,
including different window sizes (`win`), buy thresholds (`buy_th`), and sell thresholds (`sell_th`).
Each parameter combination was backtested to evaluate its profitability both in-sample (training phase)
and out-of-sample (validation phase).

The goal is to identify robust RSI settings that maximize return on investment (ROI) while maintaining
consistent performance outside the training period. This analysis aids in tuning the trading algorithm
to adapt effectively to EVE Online’s dynamic market conditions.
""")

# ---- 5. Trading Strategy ROI Overview ----
st.header("Trading Strategy ROI Overview (Top 20, ≥10 Trades)")

csv_path3 = r"C:\Users\Jouke\Documents\evedata-logger\output\MA_EMA_RV_roi_results.csv"
df3 = pd.read_csv(csv_path3)
df3_filtered = df3[df3['trades'] >= 10].copy()
df3_filtered['strategy_label'] = (
    df3_filtered['strategy'] + " (MAw=" +
    df3_filtered['ma_window'].astype(str) + ", Volw=" +
    df3_filtered['vol_window'].astype(str) + ")"
)
df3_top20 = df3_filtered.sort_values('roi', ascending=False).head(20)
chart_height = 30 * len(df3_top20)
story3 = pynarrative.Story(df3_top20, height=chart_height)
story3 = story3.add_title(
    "Compare ROI by Strategy",
    subtitle="Each strategy’s moving average and volume windows shown. Hover bars to see profit and trades."
)
story3 = story3.mark_bar(size=20).encode(
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
story3 = story3.add_source("Source: MA_EMA_RV_roi_results.csv")

st.warning("⚠️ These trades are likely not robust and may be overfitted to historical data.")
st.markdown("This chart compares ROI for the top 20 trading strategies with at least 10 trades.")
st.altair_chart(story3.chart, use_container_width=True)

# ---- 6. Raven Battleship Market History ----
st.header("Raven Battleship Market History Overview")

csv_path4 = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Battleship_2025-07-14_18-58.csv"
df4 = pd.read_csv(csv_path4, parse_dates=['date'])
df_raven = df4[df4['type_name'] == 'Raven']

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

st.altair_chart(price_layered, use_container_width=True)

# ---- 7. Heavy Water Market History ----
st.header("Heavy Water Market History Overview")
csv_path_ice = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Ice_Product_2025-07-14_14-46.csv"
df_ice = pd.read_csv(csv_path_ice, parse_dates=['date'])
df_heavy_water = df_ice[df_ice['type_name'] == 'Heavy Water']

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

st.altair_chart(price_layered_ice, use_container_width=True)

# ---- 8. Tritanium Market History ----
st.header("Tritanium Market History Overview")
csv_path_mineral = r"C:\Users\Jouke\Documents\evedata-logger\output\market_history_Mineral_2025-07-14_17-10.csv"
df_mineral = pd.read_csv(csv_path_mineral, parse_dates=['date'])
df_tritanium = df_mineral[df_mineral['type_name'] == 'Tritanium']

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

st.altair_chart(price_layered_min, use_container_width=True)

# ---- 9. Robust OOS Strategies ----
st.header("Robust Out-of-Sample (OOS) Strategies: Train vs Test ROI")

csv_path_robust = r"C:\Users\Jouke\Documents\evedata-logger\output\robust_OOS_strategies_top.csv"
df_robust = pd.read_csv(csv_path_robust)
df_robust = df_robust.sort_values(by='test_roi', ascending=False)
df_robust['item_window'] = df_robust['item'] + " (w=" + df_robust['window'].astype(str) + ")"
df_melt = df_robust.melt(
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
st.markdown("### This chart compares the in-sample (train) and out-of-sample (test) ROI of top RSI trading strategies across different window sizes. Higher test ROI suggests better strategy robustness. Hover over bars for detailed trades and profit info.")
st.altair_chart(chart, use_container_width=True)
st.caption("_Source: robust_OOS_strategies_top.csv_")

# ---- End ----
st.info("All charts and analysis are generated automatically from your project CSVs. Scroll up and down to explore, and hover over charts for more details!")
