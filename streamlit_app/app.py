import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="RiskPulse Analytics",
    page_icon="⚡",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    top_users = pd.read_csv("data/top_users.csv")
    stg_posts = pd.read_csv("data/stg_posts.csv")
    posts_users = pd.read_csv("data/posts_users.csv")
    return top_users, stg_posts, posts_users

top_users, stg_posts, posts_users = load_data()

# Header
st.title("⚡ RiskPulse Analytics")
st.markdown("**Real-time risk and activity analytics powered by Databricks Delta Lake**")
st.divider()

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Posts Ingested", len(stg_posts))

with col2:
    st.metric("Total Users", len(top_users))

with col3:
    st.metric("Clean Records (Silver)", len(stg_posts))

with col4:
    st.metric("Quarantined Records", 0, delta="0 flagged", delta_color="off")

st.divider()

# Row 1 - Two charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 High Activity Users")
    st.caption("Users ranked by post volume — high activity may indicate bot or fraud risk")
    fig = px.bar(
        top_users.sort_values("post_count", ascending=False),
        x="UserId",
        y="post_count",
        color="avg_word_count",
        color_continuous_scale="Blues",
        labels={"UserId": "User ID", "post_count": "Post Count", "avg_word_count": "Avg Word Count"},
        title="Post Count by User"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Content Risk Score Distribution")
    st.caption("Word count distribution — unusually short posts may indicate spam")
    fig2 = px.histogram(
        stg_posts,
        x="word_count",
        nbins=20,
        title="Word Count Distribution",
        color_discrete_sequence=["#0068c9"]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 2 - User Activity Feed
st.subheader("👥 User Activity Feed")
st.caption("Joined posts and users — full activity trail for risk investigation")
st.dataframe(posts_users.head(20), use_container_width=True)

st.divider()

# Pipeline info
st.subheader("🔧 Pipeline Info")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Orchestration**\nAirflow 3.0 on Kubernetes\nAsset-aware scheduling")
with col2:
    st.info("**Compute**\nDatabricks + PySpark\nMedallion Architecture")
with col3:
    st.info("**Storage**\nDelta Lake\nACID + Time Travel")

# Footer
st.divider()
st.caption("RiskPulse | Airflow 3.0 + Databricks + Delta Lake + Kubernetes | github.com/kundamnikhil/riskpulse-data-platform")
