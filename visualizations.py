import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA = "retail_customer_sales_dataset.csv"
OUT = "charts"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)
for c in ["Order_Date", "Delivery_Date"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")
for c in ["Gender","Region","Customer_Segment","Product_Category","Product",
          "Payment_Method","Delivery_Mode","Satisfaction_Level","Returned"]:
    df[c] = df[c].astype("string").str.strip().str.title()

df.loc[~df["Age"].between(0,100), "Age"] = np.nan
df.loc[df["Income"] < 0, "Income"] = np.nan
df.loc[df["Quantity"] <= 0, "Quantity"] = np.nan
df.loc[df["Unit_Price"] < 0, "Unit_Price"] = np.nan
df.loc[~df["Discount"].between(0,0.5), "Discount"] = np.nan
df.loc[~df["Customer_Rating"].between(1,5), "Customer_Rating"] = np.nan
df.loc[df["Delivery_Date"] < df["Order_Date"], "Delivery_Date"] = pd.NaT
df = df.drop_duplicates().drop_duplicates(subset=["Transaction_ID"], keep="first")
df["Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()

sns.set_theme(style="whitegrid")
P = ["#243B53", "#486581", "#829AB1", "#D9A441", "#C76D5D"]

def finish(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT,name), dpi=180, bbox_inches="tight")
    plt.close()

# 1 Monthly sales trend
m = df.groupby("Month")["Sales"].sum()
plt.figure(figsize=(10,5)); plt.plot(m.index,m.values,marker="o",color=P[0])
plt.title("Monthly Retail Sales Trend"); plt.xlabel("Month"); plt.ylabel("Sales (₹)"); plt.xticks(rotation=35); finish("01_monthly_sales_trend.png")

# 2 Sales by region
x=df.groupby("Region")["Sales"].sum().sort_values()
plt.figure(figsize=(8,5)); plt.barh(x.index,x.values,color=P[1])
plt.title("Total Sales by Region"); plt.xlabel("Sales (₹)"); plt.ylabel("Region"); finish("02_sales_by_region.png")

# 3 Sales by category
x=df.groupby("Product_Category")["Sales"].sum().sort_values()
plt.figure(figsize=(8,5)); plt.barh(x.index,x.values,color=P[1])
plt.title("Total Sales by Product Category"); plt.xlabel("Sales (₹)"); plt.ylabel("Category"); finish("03_sales_by_category.png")

# 4 Age histogram
plt.figure(figsize=(8,5)); sns.histplot(df["Age"].dropna(),bins=20,kde=True,color=P[1])
plt.title("Customer Age Distribution"); plt.xlabel("Age (years)"); plt.ylabel("Transactions"); finish("04_age_distribution.png")

# 5 Income histogram
plt.figure(figsize=(8,5)); sns.histplot(df["Income"].dropna(),bins=30,kde=True,color=P[3])
plt.title("Annual Customer Income Distribution"); plt.xlabel("Income (₹)"); plt.ylabel("Transactions"); finish("05_income_distribution.png")

# 6 Sales boxplot by category
plt.figure(figsize=(9,5)); sns.boxplot(data=df,x="Product_Category",y="Sales",palette=P)
plt.title("Sales Spread Across Product Categories"); plt.xlabel("Category"); plt.ylabel("Sales per transaction (₹)"); plt.xticks(rotation=20); finish("06_sales_boxplot_by_category.png")

# 7 Sales vs Profit
plt.figure(figsize=(8,5)); sns.regplot(data=df,x="Sales",y="Profit",scatter_kws={"alpha":.35,"s":18},line_kws={"color":P[4]})
plt.title("Relationship Between Sales and Profit"); plt.xlabel("Sales (₹)"); plt.ylabel("Profit (₹)"); finish("07_sales_vs_profit.png")

# 8 Discount vs Profit
plt.figure(figsize=(8,5)); sns.regplot(data=df,x="Discount",y="Profit",scatter_kws={"alpha":.35,"s":18},line_kws={"color":P[4]})
plt.title("Impact of Discount on Transaction Profit"); plt.xlabel("Discount rate"); plt.ylabel("Profit (₹)"); finish("08_discount_vs_profit.png")

# 9 Segment sales donut
x=df.groupby("Customer_Segment")["Sales"].sum()
plt.figure(figsize=(7,5)); plt.pie(x.values,labels=x.index,autopct="%1.1f%%",startangle=90,colors=P[:len(x)],wedgeprops={"width":.42})
plt.title("Share of Total Sales by Customer Segment"); finish("09_sales_share_by_segment.png")

# 10 Correlation heatmap
cols=["Sales","Profit","Discount","Quantity","Age","Income"]
plt.figure(figsize=(8,6)); sns.heatmap(df[cols].corr(),annot=True,fmt=".2f",cmap="vlag",center=0,square=True)
plt.title("Correlation Across Sales, Profit and Customer Variables"); finish("10_correlation_heatmap.png")

# 11 Average sales category-region heatmap
x=df.pivot_table(index="Product_Category",columns="Region",values="Sales",aggfunc="mean")
plt.figure(figsize=(8,5)); sns.heatmap(x,annot=True,fmt=".0f",cmap="YlGnBu")
plt.title("Average Sales by Product Category and Region"); plt.xlabel("Region"); plt.ylabel("Category"); finish("11_avg_sales_category_region_heatmap.png")

print(f"Generated 11 charts in {OUT}/")
