import os
import matplotlib
os.environ['MPLCONFIGDIR'] = os.path.abspath('.matplotlib')
os.makedirs('.matplotlib', exist_ok=True)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

os.makedirs('images', exist_ok=True)
sns.set_theme(style='whitegrid', font_scale=1.05)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# Load and clean data
df = pd.read_csv('retail_customer_sales_dataset.csv').drop_duplicates(subset=['Transaction_ID']).copy()
region_map = {
    'West': 'West', 'west': 'West', 'WEST': 'West',
    'East': 'East', 'east': 'East',
    'South': 'South', 'south': 'South', 'Sth': 'South',
    'North': 'North', 'north': 'North', 'NORTH': 'North', 'Nort': 'North'
}
df['Region'] = df['Region'].map(region_map)
df.loc[(df['Age'] < 18) | (df['Age'] > 100), 'Age'] = np.nan
df.loc[(df['Discount'] < 0) | (df['Discount'] > 0.5), 'Discount'] = np.nan

# Plot 1: Key Metrics Distributions (Sales, Profit, Age, Income)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
mean_s, med_s = df['Sales'].mean(), df['Sales'].median()
sns.histplot(df['Sales'], kde=True, ax=axes[0, 0], color='#1f77b4', bins=40)
axes[0, 0].axvline(mean_s, color='red', linestyle='--', label=f'Mean: Rs. {mean_s:,.0f}')
axes[0, 0].axvline(med_s, color='green', linestyle='-', label=f'Median: Rs. {med_s:,.0f}')
axes[0, 0].set_title('Sales Distribution (Right-Skewed, Mean > Median)', fontsize=13, fontweight='bold')
axes[0, 0].legend()

mean_p, med_p = df['Profit'].mean(), df['Profit'].median()
sns.histplot(df['Profit'], kde=True, ax=axes[0, 1], color='#2ca02c', bins=40)
axes[0, 1].axvline(mean_p, color='red', linestyle='--', label=f'Mean: Rs. {mean_p:,.0f}')
axes[0, 1].axvline(med_p, color='green', linestyle='-', label=f'Median: Rs. {med_p:,.0f}')
axes[0, 1].set_title('Profit Distribution (Right-Skewed, Mean > Median)', fontsize=13, fontweight='bold')
axes[0, 1].legend()

mean_a, med_a = df['Age'].mean(), df['Age'].median()
sns.histplot(df['Age'].dropna(), kde=True, ax=axes[1, 0], color='#ff7f0e', bins=30)
axes[1, 0].axvline(mean_a, color='red', linestyle='--', label=f'Mean: {mean_a:.1f} yrs')
axes[1, 0].axvline(med_a, color='green', linestyle='-', label=f'Median: {med_a:.1f} yrs')
axes[1, 0].set_title('Age Distribution (Approximately Symmetric)', fontsize=13, fontweight='bold')
axes[1, 0].legend()

mean_i, med_i = df['Income'].mean(), df['Income'].median()
sns.histplot(df['Income'].dropna(), kde=True, ax=axes[1, 1], color='#9467bd', bins=40)
axes[1, 1].axvline(mean_i, color='red', linestyle='--', label=f'Mean: Rs. {mean_i:,.0f}')
axes[1, 1].axvline(med_i, color='green', linestyle='-', label=f'Median: Rs. {med_i:,.0f}')
axes[1, 1].set_title('Income Distribution (Right-Skewed with High Earners)', fontsize=13, fontweight='bold')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('images/descriptive_distributions.png', dpi=300)
plt.close()

# Plot 2: Regional Sales Comparison (T-test & ANOVA)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
region_order = ['North', 'South', 'East', 'West']
sns.boxplot(x='Region', y='Sales', data=df, order=region_order, palette='Set2', ax=ax1, showmeans=True,
            meanprops={'marker':'o', 'markerfacecolor':'white', 'markeredgecolor':'black', 'markersize':'8'})
ax1.set_title('Sales Distribution Across Regions (ANOVA: F=0.646, p=0.586)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Sales (Rs.)')

regional_stats = df.groupby('Region')['Sales'].agg(['mean', 'sem']).reindex(region_order)
ax2.bar(regional_stats.index, regional_stats['mean'], yerr=regional_stats['sem']*1.96, capsize=5, color='#4575b4', alpha=0.85, edgecolor='black')
ax2.set_title('Mean Sales by Region with 95% CI Error Bars', fontsize=12, fontweight='bold')
ax2.set_ylabel('Mean Sales (Rs.)')
for idx, (reg, row) in enumerate(regional_stats.iterrows()):
    ax2.text(idx, row['mean'] * 0.5, f'Rs. {row["mean"]:,.0f}', ha='center', color='white', fontweight='bold')
