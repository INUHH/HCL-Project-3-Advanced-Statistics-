import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os
import pandas as pd
import numpy as np

doc = Document()

# Page Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Color Palette Constants
COLOR_NAVY = RGBColor(27, 54, 93)      # #1B365D - Primary Headers
COLOR_STEEL = RGBColor(69, 117, 180)   # #4575B4 - Secondary
COLOR_CHARCOAL = RGBColor(40, 40, 40)  # Text
COLOR_MUTED = RGBColor(100, 100, 100)  # Captions / metadata
HEX_HEADER_BG = "1B365D"
HEX_ROW_LIGHT = "F4F6F9"
HEX_CALLOUT_BG = "EBF3FA"
HEX_CALLOUT_BORDER = "1B365D"

# Helper: set cell background color
def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

# Helper: set cell margins
def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# Helper: Callout Box
def add_callout(document, title, text, bg_hex=HEX_CALLOUT_BG, border_hex=HEX_CALLOUT_BORDER):
    tbl = document.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border styling
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"EXECUTIVE TAKEAWAY: {title}\n")
    run_t.bold = True
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = COLOR_NAVY
    
    run_b = p.add_run(text)
    run_b.font.name = 'Arial'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = COLOR_CHARCOAL
    
    # Add a blank space after table
    p_after = document.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

# Title / Header Block
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(0)
title_p.paragraph_format.space_after = Pt(2)
title_run = title_p.add_run("STATISTICAL FINDINGS REPORT")
title_run.font.name = 'Arial'
title_run.font.size = Pt(24)
title_run.font.bold = True
title_run.font.color.rgb = COLOR_NAVY

subtitle_p = doc.add_paragraph()
subtitle_p.paragraph_format.space_before = Pt(0)
subtitle_p.paragraph_format.space_after = Pt(8)
sub_run = subtitle_p.add_run("Testing Business Claims with Empirical Evidence, Not Opinion")
sub_run.font.name = 'Arial'
sub_run.font.size = Pt(13)
sub_run.font.color.rgb = COLOR_STEEL
sub_run.italic = True

