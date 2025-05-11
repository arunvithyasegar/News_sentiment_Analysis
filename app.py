import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from trade_analysis import (
    load_and_clean_data, 
    calculate_growth_rates, 
    calculate_volatility, 
    classify_countries,
    analyze_distribution
)
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, visualize_sentiment

# Set page configuration
st.set_page_config(
    page_title="Trade & News Sentiment Analysis Dashboard",
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
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
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
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("<div class='main-header'>Trade & News Sentiment Analysis Dashboard</div>", unsafe_allow_html=True)
st.markdown("### GUIDANCE – BIU TEAM ASSIGNMENT")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Section",
    ["Home", "Trade Data Analysis", "News Sentiment Analysis"]
)

# Home Page
if page == "Home":
    st.markdown("<div class='sub-header'>Welcome to the Dashboard</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    This interactive dashboard provides analysis for:
    <ul>
        <li><b>Trade Data Analysis</b>: Analyzing electrical machinery and equipment export data from 2016-2024</li>
        <li><b>News Sentiment Analysis</b>: Analyzing sentiment of recent news headlines related to electronics, semiconductors, or manufacturing</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Instructions</div>", unsafe_allow_html=True)
    st.markdown("""
    - Use the sidebar to navigate between different sections
    - In the Trade Data Analysis section, you can:
        - View the cleaned dataset
        - Analyze growth trends
        - Examine volatility
        - See country classifications
        - Explore statistical distributions
    - In the News Sentiment Analysis section, you can:
        - View scraped news headlines
        - See sentiment analysis results
        - Explore sentiment distribution visualizations
    """)
    
    # Sample visualization for the home page
    st.markdown("<div class='section-header'>Dashboard Preview</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://www.un.org/sites/un2.un.org/files/styles/large-article-image-style-16-9/public/field/image/un-comtrade-database.jpg?itok=Qb5oFJQO", 
                 caption="UN Comtrade Database")
    
    with col2:
        st.image("https://miro.medium.com/max/1400/1*Uu0RqBu1CgEfSLUzQEFIHw.png", 
                 caption="Sentiment Analysis Visualization")

# Trade Data Analysis Page
elif page == "Trade Data Analysis":
    st.markdown("<div class='sub-header'>Trade Data Analysis</div>", unsafe_allow_html=True)
    
    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload UN Comtrade CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Load and clean data
        df, filtered_df = load_and_clean_data(uploaded_file)
        
        # Display tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Cleaned Data", 
            "Growth Trends", 
            "Volatility Analysis", 
            "Country Classification",
            "Statistical Analysis"
        ])
        
        with tab1:
            st.markdown("<div class='section-header'>Cleaned Trade Data</div>", unsafe_allow_html=True)
            st.markdown("Filtered to include only countries with export values above $500 million in 2024")
            st.dataframe(filtered_df)
            
            # Download button for cleaned data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Cleaned Data as CSV",
                data=csv,
                file_name="cleaned_trade_data.csv",
                mime="text/csv",
            )
        
        with tab2:
            st.markdown("<div class='section-header'>Growth Trend Analysis</div>", unsafe_allow_html=True)
            
            # Calculate growth rates
            growth_df = calculate_growth_rates(filtered_df)
            
            # Display growth rates table
            st.markdown("##### Year-on-Year Growth Rates")
            st.dataframe(growth_df)
            
            # Visualize top 3 countries by growth
            st.markdown("##### Export Trends for Top 3 Countries by Average Growth Rate")
            
            # Get top 3 countries
            top_countries = growth_df.sort_values(by='Average Growth Rate', ascending=False).head(3)
            
            # Create and display the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            for country in top_countries.index:
                country_data = filtered_df[filtered_df['Reporter'] == country]
                years = [col for col in filtered_df.columns if col.isdigit()]
                values = country_data[years].values[0]
                ax.plot(years, values, marker='o', linewidth=2, label=country)
            
            ax.set_title('Export Trends for Top 3 Countries (2016-2024)')
            ax.set_xlabel('Year')
            ax.set_ylabel('Export Value (USD)')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
        
        with tab3:
            st.markdown("<div class='section-header'>Volatility Analysis</div>", unsafe_allow_html=True)
            
            # Calculate volatility
            volatility_df = calculate_volatility(filtered_df)
            
            # Display volatility table
            st.markdown("##### Export Volatility by Country")
            st.dataframe(volatility_df)
            
            # Visualize top 10 most volatile countries
            st.markdown("##### Top 10 Most Volatile Exporters")
            
            # Get top 10 volatile countries
            top_volatile = volatility_df.sort_values(by='Volatility', ascending=False).head(10)
            
            # Create and display the plot
            fig, ax = plt.subplots(figsize=(12, 6))
            
            sns.barplot(x=top_volatile.index, y=top_volatile['Volatility'], ax=ax)
            ax.set_title('Top 10 Most Volatile Exporters')
            ax.set_xlabel('Country')
            ax.set_ylabel('Volatility (Standard Deviation)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Compare volatility with growth rate
            st.markdown("##### Volatility vs. Growth Rate")
            
            # Merge growth and volatility data
            comparison_df = pd.merge(
                growth_df['Average Growth Rate'], 
                volatility_df['Volatility'], 
                left_index=True, 
                right_index=True
            )
            
            # Create and display the scatter plot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            sns.scatterplot(
                data=comparison_df, 
                x='Average Growth Rate', 
                y='Volatility', 
                ax=ax
            )
            
            # Add country labels to points
            for idx, row in comparison_df.iterrows():
                ax.text(row['Average Growth Rate'], row['Volatility'], idx, fontsize=8)
            
            ax.set_title('Volatility vs. Average Growth Rate by Country')
            ax.set_xlabel('Average Growth Rate (%)')
            ax.set_ylabel('Volatility (Standard Deviation)')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
        
        with tab4:
            st.markdown("<div class='section-header'>Country Classification</div>", unsafe_allow_html=True)
            
            # Classify countries
            classification_df = classify_countries(growth_df, volatility_df)
            
            # Display classification table
            st.markdown("##### Country Classification")
            st.dataframe(classification_df)
            
            # Visualize classification in a quadrant chart
            st.markdown("##### Classification Quadrant Chart")
            
            # Create and display the quadrant chart
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Define colors for each category
            colors = {
                'Stable High-Growth': 'green',
                'Volatile High-Growth': 'orange',
                'Stable Low-Growth': 'blue',
                'Volatile Low-Growth': 'red'
            }
            
            # Create scatter plot with colors by category
            for category in colors.keys():
                category_data = classification_df[classification_df['Classification'] == category]
                if not category_data.empty:
                    sns.scatterplot(
                        data=category_data, 
                        x='Average Growth Rate', 
                        y='Volatility', 
                        label=category,
                        color=colors[category],
                        s=100,
                        ax=ax
                    )
            
            # Add country labels
            for idx, row in classification_df.iterrows():
                ax.text(row['Average Growth Rate'], row['Volatility'], idx, fontsize=8)
            
            # Add quadrant lines
            growth_median = classification_df['Average Growth Rate'].median()
            volatility_median = classification_df['Volatility'].median()
            
            ax.axhline(y=volatility_median, color='gray', linestyle='--', alpha=0.7)
            ax.axvline(x=growth_median, color='gray', linestyle='--', alpha=0.7)
            
            # Add quadrant labels
            ax.text(
                classification_df['Average Growth Rate'].max() * 0.8, 
                classification_df['Volatility'].min() * 1.2, 
                'Stable High-Growth', 
                fontsize=12, 
                color='green'
            )
            ax.text(
                classification_df['Average Growth Rate'].max() * 0.8, 
                classification_df['Volatility'].max() * 0.8, 
                'Volatile High-Growth', 
                fontsize=12, 
                color='orange'
            )
            ax.text(
                classification_df['Average Growth Rate'].min() * 1.2, 
                classification_df['Volatility'].min() * 1.2, 
                'Stable Low-Growth', 
                fontsize=12, 
                color='blue'
            )
            ax.text(
                classification_df['Average Growth Rate'].min() * 1.2, 
                classification_df['Volatility'].max() * 0.8, 
                'Volatile Low-Growth', 
                fontsize=12, 
                color='red'
            )
            
            ax.set_title('Country Classification by Growth and Volatility')
            ax.set_xlabel('Average Growth Rate (%)')
            ax.set_ylabel('Volatility (Standard Deviation)')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            st.pyplot(fig)
        
        with tab5:
            st.markdown("<div class='section-header'>Statistical Analysis</div>", unsafe_allow_html=True)
            
            # Analyze distribution
            dist_fig, top_performers, bottom_performers = analyze_distribution(growth_df)
            
            # Display distribution plot
            st.markdown("##### Distribution of Average Annual Growth Rates")
            st.pyplot(dist_fig)
            
            # Display top and bottom performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Top Performers (Top 10%)")
                st.dataframe(top_performers)
            
            with col2:
                st.markdown("##### Underperformers (Bottom 10%)")
                st.dataframe(bottom_performers)
            
            # Create boxplot
            st.markdown("##### Boxplot of Growth Rates")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=growth_df['Average Growth Rate'], ax=ax)
            ax.set_title('Boxplot of Average Growth Rates')
            ax.set_xlabel('Average Growth Rate (%)')
            
            st.pyplot(fig)
    
    else:
        st.info("Please upload a CSV file from the UN Comtrade Database to begin analysis.")
        
        # Sample data for demonstration
        st.markdown("<div class='section-header'>Sample Data Format</div>", unsafe_allow_html=True)
        
        sample_data = {
            'Reporter': ['China', 'United States', 'Germany', 'Japan', 'South Korea'],
            '2016': [600000000, 550000000, 400000000, 350000000, 300000000],
            '2017': [650000000, 560000000, 420000000, 360000000, 320000000],
            '2018': [700000000, 570000000, 440000000, 370000000, 340000000],
            '2019': [750000000, 580000000, 460000000, 380000000, 360000000],
            '2020': [800000000, 590000000, 480000000, 390000000, 380000000],
            '2021': [850000000, 600000000, 500000000, 400000000, 400000000],
            '2022': [900000000, 610000000, 520000000, 410000000, 420000000],
            '2023': [950000000, 620000000, 540000000, 420000000, 440000000],
            '2024': [1000000000, 630000000, 560000000, 430000000, 460000000]
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df)
        
        st.markdown("""
        The expected format for the UN Comtrade data should include:
        - Reporter column with country names
        - Year columns (2016-2024) with export values in USD
        
        You can download data from the [UN Comtrade Database](https://comtrade.un.org/data/) with the following parameters:
        - Type: Goods
        - Frequency: Annual
        - Reporter: All countries
        - Partner: World
        - HS Code: 85 (Electrical machinery and equipment)
        - Trade Flow: Export
        - Measure: USD
        """)

