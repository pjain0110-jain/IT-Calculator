import streamlit as st

# ---------------------------------------------------
# INCOME TAX CALCULATOR - INDIA
# Built using Streamlit
# ---------------------------------------------------

st.set_page_config(
    page_title="SJ Income Tax Calculator",
    page_icon="💰",
    layout="centered"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("💰 SJ Income Tax Calculator")
st.write("### Income Tax Calculator – India")
st.info("Enter your income details below to estimate your income tax.")

# ---------------------------------------------------
# PERSONAL DETAILS
# ---------------------------------------------------

st.subheader("1. Personal Details")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

with col_p2:
    financial_year = st.selectbox(
        "Financial Year (FY)",
        ["2025-26", "2024-25", "2023-24"],
        index=0,
        help="Select the financial year in which the income was earned."
    )

# Mapping Financial Year to corresponding Assessment Year
fy_to_ay = {
    "2025-26": "2026-27",
    "2024-25": "2025-26",
    "2023-24": "2024-25"
}

with col_p3:
    ay_list = ["2026-27", "2025-26", "2024-25"]
    default_ay_idx = ["2025-26", "2024-25", "2023-24"].index(financial_year)
    assessment_year = st.selectbox(
        "Assessment Year (AY)",
        ay_list,
        index=default_ay_idx,
        help="Assessment Year is the year following the Financial Year.",
        key=f"ay_select_{financial_year}"
    )

# ---------------------------------------------------
# INCOME DETAILS
# ---------------------------------------------------

st.subheader("2. Income Details")

salary = st.number_input(
    "Salary Income (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

house_property = st.number_input(
    "Income from House Property (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

business_income = st.number_input(
    "Business / Profession Income (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

capital_gain = st.number_input(
    "Capital Gains (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

other_income = st.number_input(
    "Income from Other Sources (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

gross_income = (
    salary
    + house_property
    + business_income
    + capital_gain
    + other_income
)

st.write("**Gross Total Income:** ₹", f"{gross_income:,.2f}")

# ---------------------------------------------------
# DEDUCTIONS - OLD REGIME
# ---------------------------------------------------

st.subheader("3. Deductions – Old Regime")

section_80c = st.number_input(
    "Section 80C – Investments / Payments (₹)",
    min_value=0.0,
    max_value=150000.0,
    value=0.0,
    step=1000.0
)

section_80d = st.number_input(
    "Section 80D – Medical Insurance (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

section_80g = st.number_input(
    "Section 80G – Donations (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

other_deductions = st.number_input(
    "Other Eligible Deductions (₹)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

total_deductions = (
    section_80c
    + section_80d
    + section_80g
    + other_deductions
)

# ---------------------------------------------------
# STANDARD DEDUCTION
# ---------------------------------------------------

st.subheader("4. Standard Deduction")

standard_deduction_old = 50000
standard_deduction_new = 50000 if financial_year == "2023-24" else 75000

st.write(
    f"Old Regime Standard Deduction: ₹{standard_deduction_old:,.0f}"
)

st.write(
    f"New Regime Standard Deduction ({financial_year}): ₹{standard_deduction_new:,.0f}"
)

# ---------------------------------------------------
# TAX CALCULATION FUNCTION
# ---------------------------------------------------

def calculate_old_regime(taxable_income, age=25):
    """
    Simplified old-regime slab calculation considering age exemption.
    """

    tax = 0.0

    # Basic exemption based on age
    if age >= 80:
        exemption = 500000.0  # Super senior citizen
    elif age >= 60:
        exemption = 300000.0  # Senior citizen
    else:
        exemption = 250000.0  # Individual < 60 years

    # Up to basic exemption
    if taxable_income <= exemption:
        tax = 0.0

    # Exemption to ₹5 lakh
    elif taxable_income <= 500000:
        tax = (taxable_income - exemption) * 0.05

    # ₹5 lakh – ₹10 lakh
    elif taxable_income <= 1000000:
        tax = (500000 - exemption) * 0.05 + (taxable_income - 500000) * 0.20

    # Above ₹10 lakh
    else:
        tax = (
            (500000 - exemption) * 0.05
            + 500000 * 0.20
            + (taxable_income - 1000000) * 0.30
        )

    # Simplified rebate under Section 87A (taxable income up to ₹5 lakh)
    if taxable_income <= 500000:
        tax = 0.0

    return tax


def calculate_new_regime(taxable_income, fy="2025-26"):
    """
    Simplified new-regime slab calculation based on Financial Year.
    """

    tax = 0.0

    if fy == "2024-25":
        # FY 2024-25 (AY 2025-26) slabs
        if taxable_income <= 300000:
            tax = 0.0
        elif taxable_income <= 700000:
            tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 1000000:
            tax = 20000.0 + (taxable_income - 700000) * 0.10
        elif taxable_income <= 1200000:
            tax = 50000.0 + (taxable_income - 1000000) * 0.15
        elif taxable_income <= 1500000:
            tax = 80000.0 + (taxable_income - 1200000) * 0.20
        else:
            tax = 140000.0 + (taxable_income - 1500000) * 0.30

        # Section 87A rebate for FY 2024-25 (Taxable income up to ₹7 lakh)
        if taxable_income <= 700000:
            tax = 0.0

    elif fy == "2023-24":
        # FY 2023-24 (AY 2024-25) slabs
        if taxable_income <= 300000:
            tax = 0.0
        elif taxable_income <= 600000:
            tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 900000:
            tax = 15000.0 + (taxable_income - 600000) * 0.10
        elif taxable_income <= 1200000:
            tax = 45000.0 + (taxable_income - 900000) * 0.15
        elif taxable_income <= 1500000:
            tax = 90000.0 + (taxable_income - 1200000) * 0.20
        else:
            tax = 150000.0 + (taxable_income - 1500000) * 0.30

        # Section 87A rebate
        if taxable_income <= 700000:
            tax = 0.0

    else:
        # FY 2025-26 (AY 2026-27) slabs
        if taxable_income <= 400000:
            tax = 0.0
        elif taxable_income <= 800000:
            tax = (taxable_income - 400000) * 0.05
        elif taxable_income <= 1200000:
            tax = 20000.0 + (taxable_income - 800000) * 0.10
        elif taxable_income <= 1600000:
            tax = 60000.0 + (taxable_income - 1200000) * 0.15
        elif taxable_income <= 2000000:
            tax = 120000.0 + (taxable_income - 1600000) * 0.20
        elif taxable_income <= 2400000:
            tax = 200000.0 + (taxable_income - 2000000) * 0.25
        else:
            tax = 300000.0 + (taxable_income - 2400000) * 0.30

        # Simplified Section 87A rebate for FY 2025-26
        if taxable_income <= 1200000:
            tax = 0.0

    return tax


# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

old_regime_taxable_income = max(
    0,
    gross_income
    - standard_deduction_old
    - total_deductions
)

new_regime_taxable_income = max(
    0,
    gross_income
    - standard_deduction_new
)

old_tax = calculate_old_regime(
    old_regime_taxable_income,
    age=age
)

new_tax = calculate_new_regime(
    new_regime_taxable_income,
    fy=financial_year
)

# Health & Education Cess = 4%
old_cess = old_tax * 0.04
new_cess = new_tax * 0.04

old_total_tax = old_tax + old_cess
new_total_tax = new_tax + new_cess

# ---------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------

st.subheader("5. Tax Calculation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧾 Old Regime")

    st.write(
        "Taxable Income:",
        f"₹{old_regime_taxable_income:,.2f}"
    )

    st.write(
        "Income Tax:",
        f"₹{old_tax:,.2f}"
    )

    st.write(
        "4% Cess:",
        f"₹{old_cess:,.2f}"
    )

    st.metric(
        "Total Tax",
        f"₹{old_total_tax:,.2f}"
    )

with col2:
    st.markdown("### 🆕 New Regime")

    st.write(
        "Taxable Income:",
        f"₹{new_regime_taxable_income:,.2f}"
    )

    st.write(
        "Income Tax:",
        f"₹{new_tax:,.2f}"
    )

    st.write(
        "4% Cess:",
        f"₹{new_cess:,.2f}"
    )

    st.metric(
        "Total Tax",
        f"₹{new_total_tax:,.2f}"
    )

# ---------------------------------------------------
# COMPARISON
# ---------------------------------------------------

st.subheader("6. Regime Comparison")

difference = abs(old_total_tax - new_total_tax)

if old_total_tax < new_total_tax:
    st.success(
        f"💡 **Old Regime is more beneficial!** You save "
        f"₹{difference:,.2f} compared to the New Regime."
    )

elif new_total_tax < old_total_tax:
    st.success(
        f"💡 **New Regime is more beneficial!** You save "
        f"₹{difference:,.2f} compared to the Old Regime."
    )

else:
    st.info("Estimated tax is the same under both regimes.")

# ---------------------------------------------------
# TAX SUMMARY
# ---------------------------------------------------

st.subheader("7. Summary")

summary_data = {
    "Particulars": [
        "Financial Year (FY)",
        "Assessment Year (AY)",
        "Gross Total Income",
        "Old Regime Taxable Income",
        "Old Regime Tax",
        "Old Regime Cess (4%)",
        "Old Regime Total Tax",
        "New Regime Taxable Income",
        "New Regime Tax",
        "New Regime Cess (4%)",
        "New Regime Total Tax"
    ],

    "Amount / Details": [
        financial_year,
        assessment_year,
        f"₹{gross_income:,.2f}",
        f"₹{old_regime_taxable_income:,.2f}",
        f"₹{old_tax:,.2f}",
        f"₹{old_cess:,.2f}",
        f"₹{old_total_tax:,.2f}",
        f"₹{new_regime_taxable_income:,.2f}",
        f"₹{new_tax:,.2f}",
        f"₹{new_cess:,.2f}",
        f"₹{new_total_tax:,.2f}"
    ]
}

st.table(summary_data)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "SJ Income Tax Calculator | Educational purpose only"
)

st.warning(
    "This calculator is a simplified educational model. "
    "Actual tax liability may differ because of special tax rates, "
    "capital gains, surcharge, marginal relief, deductions, "
    "rebates and other provisions."
)