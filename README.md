# YouTube Video Comments Analyzer

## Overview

A Python-based project leveraging Natural Language Processing (NLP) and Streamlit to analyze the sentiment of comments on a YouTube video. This tool categorizes comments into Positive, Negative, or Neutral sentiments and provides detailed visual insights.

---

## Features

- **Input Section**:
  - Accepts the YouTube video link to fetch comments.
  - Allows users to specify the sample length (number of comments to analyze).
- **Sentiment Analysis**:
  - Analyzes each comment and classifies it as Positive, Negative, or Neutral.
- **Visualization**:
  - Displays a bar chart for sentiment distribution, showing:
    - Sentiments (Positive, Negative, Neutral) on the horizontal axis.
    - Number of comments on the vertical axis.
- **Summary Status**:
  - Provides the percentage distribution of Positive, Negative, and Neutral reviews.

---

## How It Works

1. **Input Section**:
   - Paste the YouTube video link into the input field.
   - Specify the sample length (e.g., analyze the first 100 comments).
2. **Analyze**:
   - Click the `Analyze` button.
   - The application fetches the specified number of comments from the video.
   - Each comment is analyzed for sentiment.
3. **Results**:
   - Displays comments alongside their respective sentiment (Positive, Negative, or Neutral).
   - Shows a bar chart visualizing the sentiment distribution.
   - Displays a summary of the sentiment analysis in percentages.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shiveshdixit07/YouTube-Video-Comments-Analyzer.git
   cd YouTube-Video-Comments-Analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Technologies Used

- **Python**: For backend and logic.
- **Natural Language Processing (NLP)**: To analyze and classify sentiments.
- **Streamlit**: For an interactive and user-friendly UI.

---

## Example Usage

1. Paste a YouTube video link in the input field.
2. Specify a sample length (e.g., 100 comments).
3. Click `Analyze` to view:
   - Sentiment classification for each comment.
   - Sentiment distribution bar chart.
   - Status summary of Positive, Negative, and Neutral reviews.

---

## Future Enhancements

- Add support for analyzing replies to comments.
- Improve visualization with more chart options.
- Provide downloadable reports.

---

## Contact

For queries or support, please reach out to [shiveshdixit8400@gmail.com](mailto:shiveshdixit8400@gmail.com).


