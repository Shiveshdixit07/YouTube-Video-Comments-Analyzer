import base64
from itertools import islice
import re
import pandas as pd
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from youtube_comment_downloader import YoutubeCommentDownloader
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="YouTube Comments Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None

st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(238, 90, 36, 0.3);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .youtube-icon {
        font-size: 3rem;
        margin-right: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        margin: 0.5rem 0;
    }
    
    .positive-metric {
        border-left-color: #2ecc71;
        background: linear-gradient(135deg, #a8e6cf, #dcedc8);
    }
    
    .neutral-metric {
        border-left-color: #f39c12;
        background: linear-gradient(135deg, #ffd93d, #fff176);
    }
    
    .negative-metric {
        border-left-color: #e74c3c;
        background: linear-gradient(135deg, #ffab91, #ffcdd2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        margin: 0.5rem 0;
        opacity: 0.8;
    }
    
    .status-container {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(9, 132, 227, 0.3);
    }
    
    .sidebar .stButton > button {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .sidebar .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 184, 148, 0.4);
    }
    
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .instruction-box {
        background: linear-gradient(135deg, #a29bfe, #6c5ce7);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .success-box {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="youtube-icon">🎥</div>
    <h1 class="main-title">YouTube Comments Analyzer</h1>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔧 Configuration Panel")
    st.markdown("---")
    
    url_input = st.text_input(
        "📺 YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste your YouTube video link here"
    )
    
    sample_length = st.number_input(
        "📊 Sample Size",
        min_value=1,
        max_value=1000,
        value=50,
        step=10,
        help="Number of comments to analyze (1-1000)"
    )
    
    st.markdown("---")
    analyze_button = st.button("🚀 Analyze Comments", type="primary")
    
    st.markdown("---")
    st.markdown("""
    ### 💡 How to Use
    1. **Paste** your YouTube video URL
    2. **Select** the number of comments to analyze
    3. **Click** the Analyze button
    4. **View** the sentiment analysis results
    """)

if not analyze_button:
    st.markdown("""
    <div class="instruction-box">
        <h3>🎯 Welcome to YouTube Comments Analyzer!</h3>
        <p>Discover the sentiment behind any YouTube video's comments with advanced AI analysis.</p>
        <p><strong>Ready to start?</strong> Enter a YouTube URL in the sidebar and click 'Analyze Comments'</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-container positive-metric">
            <div class="metric-value">😊</div>
            <div class="metric-label">Positive Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container neutral-metric">
            <div class="metric-value">😐</div>
            <div class="metric-label">Neutral Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container negative-metric">
            <div class="metric-value">😔</div>
            <div class="metric-label">Negative Sentiment</div>
        </div>
        """, unsafe_allow_html=True)

elif not url_input:
    st.markdown("""
    <div class="error-box">
        <h3>⚠️ Missing YouTube URL</h3>
        <p>Please enter a valid YouTube video URL in the sidebar to continue.</p>
    </div>
    """, unsafe_allow_html=True)

elif not is_valid_youtube_url(url_input):
    st.markdown("""
    <div class="error-box">
        <h3>❌ Invalid YouTube URL</h3>
        <p>Please enter a valid YouTube video URL (e.g., https://www.youtube.com/watch?v=...)</p>
    </div>
    """, unsafe_allow_html=True)

else:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔍 Initializing comment downloader...")
        progress_bar.progress(0.1)
        
        downloader = YoutubeCommentDownloader()
        
        status_text.text("📥 Fetching comments from YouTube...")
        progress_bar.progress(0.3)
        
        data = []
        comments = downloader.get_comments_from_url(url_input)
        
        for i, comment in enumerate(islice(comments, sample_length)):
            data.append(comment["text"])
            if i % 10 == 0:
                progress_bar.progress(0.3 + (i / sample_length) * 0.4)
        
        actual_sample_length = len(data)
        df = pd.DataFrame(data, columns=["Comments"])
        
        status_text.text("🧠 Performing sentiment analysis...")
        progress_bar.progress(0.8)
        
        sentiments = SentimentIntensityAnalyzer()
        positive_scores = []
        negative_scores = []
        neutral_scores = []
        compound_scores = []
        reviews = []
        
        for i, comment in enumerate(df["Comments"]):
            score = sentiments.polarity_scores(comment)
            positive_scores.append(score["pos"])
            negative_scores.append(score["neg"])
            neutral_scores.append(score["neu"])
            compound_scores.append(score["compound"])
            
            if score["compound"] >= 0.05:
                reviews.append("Positive")
            elif score["compound"] <= -0.05:
                reviews.append("Negative")
            else:
                reviews.append("Neutral")
            
            if i % 5 == 0:
                progress_bar.progress(0.8 + (i / len(df)) * 0.15)
        
        df["Positive"] = positive_scores
        df["Negative"] = negative_scores
        df["Neutral"] = neutral_scores
        df["Compound"] = compound_scores
        df["Review"] = reviews
        
        progress_bar.progress(1.0)
        status_text.text("✅ Analysis complete!")
        
        st.balloons()
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎉 Analysis Complete!</h3>
            <p>Successfully analyzed <strong>{actual_sample_length}</strong> comments from the video</p>
        </div>
        """, unsafe_allow_html=True)
        
        review_counts = df["Review"].value_counts()
        total = len(df)
        positive_pct = round((review_counts.get("Positive", 0) / total) * 100, 2)
        neutral_pct = round((review_counts.get("Neutral", 0) / total) * 100, 2)
        negative_pct = round((review_counts.get("Negative", 0) / total) * 100, 2)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container positive-metric">
                <div class="metric-value">{positive_pct}%</div>
                <div class="metric-label">😊 Positive ({review_counts.get("Positive", 0)} comments)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container neutral-metric">
                <div class="metric-value">{neutral_pct}%</div>
                <div class="metric-label">😐 Neutral ({review_counts.get("Neutral", 0)} comments)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container negative-metric">
                <div class="metric-value">{negative_pct}%</div>
                <div class="metric-label">😔 Negative ({review_counts.get("Negative", 0)} comments)</div>
            </div>
            """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📊 Visualization", "📋 Comments Data", "📈 Detailed Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    values=review_counts.values,
                    names=review_counts.index,
                    title="Sentiment Distribution",
                    color_discrete_map={
                        'Positive': '#2ecc71',
                        'Neutral': '#f39c12',
                        'Negative': '#e74c3c'
                    }
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    title_font_size=20,
                    font=dict(size=14),
                    showlegend=True
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(
                    x=review_counts.index,
                    y=review_counts.values,
                    title="Comment Count by Sentiment",
                    color=review_counts.index,
                    color_discrete_map={
                        'Positive': '#2ecc71',
                        'Neutral': '#f39c12',
                        'Negative': '#e74c3c'
                    }
                )
                fig_bar.update_layout(
                    title_font_size=20,
                    xaxis_title="Sentiment",
                    yaxis_title="Number of Comments",
                    font=dict(size=14),
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            st.markdown("### 💬 Comments and Their Sentiments")
            
            
            filtered_df = df
            
            display_df = filtered_df[["Comments", "Review", "Compound"]].copy()
            display_df = display_df.drop("Compound", axis=1)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Comments": st.column_config.TextColumn("Comment", width="large"),
                    "Review": st.column_config.TextColumn("Sentiment", width="small")
                    
                }
            )
        
        with tab3:
            st.markdown("### 📊 Statistical Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_compound = df["Compound"].mean()
                sentiment_interpretation = ""
                if avg_compound >= 0.05:
                    sentiment_interpretation = "Overall Positive 😊"
                elif avg_compound <= -0.05:
                    sentiment_interpretation = "Overall Negative 😔"
                else:
                    sentiment_interpretation = "Overall Neutral 😐"
                
                st.markdown(f"""
                <div class="status-container">
                    <h4>📈 Overall Sentiment Score</h4>
                    <p style="font-size: 1.5rem; margin: 0;"><strong>{avg_compound:.3f}</strong></p>
                    <p style="color: white; font-weight: bold;">{sentiment_interpretation}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                most_common_sentiment = review_counts.index[0]
                most_common_count = review_counts.iloc[0]
                most_common_pct = round((most_common_count / total) * 100, 1)
                
                emoji_map = {"Positive": "😊", "Neutral": "😐", "Negative": "😔"}
                
                st.markdown(f"""
                <div class="status-container">
                    <h4>🏆 Dominant Sentiment</h4>
                    <p style="font-size: 1.5rem; margin: 0;">{emoji_map[most_common_sentiment]} <strong>{most_common_sentiment}</strong></p>
                    <p>{most_common_count} comments ({most_common_pct}%)</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_histogram = px.histogram(
                df,
                x="Compound",
                nbins=20,
                title="Distribution of Sentiment Scores",
                color_discrete_sequence=['#667eea']
            )
            fig_histogram.update_layout(
                title_font_size=20,
                xaxis_title="Compound Sentiment Score",
                yaxis_title="Number of Comments",
                font=dict(size=14)
            )
            st.plotly_chart(fig_histogram, use_container_width=True)
        
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.markdown(f"""
        <div class="error-box">
            <h3>❌ Analysis Failed</h3>
            <p>An error occurred while analyzing the comments: <strong>{str(e)}</strong></p>
            <p>Please check your YouTube URL and try again.</p>
        </div>
        """, unsafe_allow_html=True)