"""Find useful patterns in the orders using Python, without an AI API."""
import pandas as pd
from scipy.stats import chi2_contingency



def association_note(data: pd.DataFrame, group_column: str) -> str:
    """Explain a chi-square comparison using only the current selection."""
    if data.empty or group_column not in data.columns:
        return "There aren't enough orders to make this comparison. Try widening your filters."
    if group_column == "coupon_used":
        groups = data[group_column].map({True: "Coupon used", False: "No coupon"}).astype("string")
    else:
        groups = data[group_column].astype("string").fillna("Missing").str.strip().replace("", "Missing")
        if group_column == "couponcode":
            groups = groups.replace("Missing", "No coupon")
    outcome = data["problem_order"].fillna(False).astype(bool)
    contingency = pd.crosstab(groups, outcome)
    if contingency.shape[0] < 2:
        return "Only one group is selected, so there's nothing to compare."
    if contingency.shape[1] < 2:
        return "Every selected order has the same outcome, so there's nothing to compare."
    _, p_value, _, expected = chi2_contingency(contingency, correction=False)
    if (expected < 5).any():
        return "There aren't enough orders in some groups to test this reliably. Try widening your filters."
    if p_value < 0.05:
        return (f"The differences are larger than we'd usually expect by chance (p = {p_value:.3f}). "
                "It's worth looking more closely, but this doesn't tell us why they differ.")
    return (f"The differences could easily occur by chance (p = {p_value:.3f}). "
            "We don't have enough evidence to say these groups have different cancellation and return rates.")


