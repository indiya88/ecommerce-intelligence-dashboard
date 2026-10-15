"""E-Commerce dashboard built with Python.

To open it, run: python -m streamlit run app.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from insights import build_insights

# Set up the dashboard page and choose the main colours.
st.set_page_config(page_title="E-Commerce Intelligence", page_icon="📈", layout="wide")
# Cyber Glass: deep obsidian with violet, magenta and cyan lighting.
BG_COLOR = "#090A0F"
PANEL = "#12141E"
BORDER = "#39304F"
TEXT = "#F3F4F6"
MUTED = "#A8A7BC"
ACCENT = "#A855F7"
BLUE = "#22D3EE"
GOLD = "#F59E79"  # Warm accent for the largest category.
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#FB7185"
GRID = "#302B42"
STATUS_COLORS = {
    "Delivered": "#10B981", "Shipped": "#22D3EE",
    "Pending": "#F59E0B", "Cancelled": "#FB7185", "Returned": "#A855F7",
}

# Give the dashboard floating glass panels and gentle background lighting.
st.markdown("""
<style>
.stApp {
    color:#F3F4F6!important;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    background:
      radial-gradient(ellipse 55% 45% at 55% -10%,rgba(130,58,232,.29),transparent 75%),
      radial-gradient(ellipse 40% 40% at 100% 46%,rgba(214,50,142,.105),transparent 80%),
      radial-gradient(ellipse 45% 45% at 0% 80%,rgba(31,131,194,.075),transparent 78%),
      linear-gradient(155deg,#090A0F 0%,#0D0D19 50%,#0B0A13 100%)!important;
    background-attachment:fixed!important;
}
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,rgba(15,15,29,.96),rgba(10,11,20,.98))!important;
    border-right:1px solid rgba(168,85,247,.18)!important;
    box-shadow:12px 0 36px rgba(0,0,0,.18)!important;
}
[data-testid="stHeader"],[data-testid="stToolbar"] {background:transparent!important}
[data-testid="stDecoration"] {display:none!important}
.block-container {max-width:1650px;padding-top:.7rem!important;padding-bottom:1.4rem!important}
h1,h2,h3 {color:#F3F4F6!important;letter-spacing:-.028em}
h1 {text-shadow:0 5px 28px rgba(168,85,247,.19)}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#CFD0E5!important;opacity:1!important}
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background:rgba(26,25,42,.95)!important;
    border:1px solid rgba(168,85,247,.24)!important;
    color:#F3F4F6!important;border-radius:10px!important;
}
[data-testid="stSidebar"] [data-baseweb="select"] input {color:#F3F4F6!important}
[data-testid="stSidebar"] [data-baseweb="tag"],
[data-testid="stSidebar"] [data-baseweb="tag"] > span,
[data-testid="stSidebar"] [data-baseweb="tag"] > div {
    background:#33244D!important;color:#F3F4F6!important;
    border-color:#62438C!important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] svg {fill:#F3F4F6!important;color:#F3F4F6!important}
/* Translucent containers: light comes from the background, not thick borders. */
[data-testid="stMetric"],
[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
    background:linear-gradient(135deg,rgba(36,29,57,.73),rgba(17,20,33,.78))!important;
    border:1px solid rgba(168,85,247,.16)!important;
    border-radius:16px!important;
    -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.065),0 14px 40px rgba(0,0,0,.27)!important;
}
[data-testid="stMetric"] {padding:16px!important}
[data-testid="stMetricLabel"] {color:#B4B1C8!important;font-size:.85rem!important}
[data-testid="stMetricValue"] {color:#FFF!important;font-weight:650!important}
/* Charts remain transparent so they sit naturally inside their glass cards. */
[data-testid="stPlotlyChart"] {
    border-radius:16px;overflow:hidden;
    background:linear-gradient(140deg,rgba(36,28,58,.72),rgba(17,20,32,.8))!important;
    border:1px solid rgba(168,85,247,.16)!important;
    -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.055),0 12px 34px rgba(0,0,0,.24)!important;
}
[data-testid="stPlotlyChart"] > div {background:transparent!important}
/* Keep ordinary buttons quiet; the insight action gets a violet hover glow. */
div.stButton > button {
    background:linear-gradient(125deg,rgba(47,33,76,.92),rgba(26,29,48,.94))!important;
    color:#F3F4F6!important;border:1px solid rgba(168,85,247,.25)!important;
    border-radius:11px!important;font-weight:550!important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 5px 18px rgba(0,0,0,.18)!important;
    transition:background .2s ease,border-color .2s ease,box-shadow .2s ease;
}
div.stButton > button:hover {
    background:linear-gradient(125deg,#54347F,#352C65)!important;color:#FFF!important;
    border-color:#A855F7!important;box-shadow:0 0 18px rgba(168,85,247,.25)!important;
}
/* Full-size KPI cards: the value is the visual focus, not the button label. */
.kpi-face {
    min-height: 112px; padding: 15px 16px 7px;
    border: 1px solid rgba(168,85,247,.38);
    border-bottom: 0; border-radius: 13px 13px 0 0;
    background: linear-gradient(140deg,rgba(52,36,83,.72),rgba(24,23,43,.93));
    text-align: left;
}
.kpi-label {font-size:.76rem;font-weight:750;letter-spacing:.07em;color:#C8BCE7;}
.kpi-number {font-size:clamp(1.85rem,2.7vw,2.85rem);font-weight:850;
    line-height:1.22;letter-spacing:-.04em;color:#FFFFFF;margin:7px 0 4px;}
.kpi-number.problem {color:#FDA4AF;}
.kpi-detail {font-size:.8rem;color:#C5BFD4;}
.st-key-kpi_all button, .st-key-kpi_value button,
.st-key-kpi_fulfilled button, .st-key-kpi_problems button {
    width:100%;min-height:34px!important;padding:5px 12px!important;
    font-size:.78rem!important;border-radius:0 0 13px 13px!important;
    border-top:1px solid rgba(168,85,247,.17)!important;
    margin-top:-1rem!important;
}
.st-key-open_insights button {border-color:rgba(168,85,247,.65)!important;}
/* Streamlit's data grid needs a dark application theme as well (config.toml). */
[data-testid="stDataFrame"] {
    background:rgba(18,20,30,.78)!important;
    border:1px solid rgba(168,85,247,.18)!important;
    border-radius:12px!important;overflow:hidden;
}

/* Compact spacing for the overview; tabs hold the deeper analysis. */
[data-testid="stMetric"] {padding:12px!important}
[data-testid="stPlotlyChart"] {margin-bottom:0!important}
.stTabs [data-baseweb="tab-list"] {gap:10px}
.stTabs [data-baseweb="tab"] {
    border-radius:10px 10px 0 0;
    color:#CFC9E7!important;
    padding:9px 16px;
}
.stTabs [aria-selected="true"] {color:#F5EFFF!important}

/* Only the KPI drill-down tables use this centered, balanced layout. */
.kpi-detail-table {width:100%;table-layout:fixed;border-collapse:separate;border-spacing:0;
  background:rgba(12,12,22,.6);border:1px solid rgba(168,85,247,.23);
  border-radius:10px;overflow:hidden;color:#F3F4F6;font-size:.84rem}
.kpi-detail-table th,.kpi-detail-table td {text-align:center!important;
  padding:10px 8px;border-right:1px solid rgba(168,85,247,.1);
  border-bottom:1px solid rgba(168,85,247,.1);overflow-wrap:anywhere}
.kpi-detail-table th {color:#B8AFD2;font-weight:600;background:rgba(168,85,247,.09)}
.kpi-detail-table tr:last-child td {border-bottom:0}
.kpi-detail-table th:last-child,.kpi-detail-table td:last-child {border-right:0}
.kpi-detail-table tbody tr:hover {background:rgba(168,85,247,.08)}

/* Executive command centre: charts in two tight rows, not a long report. */
.overview-headline {font-size:.9rem;color:#D8D1E9;margin:-3px 0 8px}
.overview-section-title {font-size:.8rem;font-weight:800;letter-spacing:.11em;
    color:#C9B7F2;margin:9px 0 6px}
.overview-section-title span {font-size:.72rem;letter-spacing:0;font-weight:450;color:#A8A7BC}
.compact-chart-title {font-size:.91rem;font-weight:750;color:#F3F4F6;margin:0 0 1px}
.compact-chart-note {font-size:.73rem;color:#B7B2C9;min-height:1.1rem;margin:-5px 0 5px}
[data-testid="stVerticalBlockBorderWrapper"]:has(.compact-chart-title) > div[data-testid="stVerticalBlock"] {
    padding:10px 11px 8px!important;gap:.25rem!important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.compact-chart-title) [data-testid="stPlotlyChart"] {
    box-shadow:none!important;border:0!important;background:transparent!important;
}
.st-key-detail_products button,.st-key-detail_monthly button,.st-key-detail_status button,
.st-key-detail_marketing button,.st-key-detail_cart button,.st-key-detail_coupons button,
.st-key-quick_insight_products button,.st-key-quick_insight_monthly button,
.st-key-quick_insight_status button,.st-key-quick_insight_marketing button,
.st-key-quick_insight_cart button,.st-key-quick_insight_coupons button {
    font-size:.75rem!important;min-height:30px!important;padding:4px 7px!important;
}
@media (min-width: 1100px) {
    .block-container {max-width:1780px;padding-top:.4rem!important}
    .kpi-face {min-height:99px;padding:10px 13px 6px}
    .kpi-number {font-size:clamp(1.9rem,2.5vw,2.7rem);margin:3px 0 2px}
}
</style>
""", unsafe_allow_html=True)

# Read the CSV, fix data types and add columns we need for analysis.
@st.cache_data
def load_data():
    path = Path(__file__).parent / "data" / "cleaned_E-Commerce Orders.csv"
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip().str.lower()
    for column in ("date",):
        data[column] = pd.to_datetime(data[column], errors="coerce")
    for column in ("totalprice", "unitprice", "quantity", "itemsincart"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    for column in ("order_status", "product_name", "referralsource"):
        data[column] = data[column].astype("string").str.strip().str.title()
    data["year"] = data["date"].dt.year
    data["month_start"] = data["date"].dt.to_period("M").dt.to_timestamp()
    data["coupon_used"] = data["couponcode"].notna() & data["couponcode"].astype(str).str.strip().ne("")
    data["problem_order"] = data["order_status"].isin(["Cancelled", "Returned"])
    data["shipped_delivered"] = data["order_status"].isin(["Shipped", "Delivered"])
    return data.sort_values("date")

try:
    df = load_data()
except (FileNotFoundError, KeyError, ValueError) as exc:
    st.error(f"Unable to load the cleaned CSV: {exc}")
    st.stop()

# Add filters so users can choose which orders they want to see.
st.sidebar.markdown("### E-COMMERCE")
st.sidebar.caption("INTELLIGENCE  /  ORDER QUALITY")
st.sidebar.divider()
st.sidebar.markdown("**Explore your data**")
years = sorted(df["year"].dropna().astype(int).unique().tolist())
products = sorted(df["product_name"].dropna().unique().tolist())
sources = sorted(df["referralsource"].dropna().unique().tolist())
st.sidebar.caption("Leave a filter blank to include all values.")
selected_years = st.sidebar.multiselect("Year", years, default=[], placeholder="All years")
selected_products = st.sidebar.multiselect("Product", products, default=[], placeholder="All products")
selected_sources = st.sidebar.multiselect("Referral source", sources, default=[], placeholder="All sources")
filtered = df.copy()
if selected_years:
    filtered = filtered[filtered["year"].isin(selected_years)]
if selected_products:
    filtered = filtered[filtered["product_name"].isin(selected_products)]
if selected_sources:
    filtered = filtered[filtered["referralsource"].isin(selected_sources)]
st.sidebar.divider()
st.sidebar.caption(f"{len(filtered):,} of {len(df):,} orders selected")

# Reuse these chart settings so all graphs have a matching style.
def finish_chart(fig, height=245, right_margin=25):
    # Match the chart canvas to our cards, keeping each chart's axis titles.
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI Semibold, Segoe UI, Arial, sans-serif", color=TEXT, size=12),
        margin=dict(l=22, r=right_margin, t=26, b=42),
        hoverlabel=dict(bgcolor="#221A36", bordercolor=ACCENT, font_color=TEXT),
        bargap=0.62, bargroupgap=0.18,
        legend=dict(font=dict(family="Segoe UI Semibold, Segoe UI, Arial, sans-serif", color="#DCD5F0", size=12), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=BORDER,
                     tickfont=dict(family="Segoe UI Semibold, Segoe UI, Arial, sans-serif", color="#D6CCE9", size=12), title_font=dict(color="#D6CCE9", size=12))
    fig.update_yaxes(gridcolor="rgba(168,85,247,0.11)", griddash="dot", zeroline=False,
                     tickfont=dict(family="Segoe UI Semibold, Segoe UI, Arial, sans-serif", color="#D6CCE9", size=12), title_font=dict(color="#D6CCE9", size=12))
    return fig


def bar_chart(table, category, metric, *, percent=False, horizontal=False, height=245):
    """Draw slim neon bars, with a warm accent on the highest value."""
    colors = [GOLD if i == int(table[metric].argmax()) else BLUE for i in range(len(table))]
    if horizontal:
        fig = go.Figure(go.Bar(x=table[metric], y=table[category], orientation="h",
            width=0.42, marker=dict(color=colors, line=dict(width=0)),
            customdata=table[category],
            hovertemplate="%{customdata}: %{x:.1f}%<extra></extra>" if percent else "%{customdata}: %{x:,.0f}<extra></extra>"))
        fig.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Cancellation & Return Rate (%)" if percent else "Orders")
    else:
        fig = go.Figure(go.Bar(x=table[category], y=table[metric],
            width=0.42, marker=dict(color=colors, line=dict(width=0)),
            hovertemplate="%{x}: %{y:.1f}%<extra></extra>" if percent else "%{x}: %{y:,.0f}<extra></extra>"))
        fig.update_layout(xaxis_title="", yaxis_title="Cancellation & Return Rate (%)" if percent else "Orders")
    return finish_chart(fig, height)

# Show the dashboard title and calculate the main order numbers.
st.caption("BUSINESS INTELLIGENCE  /  PERFORMANCE OVERVIEW")
st.title("E-Commerce Intelligence")
st.markdown(f"<p style='color:{MUTED};margin-top:-12px'>Explore product performance, order outcomes, and shopping patterns with interactive analysis.</p>", unsafe_allow_html=True)
if filtered.empty:
    st.warning("No orders match your filters. Choose more years, products or sources.")
    st.stop()

n_orders = len(filtered)
order_value = filtered["totalprice"].sum()
fulfilled_count = int(filtered["shipped_delivered"].sum())
problem_count = int(filtered["problem_order"].sum())
problem_rate = 100 * problem_count / n_orders

# Show the business findings in a popup when the button is clicked.
# The findings change whenever the user changes the filters.
@st.dialog("Executive Insights", width="large")
def show_executive_insights():
    st.caption("Business findings from your selected orders")
    for item in build_insights(filtered):
        with st.container(border=True):
            st.markdown(f"**{item['title']}**")
            st.write(item["finding"])
            st.caption("Management follow-up: " + item["action"])

    st.markdown("#### Which orders were cancelled or returned?")
    problem_records = filtered.loc[filtered["problem_order"], [
        "order_id", "date", "product_name", "order_status",
        "quantity", "totalprice", "referralsource"
    ]].copy()
    problem_records["date"] = problem_records["date"].dt.strftime("%Y-%m-%d")
    problem_records = problem_records.sort_values(["product_name", "order_status"])
    st.dataframe(problem_records, height=310, hide_index=True, use_container_width=True,
        column_config={"totalprice": st.column_config.NumberColumn("Order value", format="$%.2f")})
    st.download_button("Download problem orders (CSV)", problem_records.to_csv(index=False),
        "cancelled_returned_orders.csv", "text/csv", key="download_problem_orders")

if st.button("💡 Explore Executive Insights · " + str(len(build_insights(filtered))) + " findings ↗", key="open_insights", type="primary"):
    show_executive_insights()

# Explain each chart in plain English, using the current filters.
# Keep the finding separate from possible explanations and next steps.
@st.dialog("Chart Insight", width="large")
def show_chart_insight(section):
    def explain(finding, impact, recommendation):
        st.markdown("**Finding**")
        st.write(finding)
        st.markdown("**Business Impact**")
        st.write(impact)
        st.markdown("**Recommendation**")
        st.write(recommendation)

    if section == "products":
        t = filtered.groupby("product_name").agg(
            orders=("order_id", "size"), problems=("problem_order", "sum"),
            cancelled=("order_status", lambda x: (x == "Cancelled").sum()),
            returned=("order_status", lambda x: (x == "Returned").sum()))
        if t.empty:
            st.write("No product information is available for this selection.")
        else:
            t["rate"] = 100 * t["problems"] / t["orders"]
            name, row = next(iter(t.sort_values("rate", ascending=False).iterrows()))
            explain(
                f"{name} has the highest cancellation and return rate at **{row['rate']:.1f}%**. "
                f"Of {int(row['orders'])} orders, {int(row['cancelled'])} were cancelled "
                f"and {int(row['returned'])} were returned.",
                f"This means {int(row['problems'])} {name} orders did not result in a retained sale. "
                "That makes this product worth reviewing, especially alongside products with more total problem orders.",
                "Management should review cancellation and return records separately, focusing on "
                "inventory availability, delivery performance, product descriptions, and supplier quality. "
                "These are areas to investigate, not confirmed causes."
            )
    elif section == "monthly":
        t = filtered.dropna(subset=["month_start"]).groupby("month_start").size()
        if t.empty:
            st.write("No dated orders are available for this selection.")
        else:
            high, low = t.idxmax(), t.idxmin()
            explain(
                f"**{high:%B %Y}** had the most orders (**{int(t.max())}**), while "
                f"**{low:%B %Y}** had the fewest (**{int(t.min())}**).",
                "Order activity varies by month. Knowing when demand rises and falls can help "
                "management plan staffing, inventory, and promotions.",
                "Management should compare the busiest and slowest months with promotional calendars, "
                "inventory levels, and seasonal demand. Partial months should be checked before drawing conclusions."
            )
    elif section == "status":
        t = filtered["order_status"].value_counts()
        explain(
            f"**{problem_count:,} of {n_orders:,} orders ({problem_rate:.1f}%)** were cancelled or returned. "
            f"That includes **{int(t.get('Cancelled', 0)):,} cancellations** and "
            f"**{int(t.get('Returned', 0)):,} returns**. Another **{fulfilled_count:,}** orders "
            "were shipped or delivered.",
            "A substantial share of orders is not ending in a retained sale. This can affect "
            "sales performance and create additional operational work.",
            "Management should review cancellation and return reasons separately and track whether "
            "the problem rate improves over time. Order value should not be treated as confirmed revenue."
        )
    elif section == "marketing":
        t = filtered.groupby("referralsource").agg(orders=("order_id", "size"), problems=("problem_order", "sum"))
        if t.empty:
            st.write("No referral-source information is available for this selection.")
        else:
            t["rate"] = 100 * t["problems"] / t["orders"]
            volume_name = t["orders"].idxmax()
            best_name = t["rate"].idxmin()
            explain(
                f"**{volume_name}** brings in the most orders (**{int(t.loc[volume_name, 'orders'])}**). "
                f"**{best_name}** has the lowest cancellation and return rate (**{t.loc[best_name, 'rate']:.1f}%**).",
                "The channel bringing the most orders is not necessarily the one bringing "
                "the strongest order outcomes. Both volume and quality matter when assessing marketing performance.",
                "Management should compare order volume, cancellation and return rates, and campaign costs "
                "before changing marketing spending. Differences in products and customer groups also deserve review."
            )
    elif section == "cart":
        t = filtered.dropna(subset=["itemsincart"]).groupby("itemsincart").agg(
            orders=("order_id", "size"), problems=("problem_order", "sum"))
        if t.empty:
            st.write("No cart-size information is available for this selection.")
        else:
            t["rate"] = 100 * t["problems"] / t["orders"]
            most = t["orders"].idxmax()
            highest = t["rate"].idxmax()
            explain(
                f"The most common cart size is **{most:g} items**, appearing in "
                f"**{int(t.loc[most, 'orders'])} orders**. Carts with **{highest:g} items** "
                f"have the highest observed cancellation and return rate (**{t.loc[highest, 'rate']:.1f}%** "
                f"across {int(t.loc[highest, 'orders'])} orders).",
                "Some cart sizes have a higher share of problem orders than others. "
                "Small groups can produce unusually high percentages, so the order counts matter too.",
                "Management should compare cart-size groups with enough orders and review the "
                "products and order outcomes within them. This dataset does not measure abandoned carts."
            )
    elif section == "coupons":
        t = filtered.copy()
        t["coupon_group"] = t["couponcode"].fillna("").astype(str).str.strip().replace("", "No coupon")
        t = t.groupby("coupon_group").agg(orders=("order_id", "size"), problems=("problem_order", "sum"))
        if t.empty:
            st.write("No coupon information is available for this selection.")
        else:
            t["rate"] = 100 * t["problems"] / t["orders"]
            most = t["orders"].idxmax()
            comparison = (f" Orders without a coupon have a **{t.loc['No coupon', 'rate']:.1f}%** "
                          "cancellation and return rate." if "No coupon" in t.index else "")
            explain(
                f"**{most}** is the most common coupon group, appearing in "
                f"**{int(t.loc[most, 'orders'])} orders**. Its cancellation and return rate is "
                f"**{t.loc[most, 'rate']:.1f}%**.{comparison}",
                "Coupon groups differ in both order volume and the share of orders cancelled or returned. "
                "A popular coupon does not automatically mean stronger sales performance.",
                "Management should compare coupon groups by order outcomes, discount costs, "
                "and campaign timing before deciding which promotions to continue or adjust."
            )


def insight_button(section, label="💡 View Insight"):
    if st.button(label, key=f"insight_{section}", type="secondary"):
        show_chart_insight(section)

# Center the small KPI detail tables so the numbers sit beneath their headings.
# These are short summaries, so a simple styled table is easier to read than a wide spreadsheet.
def show_kpi_table(data, money_columns=(), percent_columns=()):
    display = data.reset_index() if not isinstance(data.index, pd.RangeIndex) else data.copy()
    display.columns = [str(c).replace("_", " ").title() for c in display.columns]
    for name in money_columns:
        col = name.replace("_", " ").title()
        if col in display:
            display[col] = display[col].map(lambda x: f"${x:,.2f}")
    for name in percent_columns:
        col = name.replace("_", " ").title()
        if col in display:
            display[col] = display[col].map(lambda x: f"{x:.1f}%")
    html_table = display.to_html(index=False, escape=True, classes="kpi-detail-table", border=0)
    st.markdown(html_table, unsafe_allow_html=True)

# A compact executive overview: six charts in a 3-by-2 grid, with detail on demand.
# All calculations use the active sidebar filters; detailed views remain interactive.
overview_tab, orders_tab = st.tabs(["📊 Dashboard", "📋 Order Records"])

product = filtered.groupby("product_name").agg(
    orders=("order_id", "size"), problem_orders=("problem_order", "sum"),
    cancelled=("order_status", lambda x: (x == "Cancelled").sum()),
    returned=("order_status", lambda x: (x == "Returned").sum()),
).reset_index()
product["problem_rate"] = 100 * product["problem_orders"] / product["orders"]
product = product.sort_values("problem_rate", ascending=False)
monthly = filtered.dropna(subset=["month_start"]).groupby("month_start").size().reset_index(name="orders")
statuses = filtered["order_status"].value_counts().rename_axis("status").reset_index(name="orders")
channel = filtered.groupby("referralsource").agg(
    orders=("order_id", "size"), problem_orders=("problem_order", "sum"),
    shipped_delivered=("shipped_delivered", "sum"),
).reset_index()
channel["problem_rate"] = 100 * channel["problem_orders"] / channel["orders"]
channel = channel.sort_values("orders", ascending=False)
cart = filtered.dropna(subset=["itemsincart"]).groupby("itemsincart").agg(
    orders=("order_id", "size"), problem_orders=("problem_order", "sum"),
).reset_index()
cart["problem_rate"] = 100 * cart["problem_orders"] / cart["orders"]
coupon_data = filtered.copy()
coupon_data["coupon_group"] = coupon_data["couponcode"].fillna("").astype(str).str.strip().replace("", "No coupon")
coupons = coupon_data.groupby("coupon_group", as_index=False).agg(
    orders=("order_id", "size"), problem_orders=("problem_order", "sum"),
    average_order_value=("totalprice", "mean"),
)
coupons["problem_rate"] = 100 * coupons["problem_orders"] / coupons["orders"]
coupons = coupons.sort_values("orders", ascending=False)


def monthly_figure(height=205):
    fig = go.Figure(go.Scatter(
        x=monthly["month_start"], y=monthly["orders"], mode="lines+markers",
        fill="tozeroy", fillcolor="rgba(168,85,247,0.14)",
        line=dict(color="#B87AFF", width=3, shape="spline", smoothing=.55),
        marker=dict(color="#EC4899", size=5),
        hovertemplate="%{x|%b %Y}: %{y} orders<extra></extra>", name="Orders",
    ))
    fig.update_layout(xaxis_title="", yaxis_title="Orders")
    return finish_chart(fig, height)


def status_figure(height=205):
    fig = go.Figure(go.Pie(
        labels=statuses["status"], values=statuses["orders"], hole=.60,
        marker=dict(colors=[STATUS_COLORS.get(v, BLUE) for v in statuses["status"]],
                    line=dict(color=PANEL, width=2)),
        textinfo="percent", textposition="inside",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(showlegend=True, legend=dict(orientation="v", x=1.02, y=.5,
        xanchor="left", yanchor="middle", font=dict(family="Segoe UI Semibold, Segoe UI, Arial, sans-serif", color="#DCD5F0", size=12)),
        margin=dict(l=4, r=95, t=10, b=10))
    return finish_chart(fig, height, 95)


@st.dialog("Explore chart details", width="large")
def show_chart_details(section):
    if section == "products":
        st.subheader("Product cancellation & return rates")
        st.plotly_chart(bar_chart(product, "product_name", "problem_rate", percent=True, horizontal=True, height=320), use_container_width=True)
        show_kpi_table(product, percent_columns=("problem_rate",))
        st.caption("Rates account for differences in product order volume.")
    elif section == "monthly":
        st.subheader("Monthly order activity")
        st.plotly_chart(monthly_figure(350), use_container_width=True)
        show_kpi_table(monthly)
    elif section == "status":
        st.subheader("Order outcomes")
        st.plotly_chart(status_figure(330), use_container_width=True)
        show_kpi_table(statuses)
        st.caption("Shipped means dispatched, not necessarily delivered.")
    elif section == "marketing":
        st.subheader("Referral sources: volume and quality")
        l, r = st.columns(2)
        with l:
            st.plotly_chart(bar_chart(channel, "referralsource", "orders", height=300), use_container_width=True)
        with r:
            st.plotly_chart(bar_chart(channel, "referralsource", "problem_rate", percent=True, height=300), use_container_width=True)
        show_kpi_table(channel, percent_columns=("problem_rate",))
        st.caption("These associations do not establish why a referral source has more returns.")
    elif section == "cart":
        st.subheader("Cart size and order outcomes")
        l, r = st.columns(2)
        with l:
            f = bar_chart(cart, "itemsincart", "orders", height=300)
            f.update_xaxes(title_text="Items in Cart", type="category")
            st.plotly_chart(f, use_container_width=True)
        with r:
            f = bar_chart(cart, "itemsincart", "problem_rate", percent=True, height=300)
            f.update_xaxes(title_text="Items in Cart", type="category")
            st.plotly_chart(f, use_container_width=True)
        show_kpi_table(cart, percent_columns=("problem_rate",))
        st.caption("This dataset cannot measure cart abandonment; it records completed order rows, not cart events.")
    elif section == "coupons":
        st.subheader("Coupon groups: volume and outcomes")
        l, r = st.columns(2)
        with l:
            st.plotly_chart(bar_chart(coupons, "coupon_group", "orders", height=300), use_container_width=True)
        with r:
            st.plotly_chart(bar_chart(coupons, "coupon_group", "problem_rate", percent=True, height=300), use_container_width=True)
        show_kpi_table(coupons, money_columns=("average_order_value",), percent_columns=("problem_rate",))
        st.caption("Coupon usage does not prove a promotion caused an order or return.")


@st.dialog("KPI breakdown", width="large")
def show_kpi_breakdown(view):
    if view == "fulfilled":
        st.subheader("Shipped and delivered by product")
        focus = filtered[filtered["shipped_delivered"]]
        summary = focus.groupby(["product_name", "order_status"]).size().unstack(fill_value=0)
        show_kpi_table(summary)
        st.caption("Shipped orders are not necessarily delivered.")
    elif view == "problems":
        show_chart_details_content_products()
    elif view == "value":
        st.subheader("Order value by status")
        t = filtered.groupby("order_status", as_index=False).agg(orders=("order_id", "size"), order_value=("totalprice", "sum"))
        show_kpi_table(t, money_columns=("order_value",))
        st.caption("Order value includes pending, cancelled and returned records; it is not verified revenue.")
    else:
        st.subheader("Orders and value by product")
        t = filtered.groupby("product_name", as_index=False).agg(orders=("order_id", "size"), order_value=("totalprice", "sum"))
        show_kpi_table(t.sort_values("orders", ascending=False), money_columns=("order_value",))


def show_chart_details_content_products():
    st.subheader("Problem orders by product")
    st.plotly_chart(bar_chart(product, "product_name", "problem_rate", percent=True, horizontal=True, height=315), use_container_width=True)
    show_kpi_table(product, percent_columns=("problem_rate",))


def compact_chart(title, section, figure, note):
    # Plotly tooltips remain interactive. The buttons reveal deeper charts or insights.
    with st.container(border=True):
        st.markdown(f'<div class="compact-chart-title">{title}</div>', unsafe_allow_html=True)
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False}, key=f"overview_plot_{section}")
        st.markdown(f'<div class="compact-chart-note">{note}</div>', unsafe_allow_html=True)
        detail_col, insight_col = st.columns(2, gap="small")
        with detail_col:
            if st.button("↗ Details", key=f"detail_{section}", use_container_width=True):
                show_chart_details(section)
        with insight_col:
            if st.button("💡 Insight", key=f"quick_insight_{section}", use_container_width=True):
                show_chart_insight(section)


with overview_tab:
    st.markdown(
        f'<div class="overview-headline"><strong>At a glance:</strong> '
        f'{problem_count:,} of {n_orders:,} orders ({problem_rate:.1f}%) were cancelled or returned. '
        'Select any KPI or chart to investigate.</div>', unsafe_allow_html=True,
    )
    metrics = [
        ("TOTAL ORDERS", f"{n_orders:,}", "Recorded customer orders", "all"),
        ("TOTAL ORDER VALUE", f"${order_value / 1_000_000:.2f}M" if order_value >= 1_000_000 else f"${order_value:,.0f}", "Includes all order statuses", "value"),
        ("SHIPPED / DELIVERED", f"{fulfilled_count:,}", f"{fulfilled_count / n_orders:.1%} of orders", "fulfilled"),
        ("CANCELLED / RETURNED", f"{problem_rate:.1f}%", f"{problem_count:,} orders need attention", "problems"),
    ]
    for col, (label, value, detail, key) in zip(st.columns(4, gap="small"), metrics):
        with col:
            emphasis = " problem" if key == "problems" else ""
            st.markdown(
                f'<div class="kpi-face"><div class="kpi-label">{label}</div>'
                f'<div class="kpi-number{emphasis}">{value}</div>'
                f'<div class="kpi-detail">{detail}</div></div>', unsafe_allow_html=True,
            )
            if st.button("↗ View breakdown", key=f"kpi_{key}", use_container_width=True):
                show_kpi_breakdown(key)

    st.markdown('<div class="overview-section-title">PERFORMANCE AT A GLANCE <span>· Hover for values · Click for deeper analysis</span></div>', unsafe_allow_html=True)
    row1 = st.columns(3, gap="small")
    with row1[0]:
        compact_chart("Product problem rates", "products", bar_chart(product, "product_name", "problem_rate", percent=True, horizontal=True, height=205), "Which products need attention?")
    with row1[1]:
        compact_chart("Monthly order activity", "monthly", monthly_figure(), "How does demand change over time?")
    with row1[2]:
        compact_chart("Order status breakdown", "status", status_figure(), "How many orders reach fulfillment?")
    row2 = st.columns(3, gap="small")
    with row2[0]:
        compact_chart("Marketing referrals", "marketing", bar_chart(channel, "referralsource", "orders", height=205), "Which sources generate the most orders?")
    with row2[1]:
        f = bar_chart(cart, "itemsincart", "orders", height=205)
        f.update_xaxes(title_text="Items in Cart", type="category")
        compact_chart("Shopping cart sizes", "cart", f, "How many items are in each order's cart?")
    with row2[2]:
        compact_chart("Coupon usage", "coupons", bar_chart(coupons, "coupon_group", "orders", height=205), "Which coupon groups appear most often?")

with orders_tab:
    # Keep the individual orders in a table users can open when needed.
    with st.expander("Explore individual order records"):
        preview = filtered.copy()
        preview["date"] = preview["date"].dt.strftime("%Y-%m-%d")
        for column in ("unitprice", "totalprice"):
            preview[column] = preview[column].map(lambda v: f"${v:,.2f}" if pd.notna(v) else "")
        st.dataframe(preview, use_container_width=True, hide_index=True)
    st.caption("Source: cleaned e-commerce orders · Python / Pandas / Plotly / Streamlit")
