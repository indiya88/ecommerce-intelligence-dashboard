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
        font=dict(family="Segoe UI, Arial, sans-serif", color=TEXT, size=12),
        margin=dict(l=22, r=right_margin, t=26, b=42),
        hoverlabel=dict(bgcolor="#221A36", bordercolor=ACCENT, font_color=TEXT),
        bargap=0.62, bargroupgap=0.18,
        legend=dict(font=dict(color=TEXT, size=11), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=BORDER,
                     tickfont=dict(color=MUTED), title_font=dict(color=MUTED))
    fig.update_yaxes(gridcolor="rgba(168,85,247,0.11)", griddash="dot", zeroline=False,
                     tickfont=dict(color=MUTED), title_font=dict(color=MUTED))
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
st.markdown(f"<p style='color:{MUTED};margin-top:-12px'>Find what sells, what gets returned, and which channels bring better orders.</p>", unsafe_allow_html=True)
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

if st.button("💡 Executive Insights · " + str(len(build_insights(filtered))) + " findings", key="open_insights", type="secondary"):
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

# Keep the first screen focused on the most important business questions.
# Detailed charts live in tabs so the dashboard stays readable without endless scrolling.
overview_tab, marketing_tab, cart_tab, coupon_tab, orders_tab = st.tabs(
    ["📊 Overview", "📣 Marketing", "🛒 Shopping Carts", "🏷️ Coupons", "📋 Order Records"]
)

