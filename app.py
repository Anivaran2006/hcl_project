import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Sales Intelligence", page_icon="📊", layout="wide")
st.markdown("""
<style>
.main {background:#f5f7fb}
[data-testid="stMetric"] {background:white;padding:16px;border:1px solid #e3e8ef;border-radius:12px}
h1,h2,h3 {color:#243B53}
</style>
""", unsafe_allow_html=True)
st.title("Retail Sales Intelligence")
st.caption("An interactive view of sales, profitability and customer patterns")

@st.cache_data
def load_data():
    d=pd.read_csv("retail_customer_sales_cleaned.csv")
    d["Order_Date"]=pd.to_datetime(d["Order_Date"],errors="coerce")
    return d
df=load_data()

with st.sidebar:
    st.header("Filters")
    years=sorted(df["Order_Date"].dt.year.dropna().unique().tolist())
    selected_years=st.multiselect("Year",years,default=years)
    regions=sorted(df["Region"].dropna().unique().tolist())
    selected_regions=st.multiselect("Region",regions,default=regions)
    cats=sorted(df["Product_Category"].dropna().unique().tolist())
    selected_cats=st.multiselect("Product category",cats,default=cats)

f=df[df["Order_Date"].dt.year.isin(selected_years)]
f=f[f["Region"].isin(selected_regions)]
f=f[f["Product_Category"].isin(selected_cats)]
if f.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

sales=f["Sales"].sum()
profit=f["Profit"].sum()
margin=(profit/sales*100) if sales else 0
aov=f["Sales"].mean()
c1,c2,c3,c4=st.columns(4)
c1.metric("Total Sales",f"₹{sales:,.0f}")
c2.metric("Total Profit",f"₹{profit:,.0f}")
c3.metric("Profit Margin",f"{margin:.1f}%")
c4.metric("Average Order Value",f"₹{aov:,.0f}")

left,right=st.columns(2)
monthly=f.dropna(subset=["Order_Date"]).groupby(f["Order_Date"].dt.to_period("M").astype(str))["Sales"].sum().reset_index()
monthly.columns=["Month","Sales"]
left.subheader("Monthly sales trend")
left.plotly_chart(px.line(monthly,x="Month",y="Sales",markers=True,template="plotly_white"),use_container_width=True)
region=f.groupby("Region",as_index=False)["Sales"].sum().sort_values("Sales",ascending=False)
right.subheader("Sales by region")
right.plotly_chart(px.bar(region,x="Region",y="Sales",color="Region",template="plotly_white"),use_container_width=True)

left,right=st.columns(2)
category=f.groupby("Product_Category",as_index=False)["Sales"].sum()
left.subheader("Sales by product category")
left.plotly_chart(px.bar(category,x="Product_Category",y="Sales",color="Product_Category",template="plotly_white"),use_container_width=True)
seg=f.groupby("Customer_Segment",as_index=False)["Sales"].sum()
right.subheader("Customer segment mix")
right.plotly_chart(px.pie(seg,names="Customer_Segment",values="Sales",hole=.55,template="plotly_white"),use_container_width=True)

st.subheader("Transaction-level relationship")
st.plotly_chart(px.scatter(f,x="Sales",y="Profit",color="Product_Category",hover_data=["Region","Customer_Segment"],template="plotly_white"),use_container_width=True)
st.caption("All figures respond to the selected Year, Region and Product Category filters.")
