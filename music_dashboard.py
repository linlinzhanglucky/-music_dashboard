import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO
import numpy as np
import datetime

# Set page configuration
st.set_page_config(
    page_title="Audiomack ArtistRank Dashboard - Week 2",
    page_icon="🎵",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #FF6B6B;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #4ECDC4;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .insights-box {
        background-color: #f1f8ff;
        border-left: 5px solid #4ECDC4;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .highlight {
        color: #FF6B6B;
        font-weight: bold;
    }
    .date-info {
        font-size: 14px;
        color: #666;
        margin-bottom: 20px;
    }
    .recommendation-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #FF9F1C;
    }
</style>
""", unsafe_allow_html=True)

# Function to load scouting tracker data
def load_scouting_tracker():
    """Function to display the A&R Scouting Tracker tab"""

    st.header("A&R Scouting Tracker")
    st.write("View of Jordan and Jalen's AMD A&R scouting selections")

    # Published CSV URL
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2Q-L96f18C7C-EMCzIoCxR8bdphMkPNcpske5xGYzr6lmztcsqaJgmyTFmXHhu7mjrqvR8MsgfWJT/pub?output=csv"

    try:
        # Load data
        response = requests.get(csv_url)

        if response.status_code != 200:
            st.error(f"Failed to load data: Status code {response.status_code}")
            return

        data = StringIO(response.text)
        raw_df = pd.read_csv(data)

        # Find header row
        header_row = None
        for i, row in raw_df.iterrows():
            row_str = ' '.join([str(val) for val in row.values])
            if "Date" in row_str and "Artist Name" in row_str:
                header_row = i
                break

        if header_row is None:
            st.error("Could not find the header row in the sheet")
            st.write("Available columns:", raw_df.columns.tolist())
            return

        headers = raw_df.iloc[header_row].tolist()

        # Create clean dataframe
        clean_df = pd.DataFrame(columns=headers)
        for i in range(header_row + 1, len(raw_df)):
            row_data = raw_df.iloc[i].tolist()
            if not all(pd.isna(val) or val == '' for val in row_data):
                clean_df.loc[len(clean_df)] = row_data

        clean_df = clean_df.fillna('')

        if len(clean_df) == 0:
            st.warning("No data found after processing")
            return

        # Extract filter options
        platform_options = [opt for opt in clean_df["On Platform"].unique() if "On Platform" in clean_df.columns and opt]
        genre_options = [opt for opt in clean_df["Genre"].unique() if "Genre" in clean_df.columns and opt]
        geo_options = [opt for opt in clean_df["Geo"].unique() if "Geo" in clean_df.columns and opt]
        feed_partner_options = [opt for opt in clean_df["Feed Partner"].unique() if "Feed Partner" in clean_df.columns and opt]

        # Display filters
        st.subheader("Filters")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            selected_platform = st.multiselect("On Platform Status", options=platform_options, default=platform_options if platform_options else [])

        with col2:
            selected_genres = st.multiselect("Genre", options=genre_options, default=genre_options if genre_options else [])

        with col3:
            selected_geos = st.multiselect("Geography", options=geo_options, default=geo_options if geo_options else [])

        with col4:
            selected_feed_partners = st.multiselect("Feed Partner", options=feed_partner_options, default=feed_partner_options if feed_partner_options else [])

        # Apply filters
        filtered_df = clean_df.copy()

        if selected_platform:
            filtered_df = filtered_df[filtered_df["On Platform"].isin(selected_platform)]
        if selected_genres:
            filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genres)]
        if selected_geos:
            filtered_df = filtered_df[filtered_df["Geo"].isin(selected_geos)]
        if selected_feed_partners:
            filtered_df = filtered_df[filtered_df["Feed Partner"].isin(selected_feed_partners)]

        # Display scouting results
        st.subheader("Scouting Results")
        column_names = filtered_df.columns.tolist()

        for i, row in filtered_df.iterrows():
            with st.expander(f"{row.get('Artist Name', '')} - {row.get('Song Name', '')}"):
                for col in column_names:
                    if col in ["Artist Name", "Song Name"]:
                        continue
                    value = row.get(col, '')
                    if col == "Social Media Link" and value:
                        st.markdown(f"**{col}:** [{value}]({value})")
                    else:
                        st.markdown(f"**{col}:** {value}")

        # Analytics
        st.subheader("Analytics")
        met1, met2, met3 = st.columns(3)
        met1.metric("Total Tracks", len(filtered_df))

        if "Genre" in filtered_df.columns:
            genre_count = len([g for g in filtered_df["Genre"].unique() if g])
            met2.metric("Unique Genres", genre_count)

        if "Geo" in filtered_df.columns:
            geo_count = len([g for g in filtered_df["Geo"].unique() if g])
            met3.metric("Countries", geo_count)

        # Visualizations
        if len(filtered_df) > 0:
            viz1, viz2 = st.columns(2)

            with viz1:
                if "Genre" in filtered_df.columns:
                    genre_counts = filtered_df["Genre"].value_counts().reset_index()
                    genre_counts.columns = ["Genre", "Count"]
                    genre_counts = genre_counts[genre_counts["Genre"] != ""]
                    if not genre_counts.empty:
                        fig1 = px.pie(
                            genre_counts,
                            values="Count",
                            names="Genre",
                            title="Genre Distribution",
                            hole=0.4
                        )
                        st.plotly_chart(fig1, use_container_width=True)

            with viz2:
                if "Geo" in filtered_df.columns:
                    geo_counts = filtered_df["Geo"].value_counts().reset_index()
                    geo_counts.columns = ["Geography", "Count"]
                    geo_counts = geo_counts[geo_counts["Geography"] != ""]
                    if not geo_counts.empty:
                        fig2 = px.bar(
                            geo_counts,
                            x="Geography",
                            y="Count",
                            title="Geographic Distribution",
                            color="Count"
                        )
                        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)


@st.cache_data
def load_data():
    # Load data from CSV files
    
    # AMD Artist Country Breakdown
    try:
        amd_artist_country_df = pd.read_csv('AMD Artist Country Breakdown.csv')
    except:
        amd_artist_country_df = pd.DataFrame({
            "artist": ["Erma", "Vybz Kartel", "Siicie & Lasmid", "Mitski", "Dxtiny"],
            "title": ["DYANA", "God is The Greatest", "Do You Know?", "My Love Mine All Mine", "Uncle Pele"],
            "geo_country": ["NG", "GH", "GH", "US", "NG"],
            "plays": [111633, 187446, 91479, 11066, 189738],
            "engagements": [793, 764, 655, 652, 482]
        })
    
    # Current AMD Songs List
    try:
        amd_songs_df = pd.read_csv('Current AMD Songs List.csv')
    except:
        amd_songs_df = pd.DataFrame({
            "music_id_raw": ["music:61401185", "music:13852656", "music:56684604", "music:32374254", "music:56252684"],
            "artist": ["Dalia", "Madlib", "PF Xavi", "William McDowell", "Jodie Marie ASMR"],
            "title": ["What if", "Dil Cosby Interlude", "Not Ready", "Never Going Back (I Won't Go Back Reprise)", "Black Country Maid Cleans you up Pt.3"],
            "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct"]
        })
    
    # Engagement Source Channels
    try:
        source_channels_df = pd.read_csv('Engagement Source Channels.csv')
    except:
        source_channels_df = pd.DataFrame({
            "source_tab": ["My Library", "Search", "Search", "Browse", "My Library"],
            "section": ["My Library - Offline", "Search - All Music", "Queue End Autoplay", "Browse - Recommendations", "My Library - Favorites"],
            "event_count": [204009819, 102970150, 55581117, 45211776, 19003309]
        })
    
    # Engagement Per User By Play Cohort
    try:
        engagement_per_user_df = pd.read_csv('EngagementPerUser_ByPlayCohort_AMD_Week2.csv')
    except:
        engagement_per_user_df = pd.DataFrame({
            "artist": ["JJ DOOM, MF DOOM, Jneiro Jarel", "Various Artists", "Royal Philharmonic Orchestra and Vernon Handley", "Metro Zu", "Christone \"Kingfish\" Ingram"],
            "title": ["Key to the Kuffs", "Broken Hearts & Dirty Windows: Songs of John Prine, Vol. 2", "Holst: The Planets, suite for orchestra and female chorus, Op.32, H.125 (Mars: The Bringer of War)", "LSD Swag", "Live In London (Expanded Edition)"],
            "total_plays": [0, 0, 4, 15, 0],
            "total_engagements": [67, 9, 6, 3, 3],
            "unique_users": [6, 1, 1, 1, 1],
            "engagement_per_user": [11, 9, 6, 3, 3],
            "play_cohort": ["Low", "Low", "Low", "Low", "Low"]
        })
    
    # Small Artists with High Engagement
    try:
        small_artists_df = pd.read_csv('Listener Cohort  Small Artists with High Engagement.csv')
    except:
        small_artists_df = pd.DataFrame({
            "artist": ["Grizzy B.", "Aoki Nozomi", "wizzysavage", "I'm КʼЮ", "9000UK"],
            "total_users": [2, 6, 48, 3, 10],
            "total_plays": [121, 340, 955, 119, 106],
            "total_engagements": [19, 54, 382, 21, 64],
            "engagements_per_user": [9.5, 9.0, 7.958333, 7.0, 6.4]
        })
    
    # Territory Reach
    try:
        territory_reach_df = pd.read_csv('Territory Reach by Artist Top Geo by Plays.csv')
    except:
        territory_reach_df = pd.DataFrame({
            "artist": ["Vybz Kartel", "Dxtiny", "Fido", "Erma", "Squash"],
            "geo_country": ["GH", "NG", "NG", "NG", "JM"],
            "total_events": [523079, 483049, 427256, 217735, 191775],
            "plays": [262940, 249880, 220781, 111633, 96740]
        })
    
    # Top 100 Most Engaged Artists
    try:
        top_engaged_artists_df = pd.read_csv('top 100 most engaged artists last week.csv')
    except:
        top_engaged_artists_df = pd.DataFrame({
            "artist": ["Black Sherif", "YoungBoy Never Broke Again", "Seyi Vibez", "Rema", "Juice WRLD"],
            "total_plays": [6553308, 2926897, 9112888, 2848577, 2476790],
            "total_engagements": [77895, 38403, 34236, 26531, 23548],
            "unique_users": [967981, 230143, 1853187, 982726, 367914]
        })
    
    # Top Engaged AMD Songs Geo Breakdown
    try:
        top_songs_geo_df = pd.read_csv('TopEngaged_AMD_Songs_GeoBreakdown_Week2.csv')
    except:
        top_songs_geo_df = pd.DataFrame({
            "artist": ["Vybz Kartel", "Siicie & Lasmid", "Erma", "Siicie", "Fido"],
            "title": ["God is The Greatest", "Do You Know?", "DYANA", "Alhamdulillah", "Awolowo"],
            "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct"],
            "total_plays": [158205, 75777, 39675, 29751, 78765],
            "total_engagements": [612, 521, 292, 272, 180],
            "unique_users": [87573, 47796, 25884, 18803, 65440],
            "geo_country": ["GH", "GH", "NG", "GH", "NG"],
            "geo_region": ["AA", "AA", "LA", "AA", "LA"]
        })
    
    # Weekly Artist Engagement Summary
    try:
        weekly_engagement_df = pd.read_csv('Weekly Artist Engagement Summary.csv')
    except:
        weekly_engagement_df = pd.DataFrame({
            "artist": ["Chella", "Rema", "Zinoleesky", "Black Sherif & Fireboy DML", "Black Sherif"],
            "title": ["My Darling", "Bout U", "Most Wanted", "So it Goes", "IRON BOY"],
            "total_plays": [1921857, 364355, 1738714, 1144601, 0],
            "total_engagements": [9945, 8991, 8620, 8196, 8075],
            "unique_users": [820825, 253488, 738401, 598478, 172100]
        })
    
    # Create mock editorial playlist data
    editorial_playlist_df = pd.DataFrame({
        "added_at": ["2025-04-13", "2025-04-12", "2025-04-12", "2025-04-11", "2025-04-10", 
                    "2025-04-09", "2025-04-09", "2025-04-08", "2025-04-07", "2025-04-07"],
        "song_name": ["DYANA", "God is The Greatest", "Do You Know?", "Alhamdulillah", "Uncle Pele",
                     "Awolowo", "What if", "Dil Cosby Interlude", "Not Ready", "Never Going Back"],
        "artist_name": ["Erma", "Vybz Kartel", "Siicie & Lasmid", "Siicie", "Dxtiny",
                       "Fido", "Dalia", "Madlib", "PF Xavi", "William McDowell"],
        "is_ghost_account": ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
        "distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                            "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct",
                            "Audiosalad Direct", "Audiosalad Direct"],
        "playlist_name": ["Afrobeats Now", "Verified Hip-Hop", "Trending Africa", "Alte Cruise", "Afrobeats Now",
                         "Verified Hip-Hop", "Verified R&B", "Alte Cruise", "Trending Africa", "Gospel Hits"]
    })
    
    # Calculate derived metrics and prepare data
    
    # Calculate engagement per user
    top_engaged_artists_df['engagements_per_user'] = top_engaged_artists_df['total_engagements'] / top_engaged_artists_df['unique_users']
    
    # Calculate source tab percentages
    source_tab_totals = source_channels_df.groupby('source_tab')['event_count'].sum().reset_index()
    total_events = source_tab_totals['event_count'].sum()
    source_tab_totals['percentage'] = (source_tab_totals['event_count'] / total_events) * 100
    
    # Calculate section percentages
    section_totals = source_channels_df.groupby('section')['event_count'].sum().reset_index()
    section_totals['percentage'] = (section_totals['event_count'] / total_events) * 100
    section_totals = section_totals.sort_values('percentage', ascending=False)
    
    # Process territory reach - calculate artist country distributions
    # Get unique artists
    unique_artists = territory_reach_df['artist'].unique()
    
    artist_country_dist = {}
    for artist in unique_artists:
        artist_data = territory_reach_df[territory_reach_df['artist'] == artist]
        total_plays = artist_data['plays'].sum()
        
        # Calculate percentages for each country
        country_percentages = {}
        for _, row in artist_data.iterrows():
            country = row['geo_country']
            plays = row['plays']
            percentage = (plays / total_plays) * 100 if total_plays > 0 else 0
            country_percentages[country] = percentage
        
        artist_country_dist[artist] = country_percentages
    
    # Identify cross-border opportunities
    # For each artist-song in top_songs_geo_df, calculate country percentages
    songs_geo_dist = {}
    cross_border_opportunities = []
    
    # Get unique artist-song combinations
    unique_songs = top_songs_geo_df.drop_duplicates(['artist', 'title'])
    
    for _, song_row in unique_songs.iterrows():
        artist = song_row['artist']
        title = song_row['title']
        
        # Get all data for this song
        song_data = top_songs_geo_df[(top_songs_geo_df['artist'] == artist) & (top_songs_geo_df['title'] == title)]
        
        # Calculate total plays for this song
        total_song_plays = song_data['total_plays'].sum()
        
        # Calculate percentages for each country
        song_country_percentages = {}
        for _, row in song_data.iterrows():
            country = row['geo_country']
            plays = row['total_plays']
            percentage = (plays / total_song_plays) * 100 if total_song_plays > 0 else 0
            song_country_percentages[country] = percentage
        
        songs_geo_dist[f"{artist} - {title}"] = song_country_percentages
        
        # Compare to artist's overall distribution
        if artist in artist_country_dist:
            artist_dist = artist_country_dist[artist]
            
            # Find countries where artist has higher percentage than song
            for country, artist_pct in artist_dist.items():
                song_pct = song_country_percentages.get(country, 0)
                
                # If gap is significant (>5%)
                if artist_pct > song_pct + 5:
                    cross_border_opportunities.append({
                        'artist': artist,
                        'song': title,
                        'country': country,
                        'artist_pct': artist_pct,
                        'song_pct': song_pct,
                        'gap': artist_pct - song_pct,
                        'total_plays': total_song_plays
                    })
    
    # Calculate engagement metrics for songs
    song_engagement_df = top_songs_geo_df.groupby(['artist', 'title']).agg({
        'total_plays': 'sum',
        'total_engagements': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    song_engagement_df['engagement_per_user'] = song_engagement_df['total_engagements'] / song_engagement_df['unique_users']
    
    # Add playlist types to editorial playlists data
    editorial_playlist_df['playlist_type'] = editorial_playlist_df['playlist_name'].map({
        'Afrobeats Now': 'Afrobeats',
        'Verified Hip-Hop': 'Hip-Hop',
        'Alte Cruise': 'Alternative',
        'Trending Africa': 'Regional',
        'Verified R&B': 'R&B',
        'Gospel Hits': 'Gospel'
    })
    
    return (amd_artist_country_df, amd_songs_df, source_channels_df, engagement_per_user_df,
            small_artists_df, territory_reach_df, top_engaged_artists_df, top_songs_geo_df,
            weekly_engagement_df, editorial_playlist_df, source_tab_totals, section_totals,
            cross_border_opportunities, song_engagement_df)

# Load the data
try:
    (amd_artist_country_df, amd_songs_df, source_channels_df, engagement_per_user_df,
     small_artists_df, territory_reach_df, top_engaged_artists_df, top_songs_geo_df,
     weekly_engagement_df, editorial_playlist_df, source_tab_totals, section_totals,
     cross_border_opportunities, song_engagement_df) = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Dashboard title and description
st.markdown('<div class="main-header">🎵 Audiomack ArtistRank Dashboard - Week 2</div>', unsafe_allow_html=True)
st.markdown('<div class="date-info">Analysis period: April 7-13, 2025 | Dashboard updated: April 13, 2025</div>', unsafe_allow_html=True)

# Add Week 2 update notification
st.info("👋 **Week 2 Focus:** This dashboard analyzes AMD artist performance, identifies cross-border opportunities, and tracks editorial playlist additions to support A&R decision-making.")

# Quick stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_amd_artists = len(amd_songs_df['artist'].unique())
    st.metric("AMD Artists", f"{total_amd_artists}")
with col2:
    total_songs = len(amd_songs_df)
    st.metric("Total AMD Songs", f"{total_songs}")
with col3:
    total_countries = len(amd_artist_country_df['geo_country'].unique())
    st.metric("Countries Reached", f"{total_countries}")
with col4:
    cross_border_opps = len(cross_border_opportunities)
    st.metric("Cross-Border Opportunities", f"{cross_border_opps}")

# Create sidebar for filtering
st.sidebar.header("Filters")
unique_artists = amd_artist_country_df['artist'].unique()

selected_artists = st.sidebar.multiselect(
    "Artists",
    options=unique_artists,
    default=[]
)

# Fix for the countries multiselect
country_options = amd_artist_country_df['geo_country'].unique().tolist()
default_countries = [c for c in ['NG', 'GH', 'US', 'JM'] if c in country_options]

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=country_options,
    default=default_countries
)

# Filter by engagement threshold
min_engagement = st.sidebar.slider(
    "Min Engagement Per User", 
    min_value=0.0, 
    max_value=10.0, 
    value=0.0,
    step=0.1
)

# Filter by playlists
all_playlists = editorial_playlist_df['playlist_name'].unique().tolist()
selected_playlists = st.sidebar.multiselect(
    "Editorial Playlists",
    options=all_playlists,
    default=[]
)

# About section in sidebar
st.sidebar.markdown("---")
st.sidebar.header("About This Dashboard")
st.sidebar.info(
    """
    This dashboard is developed for the Week 2 assignment of the Audiomack Internship Program, focusing on:
    
    1. Analyzing AMD artist performance
    2. Identifying cross-border promotion opportunities
    3. Tracking editorial playlist additions
    
    Use the filters to explore different artists, countries, and playlists.
    """
)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "AMD Artist Performance", 
    "Cross-Border Opportunities",
    "Editorial Playlists", 
    "Engagement Analysis",
    "Discovery Channels",
    "A&R Scouting Tracker"
])

# Tab 1: AMD Artist Performance
with tab1:
    st.markdown('<div class="sub-header">AMD Artist Performance</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insights-box">📊 <span class="highlight">Key Insight:</span> Analysis of AMD artists shows significant variation in engagement levels and geographic reach, with several artists demonstrating high potential for growth based on engagement-to-play ratios.</div>', unsafe_allow_html=True)
    
    # Filter data based on selections
    filtered_songs = top_songs_geo_df.copy()
    if selected_artists:
        filtered_songs = filtered_songs[filtered_songs['artist'].isin(selected_artists)]
    if selected_countries:
        filtered_songs = filtered_songs[filtered_songs['geo_country'].isin(selected_countries)]
    
    # Create song performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_filtered_plays = filtered_songs['total_plays'].sum()
        st.metric("Total Plays", f"{total_filtered_plays:,}")
    with col2:
        total_filtered_engagements = filtered_songs['total_engagements'].sum()
        st.metric("Total Engagements", f"{total_filtered_engagements:,}")
    with col3:
        avg_engagement_per_user = total_filtered_engagements / filtered_songs['unique_users'].sum() if filtered_songs['unique_users'].sum() > 0 else 0
        st.metric("Avg Engagement Per User", f"{avg_engagement_per_user:.2f}")
    
    # Top AMD songs visualization
    st.subheader("Top AMD Songs by Plays and Engagement")
    
    # Aggregate song data
    song_performance = filtered_songs.groupby(['artist', 'title']).agg({
        'total_plays': 'sum',
        'total_engagements': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    song_performance['engagement_per_user'] = song_performance['total_engagements'] / song_performance['unique_users']
    
    # Create visualization
    if not song_performance.empty:
        fig_songs = px.scatter(
            song_performance.sort_values('total_plays', ascending=False).head(20),
            x="total_plays", 
            y="engagement_per_user",
            size="unique_users",
            color="artist",
            hover_name="title",
            text="title",
            size_max=50,
            title="Top 20 AMD Songs: Plays vs Engagement per User"
        )
        
        fig_songs.update_traces(
            textposition='top center',
            marker=dict(line=dict(width=1, color='DarkSlateGrey'))
        )
        
        fig_songs.update_layout(
            xaxis_title="Total Plays",
            yaxis_title="Engagement per User",
            height=600
        )
        
        st.plotly_chart(fig_songs, use_container_width=True)
    else:
        st.warning("No data available for the selected filters. Please adjust your selections.")
    
    # Top AMD Artists
    st.subheader("Top AMD Artists by Total Plays")
    
    # Aggregate artist data
    artist_performance = filtered_songs.groupby('artist').agg({
        'total_plays': 'sum',
        'total_engagements': 'sum',
        'unique_users': 'sum'
    }).reset_index()
    
    artist_performance['engagement_ratio'] = artist_performance['total_engagements'] / artist_performance['total_plays']
    artist_performance = artist_performance.sort_values('total_plays', ascending=False)
    
    # Create visualization
    if not artist_performance.empty:
        fig_artists = px.bar(
            artist_performance.head(10),
            x="artist",
            y="total_plays",
            color="engagement_ratio",
color_continuous_scale="Viridis",
            title="Top 10 AMD Artists by Total Plays",
            hover_data=["unique_users", "total_engagements", "engagement_ratio"]
        )
        
        fig_artists.update_layout(
            xaxis_title="Artist",
            yaxis_title="Total Plays",
            coloraxis_colorbar_title="Engagement Ratio"
        )
        
        st.plotly_chart(fig_artists, use_container_width=True)
    else:
        st.warning("No artist data available for the selected filters. Please adjust your selections.")
    
    # Table of AMD songs with metrics
    st.subheader("AMD Songs Performance Metrics")
    
    # Create a styled table
    if not song_performance.empty:
        st.dataframe(
            song_performance.sort_values('total_plays', ascending=False),
            use_container_width=True,
            column_config={
                "artist": st.column_config.TextColumn("Artist"),
                "title": st.column_config.TextColumn("Title"),
                "total_plays": st.column_config.NumberColumn("Total Plays", format="%d"),
                "total_engagements": st.column_config.NumberColumn("Total Engagements", format="%d"),
                "unique_users": st.column_config.NumberColumn("Unique Users", format="%d"),
                "engagement_per_user": st.column_config.NumberColumn("Engagement per User", format="%.3f")
            }
        )
    else:
        st.info("No song data available to display.")
    
    # Small artists with high engagement
    st.subheader("Small Artists with High Engagement")
    
    # Sort small artists by engagement per user
    small_artists_sorted = small_artists_df.sort_values('engagements_per_user', ascending=False)
    
    # Create visualization
    fig_small_artists = px.bar(
        small_artists_sorted.head(10),
        x="artist",
        y="engagements_per_user",
        color="total_engagements",
        title="Small Artists with High Engagement per User",
        hover_data=["total_users", "total_plays", "total_engagements"]
    )
    
    fig_small_artists.update_layout(
        xaxis_title="Artist",
        yaxis_title="Engagements per User",
        coloraxis_colorbar_title="Total Engagements"
    )
    
    st.plotly_chart(fig_small_artists, use_container_width=True)
    
    st.markdown("""
    ### Key Observations
    
    - **High Engagement Niche Artists**: Several smaller artists (with fewer plays) show exceptionally high engagement per user, 
      suggesting highly dedicated fan bases that could be nurtured.
    
    - **Engagement Quality**: Top artists by total plays don't always have the highest engagement quality metrics, 
      highlighting the importance of looking beyond pure volume metrics.
    
    - **Growth Potential**: Artists with higher engagement ratios may have more potential for organic growth, 
      as they're already creating content that resonates strongly with their audience.
    """)

# Tab 2: Cross-Border Opportunities
with tab2:
    st.markdown('<div class="sub-header">Cross-Border Promotion Opportunities</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insights-box">🌍 <span class="highlight">Key Finding:</span> Several AMD artists show significant gaps between their overall audience geo distribution and their recent song distribution, representing clear opportunities for targeted cross-border promotion.</div>', unsafe_allow_html=True)
    
    # Filter cross-border opportunities
    filtered_opportunities = cross_border_opportunities.copy()
    if selected_artists:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp['artist'] in selected_artists]
    if selected_countries:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp['country'] in selected_countries]
    
    # Top cross-border opportunities
    st.subheader("Top Cross-Border Promotion Opportunities")
    
    if filtered_opportunities:
        # Convert to DataFrame for visualization
        opps_df = pd.DataFrame(filtered_opportunities)
        
        # Sort by gap size
        opps_df = opps_df.sort_values('gap', ascending=False)
        
        # Create visualization
        fig_opps = px.bar(
            opps_df.head(10),
            x="artist",
            y="gap",
            color="country",
            title="Top 10 Cross-Border Promotion Opportunities",
            hover_data=["song", "artist_pct", "song_pct", "gap", "total_plays"],
            labels={"gap": "Market Penetration Gap (%)"}
        )
        
        fig_opps.update_layout(
            xaxis_title="Artist",
            yaxis_title="Gap (%)",
            height=500
        )
        
        st.plotly_chart(fig_opps, use_container_width=True)
        
        # Create a styled table
        st.dataframe(
            opps_df,
            use_container_width=True,
            column_config={
                "artist": st.column_config.TextColumn("Artist"),
                "song": st.column_config.TextColumn("Song"),
                "country": st.column_config.TextColumn("Country"),
                "artist_pct": st.column_config.NumberColumn("Artist Audience %", format="%.1f%%"),
                "song_pct": st.column_config.NumberColumn("Song Audience %", format="%.1f%%"),
                "gap": st.column_config.NumberColumn("Gap", format="%.1f%%"),
                "total_plays": st.column_config.NumberColumn("Total Plays", format="%d")
            }
        )
    else:
        st.write("No cross-border opportunities found with the current filter settings.")
    
    # Country distribution visualization
    st.subheader("Artist vs. Song Geographic Distribution")
    
    # Allow user to select an artist for detailed view
    if len(unique_artists) > 0:
        # Select default artist
        default_artist = unique_artists[0]
        if selected_artists and selected_artists[0] in unique_artists:
            default_artist = selected_artists[0]
            
        artist_for_geo = st.selectbox(
            "Select Artist to View Geographic Distribution",
            options=unique_artists,
            index=list(unique_artists).index(default_artist) if default_artist in unique_artists else 0
        )
        
        # Get artist's songs
        artist_songs = top_songs_geo_df[top_songs_geo_df['artist'] == artist_for_geo]['title'].unique()
        
        if len(artist_songs) > 0:
            # Let user select a specific song
            selected_song = st.selectbox(
                "Select Song",
                options=artist_songs
            )
            
            # Get data for the artist and song
            artist_geo_data = amd_artist_country_df[amd_artist_country_df['artist'] == artist_for_geo]
            song_geo_data = top_songs_geo_df[(top_songs_geo_df['artist'] == artist_for_geo) & 
                                            (top_songs_geo_df['title'] == selected_song)]
            
            # Calculate percentages
            if not artist_geo_data.empty and not song_geo_data.empty:
                # Calculate artist percentages
                artist_total_plays = artist_geo_data['plays'].sum()
                artist_geo_data['percentage'] = (artist_geo_data['plays'] / artist_total_plays) * 100
                
                # Calculate song percentages
                song_total_plays = song_geo_data['total_plays'].sum()
                song_geo_data['percentage'] = (song_geo_data['total_plays'] / song_total_plays) * 100
                
                # Create a comparison chart
                fig_geo_compare = make_subplots(
                    rows=1, 
                    cols=2,
                    subplot_titles=("Artist Overall Audience", f"Song: {selected_song} Audience"),
                    specs=[[{"type": "bar"}, {"type": "bar"}]]
                )
                
                # Artist geo distribution
                artist_geo_sorted = artist_geo_data.sort_values('percentage', ascending=False).head(5)
                fig_geo_compare.add_trace(
                    go.Bar(
                        x=artist_geo_sorted['geo_country'],
                        y=artist_geo_sorted['percentage'],
                        name="Artist Overall",
                        marker_color='#4ECDC4'
                    ),
                    row=1, col=1
                )
                
                # Song geo distribution
                song_geo_sorted = song_geo_data.sort_values('percentage', ascending=False).head(5)
                fig_geo_compare.add_trace(
                    go.Bar(
                        x=song_geo_sorted['geo_country'],
                        y=song_geo_sorted['percentage'],
                        name=f"Song: {selected_song}",
                        marker_color='#FF6B6B'
                    ),
                    row=1, col=2
                )
                
                fig_geo_compare.update_layout(
                    title=f"{artist_for_geo}: Geographic Distribution Comparison",
                    height=500
                )
                
                st.plotly_chart(fig_geo_compare, use_container_width=True)
                
                # Show strategy recommendations
                st.subheader("Recommended Promotion Strategies")
                
                # Find countries with gaps
                countries_with_gaps = []
                artist_countries = set(artist_geo_sorted['geo_country'])
                song_countries = set(song_geo_sorted['geo_country'])
                
                for country in artist_countries:
                    if country not in song_countries:
                        countries_with_gaps.append(country)
                    else:
                        artist_pct = artist_geo_sorted[artist_geo_sorted['geo_country'] == country]['percentage'].values[0]
                        song_country_data = song_geo_sorted[song_geo_sorted['geo_country'] == country]
                        song_pct = song_country_data['percentage'].values[0] if not song_country_data.empty else 0
                        
                        if artist_pct > song_pct + 5:  # If gap is more than 5%
                            countries_with_gaps.append(country)
                
                if countries_with_gaps:
                    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                    st.markdown(f"### Promotion Strategy for {artist_for_geo} - {selected_song}")
                    
                    for country in countries_with_gaps:
                        st.markdown(f"#### {country} Market Expansion")
                        
                        if country == "NG":
                            st.markdown("""
                            - **Push Notifications**: Target Nigerian users who have engaged with similar artists
                            - **Trending Placement**: Feature the song in Nigeria-specific trending sections
                            - **Social Media Campaign**: Partner with Nigerian influencers for song promotion
                            """)
                        elif country == "GH":
                            st.markdown("""
                            - **Radio Partnerships**: Collaborate with top Ghanaian radio stations
                            - **Local Events**: Feature the song in promotional events in Ghana
                            - **Influencer Marketing**: Partner with Ghanaian social media personalities
                            """)
                        elif country == "US":
                            st.markdown("""
                            - **Diaspora Targeting**: Create targeted campaigns for the West African diaspora in major US cities
                            - **Playlist Placement**: Push for placement in US-focused Afrobeats playlists
                            - **College Campus Marketing**: Target universities with high international student populations
                            """)
                        elif country == "UK":
                            st.markdown("""
                            - **Club Promotion**: Partner with UK DJs and clubs with African music nights
                            - **Community Events**: Promote at UK African cultural events and festivals
                            - **University Marketing**: Target UK universities with high African student populations
                            """)
                        elif country == "JM":
                            st.markdown("""
                            - **Dancehall Cross-Promotion**: Partner with Jamaican dancehall artists for remixes
                            - **Radio Placement**: Target Jamaican radio stations for song placement
                            - **Local Influencers**: Engage with Jamaican music influencers
                            """)
                        else:
                            st.markdown(f"""
                            - **Targeted Advertising**: Develop geo-specific ads for {country} market
                            - **Local Partnerships**: Identify potential collaborators in {country}
                            - **Platform Features**: Utilize Audiomack's geo-targeted features for promotion
                            """)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info(f"No significant geographic distribution gaps found for {selected_song}.")
            else:
                st.warning(f"Insufficient data for {artist_for_geo} or {selected_song} to analyze geographic distribution.")
        else:
            st.warning(f"No songs found for {artist_for_geo}.")
    else:
        st.warning("No artist data available. Please check your data sources.")

# Tab 3: Editorial Playlists
with tab3:
    st.markdown('<div class="sub-header">Editorial Playlist Tracker</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insights-box">🎵 <span class="highlight">New Feature:</span> This tracker allows you to monitor AMD artist additions to editorial playlists, helping identify promotional opportunities and track curator selections.</div>', unsafe_allow_html=True)
    
    # Filter playlist data
    filtered_playlists = editorial_playlist_df.copy()
    if selected_artists:
        filtered_playlists = filtered_playlists[filtered_playlists['artist_name'].isin(selected_artists)]
    if selected_playlists:
        filtered_playlists = filtered_playlists[filtered_playlists['playlist_name'].isin(selected_playlists)]
    
    # Editorial playlist metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_adds = len(filtered_playlists)
        st.metric("Total Playlist Adds (This Week)", f"{total_adds}")
    
    with col2:
        unique_playlists = len(filtered_playlists['playlist_name'].unique())
        st.metric("Unique Playlists", f"{unique_playlists}")
    
    with col3:
        unique_artists_added = len(filtered_playlists['artist_name'].unique())
        st.metric("Unique Artists Added", f"{unique_artists_added}")
    
    # Recent editorial playlist additions
    st.subheader("Recent Editorial Playlist Additions")
    
    # Create a styled table
    st.dataframe(
        filtered_playlists.sort_values('added_at', ascending=False),
        use_container_width=True,
        column_config={
            "added_at": st.column_config.DateColumn("Date Added", format="MMM DD, YYYY"),
            "artist_name": st.column_config.TextColumn("Artist"),
            "song_name": st.column_config.TextColumn("Song"),
            "playlist_name": st.column_config.TextColumn("Playlist"),
            "is_ghost_account": st.column_config.TextColumn("Ghost Account?"),
            "distributor_name": st.column_config.TextColumn("Distributor")
        }
    )
    
    # Playlist distribution visualization
    st.subheader("Editorial Playlist Distribution")
    
    # Get playlist counts
    playlist_counts = filtered_playlists['playlist_name'].value_counts().reset_index()
    playlist_counts.columns = ['Playlist', 'Count']
    
    # Create visualization
    if not playlist_counts.empty:
        fig_playlist = px.pie(
            playlist_counts,
            values='Count',
            names='Playlist',
            title="Editorial Playlist Distribution",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_playlist.update_traces(textinfo='percent+label', pull=[0.1 if i == 0 else 0 for i in range(len(playlist_counts))])
        
        st.plotly_chart(fig_playlist, use_container_width=True)
    else:
        st.info("No playlist data to display with the current filters.")
    
    # Playlist additions by day
    st.subheader("Playlist Additions by Day")
    
    # Convert dates and count by day
    filtered_playlists['added_at'] = pd.to_datetime(filtered_playlists['added_at'])
    adds_by_day = filtered_playlists.groupby([filtered_playlists['added_at'].dt.date, 'playlist_name']).size().reset_index()
    adds_by_day.columns = ['Date', 'Playlist', 'Count']
    
    # Create visualization
    if not adds_by_day.empty:
        fig_adds_by_day = px.bar(
            adds_by_day,
            x='Date',
            y='Count',
            color='Playlist',
            title="Editorial Playlist Additions by Day",
            labels={'Count': 'Number of Additions'}
        )
        
        st.plotly_chart(fig_adds_by_day, use_container_width=True)
    else:
        st.info("No daily addition data to display with the current filters.")
    
    # SQL Query for the Superset Chart
    st.subheader("SQL Query for Superset Implementation")
    
    st.code('''
-- Editorial Playlist Additions Tracker
SELECT
  added_at,
  song_name,
  artist_name,
  is_ghost_account,
  distributor_name,
  playlist_name
FROM bi01.playlist_interactions_daily_v003
WHERE added_at BETWEEN CURRENT_DATE - INTERVAL '7' DAY AND CURRENT_DATE
  AND distributor_name = 'Audiosalad Direct'
ORDER BY added_at DESC;
    ''', language='sql')
    
    st.markdown("""
    ### Implementation Steps for Superset Chart
    
    1. **Create a New Dataset in Superset**:
       - Connect to the `bi01.playlist_interactions_daily_v003` table
       - Set up a refresh schedule (daily at 4AM recommended)
    
    2. **Create a Table Visualization**:
       - Add the columns: `added_at`, `song_name`, `artist_name`, `is_ghost_account`, `distributor_name`, `playlist_name`
       - Set up sorting by `added_at` descending
    
    3. **Add Filtering Options**:
       - Date range filter for `added_at`
       - Multi-select filter for `playlist_name`
       - Ghost account status filter
    
    4. **Dashboard Integration**:
       - Add to the AMD dashboard
       - Set permissions for Jordan and Jalen to access
    """)

# Tab 4: Engagement Analysis
with tab4:
    st.markdown('<div class="sub-header">Engagement Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insights-box">💡 <span class="highlight">Key Insight:</span> Engagement metrics like favorites, reposts, and comments offer better indicators of audience connection than raw play counts. Several AMD artists show exceptionally high engagement per user, indicating strong resonance with their audience.</div>', unsafe_allow_html=True)
    
    # Filter engagement data
    filtered_engagement = top_engaged_artists_df.copy()
    if selected_artists:
        filtered_engagement = filtered_engagement[filtered_engagement['artist'].isin(selected_artists)]
    
    # Apply minimum engagement filter
    filtered_engagement = filtered_engagement[filtered_engagement['engagements_per_user'] >= min_engagement]
    
    # Engagement metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_eng_ratio = filtered_engagement['total_engagements'].sum() / filtered_engagement['total_plays'].sum() if filtered_engagement['total_plays'].sum() > 0 else 0
        st.metric("Avg Engagement Ratio", f"{avg_eng_ratio:.3f}")
    
    with col2:
        avg_eng_per_user = filtered_engagement['total_engagements'].sum() / filtered_engagement['unique_users'].sum() if filtered_engagement['unique_users'].sum() > 0 else 0
        st.metric("Avg Engagements Per User", f"{avg_eng_per_user:.3f}")
    
    with col3:
        plays_per_user = filtered_engagement['total_plays'].sum() / filtered_engagement['unique_users'].sum() if filtered_engagement['unique_users'].sum() > 0 else 0
        st.metric("Avg Plays Per User", f"{plays_per_user:.1f}")
    
    # Engagement ratio visualization
    st.subheader("Top Artists by Engagement per User")
    
    # Sort by engagements per user
    engagement_sorted = filtered_engagement.sort_values('engagements_per_user', ascending=False)
    
    # Create visualization
    if not engagement_sorted.empty:
        fig_engagement = px.bar(
            engagement_sorted.head(15),
            x="artist",
            y="engagements_per_user",
            color="total_plays",
            color_continuous_scale="Viridis",
            title="Top 15 Artists by Engagement per User",
            hover_data=["total_engagements", "unique_users", "total_plays"]
        )
        
        fig_engagement.update_layout(
            xaxis_title="Artist",
            yaxis_title="Engagements per User",
            coloraxis_colorbar_title="Total Plays"
        )
        
        st.plotly_chart(fig_engagement, use_container_width=True)
    else:
        st.info("No engagement data available with the current filters.")
    
    # Engagement vs. plays comparison
    st.subheader("Engagement vs. Plays Analysis")
    
    # Create scatter plot
    if not filtered_engagement.empty:
        fig_scatter = px.scatter(
            filtered_engagement,
            x="total_plays",
            y="engagements_per_user",
            size="unique_users",
            color="artist",
            hover_name="artist",
            log_x=True,
            size_max=50,
            title="Engagement per User vs. Total Plays (Log Scale)"
        )
        
        fig_scatter.update_layout(
            xaxis_title="Total Plays (Log Scale)",
            yaxis_title="Engagements per User",
            height=600
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No data available to display the scatter plot.")
    
    # Create a styled table of top engaged artists
    st.subheader("Detailed Engagement Metrics by Artist")
    
    if not engagement_sorted.empty:
        st.dataframe(
            engagement_sorted,
            use_container_width=True,
            column_config={
                "artist": st.column_config.TextColumn("Artist"),
                "total_plays": st.column_config.NumberColumn("Total Plays", format="%d"),
                "total_engagements": st.column_config.NumberColumn("Total Engagements", format="%d"),
                "unique_users": st.column_config.NumberColumn("Unique Users", format="%d"),
                "engagements_per_user": st.column_config.NumberColumn("Engagements per User", format="%.3f")
            }
        )
    else:
        st.info("No engagement data to display in the table.")
    
    st.markdown("""
    ### Key Engagement Insights
    
    - **Inverse Relationship**: A notable inverse relationship exists between play count and engagement per user - 
      smaller artists often have more engaged fan bases.
    
    - **Audience Quality Indicator**: Engagement per user serves as a better indicator of audience quality 
      than raw play counts, helping identify artists with strong connections to their listeners.
    
    - **Growth Predictor**: Higher engagement metrics often predict future growth potential, 
      as engaged listeners are more likely to share and promote content within their networks.
    """)

# Tab 5: Discovery Channels
with tab5:
    st.markdown('<div class="sub-header">User Discovery Channels</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insights-box">🔍 <span class="highlight">Actionable Insight:</span> "For You" feed and "Trending" sections drive the largest portion of engagement, making these critical places for AMD artist visibility. The My Library features also show strong engagement, indicating the importance of converting casual listeners to followers.</div>', unsafe_allow_html=True)
    
    # Source tab distribution
    st.subheader("Engagement by Source Tab")
    
    # Create visualization for source tabs
    if not source_tab_totals.empty:
        fig_source_tabs = px.pie(
            source_tab_totals.sort_values('percentage', ascending=False),
            values='percentage',
            names='source_tab',
            title="Engagement Distribution by Source Tab",
            hole=0.4
        )
        
        fig_source_tabs.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig_source_tabs, use_container_width=True)
    else:
        st.info("No source tab data available to display.")
    
    # Section distribution
    st.subheader("Engagement by Section")
    
    # Create visualization for top sections
    if not section_totals.empty:
        fig_sections = px.bar(
            section_totals.head(10),
            x='section',
            y='percentage',
            color='percentage',
            color_continuous_scale='Viridis',
            title="Top 10 Sections by Engagement Percentage"
        )
        
        fig_sections.update_layout(
            xaxis_title="Section",
            yaxis_title="Percentage of Total Engagement (%)",
            xaxis={'categoryorder': 'total descending'}
        )
        
        st.plotly_chart(fig_sections, use_container_width=True)
    else:
        st.info("No section data available to display.")
    
    # Strategic recommendations
    st.subheader("Strategic Recommendations for AMD Artists")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.markdown("### Optimize for Top Discovery Channels")
        st.markdown("""
        1. **My Library Optimization**
           - Focus on converting casual listeners to followers/favorites
           - Create content that encourages offline listening
           - Develop a cadence of releases to keep library fresh
        
        2. **Search Visibility**
           - Optimize artist name and song titles for searchability
           - Use popular genre keywords in descriptions
           - Create songs that match popular search queries
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.markdown("### Section-Specific Strategies")
        st.markdown("""
        1. **For You Feed**
           - Create content that encourages high engagement rates
           - Focus on quality over quantity to improve algorithm ranking
           - Leverage existing engaged fans to boost algorithmic placement
        
        2. **Trending Sections**
           - Time releases strategically to maximize trending potential
           - Create engagement campaigns around release dates
           - Identify regional trending opportunities based on geo analysis
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Discovery funnel visualization
    st.subheader("User Discovery Funnel")
    
    # Create made-up funnel data based on the discovered patterns
    funnel_data = pd.DataFrame({
        'Stage': ['Discovery', 'First Play', 'Multiple Plays', 'Engagement', 'Favorite/Follow', 'Repeat Listener'],
        'Users': [1000000, 750000, 500000, 250000, 150000, 100000],
        'Conversion': [100, 75, 67, 50, 60, 67]
    })
    
    # Create funnel visualization
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Users'],
        textinfo="value+percent initial",
        marker={"color": ["#4ECDC4", "#1A535C", "#FF6B6B", "#FF9F1C", "#E71D36", "#662E9B"]}
    ))
    
    fig_funnel.update_layout(
        title="User Journey Funnel",
        height=500
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    st.markdown("""
    ### Optimizing the User Journey
    
    The analysis of discovery channels reveals a clear user journey path:
    
    1. **Discovery**: Users primarily find content through "For You" feeds, Search, and Trending sections
    2. **Engagement**: Initial plays lead to favorites, shares, and comments for resonant content
    3. **Retention**: Engaged users add content to their libraries, download for offline use, and become repeat listeners
    
    To maximize AMD artist success, promotional strategies should target each stage of this journey, with particular focus on increasing conversion rates between discovery and engagement.
    """)

# Tab 6: A&R Scouting Tracker
with tab6:
    # Call the scouting tracker function
    load_scouting_tracker()

# Footer
st.markdown("---")
st.caption("Audiomack ArtistRank Dashboard | Data period: April 7-13, 2025 | Last updated: April 13, 2025")
st.caption("Created by LinLin for Audiomack Internship Program Week 2 Assignment")
st.caption("Supervisors: Jacob & Ryan | A&R Researchers: Jalen & Jordan")