with overview_tab:
    # Let users click a KPI card to see more details about those orders.
    if "kpi_view" not in st.session_state:
        st.session_state.kpi_view = "problems"
    metrics = [
        ("Total orders", f"{n_orders:,}", "all"),
        ("Total order value", f"${order_value:,.2f}", "value"),
        ("Shipped / delivered", f"{fulfilled_count:,}", "fulfilled"),
        ("Cancelled / returned", f"{problem_rate:.1f}%", "problems"),
    ]
    cols = st.columns(4, gap="medium")
    for col, (label, value, key) in zip(cols, metrics):
        with col:
            if st.button(f"{label}\n\n{value}   ↗", key=f"kpi_{key}", use_container_width=True):
                st.session_state.kpi_view = key

    with st.container(border=True):
        view = st.session_state.kpi_view
        if view == "fulfilled":
            st.subheader("Fulfillment detail · shipped and delivered")
            focus = filtered[filtered["shipped_delivered"]]
            summary = focus.groupby(["product_name", "order_status"]).size().unstack(fill_value=0)
            show_kpi_table(summary)
            st.caption("Shipped means dispatched; it does not necessarily mean delivered.")
        elif view == "problems":
            st.subheader("Order problems · which products need attention?")
            summary = filtered.groupby("product_name").agg(
                orders=("order_id", "size"),
                cancelled=("order_status", lambda s: (s == "Cancelled").sum()),
                returned=("order_status", lambda s: (s == "Returned").sum()),
            ).reset_index()
            summary["problem_orders"] = summary["cancelled"] + summary["returned"]
            summary["problem_rate"] = 100 * summary["problem_orders"] / summary["orders"]
            summary = summary.sort_values("problem_rate", ascending=False)
            left, right = st.columns([1.15, 1])
            with left:
                st.plotly_chart(bar_chart(summary, "product_name", "problem_rate", percent=True, horizontal=True), use_container_width=True)
            with right:
                show_kpi_table(summary, percent_columns=("problem_rate",))
            st.caption("Compare rates, not only counts: a product with more orders can naturally have more returns.")
            insight_button("products")
        elif view == "value":
            st.subheader("Order value by status")
            value_table = filtered.groupby("order_status", as_index=False).agg(orders=("order_id", "size"), order_value=("totalprice", "sum"))
            show_kpi_table(value_table, money_columns=("order_value",))
            st.caption("Order value includes pending, cancelled and returned records; it is not verified revenue.")
        else:
            st.subheader("Order overview · products")
            overview = filtered.groupby("product_name", as_index=False).agg(orders=("order_id", "size"), order_value=("totalprice", "sum"))
            show_kpi_table(overview.sort_values("orders", ascending=False), money_columns=("order_value",))

    # Show monthly orders and a doughnut chart of order statuses.
    left, right = st.columns([1.4, 1], gap="medium")
    with left:
        st.subheader("Monthly order activity")
        monthly = filtered.dropna(subset=["month_start"]).groupby("month_start").size().reset_index(name="orders")
        # A translucent violet area with a smooth magenta-purple line.
        fig = go.Figure(go.Scatter(
            x=monthly["month_start"], y=monthly["orders"],
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(168,85,247,0.14)",
            line=dict(color="#B87AFF", width=3, shape="spline", smoothing=0.55),
            marker=dict(color="#EC4899", size=6, line=dict(color="#F3C1F3", width=1)),
            hovertemplate="%{x|%b %Y}: %{y} orders<extra></extra>",
            name="Orders",
        ))
        fig.update_layout(xaxis_title="", yaxis_title="Orders")
        st.plotly_chart(finish_chart(fig), use_container_width=True)
    with right:
        st.subheader("Order status breakdown")
        statuses = filtered["order_status"].value_counts().rename_axis("status").reset_index(name="orders")
        fig = go.Figure(go.Pie(labels=statuses["status"], values=statuses["orders"], hole=.62,
            marker=dict(colors=[STATUS_COLORS.get(s, BLUE) for s in statuses["status"]], line=dict(color=PANEL, width=2)),
            textinfo="percent", textposition="inside",
            hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>"))
        fig.update_layout(showlegend=True, legend=dict(orientation="v", x=1.02, y=.5, xanchor="left", yanchor="middle", font=dict(color=TEXT, size=12)),
            margin=dict(l=10, r=120, t=20, b=15))
        st.plotly_chart(finish_chart(fig, 245, 120), use_container_width=True)

    insight_button("monthly", "💡 Monthly Activity Insight")
    insight_button("status", "💡 Order Status Insight")


with marketing_tab:
    # Compare referral sources by order count and cancellation/return rate.
    st.subheader("Marketing channels · volume versus order quality")
    channel = filtered.groupby("referralsource").agg(
        orders=("order_id", "size"), problem_orders=("problem_order", "sum"),
        shipped_delivered=("shipped_delivered", "sum"),
    ).reset_index()
    channel["problem_rate"] = 100 * channel["problem_orders"] / channel["orders"]
    channel = channel.sort_values("orders", ascending=False)
    left, right = st.columns(2, gap="medium")
    with left:
        st.markdown("**Orders by referral source**")
        st.plotly_chart(bar_chart(channel, "referralsource", "orders"), use_container_width=True)
    with right:
        st.markdown("**Cancelled / returned rate by source**")
        st.plotly_chart(bar_chart(channel.sort_values("problem_rate", ascending=False), "referralsource", "problem_rate", percent=True), use_container_width=True)
    st.caption("These patterns identify where to investigate; they do not establish why a channel has more returns.")
    insight_button("marketing")


with cart_tab:
    # Check whether orders with different cart sizes have different problem rates.
    st.subheader("Shopping cart behaviour")
    cart = filtered.dropna(subset=["itemsincart"]).groupby("itemsincart").agg(
        orders=("order_id", "size"), problem_orders=("problem_order", "sum")
    ).reset_index()
    cart["problem_rate"] = 100 * cart["problem_orders"] / cart["orders"]
    left, right = st.columns(2, gap="medium")
    with left:
        st.markdown("**Orders by cart size**")
        # Label the bottom axis so it's clear these numbers are items, not orders.
        cart_orders_fig = bar_chart(cart, "itemsincart", "orders")
        cart_orders_fig.update_xaxes(title_text="Items in Cart", type="category")
        st.plotly_chart(cart_orders_fig, use_container_width=True)
    with right:
        st.markdown("**Problem rate by cart size**")
        # Use the same cart-size label on the cancellation and return chart.
        cart_problem_fig = bar_chart(cart, "itemsincart", "problem_rate", percent=True)
        cart_problem_fig.update_xaxes(title_text="Items in Cart", type="category")
        st.plotly_chart(cart_problem_fig, use_container_width=True)
    st.caption("Cart size describes recorded items in cart. Without cart events and checkout history, we cannot calculate cart abandonment or prove items were removed.")
    insight_button("cart")


with coupon_tab:
    # Compare coupon codes to see whether some are linked to more problem orders.
    st.subheader("Coupon performance")
    st.caption("Compare orders with different coupon codes, including orders without a coupon.")
    coupon_data = filtered.copy()
    coupon_data["coupon_group"] = coupon_data["couponcode"].fillna("").astype(str).str.strip()
    coupon_data["coupon_group"] = coupon_data["coupon_group"].replace("", "No coupon")
    coupons = coupon_data.groupby("coupon_group", as_index=False).agg(
        orders=("order_id", "size"),
        problem_orders=("problem_order", "sum"),
        average_order_value=("totalprice", "mean"),
    )
    coupons["problem_rate"] = 100 * coupons["problem_orders"] / coupons["orders"]
    coupons = coupons.sort_values("orders", ascending=False)
    left, right = st.columns(2, gap="medium")
    with left:
        st.markdown("**Orders by coupon code**")
        st.plotly_chart(bar_chart(coupons, "coupon_group", "orders"), use_container_width=True)
    with right:
        st.markdown("**Cancellation & return rate by coupon**")
        st.plotly_chart(bar_chart(coupons.sort_values("problem_rate", ascending=False), "coupon_group", "problem_rate", percent=True), use_container_width=True)
    st.caption("Coupon use is associated with these order outcomes, but this data cannot prove a coupon caused a sale or return.")
    insight_button("coupons")


with orders_tab:
    # Keep the individual orders in a table users can open when needed.
    with st.expander("Explore individual order records"):
        preview = filtered.copy()
        preview["date"] = preview["date"].dt.strftime("%Y-%m-%d")
        for column in ("unitprice", "totalprice"):
            preview[column] = preview[column].map(lambda v: f"${v:,.2f}" if pd.notna(v) else "")
        st.dataframe(preview, use_container_width=True, hide_index=True)
    st.caption("Source: cleaned e-commerce orders · Python / Pandas / Plotly / Streamlit")