def build_insights(data: pd.DataFrame) -> list[dict]:
    """Generate business-focused findings for the current dashboard filters."""
    if data.empty:
        return []
    findings = []
    n = len(data)
    cancelled = int(data["order_status"].eq("Cancelled").sum())
    returned = int(data["order_status"].eq("Returned").sum())
    problem_n = int(data["problem_order"].sum())
    rate = 100 * problem_n / n
    approximate = f" That's about {round(rate / 10):d} in every 10 orders." if 35 <= rate <= 45 else ""
    findings.append({
        "title": "Cancellation and return overview",
        "finding": (f"{problem_n:,} of {n:,} orders ({rate:.1f}%) were cancelled or returned: "
                    f"{cancelled:,} cancellations and {returned:,} returns.{approximate}"),
        "action": "Find out why customers are cancelling or returning orders before spending more to attract new ones.",
    })

    products = data.groupby("product_name", dropna=True).agg(
        orders=("order_id", "size"), problems=("problem_order", "sum")
    ).reset_index()
    if not products.empty:
        products["rate"] = 100 * products["problems"] / products["orders"]
        leaders = products.sort_values(["problems", "product_name"], ascending=[False, True]).head(3)
        names = [f"{r.product_name} ({int(r.problems)})" for r in leaders.itertuples()]
        if len(names) == 1:
            finding = (f"All {int(leaders.iloc[0]['problems'])} cancelled or returned orders "
                       f"in this selection are for {leaders.iloc[0]['product_name']}.")
        else:
            first = leaders.iloc[0]
            rest = " and ".join(names[1:])
            finding = (f"{first['product_name']} has the most cancelled or returned orders "
                       f"({int(first['problems'])}), followed by {rest}.")
        findings.append({
            "title": "Products with the most cancellations and returns",
            "finding": finding,
            "action": "Review the individual orders for these products and look for recurring issues.",
        })
        minimum = max(10, int(n * .02))
        eligible = products[products["orders"] >= minimum]
        if len(eligible) > 1:
            highest = eligible.sort_values(["rate", "orders"], ascending=[False, False]).iloc[0]
            finding = (f"{highest['product_name']} has the highest cancellation and return rate at "
                       f"{highest['rate']:.1f}% ({int(highest['problems'])} of {int(highest['orders'])} orders).")
            if len(eligible) > 1:
                finding += " " + association_note(data, "product_name")
            findings.append({
                "title": "Highest cancellation and return rate",
                "finding": finding,
                "action": "Compare cancellation and return reasons, product descriptions and delivery times across products.",
            })

    channels = data.groupby("referralsource", dropna=True).agg(
        orders=("order_id", "size"), problems=("problem_order", "sum")
    ).reset_index()
    if not channels.empty:
        leader = channels.sort_values("orders", ascending=False).iloc[0]
        findings.append({
            "title": "Where most orders come from",
            "finding": (f"{leader['referralsource']} brings in the most orders: "
                        f"{int(leader['orders']):,}, or {leader['orders'] / n * 100:.1f}% of the selected orders."),
            "action": "Consider cancellation and return rates alongside order volume before changing marketing spending.",
        })
        minimum = max(10, int(n * .02))
        eligible = channels[channels["orders"] >= minimum].copy()
        if len(eligible) > 1:
            eligible["rate"] = 100 * eligible["problems"] / eligible["orders"]
            best = eligible.sort_values("rate").iloc[0]
            worst = eligible.sort_values("rate", ascending=False).iloc[0]
            findings.append({
                "title": "Which channel has the fewest cancellations and returns",
                "finding": (f"{best['referralsource']} has the lowest cancellation and return rate "
                            f"({best['rate']:.1f}%). {worst['referralsource']} has the highest "
                            f"({worst['rate']:.1f}%). " + association_note(data, "referralsource")),
                "action": "Before reallocating the marketing budget, check whether the channels are selling different products.",
            })

    carts = data.dropna(subset=["itemsincart"]).groupby("itemsincart").agg(
        orders=("order_id", "size"), problems=("problem_order", "sum")
    ).reset_index()
    minimum = max(10, int(n * .02))
    eligible = carts[carts["orders"] >= minimum].copy()
    if not eligible.empty:
        eligible["rate"] = 100 * eligible["problems"] / eligible["orders"]
        highest = eligible.sort_values("rate", ascending=False).iloc[0]
        size = int(highest["itemsincart"])
        findings.append({
            "title": "Cart size",
            "finding": (f"Orders with {size} {'item' if size == 1 else 'items'} in the cart have the "
                        f"highest cancellation and return rate among cart sizes with at least {minimum} orders "
                        f"({highest['rate']:.1f}%, across {int(highest['orders'])} orders). "
                        + (association_note(data, "itemsincart") if len(eligible) > 1 else "")),
            "action": "Review the products in these carts. This data doesn't include abandoned carts.",
        })

    coupon_data = data.copy()
    coupon_data["coupon_group"] = coupon_data["couponcode"].fillna("").astype(str).str.strip().replace("", "No coupon")
    coupon_summary = coupon_data.groupby("coupon_group").agg(
        orders=("order_id", "size"), problems=("problem_order", "sum")
    ).reset_index()
    coupon_summary["rate"] = 100 * coupon_summary["problems"] / coupon_summary["orders"]
    with_coupon = coupon_data["coupon_group"].ne("No coupon")
    if with_coupon.any() and (~with_coupon).any():
        coupon_rate = 100 * coupon_data.loc[with_coupon, "problem_order"].mean()
        no_coupon_rate = 100 * coupon_data.loc[~with_coupon, "problem_order"].mean()
        findings.append({
            "title": "Do coupons make a difference?",
            "finding": (f"Orders with a coupon were cancelled or returned {coupon_rate:.1f}% of the time, "
                        f"compared with {no_coupon_rate:.1f}% without one. "
                        + association_note(data, "coupon_used")),
            "action": "Check whether coupon orders include different products before changing promotions.",
        })
    eligible_codes = coupon_summary[
        (coupon_summary["coupon_group"] != "No coupon") & (coupon_summary["orders"] >= minimum)
    ]
    if not eligible_codes.empty:
        highest = eligible_codes.sort_values(["rate", "orders"], ascending=[False, False]).iloc[0]
        findings.append({
            "title": "Coupon code with the highest rate",
            "finding": (f"{highest['coupon_group']} has the highest cancellation and return rate among coupon codes "
                        f"with at least {minimum} orders: {highest['rate']:.1f}% "
                        f"({int(highest['problems'])} of {int(highest['orders'])} orders)."),
            "action": "Look at which products and customers are using this code.",
        })

    pending = data.loc[data["order_status"].eq("Pending")]
    if not pending.empty:
        oldest = pd.to_datetime(pending["date"], errors="coerce").min()
        date_note = f" The earliest pending order is from {oldest:%B} {oldest.day}, {oldest:%Y}." if pd.notna(oldest) else ""
        findings.append({
            "title": "Pending orders to check",
            "finding": (f"{len(pending):,} orders ({len(pending) / n:.1%}) are marked Pending."
                        + date_note),
            "action": "Confirm whether these orders are still open or whether their statuses need updating.",
        })
    return findings