plt.tight_layout()
plt.savefig('images/regional_sales_anova.png', dpi=300)
plt.close()

# Plot 3: Chi-Square - Customer Segment vs Product Category
fig, ax = plt.subplots(figsize=(10, 6))
ct = pd.crosstab(df['Customer_Segment'], df['Product_Category'], normalize='index') * 100
ct.plot(kind='bar', stacked=True, colormap='tab10', ax=ax, edgecolor='white')
ax.set_title('Product Category Distribution by Customer Segment (Chi2=3.45, p=0.903)', fontsize=13, fontweight='bold')
ax.set_ylabel('Percentage of Transactions (%)')
ax.set_xlabel('Customer Segment')
ax.legend(title='Product Category', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('images/chisquare_segment_category.png', dpi=300)
plt.close()

# Plot 4: Correlation - Discount vs Profit
fig, ax = plt.subplots(figsize=(9, 6))
clean_dp = df[['Discount', 'Profit']].dropna()
sns.regplot(x='Discount', y='Profit', data=clean_dp.sample(1500, random_state=42), scatter_kws={'alpha':0.2, 'color':'#2b83ba'}, line_kws={'color':'red', 'linewidth':2}, ax=ax)
ax.set_title('Discount vs Profit (Pearson r = -0.120, p < 0.001)', fontsize=13, fontweight='bold')
ax.set_xlabel('Discount Rate (0.0 to 0.5)')
ax.set_ylabel('Profit (Rs.)')
ax.text(0.05, 0.90, 'Pearson r = -0.1201 (p = 1.10e-23)\nWeak Negative Statistically Significant Correlation', transform=ax.transAxes,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='red', alpha=0.9), fontsize=10)
plt.tight_layout()
plt.savefig('images/correlation_discount_profit.png', dpi=300)
plt.close()

# Plot 5: Regression Models Visuals
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
# SLR: Sales ~ Quantity
sns.regplot(x='Quantity', y='Sales', data=df.sample(2000, random_state=42), x_jitter=0.2,
            scatter_kws={'alpha':0.2, 'color':'#5e3c99'}, line_kws={'color':'#e66101', 'linewidth':2.5}, ax=ax1)
ax1.set_title('Simple Linear Regression: Sales vs Quantity (R2 = 0.139)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Quantity Purchased')
ax1.set_ylabel('Sales (Rs.)')
ax1.text(0.05, 0.85, 'Sales = -609.30 + 3844.52 * Quantity\np < 0.001', transform=ax1.transAxes,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#e66101', alpha=0.9))

# MLR: Actual vs Predicted
from statsmodels.formula.api import ols
mlr_model = ols('Sales ~ Quantity + Discount + Income', data=df).fit()
clean_mlr = df[['Sales', 'Quantity', 'Discount', 'Income']].dropna()
preds = mlr_model.predict(clean_mlr)
ax2.scatter(preds, clean_mlr['Sales'], alpha=0.2, color='#1b7837')
ax2.plot([0, 80000], [0, 80000], color='red', linestyle='--', linewidth=2, label='Perfect Fit Reference')
ax2.set_title('Multiple Linear Regression: Actual vs Predicted (R2 = 0.159)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Predicted Sales (Rs.)')
ax2.set_ylabel('Actual Sales (Rs.)')
ax2.legend()
plt.tight_layout()
plt.savefig('images/regression_analysis.png', dpi=300)
plt.close()

# Plot 6: Customer Rating & 95% Confidence Interval / Z-Test
fig, ax = plt.subplots(figsize=(9, 5.5))
ratings = df['Customer_Rating'].dropna()
sns.histplot(ratings, bins=5, discrete=True, color='#41b6c4', stat='density', shrink=0.7, ax=ax)
mean_r = ratings.mean()
ci_low, ci_high = 3.0680, 3.1168
ax.axvline(mean_r, color='navy', linewidth=2.5, label=f'Sample Mean ({mean_r:.2f})')
ax.axvspan(ci_low, ci_high, color='blue', alpha=0.2, label=f'95% CI [{ci_low:.3f}, {ci_high:.3f}]')
ax.axvline(3.0, color='darkorange', linestyle='--', linewidth=2, label='Baseline mu0 = 3.0 (Z = +7.50, p < 0.001)')
ax.axvline(3.5, color='crimson', linestyle=':', linewidth=2, label='Historical mu0 = 3.5 (Z = -33.06, p < 0.001)')
ax.set_title('Customer Rating Distribution with 95% CI & Z-Test Benchmarks', fontsize=12, fontweight='bold')
ax.set_xlabel('Customer Rating (1 to 5 Stars)')
ax.set_ylabel('Density')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('images/rating_confidence_interval.png', dpi=300)
plt.close()

print('All 6 high-resolution plots successfully created in images/!')
