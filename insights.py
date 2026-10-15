"""Find useful patterns in the orders using Python, without an AI API."""
import pandas as pd


def build_insights(data: pd.DataFrame) -> list[dict]:
    """Look at the selected orders and write simple business findings."""
    if data.empty:
        return []
    # Start a list to hold the findings we want to show.
    findings = []
    n = len(data)
    problem_n = int(data['problem_order'].sum())
    rate = problem_n / n * 100
    findings.append({
        'title': 'Order quality',
        'finding': f'{problem_n:,} of {n:,} orders ({rate:.1f}%) are cancelled or returned. Of those, {int(data["order_status"].eq("Cancelled").sum()):,} were cancelled and {int(data["order_status"].eq("Returned").sum()):,} were returned.',
        'action': 'Review the reasons for cancellations and returns before increasing acquisition spending.',
    })

    # Compare products to see which ones have the most problem orders.
    products = data.groupby('product_name', dropna=True).agg(
        orders=('order_id', 'size'), problems=('problem_order', 'sum'),
        cancellations=('order_status', lambda x: x.eq('Cancelled').sum()),
        returns=('order_status', lambda x: x.eq('Returned').sum()),
    ).reset_index()
    products['rate'] = products['problems'] / products['orders'] * 100
    if not products.empty:
        highest_count = products.sort_values(['problems', 'product_name'], ascending=[False, True]).iloc[0]
        findings.append({
            'title': 'Most affected product',
            'finding': f"{highest_count['product_name']} has the most cancelled/returned orders ({int(highest_count['problems']):,} out of {int(highest_count['orders']):,}; {highest_count['rate']:.1f}%).",
            'action': 'Check product-specific cancellation and return reasons; count alone may reflect higher sales volume.',
        })
        # Find the three products with the most cancellations and returns.
        leaders = products.sort_values(['problems', 'product_name'], ascending=[False, True]).head(3)
        details = '; '.join(
            f"{r.product_name}: {int(r.problems)} problem orders ({int(r.cancellations)} cancelled, {int(r.returns)} returned; {r.rate:.1f}% of its orders)"
            for r in leaders.itertuples()
        )
        findings.append({
            'title': 'Products responsible for the most problem orders',
            'finding': details + '.',
            'action': 'Prioritize products by both problem volume and problem rate; inspect the individual orders below.',
        })
        # Ignore very small groups so their percentages are less misleading.
        minimum = max(10, int(n * .02))
        eligible = products[products['orders'] >= minimum]
        if len(eligible) > 1:
            worst = eligible.sort_values(['rate', 'orders'], ascending=[False, False]).iloc[0]
            findings.append({
                'title': 'Highest product problem rate',
                'finding': f"{worst['product_name']} has the highest problem rate among products with at least {minimum} orders: {worst['rate']:.1f}% ({int(worst['problems'])}/{int(worst['orders'])}).",
                'action': 'Compare product descriptions, quality issues, and fulfillment practices; the data does not identify the cause.',
            })

    # Check which referral sources bring orders and how often they have problems.
    channels = data.groupby('referralsource', dropna=True).agg(
        orders=('order_id', 'size'), problems=('problem_order', 'sum')
    ).reset_index()
    if not channels.empty:
        leader = channels.sort_values('orders', ascending=False).iloc[0]
        findings.append({
            'title': 'Top acquisition source',
            'finding': f"{leader['referralsource']} generates the most orders ({int(leader['orders']):,}, {leader['orders'] / n * 100:.1f}% of the selection).",
            'action': 'Compare channel quality as well as volume before deciding where to invest marketing budget.',
        })
        minimum = max(10, int(n * .02))
        eligible = channels[channels['orders'] >= minimum].copy()
        if len(eligible) > 1:
            eligible['rate'] = eligible['problems'] / eligible['orders'] * 100
            best = eligible.sort_values('rate').iloc[0]
            worst = eligible.sort_values('rate', ascending=False).iloc[0]
            findings.append({
                'title': 'Marketing channel quality',
                'finding': f"{best['referralsource']} has the lowest cancellation/return rate ({best['rate']:.1f}%), versus {worst['referralsource']} at {worst['rate']:.1f}% (minimum {minimum} orders per channel).",
                'action': 'Investigate product mix and promotional differences before attributing the gap to the referral source.',
            })

    # Compare cart sizes to see whether some have more order problems.
    carts = data.dropna(subset=['itemsincart']).groupby('itemsincart').agg(
        orders=('order_id', 'size'), problems=('problem_order', 'sum')
    ).reset_index()
    eligible = carts[carts['orders'] >= max(10, int(n * .02))].copy()
    if len(eligible) > 1:
        eligible['rate'] = eligible['problems'] / eligible['orders'] * 100
        high = eligible.sort_values('rate', ascending=False).iloc[0]
        findings.append({
            'title': 'Cart-size pattern',
            'finding': f"Orders with {int(high['itemsincart'])} items in cart have the highest cancellation/return rate among sufficiently represented cart sizes ({high['rate']:.1f}%, {int(high['orders'])} orders).",
            'action': 'Explore whether cart size is associated with order problems; cart abandonment cannot be inferred.',
        })

    # Compare orders with and without coupons, then find which code has the highest problem rate.
    coupon_data = data.copy()
    coupon_data['coupon_group'] = coupon_data['couponcode'].fillna('').astype(str).str.strip().replace('', 'No coupon')
    coupon_summary = coupon_data.groupby('coupon_group').agg(
        orders=('order_id', 'size'), problems=('problem_order', 'sum')
    ).reset_index()
    coupon_summary['rate'] = 100 * coupon_summary['problems'] / coupon_summary['orders']
    with_coupon = coupon_data['coupon_group'].ne('No coupon')
    if with_coupon.any() and (~with_coupon).any():
        coupon_rate = 100 * coupon_data.loc[with_coupon, 'problem_order'].mean()
        no_coupon_rate = 100 * coupon_data.loc[~with_coupon, 'problem_order'].mean()
        findings.append({
            'title': 'Do coupon orders have more problems?',
            'finding': f"Orders with a coupon have a {coupon_rate:.1f}% cancellation/return rate, compared with {no_coupon_rate:.1f}% for orders without one.",
            'action': 'Compare the types of products bought with coupons before deciding whether promotions affect order quality.',
        })
    coupon_codes = coupon_summary[coupon_summary['coupon_group'] != 'No coupon']
    minimum = max(10, int(n * .02))
    eligible_codes = coupon_codes[coupon_codes['orders'] >= minimum]
    if not eligible_codes.empty:
        highest = eligible_codes.sort_values(['rate', 'orders'], ascending=[False, False]).iloc[0]
        findings.append({
            'title': 'Coupon code to review',
            'finding': f"{highest['coupon_group']} has the highest cancellation/return rate among coupon codes with at least {minimum} orders: {highest['rate']:.1f}% ({int(highest['problems'])} of {int(highest['orders'])} orders).",
            'action': 'Check the products and customers using this code; the dataset does not show whether the discount caused the outcome.',
        })

    return findings
