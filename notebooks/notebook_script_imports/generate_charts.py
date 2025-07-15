import pandas as pd
import pynarrative
import altair as alt
import markdown

# Where your HTML report will be saved
output_html = r"C:\Users\Jouke\Documents\evedata-logger\output\eve_narrative_report.html"
html_parts = []

def md_to_html(md_text):
    return markdown.markdown(md_text)

# Ensures unique chart divs (Altair needs this or only 1 chart shows)
def unique_chart_html(chart, idx):
    chart_html = chart.to_html(fullhtml=False)
    chart_html = chart_html.replace('id="vis"', f'id="vis{idx}"')
    chart_html = chart_html.replace('#vis', f'#vis{idx}')
    return chart_html

chart_idx = 0

# --- 1. Portfolio Summary: Top 20 Trades ---
html_parts.append(md_to_html("## Portfolio Summary: Top 20 Trades"))
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
html_parts.append(unique_chart_html(story_top20.chart, chart_idx)); chart_idx += 1

# --- 2. Portfolio Summary: Top 20 Trades (Filtered) ---
html_parts.append(md_to_html("## Portfolio Summary: Top 20 Trades (Filtered)"))
df = pd.read_csv(csv_path)
df = df[df['Avg ROI/Trade (%)'] < 1000]
df = df.sort_values('final_alloc_value', ascending=False)
df_top20 = df.head(20)
top20_height = 28 * len(df_top20)
story_top20_filtered = pynarrative.Story(df_top20, height=top20_height)
story_top20_filtered = story_top20_filtered.mark_bar(size=20).encode(
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
story_top20_filtered = story_top20_filtered.add_title(
    "Top 20 Portfolio Items by Value (ROI filtered)",
    subtitle="This chart excludes ROI values above 1000% to avoid data anomalies."
)
story_top20_filtered = story_top20_filtered.add_source("Source: automated_portfolio.csv")
html_parts.append(unique_chart_html(story_top20_filtered.chart, chart_idx)); chart_idx += 1

# --- 3. Candidate Items ISK Flow ---
html_parts.append(md_to_html("## Candidate Items ISK Flow"))
csv_path = r"C:\Users\Jouke\Documents\evedata-logger\output\candidate_isk_flow_full.csv"
df = pd.read_csv(csv_path)
df = df[df['avg_daily_isk_flow'] > 0]
df = df.sort_values('avg_daily_isk_flow', ascending=False)
df_top3 = df.head(3).copy()
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
html_parts.append(unique_chart_html(story_top3.chart, chart_idx)); chart_idx += 1

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
html_parts.append(unique_chart_html(story_rest.chart, chart_idx)); chart_idx += 1

# --- 4. RSI Grid Sweep Narrative ---
html_parts.append(md_to_html("""
# EVE Online RSI Grid Sweep Overview

**Exploring RSI window sizes and buy/sell thresholds for optimal trading performance**

This dataset represents a comprehensive grid sweep exploring various RSI parameter combinations, including different window sizes (`win`), buy thresholds (`buy_th`), and sell thresholds (`sell_th`). Each parameter combination was backtested to evaluate its profitability both in-sample (training phase) and out-of-sample (validation phase).

The goal is to identify robust RSI settings that maximize return on investment (ROI) while maintaining consistent performance outside the training period. This analysis aids in tuning the trading algorithm to adapt effectively to EVE Onlineâ€™s dynamic market conditions.

---
"""))

# --- 5. Trading Strategy ROI Overview ---
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
html_parts.append(md_to_html("## Trading Strategy ROI Overview (Top 20, â‰¥10 Trades)"))
html_parts.append(unique_chart_html(story.chart, chart_idx)); chart_idx += 1

# --- 6. Market History Example (Raven) ---
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
html_parts.append(md_to_html("## Raven Battleship Market History Overview"))
html_parts.append(unique_chart_html(price_layered, chart_idx)); chart_idx += 1

# --- 7. SAVE EVERYTHING TO HTML FILE ---
full_html = """
<html>
<head>
    <title>EVE Online Market Narrative Report</title>
    <meta charset="UTF-8">
</head>
<body>
{}
</body>
</html>
""".format('\n<hr>\n'.join(html_parts))

with open(output_html, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"\nReport saved to: {output_html}\n")

