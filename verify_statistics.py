
import pandas as pd
from scipy.stats import chi2_contingency

# Load the same cleaned dataset used by the dashboard
df = pd.read_csv("data/cleaned_E-Commerce Orders.csv")

# Standardize the order status values
df["order_status"] = (
    df["order_status"].astype(str).str.strip().str.lower()
)

# Define cancelled or returned orders
df["problem_order"] = df["order_status"].isin(
    ["cancelled", "canceled", "returned"]
)

# Check the dataset first
print("TOTAL ORDERS:", len(df))
print("\nORDER STATUS COUNTS:")
print(df["order_status"].value_counts())

def test_association(column, label):
    # Include missing values as a separate category
    groups = df[column].fillna("Missing").astype(str).str.strip()
    groups = groups.replace("", "Missing")

    table = pd.crosstab(groups, df["problem_order"])

    print(f"\n{'=' * 55}")
    print(label)
    print("=" * 55)

    print("\nCounts by group:")
    print(table)

    rates = df.groupby(groups)["problem_order"].agg(
        orders="count", problem_rate="mean"
    )
    rates["problem_rate"] *= 100

    print("\nProblem rates (%):")
    print(rates.round(2))

    if table.shape[0] < 2 or table.shape[1] < 2:
        print("\nNot enough variation to run this test.")
        return

    chi2, p, dof, expected = chi2_contingency(
        table, correction=False
    )

    print(f"\nChi-square statistic: {chi2:.4f}")
    print(f"Degrees of freedom: {dof}")
    print(f"P-value: {p:.6f}")
    print(f"Smallest expected count: {expected.min():.2f}")

    if (expected < 5).any():
        print("CAUTION: Some expected counts are below 5.")

    if p < 0.05:
        print("RESULT: Evidence of an association.")
    else:
        print("RESULT: No statistically significant association detected.")

# Run the four comparisons
test_association("product_name", "PRODUCT")
test_association("couponcode", "COUPON")
test_association("referralsource", "REFERRAL SOURCE")

# Cart size, based on the existing itemsincart field
test_association("itemsincart", "SHOPPING CART SIZE")
