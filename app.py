import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import pdist, squareform
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Backlog Insights Copilot",
    page_icon="🧭",
    layout="wide"
)

# Title
st.title("🧭 Backlog Insights Copilot")
st.markdown("**PM-first local app** for JIRA/Linear CSV analysis")

# Sidebar
st.sidebar.header("Settings")

# File upload
uploaded_file = st.file_uploader("Upload your issues CSV", type=['csv'])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    
    st.success(f"Loaded {len(df)} issues")
    
    # Display data preview
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Basic statistics
    st.subheader("📊 Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Issues", len(df))
    
    with col2:
        if 'status' in df.columns:
            st.metric("Unique Statuses", df['status'].nunique())
    
    with col3:
        if 'priority' in df.columns:
            st.metric("Unique Priorities", df['priority'].nunique())
    
    # Clustering section
    if st.sidebar.checkbox("Run Clustering", value=True):
        st.subheader("🧩 Topic Clusters")
        
        n_clusters = st.sidebar.slider("Number of clusters", 2, 10, 5)
        
        if 'title' in df.columns and 'description' in df.columns:
            # Combine text
            df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            X = vectorizer.fit_transform(df['combined_text'])
            
            # Clustering
            kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
            df['cluster'] = kmeans.fit_predict(X)
            
            # Display clusters
            for i in range(n_clusters):
                cluster_df = df[df['cluster'] == i]
                with st.expander(f"Cluster {i+1} ({len(cluster_df)} issues)"):
                    st.dataframe(cluster_df[['title', 'priority', 'status']].head(10))
    
    # RICE/WSJF Scoring
    if st.sidebar.checkbox("Calculate RICE/WSJF", value=True):
        st.subheader("📈 Prioritization Scores")
        
        # Default values
        reach = st.sidebar.number_input("Default Reach", 1, 100, 50)
        impact = st.sidebar.number_input("Default Impact", 1, 10, 5)
        confidence = st.sidebar.number_input("Default Confidence %", 1, 100, 80)
        
        if 'story_points' in df.columns:
            df['RICE'] = (reach * impact * (confidence/100)) / df['story_points'].fillna(1)
            st.dataframe(df[['title', 'story_points', 'RICE']].sort_values('RICE', ascending=False).head(10))
    
    # Export functionality
    if st.sidebar.button("Export Results"):
        # Create exports directory
        Path('exports').mkdir(exist_ok=True)
        
        # Export CSV
        output_file = 'exports/processed_issues.csv'
        df.to_csv(output_file, index=False)
        st.success(f"Exported to {output_file}")
        
        # Download button
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='processed_issues.csv',
            mime='text/csv'
        )
else:
    st.info("👆 Upload a CSV file to get started")
    st.markdown("### Expected columns:")
    st.markdown("- `id`, `title`, `description`, `priority`, `status`, `story_points`, `created_at`")
