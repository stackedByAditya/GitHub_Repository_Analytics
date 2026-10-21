from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GitHub Repository Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- THEME / STYLING ----------------
st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --background-color: #ffffff;
        --secondary-background-color: #f3f6fb;
        --text-color: #172033;
        --primary-color: #2563eb;
    }
    html, body, [data-testid="stAppViewContainer"], .stApp,
    [data-testid="stMain"], [data-testid="stMainBlockContainer"],
    [data-testid="stHeader"] {
        background: #ffffff !important;
        color: #172033 !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"] {
        background: #f3f6fb !important;
        color: #172033 !important;
    }
    /* Make all ordinary text dark enough to read on white/light backgrounds. */
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp span, .stApp small,
    [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] {
        color: #172033;
    }
    [data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #d5deea !important;
        box-shadow: 0 1px 3px rgba(20, 35, 60, 0.06);
        padding: 14px 16px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #172033 !important;
    }
    /* Multiselect, text inputs, number inputs and dropdowns: white controls, dark text. */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
        border-color: #bdc9d8 !important;
    }
    [data-baseweb="select"] input {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }
    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    [data-baseweb="textarea"] * {
        color: #172033;
    }
    [data-baseweb="tag"] {
        background: #e2edff !important;
        color: #17365d !important;
        border: 1px solid #b9d2ff !important;
    }
    [data-baseweb="tag"] * {
        color: #17365d !important;
        -webkit-text-fill-color: #17365d !important;
    }
    [data-testid="stNumberInput"] button {
        background: #eaf0f7 !important;
        color: #172033 !important;
        border-color: #bdc9d8 !important;
    }
    [data-testid="stSlider"] [role="slider"] {
        border-color: #2563eb !important;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Force Plotly text, axes, legends, and gridlines to use readable light-theme colors.
def apply_light_plot_style(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Arial, sans-serif", size=12, color="#172033"),
        legend=dict(font=dict(color="#172033")),
    )
    fig.update_xaxes(
        color="#172033",
        tickfont=dict(color="#243247", size=11),
        title_font=dict(color="#172033", size=12),
        gridcolor="#e2e8f0",
        linecolor="#9aa9bc",
        zerolinecolor="#cbd5e1",
    )
    fig.update_yaxes(
        color="#172033",
        tickfont=dict(color="#243247", size=11),
        title_font=dict(color="#172033", size=12),
        gridcolor="#e2e8f0",
        linecolor="#9aa9bc",
        zerolinecolor="#cbd5e1",
    )
    return fig

# ---------------- LOAD DATA ----------------
BASE_DIR = Path(__file__).resolve().parent
possible_files = [
    BASE_DIR / "processed_data" / "github_repositories_enhanced.csv",
    BASE_DIR / "processed_data" / "github_repositories_cleaned.csv",
    BASE_DIR / "github_repositories.csv",
    BASE_DIR / "github_repositories (1).csv",
]

data_file = next((path for path in possible_files if path.exists()), None)

if data_file is None:
    st.error("Dataset not found. Place your CSV in processed_data/ or in the project folder.")
    st.code(
        "Expected first choice:\n"
        "processed_data/github_repositories_enhanced.csv"
    )
    st.stop()

try:
    df = pd.read_csv(data_file)
except Exception as exc:
    st.error(f"Could not read dataset: {exc}")
    st.stop()

required_columns = ["repository", "stars", "forks", "open_issues"]
missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    st.error(f"The dataset is missing required columns: {', '.join(missing_columns)}")
    st.stop()

# ---------------- DATA PREPARATION ----------------
for column in ["stars", "forks", "open_issues"]:
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).clip(lower=0)

if "language" not in df.columns:
    df["language"] = "Unknown"
df["language"] = df["language"].fillna("Unknown").astype(str).replace("", "Unknown")
df["repository"] = df["repository"].fillna("Unknown").astype(str)

optional_numeric_columns = [
    "repository_age_years",
    "days_since_update",
    "watchers",
    "size",
]
for column in optional_numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# ---------------- HEADER ----------------
st.title("📊 GitHub Repository Analytics")
st.caption(
    "Explore repository popularity, language trends, engagement, and issue activity "
    "across the loaded GitHub dataset."
)
st.caption(f"Dataset: **{data_file.name}** · {len(df):,} repositories loaded")
st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Dashboard Filters")
st.sidebar.caption("Filters update the metrics, charts, insights, and table.")

