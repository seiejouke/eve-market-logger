import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("EVE Online Market Dashboard: PLEX & Hypercores")

st.markdown("""
**Instructions:**
- **Option 1:** Upload your own PLEX and Hypercore CSV files in the sidebar.
- **Option 2:** Click 'Load Sample Data' to instantly demo the dashboard (loads Google Drive CSVs).
- Changing filters/controls will not require you to re-upload your data!
""")

# Google Drive direct download links for sample data
SAMPLE_PLEX = "https://drive.google.com/uc?id=1T7ZUuFya7GIFzPXtr8eBrDCfwlEMxKKA&export=download"
SAMPLE_HYPER = "https://drive.google.com/uc?id=1CunDPFiCqmhcfV_WunK0tdUcGRQpSpl0&export=download"

# --- SESSION STATE FOR DATA CHOICE ---
if "use_sample" not in st.session_state:
    st.session_state.use_sample = False

# --- Sidebar file uploaders and sample data button ---
st.sidebar.header("Load Data")
plex_file = st.sidebar.file_uploader("Upload PLEX CSV", type="csv", key="plex")
hypercore_file = st.sidebar.file_uploader("Upload Hypercore CSV", type="csv", key="hypercore")
if st.sidebar.button("Load Sample Data (Google Drive)"):
    st.session_state.use_sample = True

# --- Data loading logic: prioritize uploads, then sample data ---
if st.session_state.use_sample and not (plex_file and hypercore_file):
    df_plex = pd.read_csv(SAMPLE_PLEX)
    df_hypercore = pd.read_csv(SAMPLE_HYPER)
    st.success("Loaded sample data from Google Drive!")
elif plex_file and hypercore_file:
    df_plex = pd.read_csv(plex_file)
    df_hypercore = pd.read_csv(hypercore_file)
    st.session_state.use_sample = False
else:
    st.warning("Upload both CSVs in the sidebar OR click 'Load Sample Data' to begin.")
    st.stop()

# --- Data merging and cleaning ---
df = pd.merge(
    df_plex, df_hypercore,
    on='date',
    suffixes=('_plex', '_hypercore')
).sort_values('date').reset_index(drop=True)
n_before = len(df)
df = df.dropna().reset_index(drop=True)
n_after = len(df)
dropped = n_before - n_after
st.success(f"Merged {len(df)} days of data. Dropped {dropped} rows with missing values.")

# --- Sidebar column selectors ---
plex_cols = [col for col in df.columns if col.endswith('_plex')]
hypercore_cols = [col for col in df.columns if col.endswith('_hypercore')]
price_col_plex = st.sidebar.selectbox(
    "PLEX column", plex_cols,
    index=plex_cols.index('average_plex') if 'average_plex' in plex_cols else 0
)
price_col_hyper = st.sidebar.selectbox(
    "Hypercore column", hypercore_cols,
    index=hypercore_cols.index('average_hypercore') if 'average_hypercore' in hypercore_cols else 0
)

# --- Correlation and stats ---
st.subheader("Summary Statistics & Correlation")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**PLEX ({price_col_plex}):**")
    st.write(df[price_col_plex].describe())
with c2:
    st.markdown(f"**Hypercore ({price_col_hyper}):**")
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
df['date'] = pd.to_datetime(df['date'])

# --- Visualizations ---
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
    fig.autofmt_xdate()
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
    fig.autofmt_xdate()
    fig.subplots_adjust(bottom=0.25)
    st.pyplot(fig)

if st.checkbox("Show merged data sample"):
    st.dataframe(df.head(30))
