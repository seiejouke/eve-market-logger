import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("EVE Online Market Dashboard: PLEX & Hypercores")

# --- File loading ---
DEFAULT_PLEX = r"C:\Users\Jouke\Documents\evedata-logger\output\market_groups\PLEX\market_history_PLEX_only.csv"
DEFAULT_HYPER = r"C:\Users\Jouke\Documents\evedata-logger\output\market_groups\Hypercore\market_history_52568_2025-07-17_13-33_cleaned.csv"

st.sidebar.header("Load Data")
plex_file = st.sidebar.file_uploader("PLEX CSV", type=["csv"], key="plex") or DEFAULT_PLEX
hyper_file = st.sidebar.file_uploader("Hypercore CSV", type=["csv"], key="hypercore") or DEFAULT_HYPER

@st.cache_data
def load_data(path_or_file):
    return pd.read_csv(path_or_file)

df_plex = load_data(plex_file)
df_hypercore = load_data(hyper_file)

# --- Data merging ---
df = pd.merge(
    df_plex, df_hypercore,
    on='date',
    suffixes=('_plex', '_hypercore')
).sort_values('date').reset_index(drop=True)

# --- DROP NaN ROWS ---
n_before = len(df)
df = df.dropna().reset_index(drop=True)
n_after = len(df)
dropped = n_before - n_after

st.success(f"Merged {len(df)} days of data. Dropped {dropped} rows with missing values.")

# --- Column selectors ---
price_col_plex = st.sidebar.selectbox("PLEX column", [col for col in df.columns if col.endswith('_plex')])
price_col_hyper = st.sidebar.selectbox("Hypercore column", [col for col in df.columns if col.endswith('_hypercore')])

# --- Stats and correlations ---
st.subheader("Summary Statistics & Correlation")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**PLEX (selected column):**")
    st.write(df[price_col_plex].describe())
with c2:
    st.markdown("**Hypercore (selected column):**")
    st.write(df[price_col_hyper].describe())

pearson = df[price_col_plex].corr(df[price_col_hyper])
spearman = df[price_col_plex].corr(df[price_col_hyper], method='spearman')
kendall = df[price_col_plex].corr(df[price_col_hyper], method='kendall')
st.info(f"""
**Correlations for selected columns:**
- Pearson: `{pearson:.4f}`
- Spearman: `{spearman:.4f}`
- Kendall: `{kendall:.4f}`
""")

# --- Rolling correlation ---
window = st.sidebar.slider("Rolling window (days)", min_value=7, max_value=60, value=30)
rolling_corr = df[price_col_plex].rolling(window).corr(df[price_col_hyper])

# --- Plots ---
st.subheader("Visualizations")

tab1, tab2, tab3 = st.tabs(["Time Series", "Scatter Plot", "Rolling Correlation"])

with tab1:
    st.write("**Time Series Plot**")
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(df['date'], df[price_col_plex], label=price_col_plex)
    ax.plot(df['date'], df[price_col_hyper], label=price_col_hyper)
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    plt.xticks(rotation=45)
    fig.subplots_adjust(bottom=0.25)
    st.pyplot(fig)

with tab2:
    st.write("**Scatter Plot**")
    fig, ax = plt.subplots(figsize=(7,5))
    ax.scatter(df[price_col_plex], df[price_col_hyper], alpha=0.7)
    ax.set_xlabel(price_col_plex)
    ax.set_ylabel(price_col_hyper)
    st.pyplot(fig)

with tab3:
    st.write("**Rolling Correlation**")
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(df['date'], rolling_corr)
    ax.axhline(0, color='grey', linestyle='--')
    ax.set_title(f"Rolling ({window}d) Correlation: {price_col_plex} vs {price_col_hyper}")
    plt.xticks(rotation=45)
    fig.subplots_adjust(bottom=0.25)
    st.pyplot(fig)

# --- Data preview ---
if st.checkbox("Show merged data sample"):
    st.dataframe(df.head(30))