available_languages = sorted(df["language"].unique().tolist())
selected_languages = st.sidebar.multiselect(
    "Programming language",
    options=available_languages,
    default=available_languages,
)

max_stars = max(1, int(df["stars"].max()))
star_range = st.sidebar.slider(
    "Star range",
    min_value=0,
    max_value=max_stars,
    value=(0, max_stars),
)

max_forks = max(0, int(df["forks"].max()))
min_forks = st.sidebar.number_input(
    "Minimum forks",
    min_value=0,
    max_value=max_forks,
    value=0,
    step=1,
)

max_issues = max(0, int(df["open_issues"].max()))
min_issues = st.sidebar.number_input(
    "Minimum open issues",
    min_value=0,
    max_value=max_issues,
    value=0,
    step=1,
)

repo_search_filter = st.sidebar.text_input(
    "Repository name contains",
    placeholder="e.g. freeCodeCamp",
)

# ---------------- APPLY FILTERS ----------------
filtered = df[
    df["language"].isin(selected_languages)
    & df["stars"].between(star_range[0], star_range[1])
    & (df["forks"] >= min_forks)
    & (df["open_issues"] >= min_issues)
].copy()

if repo_search_filter.strip():
    filtered = filtered[
        filtered["repository"].str.contains(
            repo_search_filter.strip(), case=False, na=False, regex=False
        )
    ]

# ---------------- KPI SUMMARY ----------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Repositories", f"{len(filtered):,}", help="Number matching all current filters")
k2.metric("Total stars", f"{filtered['stars'].sum():,.0f}")
k3.metric("Total forks", f"{filtered['forks'].sum():,.0f}")
k4.metric("Open issues", f"{filtered['open_issues'].sum():,.0f}")
st.caption(f"Showing **{len(filtered):,} of {len(df):,}** repositories.")
st.divider()

if filtered.empty:
    st.warning("No repositories match these filters. Adjust the sidebar filters.")
    st.stop()

# ---------------- TABS ----------------
overview_tab, explorer_tab, insights_tab = st.tabs(
    ["📈 Overview", "🔍 Repository Explorer", "🧠 Correlation & Insights"]
)