# News Sentiment Analysis Page
elif page == "News Sentiment Analysis":
    st.markdown("<div class='sub-header'>News Sentiment Analysis</div>", unsafe_allow_html=True)
    
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
    
    # Number of articles to fetch
    num_articles = st.slider(
        "Number of articles to analyze",
        min_value=5,
        max_value=50,
        value=20
    )
    
    # Button to fetch and analyze news
    if st.button("Fetch and Analyze News"):
        with st.spinner("Fetching news and analyzing sentiment..."):
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
                    for line in manual_news.strip().split('\n'):
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
                    
                    # Display results
                    st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                    
                    # Create a DataFrame for display
                    results_df = pd.DataFrame(sentiment_results)
                    st.dataframe(results_df)
                    
                    # Visualize sentiment distribution
                    st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                    
                    # Create visualization
                    fig = visualize_sentiment(sentiment_results)
                    st.pyplot(fig)
            else:
                # Scrape news from selected source
                news_data = scrape_news(news_source, keywords.split(','), num_articles)
                
                if news_data:
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Display results
                    st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                    
                    # Create a DataFrame for display
                    results_df = pd.DataFrame(sentiment_results)
                    st.dataframe(results_df)
                    
                    # Visualize sentiment distribution
                    st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                    
                    # Create visualization
                    fig = visualize_sentiment(sentiment_results)
                    st.pyplot(fig)
                else:
                    st.error("Failed to fetch news. Please try another source or check your internet connection.")
    
    # Sample data for demonstration
    if not st.button("Fetch and Analyze News"):
        st.info("Click the button above to fetch and analyze news headlines.")
        
        st.markdown("<div class='section-header'>Sample Sentiment Analysis</div>", unsafe_allow_html=True)
        
        # Sample sentiment data
        sample_sentiment = {
            'title': [
                "Global chip shortage eases as production ramps up",
                "Electronics manufacturers face supply chain disruptions",
                "New semiconductor plant opens in Taiwan",
                "Tech companies report mixed Q2 earnings",
                "Trade tensions impact electronics exports"
            ],
            'source': ['Reuters', 'Bloomberg', 'TechCrunch', 'CNBC', 'WSJ'],
            'date': ['2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05'],
            'country': ['Global', 'China', 'Taiwan', 'USA', 'Global'],
            'sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative'],
            'score': [0.65, -0.48, 0.72, 0.05, -0.53]
        }
        
        sample_df = pd.DataFrame(sample_sentiment)
        st.dataframe(sample_df)
        
        # Sample visualization
        st.markdown("<div class='section-header'>Sample Sentiment Distribution</div>", unsafe_allow_html=True)
        
        # Count sentiments
        sentiment_counts = sample_df['sentiment'].value_counts()
        
        # Create and display the plot
        fig, ax = plt.subplots(figsize=(8, 5))
        
        bars = ax.bar(
            sentiment_counts.index, 
            sentiment_counts.values,
            color=['green', 'red', 'blue']
        )
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.1,
                f'{height}',
                ha='center',
                va='bottom'
            )
        
        ax.set_title('Sentiment Distribution of News Headlines')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')
        
        st.pyplot(fig)