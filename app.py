import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------
# Load data
df = pd.read_csv(r"processedstreamlit_data.csv")

# ---------------------------------------
# Sidebar filters
st.sidebar.title("Filters")

segments = df['market_segment'].unique()
selected_segment = st.sidebar.selectbox("Select Market Segment", segments)

tiers = df['customer_tier'].unique()
selected_tier = st.sidebar.selectbox("Select Customer Tier", tiers)

# Filter data
filtered_segment = df[df['market_segment'] == selected_segment]
filtered_segment_tier = filtered_segment[filtered_segment['customer_tier'] == selected_tier]

# ---------------------------------------
st.title("Hotel Booking Interactive Dashboard")

# Use consistent palette
main_palette = "Set2"

# ---------------------------------------
# 1 & 2 side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Daily Rate vs Revenue")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=df, x='avg_daily_rate', y='target_value', alpha=0.6, ax=ax1, color='teal')
    ax1.set_xlabel("Average Daily Rate")
    ax1.set_ylabel("Revenue (Target Value)")
    st.pyplot(fig1)

with col2:
    st.subheader("Average Daily Rate vs Competitor Rate")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=df, x='avg_daily_rate', y='competitor_rate', alpha=0.6, ax=ax2, color='teal')
    ax2.set_xlabel("Average Daily Rate")
    ax2.set_ylabel("Competitor Rate")
    st.pyplot(fig2)

# ---------------------------------------
# 3 & 4 side by side
col3, col4 = st.columns([2,1])

with col3:
    st.subheader(f"Revenue by Customer Tier for {selected_segment}")
    revenue_by_tier = filtered_segment.groupby('customer_tier')['target_value'].sum().reset_index()
    revenue_by_tier = revenue_by_tier.sort_values(by='target_value', ascending=False)

    fig3, ax3 = plt.subplots()
    sns.barplot(data=revenue_by_tier, x='customer_tier', y='target_value', ax=ax3, palette=main_palette)
    ax3.set_xlabel("Customer Tier")
    ax3.set_ylabel("Total Revenue")
    ax3.set_title("Sorted Revenue by Customer Tier")

    for i, v in enumerate(revenue_by_tier['target_value']):
        ax3.text(i, v + 0.01*max(revenue_by_tier['target_value']), f"{v:.0f}", ha='center')

    st.pyplot(fig3)

with col4:
    st.markdown("### Insights")
    st.info(
        f"""
        - Bronze remains the top tier for revenue across all segements
        - Useful to design targeted loyalty programs and promotions in tiers that generate less revenue.
        """
    )
    st.success("Use the sidebar to explore other Market Segments.")

# ---------------------------------------
# Revenue by Channel filtered by selected tier
st.subheader(f"Revenue by Channel for {selected_segment} - {selected_tier} customers")

col5, col6 = st.columns([2,1])

with col5:
    if filtered_segment_tier.empty:
        st.warning("No data available for this combination.")
    else:
        revenue_by_channel = filtered_segment_tier.groupby('channel')['target_value'].sum().reset_index()
        revenue_by_channel = revenue_by_channel.sort_values(by='target_value', ascending=False)

        fig5, ax5 = plt.subplots()
        sns.barplot(data=revenue_by_channel, x='channel', y='target_value', ax=ax5, palette=main_palette)
        ax5.set_xlabel("Distribution Channel")
        ax5.set_ylabel("Total Revenue")
        ax5.set_title(f"Revenue by Channel for {selected_tier} in {selected_segment}")

        for i, v in enumerate(revenue_by_channel['target_value']):
            ax5.text(i, v + 0.01*max(revenue_by_channel['target_value']), f"{v:.0f}", ha='center')

        st.pyplot(fig5)

with col6:
    if selected_segment == "Group":
        st.info("Group bookings often channel through agencies or corporate partners. "
                "Consider negotiating bulk deals for higher revenue.")

# ---------------------------------------
# Loyalty Points vs Revenue with insight below
st.subheader("Impact of Loyalty Points on Revenue")

df['loyalty_bin'] = pd.cut(df['loyalty_points'], bins=[0,1000,5000,10000,20000,50000], 
                           labels=["0-1k","1k-5k","5k-10k","10k-20k","20k-50k"])

loyalty_revenue = df.groupby('loyalty_bin')['target_value'].mean().reset_index()

fig6, ax6 = plt.subplots()
sns.barplot(data=loyalty_revenue, x='loyalty_bin', y='target_value', palette=main_palette, ax=ax6)
ax6.set_xlabel("Loyalty Points Bin")
ax6.set_ylabel("Average Revenue")
ax6.set_title("Higher Loyalty Points Drive Higher Revenue")

for i, v in enumerate(loyalty_revenue['target_value']):
    ax6.text(i, v + 0.01*max(loyalty_revenue['target_value']), f"{v:.0f}", ha='center')

st.pyplot(fig6)

st.success(
    "Insight: No major significant impact of loyalty points"
)

# ---------------------------------------
# New: Nights Staying vs Revenue scatter plot
st.subheader("Revenue by Number of Nights Staying")

fig7, ax7 = plt.subplots(figsize=(10, 6))
ax7.scatter(df['stay_nights'], df['target_value'], color='teal', alpha=0.7, edgecolors='w')
ax7.set_title("Realized Revenue by Nights Staying")
ax7.set_xlabel("Nights Staying")
ax7.set_ylabel("Revenue")
ax7.grid(True)

st.pyplot(fig7)

st.info(
    "Longer stays generally lead to higher revenue, though there can be variability. "
    "Promotions for extended stays might increase total booking value."
)
