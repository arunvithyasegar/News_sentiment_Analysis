import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import datetime
import time
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, visualize_sentiment

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Set page configuration
st.set_page_config(
    page_title="News Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f7ff 0%, #e1f5fe 100%);
        border-radius: 10px;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #555;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #1E88E5;
        margin-bottom: 1.5rem;
    }
    .card {
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .positive-card {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
    }
    .neutral-card {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .negative-card {
        background-color: #ffebee;
        border-left: 5px solid #F44336;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f5f5f5;
        border-radius: 0.5rem;
    }
    .stDataFrame {
        border-radius: 0.5rem;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("<div class='main-header'>News Sentiment Analysis Dashboard</div>", unsafe_allow_html=True)
st.markdown("### GUIDANCE – BIU TEAM ASSIGNMENT")
st.markdown("<p style='text-align: center; font-style: italic;'>Submitted by: Candidate Name - May 2025</p>", unsafe_allow_html=True)

# Sidebar for navigation and settings
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Section",
    ["Home", "News Sentiment Analysis", "Advanced Analytics", "About"]
)

# Add a theme selector in the sidebar
st.sidebar.title("Dashboard Settings")
theme = st.sidebar.selectbox(
    "Select Theme",
    ["Light", "Dark", "Blue", "Green"]
)

# Apply selected theme
if theme == "Dark":
    st.markdown("""
    <style>
        .main-header { background: linear-gradient(90deg, #2c3e50 0%, #1a2a38 100%); color: white; }
        .highlight { background-color: #2c3e50; border-left: 0.5rem solid #3498db; color: white; }
        .stButton>button { background-color: #3498db; }
        .stButton>button:hover { background-color: #2980b9; }
    </style>
    """, unsafe_allow_html=True)
elif theme == "Blue":
    st.markdown("""
    <style>
        .main-header { background: linear-gradient(90deg, #e1f5fe 0%, #b3e5fc 100%); }
        .highlight { background-color: #e1f5fe; border-left: 0.5rem solid #03a9f4; }
        .stButton>button { background-color: #03a9f4; }
        .stButton>button:hover { background-color: #0288d1; }
    </style>
    """, unsafe_allow_html=True)
elif theme == "Green":
    st.markdown("""
    <style>
        .main-header { background: linear-gradient(90deg, #e8f5e9 0%, #c8e6c9 100%); }
        .highlight { background-color: #e8f5e9; border-left: 0.5rem solid #4caf50; }
        .stButton>button { background-color: #4caf50; }
        .stButton>button:hover { background-color: #388e3c; }
    </style>
    """, unsafe_allow_html=True)

# Home Page
if page == "Home":
    st.markdown("<div class='sub-header'>Welcome to the Dashboard</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    <h3>Assignment Overview</h3>
    This interactive dashboard is developed as part of the GUIDANCE – BIU TEAM ASSIGNMENT, focusing on:
    <ul>
        <li><b>Web Scraping</b>: Collecting news headlines from publicly accessible sources related to electronics, semiconductors, and manufacturing</li>
        <li><b>Sentiment Analysis</b>: Analyzing the sentiment of news headlines using advanced NLP techniques</li>
        <li><b>Interactive Visualization</b>: Presenting insights through dynamic and interactive charts</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🌐 Web Scraping</h3>
            <p>Collect the latest business headlines from multiple sources including NewsAPI, Reuters, and Bloomberg.</p>
            <p>Extract title, URL, timestamp, and country mentions from each article.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🧠 Sentiment Analysis</h3>
            <p>Analyze headline sentiment using VADER and TextBlob to classify as positive, neutral, or negative.</p>
            <p>Compare sentiment scores across different news sources and topics.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="card">
            <h3>📊 Interactive Visualization</h3>
            <p>Explore sentiment distribution through interactive charts and graphs.</p>
            <p>Generate word clouds to identify key topics and themes in the news.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Instructions</div>", unsafe_allow_html=True)
    st.markdown("""
    - Use the sidebar to navigate between different sections
    - In the News Sentiment Analysis section:
        - Select a news source and enter keywords
        - View scraped headlines and their sentiment analysis
        - Explore interactive visualizations of sentiment distribution
    - In the Advanced Analytics section:
        - Discover trends and patterns in news sentiment
        - Analyze word frequency and topic distribution
        - Compare sentiment across different sources and time periods
    """)
    
    # Sample visualization for the home page
    st.markdown("<div class='section-header'>Dashboard Preview</div>", unsafe_allow_html=True)
    
    # Create a more attractive preview with tabs
    tab1, tab2 = st.tabs(["Sentiment Analysis", "Word Cloud"])
    
    with tab1:
        # Sample data for sentiment distribution
        sample_data = {
            'Sentiment': ['Positive', 'Neutral', 'Negative', 'Positive', 'Neutral', 
                         'Positive', 'Negative', 'Neutral', 'Positive', 'Negative'],
            'Score': [0.75, 0.12, -0.56, 0.68, 0.05, 0.82, -0.63, 0.22, 0.58, -0.48],
            'Source': ['Reuters', 'Bloomberg', 'CNBC', 'TechCrunch', 'WSJ', 
                      'Reuters', 'Bloomberg', 'CNBC', 'TechCrunch', 'WSJ']
        }
        df = pd.DataFrame(sample_data)
        
        # Create an interactive Plotly chart
        fig = px.histogram(df, x='Sentiment', color='Sentiment',
                          color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                          title='Sample Sentiment Distribution')
        fig.update_layout(bargap=0.2, xaxis_title='Sentiment Category', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Sample text for word cloud
        text = """
        Semiconductor manufacturing global supply chain electronics technology innovation
        chip production shortage supply demand market growth industry development
        AI artificial intelligence automation robotics smart devices IoT internet of things
        digital transformation cloud computing data analytics business technology trends
        """
        
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                             colormap='viridis', max_words=100).generate(text)
        
        # Display the word cloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

# News Sentiment Analysis Page
elif page == "News Sentiment Analysis":
    st.markdown("<div class='sub-header'>News Sentiment Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    This section allows you to scrape and analyze news headlines from various sources. 
    Select a news source, enter keywords related to electronics, semiconductors, or manufacturing, 
    and specify the number of articles to analyze.
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for input controls
    col1, col2 = st.columns(2)
    
    with col1:
        # Options for news sources
        news_source = st.selectbox(
            "Select News Source",
            ["NewsAPI", "Reuters", "Bloomberg", "Manual Input"]
        )
        
        # Keywords for filtering news
        keywords = st.text_input(
            "Enter keywords for news filtering (comma-separated)",
            value="electronics, semiconductors, manufacturing"
        )
    
    with col2:
        # Number of articles to fetch
        num_articles = st.slider(
            "Number of articles to analyze",
            min_value=5,
            max_value=50,
            value=20
        )
        
        # Add date range filter
        today = datetime.date.today()
        date_range = st.date_input(
            "Select date range (if supported by source)",
            value=(today - datetime.timedelta(days=7), today),
            max_value=today
        )
    
    # Button to fetch and analyze news
    fetch_button = st.button("Fetch and Analyze News", key="fetch_analyze_button", 
                           help="Click to scrape news headlines and analyze sentiment")
    
    if fetch_button:
        with st.spinner("Fetching news and analyzing sentiment..."):
            # Add a progress bar for better UX
            progress_bar = st.progress(0)
            
            # Scrape news based on selected source
            if news_source == "Manual Input":
                st.markdown("<div class='section-header'>Enter News Headlines Manually</div>", unsafe_allow_html=True)
                
                # Create a form for manual input
                with st.form("manual_news_form"):
                    manual_news = st.text_area(
                        "Enter news headlines (one per line)",
                        height=200,
                        help="Enter one headline per line. You can add URL, timestamp, and country after the headline, separated by commas."
                    )
                    
                    submit_button = st.form_submit_button("Analyze Entered Headlines")
                
                if submit_button and manual_news:
                    # Process manual input
                    news_data = []
                    for i, line in enumerate(manual_news.strip().split('\n')):
                        # Update progress
                        progress_bar.progress((i + 1) / len(manual_news.strip().split('\n')))
                        
                        parts = [part.strip() for part in line.split(',')]
                        title = parts[0]
                        url = parts[1] if len(parts) > 1 else "N/A"
                        timestamp = parts[2] if len(parts) > 2 else "N/A"
                        country = parts[3] if len(parts) > 3 else "N/A"
                        
                        news_data.append({
                            'title': title,
                            'url': url,
                            'timestamp': timestamp,
                            'country': country
                        })
                    
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Complete progress
                    progress_bar.progress(100)
                    
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["Data Table", "Sentiment Distribution", "Word Cloud"])
                    
                    with tab1:
                        # Display results
                        st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                        
                        # Create a DataFrame for display
                        results_df = pd.DataFrame(sentiment_results)
                        
                        # Add sentiment color highlighting
                        def highlight_sentiment(val):
                            if val == 'Positive':
                                return 'background-color: #e8f5e9; color: #2e7d32'
                            elif val == 'Negative':
                                return 'background-color: #ffebee; color: #c62828'
                            else:
                                return 'background-color: #e3f2fd; color: #1565c0'
                        
                        # Apply styling
                        styled_df = results_df.style.applymap(highlight_sentiment, subset=['sentiment'])
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Add download button
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="news_sentiment_analysis.csv",
                            mime="text/csv"
                        )
                    
                    with tab2:
                        # Visualize sentiment distribution
                        st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                        
                        # Create interactive Plotly visualization
                        sentiment_counts = pd.DataFrame(results_df['sentiment'].value_counts()).reset_index()
                        sentiment_counts.columns = ['Sentiment', 'Count']
                        
                        fig = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                                    color='Sentiment',
                                    color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                                    hole=0.4)
                        
                        fig.update_layout(
                            title_text='Sentiment Distribution of News Headlines',
                            annotations=[dict(text='Sentiment', x=0.5, y=0.5, font_size=20, showarrow=False)]
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add a bar chart with sentiment scores
                        fig2 = px.bar(results_df, x='title', y='sentiment_score', color='sentiment',
                                     color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                                     labels={'title': 'Headline', 'sentiment_score': 'Sentiment Score'})
                        
                        fig2.update_layout(
                            title_text='Sentiment Scores by Headline',
                            xaxis_tickangle=-45,
                            xaxis_title='Headlines',
                            yaxis_title='Sentiment Score'
                        )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    with tab3:
                        # Generate word cloud from headlines
                        st.markdown("<div class='section-header'>Word Cloud of Headlines</div>", unsafe_allow_html=True)
                        
                        # Combine all headlines
                        all_headlines = ' '.join(results_df['title'].tolist())
                        
                        # Tokenize and remove stopwords
                        stop_words = set(stopwords.words('english'))
                        word_tokens = word_tokenize(all_headlines.lower())
                        filtered_text = [word for word in word_tokens if word.isalpha() and word not in stop_words]
                        
                        # Generate word cloud
                        if filtered_text:
                            wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                                colormap='viridis', max_words=100).generate(' '.join(filtered_text))
                            
                            # Display the word cloud
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                        else:
                            st.warning("Not enough text to generate a word cloud.")
            else:
                # Scrape news from selected source
                for i in range(5):  # Simulate progress
                    progress_bar.progress(i * 20)
                    time.sleep(0.1)
                
                news_data = scrape_news(news_source, keywords.split(','), num_articles)
                
                # Complete progress
                progress_bar.progress(100)
                
                if news_data:
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["Data Table", "Sentiment Distribution", "Word Cloud", "Source Analysis"])
                    
                    with tab1:
                        # Display results
                        st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                        
                        # Create a DataFrame for display
                        results_df = pd.DataFrame(sentiment_results)
                        
                        # Add sentiment color highlighting
                        def highlight_sentiment(val):
                            if val == 'Positive':
                                return 'background-color: #e8f5e9; color: #2e7d32'
                            elif val == 'Negative':
                                return 'background-color: #ffebee; color: #c62828'
                            else:
                                return 'background-color: #e3f2fd; color: #1565c0'
                        
                        # Apply styling
                        styled_df = results_df.style.applymap(highlight_sentiment, subset=['sentiment'])
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Add download button
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="news_sentiment_analysis.csv",
                            mime="text/csv"
                        )
                    
                    with tab2:
                        # Visualize sentiment distribution
                        st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                        
                        # Create interactive Plotly visualization
                        sentiment_counts = pd.DataFrame(results_df['sentiment'].value_counts()).reset_index()
                        sentiment_counts.columns = ['Sentiment', 'Count']
                        
                        # Create a subplot with two charts
                        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]],
                                          subplot_titles=("Sentiment Distribution", "Sentiment Count"))
                        
                        # Add pie chart
                        fig.add_trace(
                            go.Pie(
                                labels=sentiment_counts['Sentiment'],
                                values=sentiment_counts['Count'],
                                hole=0.4,
                                marker_colors=['#4CAF50', '#2196F3', '#F44336']
                            ),
                            row=1, col=1
                        )
                        
                        # Add bar chart
                        fig.add_trace(
                            go.Bar(
                                x=sentiment_counts['Sentiment'],
                                y=sentiment_counts['Count'],
                                marker_color=['#4CAF50', '#2196F3', '#F44336']
                            ),
                            row=1, col=2
                        )
                        
                        fig.update_layout(height=500, title_text="Sentiment Analysis Results")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add a gauge chart for overall sentiment
                        if 'sentiment_score' in results_df.columns:
                            avg_sentiment = results_df['sentiment_score'].mean()
                            
                            fig2 = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = avg_sentiment,
                                domain = {'x': [0, 1], 'y': [0, 1]},
                                title = {'text': "Average Sentiment Score"},
                                gauge = {
                                    'axis': {'range': [-1, 1]},
                                    'bar': {'color': "darkblue"},
                                    'steps': [
                                        {'range': [-1, -0.05], 'color': "#F44336"},
                                        {'range': [-0.05, 0.05], 'color': "#2196F3"},
                                        {'range': [0.05, 1], 'color': "#4CAF50"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': avg_sentiment
                                    }
                                }
                            ))
                            
                            st.plotly_chart(fig2, use_container_width=True)
                    
                    with tab3:
                        # Generate word cloud from headlines
                        st.markdown("<div class='section-header'>Word Cloud of Headlines</div>", unsafe_allow_html=True)
                        
                        # Combine all headlines
                        all_headlines = ' '.join(results_df['title'].tolist())
                        
                        # Tokenize and remove stopwords
                        stop_words = set(stopwords.words('english'))
                        word_tokens = word_tokenize(all_headlines.lower())
                        filtered_text = [word for word in word_tokens if word.isalpha() and word not in stop_words]
                        
                        # Generate word cloud
                        if filtered_text:
                            wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                                colormap='viridis', max_words=100).generate(' '.join(filtered_text))
                            
                            # Display the word cloud
                            fig, ax = plt.subplots(figsize=(10, 5))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                            
                            # Add word frequency analysis
                            word_freq = pd.Series(filtered_text).value_counts().head(10)
                            
                            fig3 = px.bar(
                                x=word_freq.index, 
                                y=word_freq.values,
                                labels={'x': 'Word', 'y': 'Frequency'},
                                title='Top 10 Words in Headlines'
                            )
                            
                            st.plotly_chart(fig3, use_container_width=True)
                        else:
                            st.warning("Not enough text to generate a word cloud.")
                    
                    with tab4:
                        # Source analysis
                        st.markdown("<div class='section-header'>News Source Analysis</div>", unsafe_allow_html=True)
                        
                        if 'source' in results_df.columns:
                            # Group by source and sentiment
                            source_sentiment = results_df.groupby(['source', 'sentiment']).size().reset_index(name='count')
                            
                            # Create a grouped bar chart
                            fig4 = px.bar(
                                source_sentiment, 
                                x='source', 
                                y='count', 
                                color='sentiment',
                                color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                                title='Sentiment Distribution by News Source',
                                barmode='group'
                            )
                            
                            st.plotly_chart(fig4, use_container_width=True)
                            
                            # Add country analysis if available
                            if 'country' in results_df.columns:
                                country_sentiment = results_df.groupby(['country', 'sentiment']).size().reset_index(name='count')
                                
                                fig5 = px.bar(
                                    country_sentiment, 
                                    x='country', 
                                    y='count', 
                                    color='sentiment',
                                    color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                                    title='Sentiment Distribution by Country Mentioned',
                                    barmode='group'
                                )
                                
                                st.plotly_chart(fig5, use_container_width=True)
                        else:
                            st.warning("Source information not available for analysis.")
                else:
                    st.error("Failed to fetch news. Please try another source or check your internet connection.")
    
    # Sample data for demonstration
    if not fetch_button:
        st.info("Click the button above to fetch and analyze news headlines.")
        
        st.markdown("<div class='section-header'>Sample Sentiment Analysis</div>", unsafe_allow_html=True)
        
        # Sample sentiment data
        sample_sentiment = {
            'title': [
                "Global chip shortage eases as production ramps up",
                "Electronics manufacturers face supply chain disruptions",
                "New semiconductor plant opens in Taiwan",
                "Tech companies report mixed Q2 earnings",
                "Trade tensions impact electronics exports",
                "AI chip demand surges amid tech innovation",
                "Manufacturing sector shows signs of recovery",
                "Semiconductor industry faces regulatory challenges",
                "New electronics recycling initiative launched",
                "Supply chain resilience improves for tech manufacturers"
            ],
            'source': ['Reuters', 'Bloomberg', 'TechCrunch', 'CNBC', 'WSJ', 'Reuters', 'Bloomberg', 'TechCrunch', 'CNBC', 'WSJ'],
            'timestamp': ['2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05', '2023-05-06', '2023-05-07', '2023-05-08', '2023-05-09', '2023-05-10'],
            'country': ['Global', 'China', 'Taiwan', 'USA', 'Global', 'USA', 'Japan', 'EU', 'Global', 'South Korea'],
            'sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative', 'Positive', 'Positive', 'Negative', 'Positive', 'Neutral'],
            'sentiment_score': [0.65, -0.48, 0.72, 0.05, -0.52, 0.58, 0.63, -0.41, 0.55, 0.12]
        }
        
        sample_df = pd.DataFrame(sample_sentiment)
        
        # Display in tabs for better organization
        tab1, tab2, tab3 = st.tabs(["Data Table", "Visualizations", "Interactive Analysis"])
        
        with tab1:
            # Add sentiment color highlighting
            def highlight_sentiment(val):
                if val == 'Positive':
                    return 'background-color: #e8f5e9; color: #2e7d32'
                elif val == 'Negative':
                    return 'background-color: #ffebee; color: #c62828'
                else:
                    return 'background-color: #e3f2fd; color: #1565c0'
            
            # Apply styling
            styled_df = sample_df.style.applymap(highlight_sentiment, subset=['sentiment'])
            st.dataframe(styled_df, use_container_width=True)
        
        with tab2:
            # Create a more advanced visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Sentiment distribution pie chart
                fig = px.pie(
                    sample_df['sentiment'].value_counts().reset_index(),
                    values='count',
                    names='sentiment',
                    color='sentiment',
                    color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'},
                    hole=0.4,
                    title='Sentiment Distribution'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Sentiment by source
                source_sentiment = pd.crosstab(sample_df['source'], sample_df['sentiment'])
                fig2 = px.bar(
                    source_sentiment,
                    title='Sentiment by News Source',
                    barmode='group',
                    color_discrete_map={'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'}
                )
                fig2.update_layout(xaxis_title='News Source', yaxis_title='Count')
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            # Add interactive filters
            st.markdown("<div class='section-header'>Interactive Analysis</div>", unsafe_allow_html=True)
            
            # Source filter
            selected_source = st.multiselect(
                "Filter by Source",
                options=sample_df['source'].unique(),
                default=sample_df['source'].unique()
            )
            
            # Date range filter
            date_range = st.date_input(
                "Select Date Range",
                value=(
                    pd.to_datetime(sample_df['timestamp']).min(),
                    pd.to_datetime(sample_df['timestamp']).max()
                )
            )
            
            # Filter data based on selections
            filtered_df = sample_df[
                (sample_df['source'].isin(selected_source)) &
                (pd.to_datetime(sample_df['timestamp']).between(date_range[0], date_range[1]))
            ]
            
            # Show filtered results
            if not filtered_df.empty:
                # Sentiment trend over time
                fig3 = px.line(
                    filtered_df,
                    x='timestamp',
                    y='sentiment_score',
                    color='source',
                    title='Sentiment Trend Over Time'
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Country distribution
                fig4 = px.bar(
                    filtered_df['country'].value_counts().reset_index(),
                    x='index',
                    y='country',
                    title='News Distribution by Country'
                )
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.warning("No data available for the selected filters.")

# Add footer
st.markdown("""
<div class="footer">
    <p>News Sentiment Analysis Dashboard | Created for GUIDANCE – BIU TEAM ASSIGNMENT</p>
    <p>Data sources: Various public news APIs and RSS feeds</p>
</div>
""", unsafe_allow_html=True)