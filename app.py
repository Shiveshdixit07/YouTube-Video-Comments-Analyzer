import base64
from itertools import islice

import pandas as pd
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from youtube_comment_downloader import YoutubeCommentDownloader

st.set_page_config(
    page_title="YouTube Video Comments Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for inputs
st.sidebar.header("Input Section")
Url = st.sidebar.text_input("Enter YouTube Video Link:")
SampleLength = st.sidebar.text_input("Enter the length of the sample:")
search_button = st.sidebar.button("Analyze")


col1, col2 = st.columns([1, 20], gap="small")
with col1:
    # Load and encode the image
    with open("./image/2.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    st.markdown(
        f"""
        <style>
        .image-container {{
            display: flex;
            align-items: baseline;  /* Aligns image and text on the same baseline */
            height: 50px;  /* Adjust image height to match header text size */
            width:50px;
        }}
        .image-container img {{
            height: 50px;  /* Adjust image height to match header text size */
            width:50px;
        }}
        </style>
        <div class="image-container">
            <img src="data:image/png;base64,{encoded_image}" alt="YouTube Icon">
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 35px;
            font-weight: bold;
            color: #1f77b4;  
            margin: 0;  /* Removes default margin */
            padding: 0;  /* Removes default padding */
            display: flex;
            align-items: baseline;  /* Ensures text aligns with image */
        }
        </style>
        <div class="main-header">Video Comments Analyzer</div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("---")

if search_button and Url and SampleLength:
    with st.spinner("Fetching and analyzing comments..."):
        try:
            downloader = YoutubeCommentDownloader()
            SampleLength = int(SampleLength)
            data = []

            # Fetch comments
            comments = downloader.get_comments_from_url(Url)
            for comment in islice(comments, SampleLength):
                data.append(comment["text"])

            f = 1
            original_len = SampleLength
            if SampleLength > data.__len__():
                SampleLength = data.__len__()
                f = 0

            # Convert to DataFrame
            df = pd.DataFrame(data, columns=["Comments"])

            # Perform Sentiment Analysis
            sentiments = SentimentIntensityAnalyzer()
            positive = []
            negative = []
            neutral = []
            compound = []
            reviews = []

            for comment in df["Comments"]:
                score = sentiments.polarity_scores(comment)
                positive.append(score["pos"])
                negative.append(score["neg"])
                neutral.append(score["neu"])
                compound.append(score["compound"])

                if score["compound"] >= 0.05:
                    reviews.append("Positive")
                elif score["compound"] <= -0.05:
                    reviews.append("Negative")
                else:
                    reviews.append("Neutral")

            df["Positive"] = positive
            df["Negative"] = negative
            df["Neutral"] = neutral
            df["Compound"] = compound
            df["Review"] = reviews

            if f:
                st.subheader(f"Analyzed {SampleLength} Comments")
            else:
                st.subheader(
                    f"Analyzed {SampleLength} Comments Only( As Maximum Amount Of Comments are {SampleLength})"
                )

            # Display comments table
            st.dataframe(df[["Comments", "Review"]])

            # Chart
            st.subheader("Comments Review Distribution")
            review_counts = df["Review"].value_counts()
            st.bar_chart(
                review_counts,
                y_label="Number Of Comments",
                x_label="Review",
            )

            # Percentages
            total = len(df)
            positive_pct = round((review_counts.get("Positive", 0) / total) * 100, 2)
            neutral_pct = round((review_counts.get("Neutral", 0) / total) * 100, 2)
            negative_pct = round((review_counts.get("Negative", 0) / total) * 100, 2)

            st.subheader("Status")
            st.write(f"Positive Reviews(😊): **{positive_pct}%**")
            st.write(f"Neutral Reviews(😐): **{neutral_pct}%**")
            st.write(f"Negative Reviews(😔): **{negative_pct}%**")

        except Exception as e:
            st.error(f"An error occurred: {e}")
