import datetime as dt
from dataclasses import dataclass

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Tesla Competitor Intelligence Dashboard",
    page_icon="TSLA",
    layout="wide",
    initial_sidebar_state="expanded",
)


ACCENT = "#0f766e"
INK = "#17202a"
MUTED = "#64748b"
PANEL = "#f7faf9"


@dataclass(frozen=True)
class CompanyProfile:
    name: str
    ticker: str
    industry: str
    headquarters: str
    founded: int
    employees: str
    website: str
    overview: str


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: #ffffff;
            color: {INK};
        }}
        section[data-testid="stSidebar"] {{
            background: #f3f7f6;
            border-right: 1px solid #d9e4e1;
        }}
        .metric-card {{
            border: 1px solid #dce7e4;
            background: {PANEL};
            border-radius: 8px;
            padding: 16px 18px;
            min-height: 112px;
        }}
        .metric-label {{
            color: {MUTED};
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 8px;
        }}
        .metric-value {{
            color: {INK};
            font-weight: 760;
            font-size: 1.62rem;
            line-height: 1.15;
        }}
        .metric-note {{
            color: {MUTED};
            font-size: 0.84rem;
            margin-top: 8px;
        }}
        .section-title {{
            color: {INK};
            font-size: 1.1rem;
            font-weight: 760;
            margin: 12px 0 8px;
        }}
        .insight-box {{
            border-left: 4px solid {ACCENT};
            background: #eef7f5;
            padding: 14px 16px;
            border-radius: 6px;
            margin: 8px 0 14px;
        }}
        .news-item {{
            border-bottom: 1px solid #e2e8e6;
            padding: 10px 0;
        }}
        .news-title {{
            font-weight: 700;
            color: {INK};
        }}
        .news-meta {{
            color: {MUTED};
            font-size: 0.82rem;
        }}
        div[data-testid="stMetric"] {{
            background: {PANEL};
            border: 1px solid #dce7e4;
            border-radius: 8px;
            padding: 12px 14px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_demo_data() -> dict:
    profile = CompanyProfile(
        name="Tesla",
        ticker="TSLA",
        industry="Electric vehicles, energy storage, solar, charging and AI-enabled mobility",
        headquarters="Austin, Texas, United States",
        founded=2003,
        employees="140k+",
        website="https://www.tesla.com",
        overview=(
            "Tesla designs, manufactures and sells electric vehicles, battery energy storage systems, "
            "solar products, charging infrastructure, software-enabled services and AI-driven autonomy "
            "capabilities. Its current strategic pressure points are EV demand, pricing discipline, "
            "battery cost control, energy storage growth, autonomy execution and competition from BYD, "
            "legacy automakers and premium EV challengers."
        ),
    )

    revenue = pd.DataFrame(
        [
            {"Year": 2020, "Revenue": 31.5, "Gross Profit": 6.6, "Operating Income": 2.0},
            {"Year": 2021, "Revenue": 53.8, "Gross Profit": 13.6, "Operating Income": 6.5},
            {"Year": 2022, "Revenue": 81.5, "Gross Profit": 20.9, "Operating Income": 13.7},
            {"Year": 2023, "Revenue": 96.8, "Gross Profit": 17.7, "Operating Income": 8.9},
            {"Year": 2024, "Revenue": 97.7, "Gross Profit": 17.5, "Operating Income": 7.1},
        ]
    )

    segments = pd.DataFrame(
        [
            {"Segment": "Automotive", "Revenue": 77.1, "Margin Profile": "High scale, price-sensitive"},
            {"Segment": "Energy Generation & Storage", "Revenue": 10.1, "Margin Profile": "Fast growth, improving"},
            {"Segment": "Services & Other", "Revenue": 10.5, "Margin Profile": "Lower margin, ecosystem support"},
        ]
    )

    products = pd.DataFrame(
        [
            {"Product": "Model Y", "Category": "Vehicle", "Role": "Volume SUV", "Priority": 96},
            {"Product": "Model 3", "Category": "Vehicle", "Role": "Volume sedan", "Priority": 89},
            {"Product": "Cybertruck", "Category": "Vehicle", "Role": "Pickup and brand halo", "Priority": 70},
            {"Product": "Model S/X", "Category": "Vehicle", "Role": "Premium portfolio", "Priority": 54},
            {"Product": "Megapack", "Category": "Energy", "Role": "Utility-scale storage", "Priority": 91},
            {"Product": "Powerwall", "Category": "Energy", "Role": "Residential storage", "Priority": 72},
            {"Product": "Supercharger", "Category": "Infrastructure", "Role": "Charging network", "Priority": 84},
            {"Product": "FSD / Autopilot", "Category": "Software", "Role": "Autonomy monetization", "Priority": 88},
        ]
    )

    pricing = pd.DataFrame(
        [
            {"Product": "Model 3", "Entry Price USD": 38990, "Positioning": "Mass-market EV sedan"},
            {"Product": "Model Y", "Entry Price USD": 44990, "Positioning": "Mass-market EV crossover"},
            {"Product": "Model S", "Entry Price USD": 74990, "Positioning": "Premium EV sedan"},
            {"Product": "Model X", "Entry Price USD": 79990, "Positioning": "Premium EV SUV"},
            {"Product": "Cybertruck", "Entry Price USD": 69990, "Positioning": "Electric pickup"},
            {"Product": "Full Self-Driving", "Entry Price USD": 8000, "Positioning": "Software option"},
        ]
    )

    competitors = pd.DataFrame(
        [
            {"Company": "BYD", "Region": "China / Global", "EV Focus": "Mass-market EVs and plug-in hybrids", "Threat Score": 94},
            {"Company": "Volkswagen Group", "Region": "Europe / Global", "EV Focus": "Multi-brand EV portfolio", "Threat Score": 77},
            {"Company": "Hyundai-Kia", "Region": "Korea / Global", "EV Focus": "Value-to-premium EV platforms", "Threat Score": 73},
            {"Company": "General Motors", "Region": "North America", "EV Focus": "Trucks, SUVs and fleet", "Threat Score": 61},
            {"Company": "Ford", "Region": "North America", "EV Focus": "F-150 Lightning and Mustang Mach-E", "Threat Score": 59},
            {"Company": "Rivian", "Region": "North America", "EV Focus": "Adventure trucks, SUVs and vans", "Threat Score": 54},
            {"Company": "Lucid", "Region": "North America / Middle East", "EV Focus": "Luxury long-range EVs", "Threat Score": 47},
        ]
    )

    market_share = pd.DataFrame(
        [
            {"Company": "Tesla", "Global EV Share": 16.8, "US EV Share": 49.0},
            {"Company": "BYD", "Global EV Share": 19.1, "US EV Share": 0.0},
            {"Company": "Volkswagen Group", "Global EV Share": 7.6, "US EV Share": 4.2},
            {"Company": "Hyundai-Kia", "Global EV Share": 5.2, "US EV Share": 8.1},
            {"Company": "GM", "Global EV Share": 2.7, "US EV Share": 6.7},
            {"Company": "Ford", "Global EV Share": 2.2, "US EV Share": 7.5},
            {"Company": "Other", "Global EV Share": 46.4, "US EV Share": 24.5},
        ]
    )

    funding = pd.DataFrame(
        [
            {"Event": "IPO", "Year": 2010, "Amount USD": 226, "Type": "Public equity"},
            {"Event": "Convertible notes", "Year": 2014, "Amount USD": 2000, "Type": "Debt financing"},
            {"Event": "Equity offering", "Year": 2020, "Amount USD": 5000, "Type": "Public equity"},
            {"Event": "Equity offering", "Year": 2020, "Amount USD": 5000, "Type": "Public equity"},
        ]
    )

    news = pd.DataFrame(
        [
            {
                "Date": "2026-06-20",
                "Headline": "Robotaxi and autonomy execution remain core investor watch items",
                "Source": "Market signal",
                "Impact": "High",
            },
            {
                "Date": "2026-05-31",
                "Headline": "Energy storage growth offsets slower EV unit growth in investor narratives",
                "Source": "Analyst theme",
                "Impact": "Medium",
            },
            {
                "Date": "2026-05-10",
                "Headline": "Pricing pressure continues across key EV markets",
                "Source": "Competitive trend",
                "Impact": "High",
            },
            {
                "Date": "2026-04-24",
                "Headline": "Chinese EV makers intensify international expansion",
                "Source": "Competitive trend",
                "Impact": "High",
            },
        ]
    )

    swot = {
        "Strengths": [
            "Brand leadership in EVs and software-defined vehicles",
            "Supercharger network and vertically integrated charging experience",
            "Battery, manufacturing and energy storage scale advantages",
        ],
        "Weaknesses": [
            "High exposure to vehicle price cuts and margin volatility",
            "Product refresh cadence is slower than several China-based rivals",
            "Autonomy valuation depends on execution and regulation",
        ],
        "Opportunities": [
            "Energy storage expansion through Megapack demand",
            "Software revenue from FSD, fleet services and insurance",
            "Robotaxi, Optimus and AI infrastructure optionality",
        ],
        "Threats": [
            "BYD and Chinese EV makers pressuring global price points",
            "Legacy OEMs improving EV quality and financing offers",
            "Regulatory, tariff and supply-chain volatility",
        ],
    }

    return {
        "profile": profile,
        "revenue": revenue,
        "segments": segments,
        "products": products,
        "pricing": pricing,
        "competitors": competitors,
        "market_share": market_share,
        "funding": funding,
        "news": news,
        "swot": swot,
    }


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def ai_summary(profile: CompanyProfile, revenue: pd.DataFrame, competitors: pd.DataFrame) -> str:
    latest = revenue.sort_values("Year").iloc[-1]
    top_threat = competitors.sort_values("Threat Score", ascending=False).iloc[0]
    return (
        f"{profile.name} remains a scale leader, with ${latest['Revenue']:.1f}B in latest demo revenue data. "
        f"The sharpest competitive pressure comes from {top_threat['Company']}, especially where lower-cost EVs, "
        "battery integration and local market depth matter. The most attractive dashboard follow-up is to track "
        "pricing changes, energy-storage mix shift and autonomy milestones as leading indicators."
    )


def revenue_chart(df: pd.DataFrame) -> alt.Chart:
    base = alt.Chart(df).encode(
        x=alt.X("Year:O", title=""),
        tooltip=[
            alt.Tooltip("Year:O"),
            alt.Tooltip("Revenue:Q", title="Revenue, USD billions", format=",.1f"),
            alt.Tooltip("Operating Income:Q", title="Operating income, USD billions", format=",.1f"),
        ],
    )
    bars = base.mark_bar(color=ACCENT).encode(
        y=alt.Y("Revenue:Q", title="USD billions"),
    )
    line = base.mark_line(point=True, color="#dc2626", strokeWidth=3).encode(
        y=alt.Y("Operating Income:Q", title="USD billions"),
    )
    return (bars + line).properties(height=360)


def segment_chart(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("Revenue:Q", title="Revenue, USD billions"),
            y=alt.Y("Segment:N", sort="-x", title=""),
            color=alt.Color("Segment:N", legend=None, scale=alt.Scale(range=["#0f766e", "#2563eb", "#f59e0b"])),
            tooltip=["Segment:N", alt.Tooltip("Revenue:Q", format=",.1f"), "Margin Profile:N"],
        )
        .properties(height=260)
    )


def donut_chart(df: pd.DataFrame, value_col: str) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=70, outerRadius=140)
        .encode(
            theta=alt.Theta(f"{value_col}:Q"),
            color=alt.Color("Company:N", scale=alt.Scale(scheme="tableau10")),
            tooltip=["Company:N", alt.Tooltip(f"{value_col}:Q", format=",.1f")],
        )
        .properties(height=360)
    )