# ---------------- OVERVIEW ----------------
with overview_tab:
    top_left, top_right = st.columns(2)

    with top_left:
        st.subheader("Top 10 repositories by stars")
        top_repos = filtered.nlargest(10, "stars").sort_values("stars")
        fig = px.bar(
            top_repos,
            x="stars",
            y="repository",
            orientation="h",
            color="stars",
            color_continuous_scale="Blues",
            hover_data={"forks": ":,", "open_issues": ":,", "stars": ":,"},
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#172033'),
            height=450,
            xaxis_title="Stars",
            yaxis_title="",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        apply_light_plot_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with top_right:
        st.subheader("Programming language distribution")
        language_counts = (
            filtered["language"]
            .value_counts()
            .head(10)
            .rename_axis("language")
            .reset_index(name="repositories")
        )
        fig = px.pie(
            language_counts,
            names="language",
            values="repositories",
            hole=0.48,
            hover_data=["repositories"],
        )
        fig.update_traces(textposition="inside", textinfo="percent")
        fig.update_layout(template="plotly_white", height=450, paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#172033'), margin=dict(l=10, r=10, t=20, b=10))
        apply_light_plot_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    bottom_left, bottom_right = st.columns(2)

    with bottom_left:
        st.subheader("Stars vs. forks")
        fig = px.scatter(
            filtered,
            x="stars",
            y="forks",
            color="language",
            hover_name="repository",
            hover_data={"open_issues": ":,", "stars": ":,", "forks": ":,"},
            opacity=0.72,
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#172033'),
            height=430,
            xaxis_title="Stars",
            yaxis_title="Forks",
            legend_title="Language",
            margin=dict(l=10, r=10, t=20, b=10),
        )
        apply_light_plot_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with bottom_right:
        st.subheader("Repositories with the most open issues")
        top_issues = filtered.nlargest(10, "open_issues").sort_values("open_issues")
        fig = px.bar(
            top_issues,
            x="open_issues",
            y="repository",
            orientation="h",
            color="open_issues",
            color_continuous_scale="Oranges",
            hover_data={"stars": ":,", "forks": ":,", "open_issues": ":,"},
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#172033'),
            height=430,
            xaxis_title="Open issues",
            yaxis_title="",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=20, b=10),
        )
        apply_light_plot_style(fig)
        st.plotly_chart(fig, use_container_width=True)

# ---------------- REPOSITORY EXPLORER ----------------
with explorer_tab:
    st.subheader("Search, sort, and inspect repositories")
    search = st.text_input(
        "Search within the filtered repositories",
        placeholder="Type part of a repository name",
        key="explorer_search",
    )
    table = filtered.copy()
    if search.strip():
        table = table[
            table["repository"].str.contains(search.strip(), case=False, na=False, regex=False)
        ]

    sort_by = st.selectbox(
        "Sort by",
        ["stars", "forks", "open_issues", "repository"],
        index=0,
    )
    ascending = sort_by == "repository"
    table = table.sort_values(sort_by, ascending=ascending)

    display_columns = [
        column for column in [
            "repository", "language", "stars", "forks", "open_issues",
            "repository_age_years", "days_since_update",
        ] if column in table.columns
    ]
    st.caption(f"{len(table):,} repositories in this table")
    st.dataframe(
        table[display_columns],
        use_container_width=True,
        hide_index=True,
        height=480,
    )
    st.download_button(
        "⬇️ Download displayed repositories as CSV",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="github_repositories_filtered.csv",
        mime="text/csv",
    )

# ---------------- CORRELATION & INSIGHTS ----------------
with insights_tab:
    st.subheader("Summary insights")

    top_repo = filtered.loc[filtered["stars"].idxmax()]
    top_fork_repo = filtered.loc[filtered["forks"].idxmax()]
    top_issue_repo = filtered.loc[filtered["open_issues"].idxmax()]
    top_language = filtered["language"].value_counts().index[0]
    top_language_count = int(filtered["language"].value_counts().iloc[0])

    a, b = st.columns(2)
    with a:
        st.markdown("**Most-starred repository**")
        st.write(str(top_repo["repository"]))
        st.metric("Stars", f"{top_repo['stars']:,.0f}")
        st.markdown("**Most-forked repository**")
        st.write(str(top_fork_repo["repository"]))
        st.metric("Forks", f"{top_fork_repo['forks']:,.0f}")

    with b:
        st.markdown("**Most common language in current selection**")
        st.write(top_language)
        st.metric("Repositories using this language", f"{top_language_count:,}")
        st.markdown("**Repository with most open issues**")
        st.write(str(top_issue_repo["repository"]))
        st.metric("Open issues", f"{top_issue_repo['open_issues']:,.0f}")

    st.divider()
    st.subheader("Correlation matrix")
    numeric_columns = ["stars", "forks", "open_issues"]
    if "repository_age_years" in filtered.columns and filtered["repository_age_years"].notna().sum() > 1:
        numeric_columns.append("repository_age_years")
    if "days_since_update" in filtered.columns and filtered["days_since_update"].notna().sum() > 1:
        numeric_columns.append("days_since_update")

    corr = filtered[numeric_columns].corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Pearson correlation between numeric repository metrics",
    )
    fig.update_layout(template="plotly_white", height=480, paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font=dict(color='#172033'), margin=dict(l=10, r=10, t=55, b=10))
    apply_light_plot_style(fig)
    st.plotly_chart(fig, use_container_width=True)

    if len(filtered) >= 2:
        stars_forks_corr = filtered["stars"].corr(filtered["forks"])
        if pd.isna(stars_forks_corr):
            st.info("Stars-versus-forks correlation cannot be calculated because one metric has no variation.")
        else:
            strength = (
                "strong" if abs(stars_forks_corr) >= 0.7
                else "moderate" if abs(stars_forks_corr) >= 0.4
                else "weak"
            )
            direction = "positive" if stars_forks_corr >= 0 else "negative"
            st.info(
                f"Stars and forks have a **{strength} {direction} correlation** "
                f"(r = {stars_forks_corr:.2f}) in the currently filtered data. "
                "Correlation describes association; it does not establish causation."
            )

    st.subheader("Language comparison")
    lang_summary = (
        filtered.groupby("language", dropna=False)
        .agg(
            repositories=("repository", "count"),
            median_stars=("stars", "median"),
            median_forks=("forks", "median"),
            total_stars=("stars", "sum"),
        )
        .sort_values("repositories", ascending=False)
        .head(15)
        .reset_index()
    )
    st.dataframe(
        lang_summary,
        use_container_width=True,
        hide_index=True,
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Built with Python, Pandas, Plotly, and Streamlit. "
    "All metrics and visualizations reflect the current filters."
)
