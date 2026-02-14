"""
Vrinda Store Data Analysis - Termux Optimized Version
Complete solution for all 8 client questions
Optimized for mobile devices and Termux environment
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Termux
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory in phone storage
OUTPUT_DIR = os.path.expanduser("~/storage/shared/vrinda_analysis_outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Saving files to:", OUTPUT_DIR)

print("\n" + "="*60)
print("VRINDA STORE DATA ANALYSIS")
print("Termux Optimized Version")
print("="*60)

# File paths - UPDATE THIS to match your file location
FILE_PATH = 'data/Vrinda Store.csv'

# Alternative paths if the above doesn't work:
# FILE_PATH = 'Vrinda_Store.csv'
# FILE_PATH = '/sdcard/Vrinda_Store.csv'
# FILE_PATH = '~/storage/shared/Vrinda_Store.csv'

print(f"\nLooking for data file at: {FILE_PATH}")

# ============================================================================
# STEP 1: LOAD AND CLEAN DATA
# ============================================================================

print("\n" + "-"*60)
print("STEP 1: LOADING DATA")
print("-"*60)
# Clean column names (remove trailing spaces)
try:
    # Load the CSV file
    df = pd.read_csv(FILE_PATH, encoding='utf-8')
    print(df.columns.tolist())

    # Clean column names
    df.columns = df.columns.str.strip()

    print(f"✓ Data loaded successfully!")
    print(f"✓ Total records: {len(df):,}")
    print(f"✓ Total columns: {len(df.columns)}")
except FileNotFoundError:
    print(f"\n❌ ERROR: File not found at {FILE_PATH}")
    print("\nPlease ensure your CSV file is at the correct location.")
    print("You can update the FILE_PATH variable in this script.\n")
    exit(1)
except Exception as e:
    print(f"\n❌ ERROR loading file: {e}\n")
    exit(1)

print("\n" + "-"*60)
print("STEP 2: CLEANING DATA")
print("-"*60)

# Clean column names (remove trailing spaces)
df.columns = df.columns.str.strip()

# 1. Standardize Gender
print("\n1. Standardizing Gender...")
gender_map = {
    'M': 'Men',
    'W': 'Women',
    'Men': 'Men',
    'Women': 'Women'
}
df['Gender'] = df['Gender'].map(gender_map)
print(f"   ✓ Gender values: {df['Gender'].value_counts().to_dict()}")

# 2. Convert Date
print("\n2. Converting Date column...")
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Year'] = df['Date'].dt.year
print(f"   ✓ Date range: {df['Date'].min()} to {df['Date'].max()}")

# 3. Clean Amount
print("\n3. Cleaning Amount column...")
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
print(f"   ✓ Amount range: ₹{df['Amount'].min():,.0f} to ₹{df['Amount'].max():,.0f}")

# 4. Standardize Status
print("\n4. Standardizing Status...")
df['Status'] = df['Status'].str.strip().str.title()
print(f"   ✓ Statuses: {df['Status'].unique()}")

# 5. Clean Channel
print("\n5. Standardizing Channel...")
df['Channel'] = df['Channel'].str.strip().str.title()
print(f"   ✓ Channels: {df['Channel'].unique()}")

# 6. Create Age Groups
print("\n6. Creating Age Groups...")
df['Age_Group'] = pd.cut(df['Age'], 
                         bins=[0, 18, 30, 40, 50, 100],
                         labels=['<18', '18-30', '30-40', '40-50', '50+'])
print(f"   ✓ Age groups: {df['Age_Group'].value_counts().to_dict()}")

# 7. Clean State names
print("\n7. Standardizing State names...")
df['ship-state'] = df['ship-state'].str.strip().str.upper()
print(f"   ✓ Total states: {df['ship-state'].nunique()}")

print("\n✓ DATA CLEANING COMPLETED!")

# ============================================================================
# QUESTION 1: Compare Sales and Orders
# ============================================================================

print("\n" + "="*60)
print("Q1: COMPARING SALES AND ORDERS BY MONTH")
print("="*60)

monthly = df.groupby('Month_Name').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()

# Sort by month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
monthly['Month_Name'] = pd.Categorical(monthly['Month_Name'], 
                                       categories=month_order, 
                                       ordered=True)
monthly = monthly.sort_values('Month_Name')
monthly.columns = ['Month', 'Orders', 'Sales']

print("\nMonthly Summary:")
for _, row in monthly.iterrows():
    print(f"{row['Month']:12} - Orders: {row['Orders']:5,} | Sales: ₹{row['Sales']:12,.2f}")

# Create chart
fig, ax1 = plt.subplots(figsize=(12, 6))
x = np.arange(len(monthly))
width = 0.35

ax1.bar(x - width/2, monthly['Orders'], width, label='Orders', color='skyblue', alpha=0.8)
ax1.set_xlabel('Month', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Orders', fontsize=11, fontweight='bold', color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

ax2 = ax1.twinx()
ax2.plot(x, monthly['Sales'], color='red', marker='o', linewidth=2, markersize=8, label='Sales')
ax2.set_ylabel('Sales Amount (₹)', fontsize=11, fontweight='bold', color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax1.set_xticks(x)
ax1.set_xticklabels(monthly['Month'], rotation=45, ha='right')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Sales vs Orders Comparison by Month', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q1_sales_orders_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q1_sales_orders_comparison.png")

# ============================================================================
# QUESTION 2: Highest Sales and Orders Month
# ============================================================================

print("\n" + "="*60)
print("Q2: MONTH WITH HIGHEST SALES AND ORDERS")
print("="*60)

highest_orders_month = monthly.loc[monthly['Orders'].idxmax()]
highest_sales_month = monthly.loc[monthly['Sales'].idxmax()]

print(f"\n📊 HIGHEST ORDERS:")
print(f"   Month: {highest_orders_month['Month']}")
print(f"   Total Orders: {highest_orders_month['Orders']:,}")

print(f"\n💰 HIGHEST SALES:")
print(f"   Month: {highest_sales_month['Month']}")
print(f"   Total Sales: ₹{highest_sales_month['Sales']:,.2f}")

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

monthly_sorted_orders = monthly.sort_values('Orders', ascending=False)
colors1 = ['#ff6b6b' if x == highest_orders_month['Month'] else '#4ecdc4' 
          for x in monthly_sorted_orders['Month']]
ax1.barh(monthly_sorted_orders['Month'], monthly_sorted_orders['Orders'], color=colors1, alpha=0.8)
ax1.set_xlabel('Number of Orders', fontweight='bold')
ax1.set_title('Orders by Month', fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

monthly_sorted_sales = monthly.sort_values('Sales', ascending=False)
colors2 = ['#ff6b6b' if x == highest_sales_month['Month'] else '#95e1d3' 
          for x in monthly_sorted_sales['Month']]
ax2.barh(monthly_sorted_sales['Month'], monthly_sorted_sales['Sales'], color=colors2, alpha=0.8)
ax2.set_xlabel('Sales Amount (₹)', fontweight='bold')
ax2.set_title('Sales by Month', fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q2_highest_month.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q2_highest_month.png")

# ============================================================================
# QUESTION 3: Gender Analysis (2022)
# ============================================================================

print("\n" + "="*60)
print("Q3: GENDER-WISE PURCHASE ANALYSIS (2022)")
print("="*60)

df_2022 = df[df['Year'] == 2022]

gender_stats = df_2022.groupby('Gender').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()
gender_stats.columns = ['Gender', 'Orders', 'Sales']
gender_stats['Avg_Order_Value'] = gender_stats['Sales'] / gender_stats['Orders']
gender_stats['Orders_Pct'] = (gender_stats['Orders'] / gender_stats['Orders'].sum() * 100).round(2)
gender_stats['Sales_Pct'] = (gender_stats['Sales'] / gender_stats['Sales'].sum() * 100).round(2)

print("\nGender Statistics (2022):")
for _, row in gender_stats.iterrows():
    print(f"\n{row['Gender']}:")
    print(f"  Orders: {row['Orders']:,} ({row['Orders_Pct']}%)")
    print(f"  Sales: ₹{row['Sales']:,.2f} ({row['Sales_Pct']}%)")
    print(f"  Avg Order Value: ₹{row['Avg_Order_Value']:,.2f}")

max_orders = gender_stats.loc[gender_stats['Orders'].idxmax()]
print(f"\n👥 MORE ORDERS: {max_orders['Gender']} with {max_orders['Orders']:,} orders")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].pie(gender_stats['Orders'], labels=gender_stats['Gender'],
              autopct='%1.1f%%', startangle=90, colors=['#ff6b6b', '#4ecdc4'])
axes[0, 0].set_title('Orders Distribution', fontweight='bold')

axes[0, 1].pie(gender_stats['Sales'], labels=gender_stats['Gender'],
              autopct='%1.1f%%', startangle=90, colors=['#ffd93d', '#6bcf7f'])
axes[0, 1].set_title('Sales Distribution', fontweight='bold')

axes[1, 0].bar(gender_stats['Gender'], gender_stats['Orders'],
              color=['#ff6b6b', '#4ecdc4'], alpha=0.8)
axes[1, 0].set_ylabel('Orders', fontweight='bold')
axes[1, 0].set_title('Total Orders', fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)

axes[1, 1].bar(gender_stats['Gender'], gender_stats['Sales'],
              color=['#ffd93d', '#6bcf7f'], alpha=0.8)
axes[1, 1].set_ylabel('Sales (₹)', fontweight='bold')
axes[1, 1].set_title('Total Sales', fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q3_gender_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q3_gender_analysis.png")

# ============================================================================
# QUESTION 4: Order Status (2022)
# ============================================================================

print("\n" + "="*60)
print("Q4: ORDER STATUS BREAKDOWN (2022)")
print("="*60)

status_stats = df_2022.groupby('Status').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()
status_stats.columns = ['Status', 'Count', 'Sales']
status_stats['Percentage'] = (status_stats['Count'] / status_stats['Count'].sum() * 100).round(2)
status_stats = status_stats.sort_values('Count', ascending=False)

print("\nOrder Status Summary:")
for _, row in status_stats.iterrows():
    print(f"{row['Status']:15} - {row['Count']:6,} orders ({row['Percentage']:5.2f}%) | ₹{row['Sales']:12,.2f}")

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

colors = plt.cm.Set3(range(len(status_stats)))
ax1.pie(status_stats['Count'], labels=status_stats['Status'],
       autopct='%1.1f%%', startangle=90, colors=colors)
ax1.set_title('Order Status Distribution', fontweight='bold')

ax2.barh(status_stats['Status'], status_stats['Count'], color=colors, alpha=0.8)
ax2.set_xlabel('Number of Orders', fontweight='bold')
ax2.set_title('Orders by Status', fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q4_order_status.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q4_order_status.png")

# ============================================================================
# QUESTION 5: Top 10 States
# ============================================================================

print("\n" + "="*60)
print("Q5: TOP 10 STATES BY SALES")
print("="*60)

state_stats = df.groupby('ship-state').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()
state_stats.columns = ['State', 'Orders', 'Sales']
state_stats = state_stats.sort_values('Sales', ascending=False).head(10)
state_stats['Sales_Pct'] = (state_stats['Sales'] / df['Amount'].sum() * 100).round(2)

print("\nTop 10 States:")
for i, row in enumerate(state_stats.itertuples(), 1):
    print(f"{i:2}. {row.State:20} - Orders: {row.Orders:6,} | Sales: ₹{row.Sales:12,.2f} ({row.Sales_Pct}%)")

# Create visualization
top_states = state_stats.head(10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

y_pos = np.arange(len(top_states))
colors = plt.cm.viridis(np.linspace(0, 1, len(top_states)))

# Sales Chart
ax1.barh(y_pos, top_states['Sales'], color=colors)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(top_states['State'])
ax1.set_xlabel('Sales (₹)', fontweight='bold')
ax1.set_title('Top States by Sales', fontweight='bold')
ax1.invert_yaxis()
ax1.grid(axis='x', alpha=0.3)

# Orders Chart
ax2.barh(y_pos, top_states['Orders'], color=colors)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(top_states['State'])
ax2.set_xlabel('Orders', fontweight='bold')
ax2.set_title('Top States by Orders', fontweight='bold')
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/q5_top_states.png", dpi=150)
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q5_top_states.png")


# ============================================================================
# QUESTION 6: Age-Gender Relationship
# ============================================================================

print("\n" + "="*60)
print("Q6: AGE AND GENDER RELATIONSHIP")
print("="*60)

age_gender = df.groupby(['Age_Group', 'Gender']).agg({
    'Order ID': 'count'
}).reset_index()
age_gender.columns = ['Age_Group', 'Gender', 'Orders']

pivot_orders = age_gender.pivot(index='Age_Group', columns='Gender', values='Orders').fillna(0)

print("\nOrders by Age Group and Gender:")
print(pivot_orders)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

age_groups = age_gender['Age_Group'].unique()
x = np.arange(len(age_groups))
width = 0.35

men_data = age_gender[age_gender['Gender'] == 'Men'].set_index('Age_Group')['Orders'].reindex(age_groups, fill_value=0)
women_data = age_gender[age_gender['Gender'] == 'Women'].set_index('Age_Group')['Orders'].reindex(age_groups, fill_value=0)

axes[0, 0].bar(x - width/2, men_data, width, label='Men', color='#4ecdc4', alpha=0.8)
axes[0, 0].bar(x + width/2, women_data, width, label='Women', color='#ff6b6b', alpha=0.8)
axes[0, 0].set_xlabel('Age Group', fontweight='bold')
axes[0, 0].set_ylabel('Orders', fontweight='bold')
axes[0, 0].set_title('Orders by Age & Gender', fontweight='bold')
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(age_groups)
axes[0, 0].legend()
axes[0, 0].grid(axis='y', alpha=0.3)

axes[0, 1].bar(age_groups, men_data, label='Men', color='#4ecdc4', alpha=0.8)
axes[0, 1].bar(age_groups, women_data, bottom=men_data, label='Women', color='#ff6b6b', alpha=0.8)
axes[0, 1].set_xlabel('Age Group', fontweight='bold')
axes[0, 1].set_ylabel('Orders', fontweight='bold')
axes[0, 1].set_title('Stacked Orders', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(axis='y', alpha=0.3)

# Heatmap
pivot_normalized = pivot_orders.div(pivot_orders.sum(axis=1), axis=0) * 100
im = axes[1, 0].imshow(pivot_normalized.T, cmap='YlOrRd', aspect='auto')
axes[1, 0].set_xticks(np.arange(len(age_groups)))
axes[1, 0].set_yticks(np.arange(len(pivot_orders.columns)))
axes[1, 0].set_xticklabels(age_groups)
axes[1, 0].set_yticklabels(pivot_orders.columns)
axes[1, 0].set_title('Distribution Heatmap (%)', fontweight='bold')
plt.colorbar(im, ax=axes[1, 0])

# Line chart
for gender in ['Men', 'Women']:
    data = age_gender[age_gender['Gender'] == gender]
    axes[1, 1].plot(data['Age_Group'], data['Orders'], marker='o', linewidth=2, markersize=8, label=gender)
axes[1, 1].set_xlabel('Age Group', fontweight='bold')
axes[1, 1].set_ylabel('Orders', fontweight='bold')
axes[1, 1].set_title('Orders Trend', fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q6_age_gender_relation.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q6_age_gender_relation.png")

# ============================================================================
# QUESTION 7: Channel Analysis
# ============================================================================

print("\n" + "="*60)
print("Q7: CHANNEL CONTRIBUTION ANALYSIS")
print("="*60)

channel_stats = df.groupby('Channel').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()
channel_stats.columns = ['Channel', 'Orders', 'Sales']
channel_stats = channel_stats.sort_values('Sales', ascending=False)
channel_stats['Sales_Pct'] = (channel_stats['Sales'] / channel_stats['Sales'].sum() * 100).round(2)

print("\nChannel Performance:")
for _, row in channel_stats.iterrows():
    print(f"{row['Channel']:12} - Orders: {row['Orders']:6,} | Sales: ₹{row['Sales']:12,.2f} ({row['Sales_Pct']:5.2f}%)")

top_channel = channel_stats.iloc[0]
print(f"\n🏆 TOP CHANNEL: {top_channel['Channel']}")
print(f"   Sales: ₹{top_channel['Sales']:,.2f} ({top_channel['Sales_Pct']}%)")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

colors = plt.cm.Set3(range(len(channel_stats)))

axes[0, 0].pie(channel_stats['Sales'], labels=channel_stats['Channel'],
              autopct='%1.1f%%', startangle=90, colors=colors)
axes[0, 0].set_title('Sales Distribution', fontweight='bold')

axes[0, 1].pie(channel_stats['Orders'], labels=channel_stats['Channel'],
              autopct='%1.1f%%', startangle=90, colors=colors)
axes[0, 1].set_title('Orders Distribution', fontweight='bold')

axes[1, 0].barh(channel_stats['Channel'], channel_stats['Sales'], color=colors, alpha=0.8)
axes[1, 0].set_xlabel('Sales (₹)', fontweight='bold')
axes[1, 0].set_title('Sales by Channel', fontweight='bold')
axes[1, 0].invert_yaxis()
axes[1, 0].grid(axis='x', alpha=0.3)

axes[1, 1].barh(channel_stats['Channel'], channel_stats['Orders'], color=colors, alpha=0.8)
axes[1, 1].set_xlabel('Orders', fontweight='bold')
axes[1, 1].set_title('Orders by Channel', fontweight='bold')
axes[1, 1].invert_yaxis()
axes[1, 1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/q7_channel_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q7_channel_analysis.png")

# ============================================================================
# QUESTION 8: Category Analysis
# ============================================================================

print("\n" + "="*60)
print("Q8: HIGHEST SELLING CATEGORY")
print("="*60)

category_stats = df.groupby('Category').agg({
    'Order ID': 'count',
    'Amount': 'sum'
}).reset_index()
category_stats.columns = ['Category', 'Orders', 'Sales']
category_stats = category_stats.sort_values('Sales', ascending=False)
category_stats['Percentage'] = (category_stats['Sales'] / category_stats['Sales'].sum() * 100).round(2)

print("\nTop 10 Categories:")
for i, row in enumerate(category_stats.head(10).itertuples(), 1):
    print(f"{i:2}. {row.Category:15} - Orders: {row.Orders:6,} | Sales: ₹{row.Sales:12,.2f} ({row.Percentage}%)")

top_category = category_stats.iloc[0]
print(f"\n🏆 HIGHEST SELLING: {top_category['Category']}")
print(f"   Sales: ₹{top_category['Sales']:,.2f} ({top_category['Percentage']}%)")

# Create visualization
# Q8 Visualization Fix
top_10 = category_stats.head(10)

fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(top_10))
colors = plt.cm.viridis(np.linspace(0, 1, len(top_10)))

ax.barh(y_pos, top_10['Sales'], color=colors, alpha=0.8)

ax.set_yticks(y_pos)
ax.set_yticklabels(top_10['Category'])
ax.set_xlabel("Sales (₹)", fontweight='bold')
ax.set_title("Top Categories by Sales", fontweight='bold')

ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/q8_top_categories.png", dpi=150)
plt.close()

print(f"\n✓ Chart saved: {OUTPUT_DIR}/q8_top_categories.png")

# ============================================================================
# SUMMARY REPORT
# ============================================================================

print("\n" + "="*60)
print("GENERATING SUMMARY REPORT")
print("="*60)

report = []
report.append("="*60)
report.append("VRINDA STORE - SALES ANALYSIS SUMMARY REPORT")
report.append("="*60)
report.append(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append(f"Data Period: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
report.append(f"Total Records: {len(df):,}")

report.append("\n" + "-"*60)
report.append("KEY METRICS")
report.append("-"*60)
report.append(f"Total Sales Revenue: ₹{df['Amount'].sum():,.2f}")
report.append(f"Total Orders: {len(df):,}")
report.append(f"Average Order Value: ₹{df['Amount'].mean():,.2f}")

report.append("\n" + "-"*60)
report.append("KEY INSIGHTS")
report.append("-"*60)

monthly_best = df.groupby('Month_Name')['Amount'].sum()
best_month = monthly_best.idxmax()
report.append(f"• Best Month: {best_month} (₹{monthly_best.max():,.2f})")

gender_best = df.groupby('Gender')['Amount'].sum()
top_gender = gender_best.idxmax()
report.append(f"• Top Gender: {top_gender} ({gender_best.max()/gender_best.sum()*100:.1f}%)")

channel_best = df.groupby('Channel')['Amount'].sum()
top_channel_name = channel_best.idxmax()
report.append(f"• Top Channel: {top_channel_name} ({channel_best.max()/channel_best.sum()*100:.1f}%)")

state_best = df.groupby('ship-state')['Amount'].sum()
top_state = state_best.idxmax()
report.append(f"• Top State: {top_state} (₹{state_best.max():,.2f})")

category_best = df.groupby('Category')['Amount'].sum()
top_cat = category_best.idxmax()
report.append(f"• Top Category: {top_cat} (₹{category_best.max():,.2f})")

delivered = len(df[df['Status'] == 'Delivered'])
report.append(f"• Success Rate: {delivered/len(df)*100:.1f}%")

report.append("\n" + "="*60)

report_text = "\n".join(report)
with open(f'{OUTPUT_DIR}/summary_report.txt', 'w') as f:
    f.write(report_text)

print(report_text)

# ============================================================================
# COMPLETION
# ============================================================================

print("\n" + "="*60)
print("✓ ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nAll outputs saved in: {OUTPUT_DIR}/")
print("\nGenerated Files:")
print("  1. q1_sales_orders_comparison.png")
print("  2. q2_highest_month.png")
print("  3. q3_gender_analysis.png")
print("  4. q4_order_status.png")
print("  5. q5_top_states.png")
print("  6. q6_age_gender_relation.png")
print("  7. q7_channel_analysis.png")
print("  8. q8_category_analysis.png")
print("  9. summary_report.txt")
print("\nYou can view the images using a file manager or gallery app.")
print("="*60 + "\n")

# =====================================================
# EXPORT FULL ANALYSIS TO EXCEL
# =====================================================

print("\nGenerating Excel Report...")

# ==============================
# CALCULATIONS FOR EXCEL REPORT
# ==============================

# Basic metrics
total_sales = df["Amount"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = df["Amount"].mean()

# Grouped analysis
monthly_stats = df.groupby("Month")["Amount"].sum().reset_index()

state_stats = (
    df.groupby("ship-state")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

category_stats = df.groupby("Category")["Amount"].sum().reset_index()

gender_stats = df.groupby("Gender")["Amount"].sum().reset_index()

channel_stats = df.groupby("Channel")["Amount"].sum().reset_index()

order_status_stats = df["Status"].value_counts().reset_index()
order_status_stats.columns = ["Status", "Count"]

# Top values
top_channel = df.groupby("Channel")["Amount"].sum().idxmax()
top_state = state_stats.iloc[0]["ship-state"]
top_category = df.groupby("Category")["Amount"].sum().idxmax()

# ==============================
# SAVE TO EXCEL
# ==============================

excel_path = os.path.join(OUTPUT_DIR, "vrinda_analysis_report.xlsx")

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

    # Summary Sheet
    summary_data = {
        "Metric": [
            "Total Sales",
            "Total Orders",
            "Average Order Value",
            "Top Channel",
            "Top State",
            "Top Category"
        ],
        "Value": [
            total_sales,
            total_orders,
            avg_order_value,
            top_channel,
            top_state,
            top_category
        ]
    }

    pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)

    # Detailed Sheets
    df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
    monthly_stats.to_excel(writer, sheet_name="Monthly_Analysis", index=False)
    state_stats.to_excel(writer, sheet_name="State_Analysis", index=False)
    category_stats.to_excel(writer, sheet_name="Category_Analysis", index=False)
    gender_stats.to_excel(writer, sheet_name="Gender_Analysis", index=False)
    channel_stats.to_excel(writer, sheet_name="Channel_Analysis", index=False)
    order_status_stats.to_excel(writer, sheet_name="Order_Status", index=False)

print(f"Excel report saved successfully at: {excel_path}")
