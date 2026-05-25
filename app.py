import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="International Debt Analytics",
    layout="wide",
    page_icon="🌍"
)

# =====================================================
# TITLE
# =====================================================
st.title("🌍 International Debt Analytics System")
st.markdown("### 📊 Interactive Finance Analytics Dashboard")

# =====================================================
# MYSQL CONNECTION
# =====================================================
@st.cache_data
def load_data():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="K@rth!1990",
        database="international_debt"
    )

    query = "SELECT * FROM debt_data"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()

# =====================================================
# CHECK DATA
# =====================================================
if df.empty:
    st.error("❌ No Data Found in Database")
    st.stop()

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.title("🎛 Dashboard Filters")

# -----------------------------------------------------
# COUNTRY FILTER
# -----------------------------------------------------
country_list = sorted(df["country_name"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "🌍 Select Countries",
    options=country_list
)

# -----------------------------------------------------
# INDICATOR FILTER
# -----------------------------------------------------
indicator_list = sorted(df["series_name"].dropna().unique())

selected_indicators = st.sidebar.multiselect(
    "📌 Select Indicators",
    options=indicator_list
)

# -----------------------------------------------------
# YEAR FILTER
# -----------------------------------------------------
min_year = int(df["year"].min())
max_year = 2025

selected_years = st.sidebar.slider(
    "📅 Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# =====================================================
# HANDLE EMPTY FILTERS
# =====================================================
if not selected_countries:
    selected_countries = country_list

if not selected_indicators:
    selected_indicators = indicator_list

# =====================================================
# APPLY FILTERS
# =====================================================
filtered_df = df[
    (df["country_name"].isin(selected_countries)) &
    (df["series_name"].isin(selected_indicators)) &
    (df["year"].between(selected_years[0], selected_years[1]))
]

# =====================================================
# ACTIVE FILTER DISPLAY
# =====================================================
st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Active Filters")

st.sidebar.write(f"🌍 Countries: {len(selected_countries)}")
st.sidebar.write(f"📌 Indicators: {len(selected_indicators)}")
st.sidebar.write(f"📅 Years: {selected_years[0]} - {selected_years[1]}")

# =====================================================
# NAVIGATION
# =====================================================
page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Executive Dashboard",
        "🌍 Global Analysis",
        "📈 Trend Analysis",
        "📊 Deep Insights",
        "🧠 SQL Analytics",
        "📥 Export Data"
    ]
)

# =====================================================
# KPI CALCULATIONS
# =====================================================
total_debt = filtered_df["debt"].sum()

avg_debt = filtered_df["debt"].mean()

total_countries = filtered_df["country_name"].nunique()

total_indicators = filtered_df["series_name"].nunique()

highest_country = (
    filtered_df.groupby("country_name")["debt"]
    .sum()
    .idxmax()
    if not filtered_df.empty else "N/A"
)

# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================
if page == "🏠 Executive Dashboard":

    st.subheader("📊 Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Debt",
        f"{total_debt:,.0f}"
    )

    col2.metric(
        "📈 Average Debt",
        f"{avg_debt:,.2f}"
    )

    col3.metric(
        "🌍 Countries",
        total_countries
    )

    col4.metric(
        "📌 Indicators",
        total_indicators
    )

    st.markdown("---")

    st.success(f"🏆 Highest Debt Country: {highest_country}")

    # -------------------------------------------------
    # TOP 10 COUNTRIES
    # -------------------------------------------------
    top10 = (
        filtered_df.groupby("country_name")["debt"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top10,
        x="country_name",
        y="debt",
        color="debt",
        title="🌍 Top 10 Countries by Debt",
        text_auto=True,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Debt"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------
    # PIE CHART
    # -------------------------------------------------
    st.subheader("📌 Debt Contribution")

    pie_fig = px.pie(
        top10,
        names="country_name",
        values="debt",
        hole=0.4,
        title="Top Country Contribution"
    )

    st.plotly_chart(pie_fig, use_container_width=True)

    # -------------------------------------------------
    # SMART INSIGHTS
    # -------------------------------------------------
    st.subheader("🧠 Smart Insights")

    st.info(f"""
    🌍 Total Countries Selected: {total_countries}

    💰 Global Debt Volume: {total_debt:,.0f}

    📈 Average Debt: {avg_debt:,.2f}

    🏆 Highest Debt Country: {highest_country}

    📌 Total Indicators: {total_indicators}
    """)

# =====================================================
# GLOBAL ANALYSIS
# =====================================================
elif page == "🌍 Global Analysis":

    st.subheader("🌍 Global Debt Distribution")

    map_df = (
        filtered_df.groupby("country_name")["debt"]
        .sum()
        .reset_index()
    )

    map_fig = px.choropleth(
        map_df,
        locations="country_name",
        locationmode="country names",
        color="debt",
        hover_name="country_name",
        color_continuous_scale="Reds",
        title="🌍 Global Debt Map"
    )

    st.plotly_chart(map_fig, use_container_width=True)

    # -------------------------------------------------
    # COUNTRY COMPARISON
    # -------------------------------------------------
    st.subheader("📊 Country Comparison")

    compare_fig = px.bar(
        map_df.sort_values("debt", ascending=False).head(20),
        x="country_name",
        y="debt",
        color="debt",
        title="Top 20 Countries by Debt"
    )

    st.plotly_chart(compare_fig, use_container_width=True)

# =====================================================
# TREND ANALYSIS
# =====================================================
elif page == "📈 Trend Analysis":

    st.subheader("📈 Debt Trend Analysis")

    trend_df = (
        filtered_df.groupby("year")["debt"]
        .sum()
        .reset_index()
    )

    trend_fig = px.line(
        trend_df,
        x="year",
        y="debt",
        markers=True,
        title="📈 Global Debt Trend"
    )

    st.plotly_chart(trend_fig, use_container_width=True)

    # -------------------------------------------------
    # AREA CHART
    # -------------------------------------------------
    area_fig = px.area(
        trend_df,
        x="year",
        y="debt",
        title="📊 Debt Growth Area Chart"
    )

    st.plotly_chart(area_fig, use_container_width=True)

    # -------------------------------------------------
    # COUNTRY TREND
    # -------------------------------------------------
    country_trend = (
        filtered_df.groupby(["year", "country_name"])["debt"]
        .sum()
        .reset_index()
    )

    line_fig = px.line(
        country_trend,
        x="year",
        y="debt",
        color="country_name",
        title="🌍 Country-wise Debt Trend"
    )

    st.plotly_chart(line_fig, use_container_width=True)

# =====================================================
# DEEP INSIGHTS
# =====================================================
elif page == "📊 Deep Insights":

    st.subheader("📌 Indicator Analysis")

    indicator_df = (
        filtered_df.groupby("series_name")["debt"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    indicator_fig = px.bar(
        indicator_df,
        x="series_name",
        y="debt",
        color="debt",
        title="📊 Top Indicators by Debt"
    )

    st.plotly_chart(indicator_fig, use_container_width=True)

    # -------------------------------------------------
    # HEATMAP
    # -------------------------------------------------
    st.subheader("🔥 Country vs Indicator Heatmap")

    pivot = filtered_df.pivot_table(
        index="country_name",
        columns="series_name",
        values="debt",
        aggfunc="sum"
    ).fillna(0)

    heatmap = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="Reds",
        title="Country vs Indicator Debt Heatmap"
    )

    st.plotly_chart(heatmap, use_container_width=True)

    # -------------------------------------------------
    # SCATTER ANALYSIS
    # -------------------------------------------------
    st.subheader("📊 Scatter Analysis")

    scatter_fig = px.scatter(
        filtered_df,
        x="year",
        y="debt",
        color="country_name",
        size="debt",
        hover_data=["series_name"],
        title="Debt Distribution Over Time"
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

# =====================================================
# SQL ANALYTICS
# =====================================================
elif page == "🧠 SQL Analytics":

    st.subheader("🧠 SQL Analytics Center")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="K@rth!1990",
        database="international_debt"
    )

    queries = {

        "1. Total Global Debt":
            "SELECT SUM(debt) AS total_debt FROM debt_data",

        "2. Total Countries":
            "SELECT COUNT(DISTINCT country_name) AS countries FROM debt_data",

        "3. Top 10 Countries":
            """
            SELECT country_name,
            SUM(debt) AS total_debt
            FROM debt_data
            GROUP BY country_name
            ORDER BY total_debt DESC
            LIMIT 10
            """,

        "4. Indicator Wise Debt":
            """
            SELECT series_name,
            SUM(debt) AS total_debt
            FROM debt_data
            GROUP BY series_name
            ORDER BY total_debt DESC
            """,

        "5. Rank Countries":
            """
            SELECT country_name,
            SUM(debt) AS total_debt,

            RANK() OVER(
                ORDER BY SUM(debt) DESC
            ) AS ranking

            FROM debt_data
            GROUP BY country_name
            """
    }

    selected_query = st.selectbox(
        "📌 Select SQL Query",
        list(queries.keys())
    )

    try:

        result = pd.read_sql(
            queries[selected_query],
            conn
        )

        st.dataframe(
            result,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"❌ Query Error: {e}")

    conn.close()

# =====================================================
# EXPORT DATA
# =====================================================
elif page == "📥 Export Data":

    st.subheader("📥 Export Filtered Dataset")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="filtered_debt_data.csv",
        mime="text/csv"
    )

    st.success("✅ Dataset Ready for Download")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")

st.caption("🚀 Developed using Python, MySQL, Streamlit & Plotly")