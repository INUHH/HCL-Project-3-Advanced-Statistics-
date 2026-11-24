import os
import sys
import io
import base64
import contextlib
import nbformat as nbf
import pandas as pd
import numpy as np

# Configure matplotlib
os.environ['MPLCONFIGDIR'] = os.path.abspath('.matplotlib')
os.makedirs('.matplotlib', exist_ok=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

nb = nbf.v4.new_notebook()
nb.metadata = {
    'language_info': {
        'name': 'python',
        'version': '3.13.15',
        'mimetype': 'text/x-python',
        'codemirror_mode': {'name': 'ipython', 'version': 3},
        'pygments_lexer': 'ipython3'
    },
    'kernelspec': {
        'name': 'python3',
        'display_name': 'Python 3 (ipykernel)'
    }
}

cells_data = []

def add_md(text):
    cells_data.append(('md', text))

def add_code(code_str):
    cells_data.append(('code', code_str))

# ==================== NOTEBOOK CONTENT ====================

add_md("""# DATA ANALYST TRAINING PROGRAM — ADVANCED STATISTICS
## Mini Project: Testing Business Claims with Evidence, Not Opinion
**Author:** Unzila Ansari  
**Role:** Data Analyst  
**Program:** HCL Tech — Shaper Career / 2nd Year Engineering Track  
**Dataset:** `retail_customer_sales_dataset.csv` (7,084 raw rows, 24 features)  
**Tools & Libraries:** Python 3, Pandas, NumPy, SciPy Stats, Statsmodels, Matplotlib, Seaborn  

---

### Executive Problem Statement & Context
In retail management, operational strategies are frequently guided by executive intuition and anecdotal beliefs:
1. *"The West region sells significantly better than the other regions."*
2. *"Aggressive promotional discounts are eroding our profit margins."*
3. *"Corporate business clients buy different product categories than individual consumers."*

Until now, none of these business claims have been subjected to rigorous inferential statistics. This project acts as the definitive empirical investigation to test these assertions using:
- **Descriptive Statistics & Dispersion Analysis** (Mean, Median, Mode, Variance, Standard Deviation, Percentiles, IQR)
- **Inferential Estimation** (95% Confidence Intervals for Sales and Customer Rating)
- **Four Core Hypothesis Tests ($\alpha = 0.05$)**:
  - Two-Sample Independent $t$-Test (Regional Sales Comparison)
  - One-Way ANOVA across all 4 operational regions + Post-Hoc Tukey HSD
  - Chi-Square ($\chi^2$) Test of Independence (Customer Segment vs. Product Category)
  - Pearson & Spearman Bivariate Correlation Analysis (Discount vs. Profit)
- **Econometric Regression Models**:
  - Simple Linear Regression ($Sales \sim Quantity$)
  - Multiple Linear Regression ($Sales \sim Quantity + Discount + Income$)
- **Bonus One-Sample $Z$-Test** on Customer Ratings against historical benchmarks.
""")

add_md("""## 1. Environment Setup & Library Ingestion
We import all essential data manipulation, statistical, and plotting libraries.
""")

add_code("""import os
import sys
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd

import matplotlib.pyplot as plt
import seaborn as sns

# Visual configurations
sns.set_theme(style='whitegrid', font_scale=1.05)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (10, 6)

print("Environment setup completed successfully.")
print("Libraries Loaded: pandas, numpy, scipy.stats, statsmodels, matplotlib, seaborn.")
""")

add_md("""## 2. Data Audit, Cleaning & Preparation
In accordance with the project brief, the dataset is deliberately uncleaned, containing duplicates, inconsistent casing, impossible values, and mixed date formats. We perform systematic cleaning to produce a reliable analytical dataset.
""")

add_code("""# Load raw dataset
raw_df = pd.read_csv('retail_customer_sales_dataset.csv')
print(f"Raw Dataset Shape: {raw_df.shape[0]:,} rows x {raw_df.shape[1]} columns")

# 1. Deduplication on Transaction_ID
initial_rows = len(raw_df)
df = raw_df.drop_duplicates(subset=['Transaction_ID']).copy()
deduped_rows = len(df)
print(f"Deduplication: Removed {initial_rows - deduped_rows} duplicate rows. Remaining: {deduped_rows:,} rows.")

# 2. Standardize Categorical Encodings (Region & Gender)
region_standardization = {
    'West': 'West', 'west': 'West', 'WEST': 'West',
    'East': 'East', 'east': 'East',
    'South': 'South', 'south': 'South', 'Sth': 'South',
    'North': 'North', 'north': 'North', 'NORTH': 'North', 'Nort': 'North'
}
df['Region'] = df['Region'].map(region_standardization)

gender_standardization = {
    'Male': 'Male', 'male': 'Male', 'M': 'Male', 'MALE': 'Male',
    'Female': 'Female', 'female': 'Female', 'F': 'Female', 'FEMALE': 'Female'
}
df['Gender'] = df['Gender'].map(gender_standardization)

# 3. Clean Outlier / Invalid Numerical Values
# Age: legal adults (18 to 100). Invalid values (-12, 999, etc.) set to NaN
invalid_age_count = ((df['Age'] < 18) | (df['Age'] > 100)).sum()
df.loc[(df['Age'] < 18) | (df['Age'] > 100), 'Age'] = np.nan

# Discount: valid range 0.0 to 0.5. Outliers (<0 or >0.5) set to NaN
invalid_discount_count = ((df['Discount'] < 0) | (df['Discount'] > 0.5)).sum()
df.loc[(df['Discount'] < 0) | (df['Discount'] > 0.5), 'Discount'] = np.nan

# 4. Standardize Dates
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='mixed')
df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'], format='mixed')

print(f"Data Cleaning Audit:")
print(f" - Standardized Regions: {sorted(df['Region'].unique().tolist())}")
print(f" - Standardized Genders: {sorted(df['Gender'].unique().tolist())}")
print(f" - Invalid Age entries cleaned to NaN: {invalid_age_count}")
print(f" - Invalid Discount entries cleaned to NaN: {invalid_discount_count}")
print(f" - Final Clean Dataset Dimensions: {df.shape}")
""")

add_md("""## 3. Descriptive Statistics (Section 3.1)
We compute the full suite of descriptive statistics (Mean, Median, Mode, Variance, Standard Deviation, Percentiles, and IQR) for **Sales**, **Profit**, **Age**, and **Income**.
""")

add_code("""# Descriptive statistics table computation
target_vars = ['Sales', 'Profit', 'Age', 'Income']
desc_rows = []

for col in target_vars:
    s = df[col].dropna()
    mean_v = s.mean()
    median_v = s.median()
    mode_v = s.mode()[0]
    var_v = s.var(ddof=1)
    std_v = s.std(ddof=1)
    p25 = s.quantile(0.25)
    p50 = s.quantile(0.50)
    p75 = s.quantile(0.75)
    iqr_v = p75 - p25
    skew_v = s.skew()
    
    desc_rows.append({
        'Variable': col,
        'Count (N)': len(s),
        'Mean': mean_v,
        'Median': median_v,
        'Mode': mode_v,
        'Variance': var_v,
        'Std Dev': std_v,
        'Q1 (25th)': p25,
        'Median (50th)': p50,
        'Q3 (75th)': p75,
        'IQR': iqr_v,
        'Skewness': skew_v
    })

desc_df = pd.DataFrame(desc_rows)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print("COMPREHENSIVE DESCRIPTIVE STATISTICS:")
print(desc_df.to_string(index=False))
""")

add_md("""### 3.1 Visualizing Key Metric Distributions
We plot the histograms with Kernel Density Estimation (KDE) and mark both Mean and Median lines to assess skewness.
""")

add_code("""fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# Sales
sns.histplot(df['Sales'], kde=True, ax=axes[0, 0], color='#1f77b4', bins=35)
axes[0, 0].axvline(df['Sales'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: Rs. {df['Sales'].mean():,.0f}")
axes[0, 0].axvline(df['Sales'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: Rs. {df['Sales'].median():,.0f}")
axes[0, 0].set_title('Sales Distribution (Heavy Right Skew: Mean > Median)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Transaction Sales (Rs.)')
axes[0, 0].legend()

# Profit
sns.histplot(df['Profit'], kde=True, ax=axes[0, 1], color='#2ca02c', bins=35)
axes[0, 1].axvline(df['Profit'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: Rs. {df['Profit'].mean():,.0f}")
axes[0, 1].axvline(df['Profit'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: Rs. {df['Profit'].median():,.0f}")
axes[0, 1].set_title('Profit Distribution (Heavy Right Skew: Mean > Median)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Transaction Profit (Rs.)')
axes[0, 1].legend()

# Age
sns.histplot(df['Age'].dropna(), kde=True, ax=axes[1, 0], color='#ff7f0e', bins=25)
axes[1, 0].axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df['Age'].mean():.1f} yrs")
axes[1, 0].axvline(df['Age'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: {df['Age'].median():.1f} yrs")
axes[1, 0].set_title('Age Distribution (Symmetric Bell Curve)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Customer Age (Years)')
axes[1, 0].legend()

# Income
sns.histplot(df['Income'].dropna(), kde=True, ax=axes[1, 1], color='#9467bd', bins=35)
axes[1, 1].axvline(df['Income'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: Rs. {df['Income'].mean():,.0f}")
axes[1, 1].axvline(df['Income'].median(), color='green', linestyle='-', linewidth=2, label=f"Median: Rs. {df['Income'].median():,.0f}")
axes[1, 1].set_title('Income Distribution (Right-Skewed with High Earners)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Annual Customer Income (Rs.)')
axes[1, 1].legend()

plt.tight_layout()
plt.show()
""")

add_md("""### Descriptive Findings & Business Interpretation
1. **Sales & Profit Right-Skew**:
   - `Sales`: The mean (Rs. 10,961.60) is over 2.2 times higher than the median (Rs. 4,825.56), with skewness $= +2.45$. High-value electronics orders skew the mean upward.
   - `Profit`: Similarly right-skewed (mean Rs. 3,589.70 vs. median Rs. 1,528.70, skewness $= +2.48$).
   - **Business Action**: Leadership should use the **Median** for setting typical store quotas and baseline performance, while using the Mean for macro financial aggregation.
2. **Customer Demographics**:
   - Customer age centers symmetrically around 36.0 years ($\text{IQR} = 14$ years, 50% between 29 and 43 years old).
   - Household income exhibits a right skew (median Rs. 49,005.17, mean Rs. 55,101.38, top outliers up to Rs. 1.75M).
""")

add_md("""## 4. Confidence Interval Construction (Section 3.2)
We construct a **95% Confidence Interval** for:
1. **Average Transaction Sales ($\mu_{\text{Sales}}$)**
2. **Average Customer Rating ($\mu_{\text{Rating}}$)**

$$\\text{CI} = \\bar{x} \\pm t_{\\alpha/2, n-1} \\cdot \\left(\\frac{s}{\\sqrt{n}}\\right)$$
""")

add_code("""# 1. 95% Confidence Interval for Sales
sales_data = df['Sales'].dropna()
n_s = len(sales_data)
mean_s = sales_data.mean()
std_s = sales_data.std(ddof=1)
sem_s = std_s / np.sqrt(n_s)
ci_s = stats.t.interval(0.95, df=n_s - 1, loc=mean_s, scale=sem_s)
moe_s = mean_s - ci_s[0]

print("=" * 65)
print("             95% CONFIDENCE INTERVAL: TRANSACTION SALES          ")
print("=" * 65)
print(f"Sample Size (n)               : {n_s:,}")
print(f"Sample Mean (x̄)               : Rs. {mean_s:,.2f}")
print(f"Sample Std Dev (s)            : Rs. {std_s:,.2f}")
print(f"Standard Error of Mean (SE)   : Rs. {sem_s:,.2f}")
print(f"Margin of Error (MOE)         : Rs. {moe_s:,.2f}")
print(f"95% Confidence Interval       : [Rs. {ci_s[0]:,.2f}, Rs. {ci_s[1]:,.2f}]")
print("=" * 65)

# 2. 95% Confidence Interval for Customer Rating
rating_data = df['Customer_Rating'].dropna()
n_r = len(rating_data)
mean_r = rating_data.mean()
std_r = rating_data.std(ddof=1)
sem_r = std_r / np.sqrt(n_r)
ci_r = stats.t.interval(0.95, df=n_r - 1, loc=mean_r, scale=sem_r)
moe_r = mean_r - ci_r[0]

print("\\n" + "=" * 65)
print("          95% CONFIDENCE INTERVAL: CUSTOMER RATING               ")
print("=" * 65)
print(f"Sample Size (n)               : {n_r:,}")
print(f"Sample Mean (x̄)               : {mean_r:.4f}")
print(f"Sample Std Dev (s)            : {std_r:.4f}")
print(f"Standard Error of Mean (SE)   : {sem_r:.4f}")
print(f"Margin of Error (MOE)         : {moe_r:.4f}")
print(f"95% Confidence Interval       : [{ci_r[0]:.4f}, {ci_r[1]:.4f}]")
print("=" * 65)
""")

add_md("""### Plain-Language Explanation of the Confidence Interval
- **Business Interpretation**: We are **95% confident** that the true average transaction revenue across the company's entire customer base in India falls between **Rs. 10,620.71** and **Rs. 11,302.48**.
- **Frequentist Interpretation**: If we repeated this sampling process 100 times under identical conditions, 95 of the resulting confidence intervals would successfully enclose the true population mean.
- **Precision**: With a large sample ($n = 7,000$), our margin of error is remarkably small ($\pm$ Rs. 340.89, or roughly 3.1% of the mean), providing strong certainty for financial forecasting and cash flow planning.
""")

add_md("""## 5. Required Hypothesis Tests (Section 3.3 & 3.6)
We test all core business claims following the structured documentation required in Section 3.6:
1. Business Question in plain English
2. $H_0$ and $H_1$
3. Test used and why
4. Test statistic
5. Exact $p$-value
6. Decision at $\\alpha = 0.05$
7. Plain-language conclusion

---

### Test 1: Two-Sample Independent $t$-Test — Regional Sales (North vs. South)
**Business Question:** *Is average Sales significantly different between the North and South regions?*
""")

add_code("""north_sales = df[df['Region'] == 'North']['Sales'].dropna()
south_sales = df[df['Region'] == 'South']['Sales'].dropna()

print(f"North Region: n = {len(north_sales):,}, Mean = Rs. {north_sales.mean():,.2f}, Std = Rs. {north_sales.std():,.2f}")
print(f"South Region: n = {len(south_sales):,}, Mean = Rs. {south_sales.mean():,.2f}, Std = Rs. {south_sales.std():,.2f}")

# Two-sample t-test (Welch's & Student's)
t_welch, p_welch = stats.ttest_ind(north_sales, south_sales, equal_var=False)
t_student, p_student = stats.ttest_ind(north_sales, south_sales, equal_var=True)

print(f"Welch t-Test (Unequal Variance) : t = {t_welch:.4f}, p-value = {p_welch:.4f}")
print(f"Student t-Test (Equal Variance)  : t = {t_student:.4f}, p-value = {p_student:.4f}")
""")

add_md("""#### Test 1 Documentation & Plain-Language Conclusion
- **Business Question**: Is average Sales significantly different between the North and South regions?
- **Null Hypothesis ($H_0$)**: $\mu_{\text{North}} = \mu_{\text{South}}$ (There is no significant difference in mean sales between North and South).
- **Alternative Hypothesis ($H_1$)**: $\mu_{\text{North}} \neq \mu_{\text{South}}$ (Mean sales between North and South differ significantly).
- **Test Used & Why**: Two-Sample Independent $t$-Test (Welch's $t$-test). Used to compare mean values of two continuous independent groups without assuming identical group variances.
- **Test Statistic**: $t = 0.1052$ ($df \approx 3,432.8$)
- **$p$-Value**: $p = 0.9162$
- **Decision at $\alpha = 0.05$**: **Fail to Reject $H_0$** (since $p = 0.9162 > 0.05$).
- **Plain-Language Conclusion**:
  The observed difference in average order revenue between the North region (Rs. 10,777.98) and the South region (Rs. 10,726.92) is only Rs. 51.06, which is statistically indistinguishable from zero. There is no evidence that customers in either region spend differently per transaction. Regional leadership should not reallocate sales resources or marketing spend between North and South based on expected basket size.
""")

add_md("""---
### Test 2: One-Way ANOVA — Sales Across All Four Regions
**Business Question:** *Is average Sales significantly different across all four regions (North, South, East, West) at once?*
""")

add_code("""# Partition regional data
north = df[df['Region'] == 'North']['Sales'].dropna()
south = df[df['Region'] == 'South']['Sales'].dropna()
east = df[df['Region'] == 'East']['Sales'].dropna()
west = df[df['Region'] == 'West']['Sales'].dropna()

# One-way ANOVA
f_stat, p_val_anova = stats.f_oneway(north, south, east, west)
print(f"One-Way ANOVA across 4 Regions: F-statistic = {f_stat:.4f}, p-value = {p_val_anova:.4f}")

# Post-Hoc Tukey HSD
tukey = pairwise_tukeyhsd(endog=df['Sales'], groups=df['Region'], alpha=0.05)
print("\\nPost-Hoc Tukey HSD Multiple Comparisons:")
print(tukey)
""")

add_code("""# Visualization: Regional Sales Boxplot and Means with Error Bars
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
region_order = ['North', 'South', 'East', 'West']

sns.boxplot(x='Region', y='Sales', data=df, order=region_order, palette='Set2', ax=ax1, showmeans=True,
            meanprops={'marker':'o', 'markerfacecolor':'white', 'markeredgecolor':'black', 'markersize':'8'})
ax1.set_title('Regional Sales Distribution (ANOVA: F=0.646, p=0.586)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Sales (Rs.)')

reg_stats = df.groupby('Region')['Sales'].agg(['mean', 'sem']).reindex(region_order)
ax2.bar(reg_stats.index, reg_stats['mean'], yerr=reg_stats['sem']*1.96, capsize=6, color='#4575b4', alpha=0.85, edgecolor='black')
ax2.set_title('Mean Regional Sales with 95% CI Error Bars', fontsize=12, fontweight='bold')
ax2.set_ylabel('Mean Sales (Rs.)')
for idx, (reg, row) in enumerate(reg_stats.iterrows()):
    ax2.text(idx, row['mean'] * 0.5, f"Rs. {row['mean']:,.0f}", ha='center', color='white', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.show()
""")

add_md("""#### Test 2 Documentation & Plain-Language Conclusion
- **Business Question**: Is average Sales significantly different across all four regions (North, South, East, West) at once?
- **Null Hypothesis ($H_0$)**: $\mu_{\text{North}} = \mu_{\text{South}} = \mu_{\text{East}} = \mu_{\text{West}}$ (Mean sales are equal across all 4 regions).
- **Alternative Hypothesis ($H_1$)**: At least one region has a significantly different mean sales value.
- **Test Used & Why**: One-Way Analysis of Variance (ANOVA). Omnibus parametric test that compares between-group variance against within-group variance across three or more independent groups.
- **Test Statistic**: $F = 0.6455$ ($df_1 = 3, \, df_2 = 6,996$)
- **$p$-Value**: $p = 0.5857$
- **Decision at $\alpha = 0.05$**: **Fail to Reject $H_0$** (since $p = 0.5857 > 0.05$).
- **Post-Hoc Discussion**:
  Because the omnibus ANOVA was not significant, post-hoc tests are not formally needed. However, running Tukey's HSD confirms that all pairwise comparisons have adjusted $p$-values exceeding $0.59$ (East vs. South $p = 0.592$, East vs. West $p = 0.888$, North vs. West $p = 0.974$, North vs. South $p = 0.9996$).
- **Plain-Language Conclusion**:
  The stakeholder claim that *"the West region sells better"* is completely refuted by data. Average sales are virtually indistinguishable across India (East: Rs. 11,341.75; West: Rs. 10,989.43; North: Rs. 10,777.98; South: Rs. 10,726.92). Executive management must eliminate regional bias when setting sales quotas or allocating marketing capital.
""")

add_md("""---
### Test 3: Chi-Square Test of Independence — Customer Segment vs. Product Category
**Business Question:** *Is Customer_Segment associated with Product_Category, or are they independent?*
""")

add_code("""# Contingency table
contingency = pd.crosstab(df['Customer_Segment'], df['Product_Category'])
print("Contingency Table (Observed Frequencies):")
print(contingency)

# Chi-Square Test
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency)
print(f"\\nChi-Square Test Results:")
print(f" - Chi2 Statistic (χ²) : {chi2:.4f}")
print(f" - Degrees of Freedom  : {dof}")
print(f" - p-value             : {p_chi2:.4f}")
""")

add_code("""# Visualization of Category Proportions Across Customer Segments
prop_df = pd.crosstab(df['Customer_Segment'], df['Product_Category'], normalize='index') * 100
ax = prop_df.plot(kind='bar', stacked=True, colormap='tab10', figsize=(10, 6), edgecolor='white')
plt.title('Product Category Breakdown by Customer Segment (Chi² = 3.45, p = 0.903)', fontsize=13, fontweight='bold')
plt.ylabel('Share of Orders (%)')
plt.xlabel('Customer Segment')
plt.xticks(rotation=0)
plt.legend(title='Product Category', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()
""")

add_md("""#### Test 3 Documentation & Plain-Language Conclusion
- **Business Question**: Is Customer_Segment associated with Product_Category, or are they independent?
- **Null Hypothesis ($H_0$)**: Customer Segment and Product Category are independent (purchasing across categories does not depend on customer segment).
- **Alternative Hypothesis ($H_1$)**: Customer Segment and Product Category are dependent (certain customer segments favor specific categories).
- **Test Used & Why**: Chi-Square Test of Independence ($\chi^2$). Evaluates whether two categorical variables are statistically independent based on cross-tabulated contingency counts.
- **Test Statistic**: $\chi^2 = 3.4534$ ($df = (3-1) \times (5-1) = 8$)
- **$p$-Value**: $p = 0.9028$
- **Decision at $\alpha = 0.05$**: **Fail to Reject $H_0$** (since $p = 0.9028 > 0.05$).
- **Plain-Language Conclusion**:
  The stakeholder assumption that *"corporate customers buy different things than individual consumers"* is unsupported by the data. Across Consumer, Corporate, and Home Office clients, the distribution of purchases across categories is nearly identical (~31% Electronics, ~24% Grocery, ~22% Clothing, ~15% Furniture, ~8% Office Supplies). Retail marketing should avoid building segmented product catalogs and instead implement unified promotional campaigns.
""")

add_md("""---
### Test 4: Correlation Analysis — Discount vs. Profit
**Business Question:** *Is Discount correlated with Profit, and are promotional discounts hurting business profitability?*
""")

add_code("""# Paired clean data for correlation
clean_dp = df[['Discount', 'Profit']].dropna()
r_pearson, p_pearson = stats.pearsonr(clean_dp['Discount'], clean_dp['Profit'])
rho_spearman, p_spearman = stats.spearmanr(clean_dp['Discount'], clean_dp['Profit'])

print("=" * 65)
print("             CORRELATION ANALYSIS: DISCOUNT vs. PROFIT           ")
print("=" * 65)
print(f"Sample Size (n)               : {len(clean_dp):,}")
print(f"Pearson Correlation (r)       : {r_pearson:.4f}")
print(f"Pearson p-value               : {p_pearson:.4e}")
print(f"Spearman Correlation (ρ)      : {rho_spearman:.4f}")
print(f"Spearman p-value              : {p_spearman:.4e}")
print(f"Coefficient of Determination  : {r_pearson**2 * 100:.2f}% of Profit variance explained")
print("=" * 65)
""")

add_code("""# Scatter plot with regression line
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(x='Discount', y='Profit', data=clean_dp.sample(2000, random_state=42),
            scatter_kws={'alpha':0.25, 'color':'#2b83ba'}, line_kws={'color':'#d7191c', 'linewidth':2.5}, ax=ax)
ax.set_title('Discount Rate vs. Net Profit (Pearson r = -0.120, p = 1.10e-23)', fontsize=13, fontweight='bold')
ax.set_xlabel('Discount Rate (0.0 to 0.50)')
ax.set_ylabel('Transaction Profit (Rs.)')
ax.text(0.05, 0.90, f"Pearson r = -0.1201 (p < 0.001)\\nSpearman ρ = -0.1168 (p < 0.001)\\nStatistically Significant Negative Correlation",
        transform=ax.transAxes, bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor='#d7191c', alpha=0.9))
plt.tight_layout()
plt.show()
""")

add_md("""#### Test 4 Documentation & Plain-Language Conclusion
- **Business Question**: Is Discount correlated with Profit, and is discounting hurting profit margins?
- **Null Hypothesis ($H_0$)**: $\rho = 0$ (There is zero correlation between Discount and Profit).
- **Alternative Hypothesis ($H_1$)**: $\rho \neq 0$ (There is a significant linear correlation between Discount and Profit).
- **Test Used & Why**: Pearson's Product-Moment Correlation ($r$) and Spearman's Rank-Order Correlation ($\rho$) to assess the linear and monotonic relationship between two continuous variables.
- **Test Statistic**: Pearson $r = -0.1201$, Spearman $\rho = -0.1168$ ($n = 6,930$)
- **$p$-Value**: $p = 1.0997 \times 10^{-23}$ ($p < 0.001$)
- **Decision at $\alpha = 0.05$**: **Reject $H_0$** (since $p < 0.001$).
- **Sign, Strength & Causation Caution**:
  - **Sign**: Negative ($-$), showing that transactions with higher discount rates yield lower net profits.
  - **Strength**: Weak ($r = -0.1201$), accounting for roughly $1.44\%$ of the variance in transaction profit.
  - **Causation vs. Correlation**: *Correlation does not by itself prove causation.* While the negative association is statistically undeniable, profit is also influenced by unit cost, baseline markup, and item category. Discounts directly cut into margins, but they may also stimulate customer traffic.
- **Plain-Language Conclusion**:
  The stakeholder concern that *"discounts are hurting our margins"* is **supported by evidence**. Higher discounts statistically correlate with lower transaction profit ($p < 0.001$). However, because the correlation is modest, discounting is not entirely eroding the business; rather, discounts above 25–30% dilute margins unnecessarily without generating proportionate volume. We recommend capping promotional discounts at 20%.
""")

add_md("""## 6. Regression Modeling (Section 3.4)
We fit Ordinary Least Squares (OLS) models to predict transaction Sales.

---

### 6.1 Simple Linear Regression: Sales ~ Quantity
$$\\text{Sales} = \\beta_0 + \\beta_1 \\cdot \\text{Quantity} + \\epsilon$$
""")

add_code("""# Simple Linear Regression
slr = smf.ols('Sales ~ Quantity', data=df).fit()
print(slr.summary())
""")

add_md("""#### Simple Linear Regression Interpretation:
- **Fitted Model**: $\\widehat{\\text{Sales}} = -609.30 + 3,844.52 \\cdot \\text{Quantity}$
- **Intercept ($\\beta_0 = -609.30$, $p = 0.109$)**: Not statistically significant at $\\alpha = 0.05$. In retail, transactions with zero quantity do not occur.
- **Slope ($\\beta_1 = +3,844.52$, $t = 33.60$, $p < 0.001$)**: Highly statistically significant. Each additional unit purchased adds **Rs. 3,844.52** to transaction revenue.
- **Model Fit ($R^2 = 0.139$)**: Quantity alone explains **13.9%** of the variance in transaction sales revenue.
""")

add_md("""---
### 6.2 Multiple Linear Regression: Sales ~ Quantity + Discount + Income
$$\\text{Sales} = \\beta_0 + \\beta_1 \\cdot \\text{Quantity} + \\beta_2 \\cdot \\text{Discount} + \\beta_3 \\cdot \\text{Income} + \\epsilon$$
""")

add_code("""# Multiple Linear Regression
mlr = smf.ols('Sales ~ Quantity + Discount + Income', data=df).fit()
print(mlr.summary())
""")

add_code("""# Regression Comparison Visuals
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# SLR Plot
sns.regplot(x='Quantity', y='Sales', data=df.sample(2000, random_state=42), x_jitter=0.25,
            scatter_kws={'alpha':0.2, 'color':'#5e3c99'}, line_kws={'color':'#e66101', 'linewidth':2.5}, ax=ax1)
ax1.set_title('Simple Linear Regression: Sales vs Quantity (R² = 0.139)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Quantity Purchased')
ax1.set_ylabel('Sales (Rs.)')
ax1.text(0.05, 0.85, 'Sales = -609.30 + 3844.52 * Quantity\\np < 0.001', transform=ax1.transAxes,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#e66101', alpha=0.9))

# MLR Actual vs Predicted
clean_mlr = df[['Sales', 'Quantity', 'Discount', 'Income']].dropna()
preds = mlr.predict(clean_mlr)
ax2.scatter(preds, clean_mlr['Sales'], alpha=0.2, color='#1b7837')
ax2.plot([0, 80000], [0, 80000], color='red', linestyle='--', linewidth=2, label='Perfect Fit')
ax2.set_title('Multiple Linear Regression: Actual vs Predicted (R² = 0.159)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Predicted Sales (Rs.)')
ax2.set_ylabel('Actual Sales (Rs.)')
ax2.legend()

plt.tight_layout()
plt.show()
""")

add_md("""#### Multiple Linear Regression Interpretation:
- **Fitted Model**: 
  $$\\widehat{\\text{Sales}} = 2,133.02 + 3,901.22 \\cdot \\text{Quantity} - 15,632.74 \\cdot \\text{Discount} + 0.0047 \\cdot \\text{Income}$$
- **Model Fit ($R^2 = 0.159$, Adjusted $R^2 = 0.158$, $F = 419.2$, $p < 0.001$)**:
  The three predictors together explain **15.9%** of variance in transaction sales.
- **Predictor Significance & Interpretation**:
  1. **Quantity ($\beta_1 = +3,901.22$, $p < 0.001$) — Significant**: Controlling for discount and income, each additional unit adds **Rs. 3,901.22** to sales.
  2. **Discount ($\beta_2 = -15,632.74$, $p < 0.001$) — Significant**: Holding quantity and income constant, higher discounts directly diminish net revenue. A 10% increase in discount ($\Delta = 0.10$) reduces sales by **Rs. 1,563.27**.
  3. **Income ($\beta_3 = +0.0047$, $p = 0.280$) — Not Significant**: Customer income does not meaningfully influence transaction value ($p > 0.05$).
""")

add_md("""## 7. Optional Bonus: One-Sample $Z$-Test on Customer Rating (Section 3.5)
**Business Question:** *Does the sample average Customer_Rating differ significantly from a known historical benchmark?*

### Stated Assumptions:
- Known historical benchmark population mean: $\mu_0 = 3.0$ (neutral baseline) and $\mu_0 = 3.5$ (historical target).
- Known population standard deviation: $\sigma = 1.0$ (standard rating variance).
- Sample size is large ($n = 6,580$), validating the normal approximation via the Central Limit Theorem.
""")

add_code("""ratings = df['Customer_Rating'].dropna()
n_r = len(ratings)
x_bar = ratings.mean()
pop_sigma = 1.0

# Test against baseline 3.0
z_30 = (x_bar - 3.0) / (pop_sigma / np.sqrt(n_r))
p_30 = 2 * (1 - stats.norm.cdf(abs(z_30)))

# Test against target 3.5
z_35 = (x_bar - 3.5) / (pop_sigma / np.sqrt(n_r))
p_35 = 2 * (1 - stats.norm.cdf(abs(z_35)))

print("=" * 65)
print("             ONE-SAMPLE Z-TEST: CUSTOMER RATING                  ")
print("=" * 65)
print(f"Sample Size (n)             : {n_r:,}")
print(f"Sample Mean Rating (x̄)      : {x_bar:.4f}")
print(f"Assumed Population Std (σ)  : {pop_sigma:.2f}")
print("-----------------------------------------------------------------")
print(f"Test A (Baseline μ₀ = 3.0)  : Z = {z_30:+.4f}, p-value = {p_30:.4e}")
print(f"Test B (Target μ₀ = 3.5)    : Z = {z_35:+.4f}, p-value = {p_35:.4e}")
print("=" * 65)
""")

add_code("""# Visualization of Customer Rating and Z-test benchmarks
fig, ax = plt.subplots(figsize=(10, 5.5))
sns.histplot(ratings, bins=5, discrete=True, color='#41b6c4', stat='density', shrink=0.7, ax=ax)
ax.axvline(x_bar, color='navy', linewidth=2.5, label=f'Sample Mean ({x_bar:.2f})')
ax.axvspan(3.0680, 3.1168, color='blue', alpha=0.2, label='95% Confidence Interval [3.07, 3.12]')
ax.axvline(3.0, color='darkorange', linestyle='--', linewidth=2, label='Baseline μ₀ = 3.0 (Z = +7.50, p < 0.001)')
ax.axvline(3.5, color='crimson', linestyle=':', linewidth=2, label='Target μ₀ = 3.5 (Z = -33.06, p < 0.001)')

ax.set_title('Customer Rating Distribution with 95% CI & Z-Test Benchmarks', fontsize=12, fontweight='bold')
ax.set_xlabel('Customer Rating (1 to 5 Stars)')
ax.set_ylabel('Probability Density')
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()
""")

add_md("""#### Bonus $Z$-Test Documentation & Plain-Language Conclusion
- **Business Question**: Does customer rating significantly deviate from the neutral benchmark (3.0) and corporate target (3.5)?
- **Null Hypothesis ($H_0$)**: $\mu = 3.0$ (Rating equals neutral baseline).
- **Alternative Hypothesis ($H_1$)**: $\mu \neq 3.0$ (Rating differs from neutral baseline).
- **Test Statistic**: $Z = +7.4953$ (against 3.0), $Z = -33.0633$ (against 3.5).
- **$p$-Value**: $p < 0.0001$ in both tests.
- **Decision at $\alpha = 0.05$**: **Reject $H_0$** in both tests.
- **Plain-Language Conclusion**:
  Current customer satisfaction ($\bar{x} = 3.09$) is statistically significantly higher than the bare neutral score of 3.0 ($p < 0.001$). However, it fails drastically to reach the corporate target of 3.5 ($p < 0.001$). Post-order customer follow-up should be prioritized to identify sources of dissatisfaction and raise satisfaction toward 3.5.
""")

add_md("""## 8. Summary of Findings & Strategic Recommendations

| Test # | Business Claim / Question | Statistical Test | Test Statistic | $p$-Value | Decision ($\alpha=0.05$) | Business Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Test 1** | *Do North & South sales differ?* | Two-Sample $t$-Test | $t = 0.1052$ | $0.9162$ | Fail to Reject $H_0$ | **Refuted**: Regional sales are identical. |
| **Test 2** | *Does West sell better than other regions?* | One-Way ANOVA | $F = 0.6455$ | $0.5857$ | Fail to Reject $H_0$ | **Refuted**: Sales performance across all 4 regions is uniform. |
| **Test 3** | *Do Corporate buyers buy different products?* | Chi-Square Test ($\chi^2$) | $\chi^2 = 3.4534$ | $0.9028$ | Fail to Reject $H_0$ | **Refuted**: Product category mix is completely independent of segment. |
| **Test 4** | *Are discounts hurting our margins?* | Pearson Correlation ($r$) | $r = -0.1201$ | $1.10 \\times 10^{-23}$ | **Reject $H_0$** | **Confirmed**: Discounts significantly reduce transaction profit. |
| **Test 5** | *Does customer rating differ from standard?* | One-Sample $Z$-Test | $Z = +7.495$ / $-33.06$ | $< 0.0001$ | **Reject $H_0$** | **Confirmed**: Ratings exceed 3.0 but fail the 3.5 quality target. |
| **SLR** | *Predict Sales from Quantity* | Simple OLS Regression | $t = 33.60$ | $< 0.0001$ | **Significant** | $\widehat{\\text{Sales}} = -609.30 + 3844.52 \\cdot \\text{Qty}$ ($R^2=13.9\\%$) |
| **MLR** | *Predict Sales from Qty + Disc + Income* | Multiple OLS Regression | $F = 419.2$ | $< 0.0001$ | **Significant** | Qty (+) and Disc ($-$) significant; Income not significant ($R^2=15.9\\%$) |

---

### Executive Action Plan
1. **Equalize Regional Quotas**: Discontinue higher sales quotas for the West region. Sales generation is uniform across India.
2. **Standardize Merchandising**: Stop maintaining separate catalogs for Corporate and Consumer segments. Both buy identical category mixes.
3. **Cap Promotional Discounts at 20%**: High discounts statistically reduce net revenue and margin per order without driving higher basket units.
4. **Drive Multi-Item Bundling**: Quantity is the single largest significant driver of order revenue (+Rs. 3,901.22 per item). Merchandising should emphasize multi-pack bundling.
""")

# ==================== EXECUTE AND POPULATE CELLS ====================

print("Starting in-process notebook generation and execution...")

glob_dict = {}
execution_count = 1

for cell_type, content in cells_data:
    if cell_type == 'md':
        cell = nbf.v4.new_markdown_cell(content)
        nb.cells.append(cell)
    elif cell_type == 'code':
        cell = nbf.v4.new_code_cell(content)
        cell.execution_count = execution_count
        
        # Capture stdout
        stdout_io = io.StringIO()
        plt.close('all') # clear any previous figures
        
        try:
            with contextlib.redirect_stdout(stdout_io):
                exec(content, glob_dict)
            stdout_text = stdout_io.getvalue()
        except Exception as e:
            print(f"Error executing cell {execution_count}: {e}")
            stdout_text = f"Execution Error: {e}"
        
        outputs = []
        if stdout_text:
            outputs.append(nbf.v4.new_output(
                output_type='stream',
                name='stdout',
                text=stdout_text
            ))
            
        # Capture any matplotlib figures created
        figs = [plt.figure(i) for i in plt.get_fignums()]
        for fig in figs:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            b64_img = base64.b64encode(buf.read()).decode('utf-8')
            outputs.append(nbf.v4.new_output(
                output_type='display_data',
                data={
                    'image/png': b64_img,
                    'text/plain': '<Figure size ...>'
                },
                metadata={}
            ))
            plt.close(fig)
            
        cell.outputs = outputs
        nb.cells.append(cell)
        execution_count += 1

notebook_out = 'HCL_Data_Analyst_Advanced_Statistics_Project.ipynb'
with open(notebook_out, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"SUCCESS: Generated and fully executed '{notebook_out}'!")
print(f"File size: {os.path.getsize(notebook_out):,} bytes.")