def threat_chart(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("Threat Score:Q", title="Threat score"),
            y=alt.Y("Company:N", sort="-x", title=""),
            color=alt.Color("Threat Score:Q", scale=alt.Scale(range=["#bfdbfe", "#dc2626"]), legend=None),
            tooltip=["Company:N", "Region:N", "EV Focus:N", "Threat Score:Q"],
        )
        .properties(height=360)
    )


def product_priority_chart(df: pd.DataFrame) -> alt.Chart:
    points = (
        alt.Chart(df)
        .mark_circle(opacity=0.82)
        .encode(
            x=alt.X("Category:N", title=""),
            y=alt.Y("Priority:Q", scale=alt.Scale(domain=[40, 100])),
            size=alt.Size("Priority:Q", legend=None, scale=alt.Scale(range=[280, 1200])),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Product:N", "Category:N", "Role:N", "Priority:Q"],
        )
    )
    labels = (
        alt.Chart(df)
        .mark_text(dy=-24, fontSize=12)
        .encode(x="Category:N", y="Priority:Q", text="Product:N", color=alt.value(INK))
    )
    return (points + labels).properties(height=380)


def pricing_chart(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df.sort_values("Entry Price USD"))
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("Entry Price USD:Q", title="USD", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("Product:N", sort="-x", title=""),
            color=alt.Color("Entry Price USD:Q", scale=alt.Scale(range=["#ccfbf1", ACCENT]), legend=None),
            tooltip=["Product:N", alt.Tooltip("Entry Price USD:Q", format="$,.0f"), "Positioning:N"],
        )
        .properties(height=380)
    )