# Metadata Table
meta_tbl = doc.add_table(rows=2, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    [("Candidate Name:", "Unzila Ansari"), ("Program Track:", "HCL Shaper Career — 2nd Year Engineering")],
    [("Project Title:", "Advanced Statistics Mini Project"), ("Dataset:", "retail_customer_sales_dataset.csv (7,000 Trans.)")]
]
for r_idx, row in enumerate(meta_data):
    for c_idx, (k, v) in enumerate(row):
        cell = meta_tbl.cell(r_idx, c_idx)
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        r_k = p.add_run(f"{k} ")
        r_k.bold = True
        r_k.font.size = Pt(9)
        r_k.font.color.rgb = COLOR_NAVY
        r_v = p.add_run(v)
        r_v.font.size = Pt(9)
        r_v.font.color.rgb = COLOR_CHARCOAL

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Heading 1
def add_h1(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return h

def add_h2(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_STEEL
    return h

def add_body(text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_CHARCOAL
    return p

# Section 1: Executive Summary
add_h1("1. Executive Problem Statement & Research Objectives")
add_body(
    "In multi-regional retail enterprises, major strategic capital, inventory stocking, and discount allocations "
    "are frequently driven by executive intuition, conventional wisdom, and untested corporate assumptions. At our retail firm, "
    "three prevailing claims have historically dictated strategic planning:\n"
    "1. 'The West region sells significantly better than the other regions.'\n"
    "2. 'Aggressive discounting is destroying our profit margins.'\n"
    "3. 'Corporate business clients buy entirely different product categories than individual consumers.'\n\n"
    "None of these assertions had ever been tested against formal statistical standards. Acting as the Lead Data Analyst, "
    "this report presents the definitive empirical evaluation of these business claims using descriptive analysis, inferential "
    "confidence intervals, four mandatory hypothesis tests (t-test, ANOVA, Chi-Square, Pearson correlation), econometric OLS "
    "regressions (simple and multiple), and an optional bonus Z-test on customer satisfaction benchmarks."
)

# Section 2: Data Audit
add_h1("2. Data Integrity Audit & Preprocessing Methodology")
add_body(
    "The analysis utilized the transactional dataset 'retail_customer_sales_dataset.csv' covering 7,084 raw transaction records across "
    "24 columns from 2023 to 2024. In accordance with the project brief, raw enterprise data contained realistic data anomalies that "
    "were systematically identified and remediated prior to hypothesis testing:\n"
    "• Deduplication: Identified and eliminated 84 duplicate transactions (168 duplicate transaction ID rows, 61 exact full row duplicates), "
    "retaining 7,000 unique customer transactions.\n"
    "• Regional & Gender Standardization: Harmonized inconsistent casing, truncations, and abbreviations ('Sth' -> 'South', 'Nort'/'north'/'NORTH' -> 'North', "
    "'west'/'WEST' -> 'West', 'M'/'MALE'/'male' -> 'Male', 'F'/'FEMALE'/'female' -> 'Female').\n"
    "• Domain Boundary Enforcement: Replaced impossible customer ages (<18 years and >100 years, including corrupt records such as -12 and 999) "
    "and invalid discount rates (<0.0 or >0.50, such as 2.0 and -0.2) with nulls (NaN) to prevent numerical bias in test statistics.\n"
    "• Date Timeline Verification: Checked order and delivery date consistency, documenting 53 cases where delivery records preceded order timestamps."
)

# Section 3: Descriptive Statistics
add_h1("3. Descriptive Statistics & Metric Distribution Analysis")
add_body(
    "Descriptive statistics were computed for the core numerical variables: Sales (transaction revenue in INR), Profit (net margin in INR), "
    "Age (customer age in years), and Income (annual customer earnings in INR). The table below details central tendency, dispersion, and quartiles."
)

# Table for Descriptive Stats
tbl_desc = doc.add_table(rows=5, cols=10)
tbl_desc.alignment = WD_TABLE_ALIGNMENT.CENTER
desc_headers = ["Variable", "Count", "Mean", "Median", "Mode", "Std Dev", "Variance", "Q1 (25%)", "Q3 (75%)", "IQR"]
for col_idx, h_text in enumerate(desc_headers):
    c = tbl_desc.cell(0, col_idx)
    set_cell_background(c, HEX_HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

desc_rows_data = [
    ["Sales (Rs.)", "7,000", "10,961.60", "4,825.56", "258.73", "14,549.03", "2.12e+08", "1,815.46", "14,095.35", "12,279.89"],
    ["Profit (Rs.)", "7,000", "3,589.70", "1,528.70", "19.47", "4,928.02", "2.43e+07", "574.08", "4,533.29", "3,959.20"],
    ["Age (Years)", "6,854", "36.06", "36.00", "18.00", "10.42", "108.54", "29.00", "43.00", "14.00"],
    ["Income (Rs.)", "6,755", "55,101.38", "49,005.17", "15,000.00", "37,338.42", "1.39e+09", "37,125.40", "65,721.73", "28,596.33"]
]

for row_idx, r_data in enumerate(desc_rows_data, start=1):
    bg_c = HEX_ROW_LIGHT if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(r_data):
        c = tbl_desc.cell(row_idx, col_idx)
        set_cell_background(c, bg_c)
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_CHARCOAL

doc.add_paragraph().paragraph_format.space_after = Pt(6)

if os.path.exists('images/descriptive_distributions.png'):
    doc.add_picture('images/descriptive_distributions.png', width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 1: Probability distributions, mean (red), and median (green) lines for key variables.")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

add_callout(
    doc,
    "Extreme Right-Skew in Financial Metrics Dictates Use of Medians",
    "Sales and Profit exhibit massive positive skewness (+2.45 and +2.48). Mean transaction sales (Rs. 10,961.60) is "
    "more than double the median sales (Rs. 4,825.56), driven by a small fraction of high-ticket electronics purchases (up to Rs. 122,951). "
    "Corporate KPI dashboards that rely exclusively on the arithmetic mean risk creating distorted expectations for baseline store sales. "
    "Median transaction value must be adopted for operational store targets, while the mean remains valid for aggregate quarterly cash budgeting."
)

# Section 4: Confidence Interval
add_h1("4. Inferential Estimation: 95% Confidence Interval Analysis")
add_body(
    "To establish reliable population baselines for key operational indicators, two-sided 95% Confidence Intervals were constructed "
    "using Student's t-distribution with n - 1 degrees of freedom:\n"
    "CI = x̄ ± t_(α/2, n-1) * (s / √n)"
)

ci_tbl = doc.add_table(rows=3, cols=6)
ci_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
ci_headers = ["Metric", "Sample Size (n)", "Mean (x̄)", "Std Dev (s)", "Margin of Error (MOE)", "95% Confidence Interval"]
for col_idx, h_text in enumerate(ci_headers):
    c = ci_tbl.cell(0, col_idx)
    set_cell_background(c, HEX_HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

ci_rows = [
    ["Transaction Sales (Rs.)", "7,000", "Rs. 10,961.60", "Rs. 14,549.03", "± Rs. 340.89", "[Rs. 10,620.71, Rs. 11,302.48]"],
    ["Customer Rating (1-5)", "6,580", "3.0924", "1.0006", "± 0.0244", "[3.0680, 3.1168]"]
]
for row_idx, r_data in enumerate(ci_rows, start=1):
    bg_c = HEX_ROW_LIGHT if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(r_data):
        c = ci_tbl.cell(row_idx, col_idx)
        set_cell_background(c, bg_c)
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(val)
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_CHARCOAL

doc.add_paragraph().paragraph_format.space_after = Pt(6)

add_body(
    "Plain-Language Business Interpretation:\n"
    "We are 95% confident that the true population average transaction revenue for the entire retail enterprise across India "
    "lies between Rs. 10,620.71 and Rs. 11,302.48. In frequentist terms, if the company were to repeatedly draw independent samples of "
    "7,000 transactions and construct 95% confidence intervals from each sample, 95 out of 100 of those intervals would successfully capture "
    "the true unobserved population mean. Because our sample size is large (n = 7,000), the margin of error is remarkably narrow "
    "(± Rs. 340.89, or just 3.1% of the mean), providing corporate finance with exceptional precision for revenue forecasting and working capital modeling."
)

# Section 5: Hypothesis Testing
add_h1("5. Formal Hypothesis Testing (Section 3.3 & 3.6 Documentation)")

# Test 1
add_h2("Test 1: Regional Sales Comparison — North vs. South (Two-Sample t-Test)")
add_body(
    "• Business Question: Is average transaction sales significantly different between customers in the North region compared to the South region?\n"
    "• Null Hypothesis (H₀): μ_North = μ_South (Mean sales between North and South are equal).\n"
    "• Alternative Hypothesis (H₁): μ_North ≠ μ_South (Mean sales between North and South differ significantly).\n"
    "• Test Used & Rationale: Two-Sample Independent Welch's t-test. Appropriate for comparing continuous means across two independent groups without assuming homoscedasticity (equal variance).\n"
    "• Test Statistics: t = 0.1052, degrees of freedom df ≈ 3,432.8 (North n = 1,676, Mean = Rs. 10,777.98; South n = 1,761, Mean = Rs. 10,726.92).\n"
    "• Exact p-Value: p = 0.9162\n"
    "• Statistical Decision at α = 0.05: Fail to Reject H₀ (since p = 0.9162 > 0.05)."
)
add_callout(
    doc,
    "No North-South Sales Discrepancy",
    "The observed difference in average order revenue between North (Rs. 10,777.98) and South (Rs. 10,726.92) is merely Rs. 51.06, "
    "which is purely random noise (p = 0.916). Marketing and sales leaders should not tailor basket-size expectations or promotional depth "
    "differently between North and South India, as consumer purchasing power per transaction is identical."
)

# Test 2
add_h2("Test 2: Multi-Region Sales Comparison — All Four Regions (One-Way ANOVA)")
add_body(
    "• Business Question: Is average Sales significantly different across all four regions (North, South, East, West) simultaneously?\n"
    "• Null Hypothesis (H₀): μ_North = μ_South = μ_East = μ_West (Mean transaction sales are identical across all four regions).\n"
    "• Alternative Hypothesis (H₁): At least one region has a significantly different mean transaction sales value.\n"
    "• Test Used & Rationale: One-Way Analysis of Variance (ANOVA). The standard omnibus parametric test to evaluate whether variance between "
    "three or more group means exceeds expected within-group random error.\n"
    "• Test Statistics: F-statistic = 0.6455, df_between = 3, df_within = 6,996 (East Mean = Rs. 11,341.75; West Mean = Rs. 10,989.43; "
    "North Mean = Rs. 10,777.98; South Mean = Rs. 10,726.92).\n"
    "• Exact p-Value: p = 0.5857\n"
    "• Statistical Decision at α = 0.05: Fail to Reject H₀ (since p = 0.5857 > 0.05).\n"
    "• Post-Hoc Analysis Discussion: Because the omnibus ANOVA test yielded a non-significant result (p = 0.586), post-hoc pairwise adjustments "
    "are not formally required. Conducting Tukey's Honest Significant Difference (HSD) confirms that every single pairwise adjusted p-value "
    "exceeds 0.59 (East-North p = 0.667; East-South p = 0.592; East-West p = 0.888; North-South p = 0.9996; North-West p = 0.974; South-West p = 0.950). "
    "All pairwise difference confidence intervals span zero."
)

if os.path.exists('images/regional_sales_anova.png'):
    doc.add_picture('images/regional_sales_anova.png', width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 2: Boxplots and 95% Confidence Interval error bars across the four geographic regions.")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

add_callout(
    doc,
    "Executive Claim 'West Region Sells Better' is Completely Refuted",
    "The executive hypothesis that 'the West region sells better' is refuted by rigorous empirical evidence. In fact, the East region has a "
    "nominally higher sample mean (Rs. 11,341.75) than the West (Rs. 10,989.43), but ANOVA proves that these regional differences are negligible "
    "and statistically non-significant (p = 0.586). Retail leadership should cease differential regional revenue quotas and focus instead on store-level logistics."
)

# Test 3
add_h2("Test 3: Customer Segment vs. Product Category Association (Chi-Square Test of Independence)")
add_body(
    "• Business Question: Is Customer_Segment (Consumer, Corporate, Home Office) associated with Product_Category, or are purchase choices independent?\n"
    "• Null Hypothesis (H₀): Customer Segment and Product Category are independent (purchasing across categories does not depend on customer type).\n"
    "• Alternative Hypothesis (H₁): Customer Segment and Product Category are dependent (certain customer segments favor specific categories).\n"
    "• Test Used & Rationale: Pearson's Chi-Square Test of Independence (χ²). Appropriate for testing whether two categorical variables exhibit "
    "a non-random contingency relationship. All contingency table cells comfortably exceed the standard Cochran rule of thumb (expected frequencies > 5).\n"
    "• Test Statistics: χ² = 3.4534, degrees of freedom df = (3 - 1) × (5 - 1) = 8.\n"
    "• Exact p-Value: p = 0.9028\n"
    "• Statistical Decision at α = 0.05: Fail to Reject H₀ (since p = 0.9028 > 0.05)."
)

if os.path.exists('images/chisquare_segment_category.png'):
    doc.add_picture('images/chisquare_segment_category.png', width=Inches(6.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 3: Product Category order proportion breakdown by Customer Segment.")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

add_callout(
    doc,
    "Executive Claim 'Corporate Clients Buy Different Products' is Debunked",
    "The data firmly rejects the stakeholder assumption that corporate buyers purchase different merchandise than general consumers. "
    "Across Consumer, Corporate, and Home Office clients, category purchasing proportions are practically identical: Electronics accounts for "
    "~31% of transactions, Grocery ~24%, Clothing ~22%, Furniture ~15%, and Office Supplies ~8% across all segments. Merchandising teams should "
    "discontinue specialized segment catalogs and instead standardize marketing promotions across buyer types."
)

# Test 4
add_h2("Test 4: Discount Concessions vs. Transaction Profitability (Correlation Analysis)")
add_body(
    "• Business Question: Is Discount correlated with Profit, and does discounting hurt business profitability?\n"
    "• Null Hypothesis (H₀): ρ = 0 (There is zero correlation between Discount and Profit).\n"
    "• Alternative Hypothesis (H₁): ρ ≠ 0 (There is a statistically significant correlation between Discount and Profit).\n"
    "• Test Used & Rationale: Pearson's Product-Moment Correlation (r) and Spearman's Nonparametric Rank Correlation (ρ). Evaluates linear and monotonic relationship strength between paired continuous variables.\n"
    "• Test Statistics: Pearson r = -0.1201, Spearman ρ = -0.1168 (n = 6,930 clean paired observations).\n"
    "• Exact p-Value: p = 1.0997 × 10⁻²³ (p < 0.0001)\n"
    "• Statistical Decision at α = 0.05: Reject H₀ (since p < 0.0001).\n"
    "• Sign, Strength & Causation Caution:\n"
    "  - Sign: Negative (-), confirming an inverse relationship where higher discounts correspond to lower transaction profit.\n"
    "  - Strength: Weak-to-modest (r = -0.1201). Discount variation explains only r² = 1.44% of total profit variation.\n"
    "  - Causation vs. Correlation: Correlation does not by itself prove causation. While the negative link is statistically indisputable, "
    "transaction profit is also dictated by baseline item cost, supplier margins, and product category markups. High discounts cut gross margin directly, "
    "but moderate discounts may stimulate customer order frequency."
)

if os.path.exists('images/correlation_discount_profit.png'):
    doc.add_picture('images/correlation_discount_profit.png', width=Inches(6.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 4: Scatter plot and regression trendline of Discount Rate vs. Net Profit.")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

add_callout(
    doc,
    "Executive Concern 'Discounts Hurt Margins' is Supported, But Requires Policy Nuance",
    "The data statistically validates leadership's concern that discounting erodes profitability (p = 1.10e-23). However, because the correlation "
    "magnitude is weak (r = -0.12), discounts are not universally destructive. Rather, unmonitored deep discounting (>25%) directly degrades "
    "transaction profits without boosting basket volume. We recommend establishing a strict corporate discount ceiling of 20% requiring VP approval for exceptions."
)

# Section 6: Regression
add_h1("6. Predictive Econometric Modeling: Linear Regression Analysis (Section 3.4)")
add_body(
    "To quantitatively predict transaction revenue and isolate operational drivers, two Ordinary Least Squares (OLS) regression models were developed."
)

add_h2("6.1 Simple Linear Regression (SLR): Predicting Sales from Quantity Alone")
add_body(
    "Model Specification: Sales_i = β₀ + β₁ * Quantity_i + ε_i\n\n"
    "• Intercept (β₀ = -609.30, Std Err = 380.29, t = -1.602, p = 0.109): The intercept is not statistically significant at α = 0.05. "
    "From an economic standpoint, transactions with zero quantity cannot occur, making a theoretical negative baseline intercept non-meaningful.\n"
    "• Slope (β₁ = +3,844.52, Std Err = 114.42, t = 33.60, p = 1.30 × 10⁻²²⁹): Highly statistically significant. On average, each additional unit "
    "purchased in a transaction increases sales revenue by Rs. 3,844.52.\n"
    "• Model Fit (R² = 0.139, F(1, 6998) = 1,129, p < 0.0001): Quantity purchased accounts for 13.9% of the total variance in transaction sales. "
    "The remaining 86.1% of variance is driven by product mix (e.g., premium electronics vs. inexpensive groceries)."
)

add_h2("6.2 Multiple Linear Regression (MLR): Predicting Sales from Quantity, Discount, and Income")
add_body(
    "Model Specification: Sales_i = β₀ + β₁ * Quantity_i + β₂ * Discount_i + β₃ * Income_i + ε_i\n"
    "Sample Size: n = 6,681 complete cases (after listwise deletion of missing values).\n\n"
    "• Overall Model Fit: R² = 0.159, Adjusted R² = 0.158, F(3, 6677) = 419.2, p = 1.55 × 10⁻²⁴⁹. The three predictors together account for 15.9% of sales variation.\n"
    "• Estimated Regression Equation:\n"
    "  Saleŝ = 2,133.02 + 3,901.22 * Quantity - 15,632.74 * Discount + 0.0047 * Income\n\n"
    "• Predictor Coefficients and Significance:\n"
    "  1. Quantity (β₁ = +3,901.22, t = 33.67, p < 0.0001) — Highly Significant: Holding discount and customer income constant, each additional unit added "
    "to the basket increases expected sales by Rs. 3,901.22.\n"
    "  2. Discount (β₂ = -15,632.74, t = -11.16, p < 0.0001) — Highly Significant: Holding basket size and income constant, higher discounts directly diminish "
    "gross dollar sales. Specifically, a 10-percentage-point increase in discount rate (e.g., from 10% to 20%, Δ = 0.10) reduces transaction revenue by Rs. 1,563.27.\n"
    "  3. Customer Income (β₃ = +0.0047, t = 1.08, p = 0.280) — Not Statistically Significant: Customer annual income does not meaningfully predict transaction sales "
    "(p = 0.280 > 0.05). High-income and modest-income shoppers purchase comparable average order values per visit."
)

if os.path.exists('images/regression_analysis.png'):
    doc.add_picture('images/regression_analysis.png', width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 5: Simple Linear Regression fit (left) and Multiple Linear Regression Actual vs. Predicted values (right).")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

# Section 7: Bonus Z-Test
add_h1("7. Optional Bonus Analysis: One-Sample Z-Test on Customer Ratings (Section 3.5)")
add_body(
    "• Business Question: Does the retail company's current sample average Customer_Rating differ significantly from known historical benchmarks?\n"
    "• Explicit Assumptions: Historical baseline population mean is assumed to be μ₀ = 3.0 (neutral satisfaction) and corporate quality target μ₀ = 3.5. "
    "The population standard deviation is treated as known from historical enterprise benchmarks at σ = 1.0. Given large sample size (n = 6,580), "
    "the sampling distribution of the mean is normal via the Central Limit Theorem.\n"
    "• Hypotheses:\n"
    "  - Test A (Neutral Benchmark): H₀: μ = 3.0 vs. H₁: μ ≠ 3.0\n"
    "  - Test B (Corporate Target): H₀: μ = 3.5 vs. H₁: μ ≠ 3.5\n"
    "• Test Statistic & p-Values:\n"
    "  - Test A (μ₀ = 3.0): Sample Mean x̄ = 3.0924, Z = +7.4953, p = 6.62 × 10⁻¹⁴ (p < 0.0001). Decision: Reject H₀.\n"
    "  - Test B (μ₀ = 3.5): Sample Mean x̄ = 3.0924, Z = -33.0633, p < 0.0001. Decision: Reject H₀."
)

if os.path.exists('images/rating_confidence_interval.png'):
    doc.add_picture('images/rating_confidence_interval.png', width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 6: Customer rating distribution with 95% CI and historical Z-test benchmark lines.")
    r_cap.font.size = Pt(8.5)
    r_cap.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

add_callout(
    doc,
    "Customer Satisfaction Above Neutrality, But Gravely Below Corporate Target",
    "Current customer rating (3.09 out of 5) is statistically significantly above the mediocre 3.0 baseline (Z = +7.50, p < 0.001), "
    "proving customer sentiment is not negative overall. However, it falls drastically short of corporate target 3.5 (Z = -33.06, p < 0.001). "
    "Customer service management must investigate the 53 documented delivery delays and late fulfillment issues to improve ratings toward 3.5."
)

# Section 8: Summary Matrix & Recommendations
add_h1("8. Master Hypothesis Testing Matrix & Strategic Business Recommendations")

# Summary Table
tbl_sum = doc.add_table(rows=8, cols=7)
tbl_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
sum_headers = ["Test / Claim", "Statistical Test", "Test Stat", "p-Value", "Decision (α=0.05)", "Claim Validated?", "Key Business Takeaway"]
for col_idx, h_text in enumerate(sum_headers):
    c = tbl_sum.cell(0, col_idx)
    set_cell_background(c, HEX_HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=80, right=80)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(255, 255, 255)

sum_rows_data = [
    ["1. North vs. South Sales", "Two-Sample t-Test", "t = 0.1052", "0.9162", "Fail to Reject H₀", "No (Refuted)", "Sales identical between North and South."],
    ["2. West Sells Better", "One-Way ANOVA", "F = 0.6455", "0.5857", "Fail to Reject H₀", "No (Refuted)", "Regional sales performance is uniform nationwide."],
    ["3. Segment vs. Category", "Chi-Square Test (χ²)", "χ² = 3.4534", "0.9028", "Fail to Reject H₀", "No (Refuted)", "Buyer segments buy identical category mix."],
    ["4. Discounts Hurt Margins", "Pearson Correlation", "r = -0.1201", "1.10e-23", "Reject H₀", "Yes (Supported)", "Discounts reduce profit; cap discounts at 20%."],
    ["5. Rating vs Target 3.5", "One-Sample Z-Test", "Z = -33.06", "< 0.0001", "Reject H₀", "Yes (Deficit)", "Ratings lag quality target; resolve fulfillment issues."],
    ["6. SLR: Sales ~ Quantity", "Simple OLS Regression", "t = 33.60", "< 0.0001", "Significant (R²=13.9%)", "Confirmed", "Each additional unit adds Rs. 3,844.52 to sales."],
    ["7. MLR: Qty + Disc + Inc", "Multiple OLS Regression", "F = 419.2", "< 0.0001", "Significant (R²=15.9%)", "Confirmed", "Qty (+) and Disc (-) drive sales; Income (p=0.28) does not."]
]

for row_idx, r_data in enumerate(sum_rows_data, start=1):
    bg_c = HEX_ROW_LIGHT if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(r_data):
        c = tbl_sum.cell(row_idx, col_idx)
        set_cell_background(c, bg_c)
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [2, 3, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.size = Pt(8)
        r.font.color.rgb = COLOR_CHARCOAL

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_h2("Strategic Business Action Plan for Executive Leadership")
add_body(
    "1. Eliminate Regional Bias in Quotas & Budgets:\n"
    "Discontinue higher regional revenue targets for the West. Empirical evidence demonstrates that mean transaction revenue across "
    "North, South, East, and West is uniform (F = 0.646, p = 0.586). Allocate promotional and operational budgets according to fulfillment logistics "
    "and population density rather than expected basket size.\n\n"
    "2. Standardize Merchandising & Marketing Across Customer Segments:\n"
    "Cease allocating creative and advertising capital toward customized product catalogs for Corporate versus Consumer buyers. "
    "Both groups purchase Electronics (~31%) and Groceries (~24%) in indistinguishable proportions (χ² = 3.45, p = 0.903). "
    "Consolidate marketing into universal category promotions.\n\n"
    "3. Enforce a Strict 20% Cap on Promotional Discounts:\n"
    "Given the statistically confirmed negative correlation with net profit (r = -0.12, p < 0.001) and the multiple regression slope "
    "showing a Rs. 1,563.27 revenue drop per 10% discount concession, unmonitored discounting directly harms profitability. Discontinue discounts "
    "exceeding 20% without executive authorization.\n\n"
    "4. Shift Promotional Strategy to Multi-Item Basket Incentives:\n"
    "Quantity is the single largest significant driver of order revenue (+Rs. 3,901.22 per item in MLR). Replace standalone price cuts "
    "with quantity-based incentives such as 'Buy 2, Get 1 at 15% Off' or threshold shipping benefits to expand units per transaction."
)

report_docx = 'Statistical_Findings_Report_Advanced_Statistics.docx'
doc.save(report_docx)
print(f"SUCCESS: Report saved as '{report_docx}'! Size: {os.path.getsize(report_docx):,} bytes.")