def swot_grid(swot: dict) -> None:
    cols = st.columns(4)
    palette = {
        "Strengths": "#ecfdf5",
        "Weaknesses": "#fff7ed",
        "Opportunities": "#eff6ff",
        "Threats": "#fef2f2",
    }
    for col, (title, items) in zip(cols, swot.items()):
        with col:
            st.markdown(f"**{title}**")
            for item in items:
                st.markdown(
                    f"""
                    <div style="background:{palette[title]};border:1px solid #d8e3df;border-radius:8px;
                    padding:10px 12px;margin-bottom:8px;font-size:0.9rem;">{item}</div>
                    """,
                    unsafe_allow_html=True,
                )


def render_dashboard(data: dict, company_query: str, region: str, scenario: str) -> None:
    profile = data["profile"]
    revenue = data["revenue"].copy()
    segments = data["segments"].copy()
    products = data["products"].copy()
    pricing = data["pricing"].copy()
    competitors = data["competitors"].copy()
    market_share = data["market_share"].copy()
    funding = data["funding"].copy()
    news = data["news"].copy()

    if scenario == "Aggressive price cuts":
        pricing["Entry Price USD"] = (pricing["Entry Price USD"] * 0.92).round(0)
        revenue["Operating Income"] = (revenue["Operating Income"] * 0.82).round(1)
    elif scenario == "Energy upside":
        segments.loc[segments["Segment"].str.contains("Energy"), "Revenue"] *= 1.25
        revenue.loc[revenue.index[-1], "Revenue"] += 2.5
    elif scenario == "Autonomy upside":
        products.loc[products["Product"].str.contains("FSD"), "Priority"] = 98

    if company_query.strip().lower() not in {"tesla", "tsla"}:
        st.warning("Demo data is available for Tesla. The search workflow is ready for additional company connectors.")

    st.title("Tesla Competitor Intelligence Dashboard")
    st.caption(
        f"AI-fetched modules: overview, revenue, products, funding, news, pricing, SWOT, competitors, "
        f"market share and business segments | Region lens: {region} | Refreshed {dt.date.today():%b %d, %Y}"
    )

    st.markdown(f"<div class='insight-box'>{ai_summary(profile, revenue, competitors)}</div>", unsafe_allow_html=True)

    latest = revenue.sort_values("Year").iloc[-1]
    previous = revenue.sort_values("Year").iloc[-2]
    yoy = ((latest["Revenue"] / previous["Revenue"]) - 1) * 100
    top_segment = segments.sort_values("Revenue", ascending=False).iloc[0]
    top_competitor = competitors.sort_values("Threat Score", ascending=False).iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Latest Revenue", f"${latest['Revenue']:.1f}B", f"{yoy:+.1f}% year over year")
    with m2:
        metric_card("Primary Segment", top_segment["Segment"], f"${top_segment['Revenue']:.1f}B demo revenue")
    with m3:
        metric_card("Top Competitive Threat", top_competitor["Company"], f"Threat score {top_competitor['Threat Score']}/100")
    with m4:
        metric_card("US EV Share", "49.0%", "Demo estimate for dashboard design")

    tab_overview, tab_market, tab_products, tab_news, tab_data = st.tabs(
        ["Overview", "Market & Competitors", "Products & Pricing", "News & SWOT", "Data Tables"]
    )

    with tab_overview:
        left, right = st.columns([1.2, 0.8])
        with left:
            st.markdown("<div class='section-title'>Revenue And Operating Performance</div>", unsafe_allow_html=True)
            st.altair_chart(revenue_chart(revenue), use_container_width=True)
        with right:
            st.markdown("<div class='section-title'>Company Overview</div>", unsafe_allow_html=True)
            st.write(profile.overview)
            st.write(f"**Ticker:** {profile.ticker}")
            st.write(f"**Industry:** {profile.industry}")
            st.write(f"**Headquarters:** {profile.headquarters}")
            st.write(f"**Founded:** {profile.founded}")
            st.write(f"**Employees:** {profile.employees}")

        st.markdown("<div class='section-title'>Business Segments</div>", unsafe_allow_html=True)
        st.altair_chart(segment_chart(segments), use_container_width=True)

    with tab_market:
        col1, col2 = st.columns([0.9, 1.1])
        share_col = "US EV Share" if region == "United States" else "Global EV Share"
        with col1:
            st.markdown("<div class='section-title'>Market Share</div>", unsafe_allow_html=True)
            st.altair_chart(donut_chart(market_share, share_col), use_container_width=True)
        with col2:
            st.markdown("<div class='section-title'>Competitor Threat Scores</div>", unsafe_allow_html=True)
            threat = competitors.sort_values("Threat Score", ascending=True)
            st.altair_chart(threat_chart(threat), use_container_width=True)

        st.dataframe(competitors, use_container_width=True, hide_index=True)

    with tab_products:
        left, right = st.columns([1, 1])
        with left:
            st.markdown("<div class='section-title'>Product Portfolio Priority</div>", unsafe_allow_html=True)
            st.altair_chart(product_priority_chart(products), use_container_width=True)
        with right:
            st.markdown("<div class='section-title'>Pricing Ladder</div>", unsafe_allow_html=True)
            st.altair_chart(pricing_chart(pricing), use_container_width=True)

        st.dataframe(pricing, use_container_width=True, hide_index=True)

    with tab_news:
        col1, col2 = st.columns([0.8, 1.2])
        with col1:
            st.markdown("<div class='section-title'>Recent News Signals</div>", unsafe_allow_html=True)
            for _, row in news.iterrows():
                st.markdown(
                    f"""
                    <div class="news-item">
                        <div class="news-title">{row['Headline']}</div>
                        <div class="news-meta">{row['Date']} | {row['Source']} | Impact: {row['Impact']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with col2:
            st.markdown("<div class='section-title'>SWOT Analysis</div>", unsafe_allow_html=True)
            swot_grid(data["swot"])

    with tab_data:
        st.markdown("<div class='section-title'>Downloadable Intelligence Tables</div>", unsafe_allow_html=True)
        table_name = st.selectbox(
            "Select table",
            ["Revenue", "Business Segments", "Products", "Pricing", "Funding", "Competitors", "Market Share", "News"],
        )
        tables = {
            "Revenue": revenue,
            "Business Segments": segments,
            "Products": products,
            "Pricing": pricing,
            "Funding": funding,
            "Competitors": competitors,
            "Market Share": market_share,
            "News": news,
        }
        selected = tables[table_name]
        st.dataframe(selected, use_container_width=True, hide_index=True)
        st.download_button(
            "Download CSV",
            selected.to_csv(index=False).encode("utf-8"),
            file_name=f"{profile.name.lower()}_{table_name.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )


def main() -> None:
    inject_css()
    data = load_demo_data()

    with st.sidebar:
        st.header("Search")
        company_query = st.text_input("Company", value="Tesla", placeholder="Enter company name or ticker")
        region = st.radio("Market share lens", ["Global", "United States"], horizontal=False)
        scenario = st.selectbox(
            "Scenario",
            ["Base case", "Aggressive price cuts", "Energy upside", "Autonomy upside"],
        )
        st.divider()
        st.subheader("AI fetch modules")
        st.checkbox("Company Overview", value=True)
        st.checkbox("Revenue", value=True)
        st.checkbox("Products", value=True)
        st.checkbox("Funding", value=True)
        st.checkbox("Recent News", value=True)
        st.checkbox("Pricing", value=True)
        st.checkbox("SWOT", value=True)
        st.checkbox("Competitors", value=True)
        st.checkbox("Market Share", value=True)
        st.checkbox("Business Segments", value=True)
        st.caption("Demo mode uses built-in Tesla intelligence. Replace `load_demo_data()` with API calls for production.")

    render_dashboard(data, company_query, region, scenario)


if __name__ == "__main__":
    main()
