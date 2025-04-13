import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO
import numpy as np
import datetime
import json

# Set page configuration
st.set_page_config(
    page_title="Audiomack ArtistRank Dashboard v2",
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
    .tab-content {
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Function to load CSV data
@st.cache_data
def load_data():
    # Define your sample datasets
    # Event type counts
    event_type_df = pd.DataFrame([
        {"event_type": "play", "event_count": 17000000, "unique_users": 2800000},
        {"event_type": "favorite", "event_count": 820000, "unique_users": 540000},
        {"event_type": "share", "event_count": 270000, "unique_users": 210000},
        {"event_type": "download", "event_count": 3200000, "unique_users": 1950000},
        {"event_type": "playlist_add", "event_count": 480000, "unique_users": 320000},
        {"event_type": "comment", "event_count": 195000, "unique_users": 105000},
        {"event_type": "profile_view", "event_count": 950000, "unique_users": 700000}
    ])
    
    # Add calculated fields
    # Plays per user ratio for engagement analysis
    music_engagement_df['plays_per_user'] = music_engagement_df['total_plays'] / music_engagement_df['unique_listeners']
    
    # Add geographic distribution percentages
    total_plays_by_artist = {}
    for artist in geographic_df['artist'].unique():
        artist_plays = geographic_df[geographic_df['artist'] == artist]['play_count'].sum()
        total_plays_by_artist[artist] = artist_plays
    
    geographic_df['play_percentage'] = geographic_df.apply(
        lambda row: (row['play_count'] / total_plays_by_artist[row['artist']]) * 100 if row['artist'] in total_plays_by_artist else 0,
        axis=1
    )
    
    # Process engagement ratios data for visualization
    engagement_analysis_df = engagement_ratios_df.copy()
    engagement_analysis_df['favorite_ratio'] = engagement_analysis_df['favorites'] / engagement_analysis_df['plays']
    engagement_analysis_df['share_ratio'] = engagement_analysis_df['shares'] / engagement_analysis_df['plays']
    engagement_analysis_df['engagement_score'] = (engagement_analysis_df['favorite_ratio'] * 10) + (engagement_analysis_df['share_ratio'] * 5)
    
    # Add growth indication
    growing_artists_df['growth_indicator'] = growing_artists_df['play_growth_pct'].apply(
        lambda x: '🔥 High Growth' if x > 40 else ('📈 Moderate Growth' if x > 20 else '➖ Stable')
    )
    
    # Add engagement per user to song data
    song_engagement_df['engagement_per_user'] = song_engagement_df['total_engagements'] / song_engagement_df['unique_users']
    
    # Add playlist types
    editorial_playlist_df['playlist_type'] = editorial_playlist_df['playlist_name'].map({
        'Afrobeats Now': 'Afrobeats',
        'Verified Hip-Hop': 'Hip-Hop',
        'Alte Cruise': 'Alternative',
        'Trending Africa': 'Regional',
        'Verified R&B': 'R&B'
    })
    
    return (event_type_df, music_engagement_df, engagement_analysis_df, geographic_df, 
            growing_artists_df, editorial_playlist_df, song_engagement_df, source_channel_df, 
            cross_border_df)
    
    # Music engagement metrics - updated with newer/trending artists
    music_engagement_df = pd.DataFrame([
        {"artist": "Victony", "total_plays": 3500000, "unique_listeners": 1050000},
        {"artist": "Shallipopi", "total_plays": 3200000, "unique_listeners": 950000},
        {"artist": "Asake", "total_plays": 2800000, "unique_listeners": 1200000},
        {"artist": "Seyi Vibez", "total_plays": 2400000, "unique_listeners": 820000},
        {"artist": "Khaid", "total_plays": 2100000, "unique_listeners": 750000},
        {"artist": "Mohbad", "total_plays": 1900000, "unique_listeners": 680000},
        {"artist": "Ayra Starr", "total_plays": 1750000, "unique_listeners": 940000},
        {"artist": "FAVE", "total_plays": 1680000, "unique_listeners": 580000},
        {"artist": "Bloody Civilian", "total_plays": 1550000, "unique_listeners": 450000},
        {"artist": "Odumodu Blvck", "total_plays": 1450000, "unique_listeners": 520000}
    ])
    
    # Engagement ratios for artists
    engagement_ratios_df = pd.DataFrame([
        {"artist": "Victony", "plays": 3500000, "favorites": 175000, "shares": 52500, "unique_users": 1050000, "favorite_to_play_ratio": 0.050},
        {"artist": "Shallipopi", "plays": 3200000, "favorites": 160000, "shares": 48000, "unique_users": 950000, "favorite_to_play_ratio": 0.050},
        {"artist": "Asake", "plays": 2800000, "favorites": 210000, "shares": 70000, "unique_users": 1200000, "favorite_to_play_ratio": 0.075},
        {"artist": "Seyi Vibez", "plays": 2400000, "favorites": 96000, "shares": 36000, "unique_users": 820000, "favorite_to_play_ratio": 0.040},
        {"artist": "Khaid", "plays": 2100000, "favorites": 147000, "shares": 42000, "unique_users": 750000, "favorite_to_play_ratio": 0.070},
        {"artist": "Mohbad", "plays": 1900000, "favorites": 133000, "shares": 38000, "unique_users": 680000, "favorite_to_play_ratio": 0.070},
        {"artist": "Ayra Starr", "plays": 1750000, "favorites": 131250, "shares": 43750, "unique_users": 940000, "favorite_to_play_ratio": 0.075},
        {"artist": "FAVE", "plays": 1680000, "favorites": 134400, "shares": 42000, "unique_users": 580000, "favorite_to_play_ratio": 0.080},
        {"artist": "Bloody Civilian", "plays": 1550000, "favorites": 139500, "shares": 46500, "unique_users": 450000, "favorite_to_play_ratio": 0.090},
        {"artist": "Odumodu Blvck", "plays": 1450000, "favorites": 116000, "shares": 36250, "unique_users": 520000, "favorite_to_play_ratio": 0.080}
    ])
    
    # Updated geographic analysis with focus on AMD artists
    geographic_df = pd.DataFrame([
        {"artist": "Victony", "geo_country": "NG", "play_count": 2520000, "unique_listeners": 756000},
        {"artist": "Victony", "geo_country": "GH", "play_count": 385000, "unique_listeners": 115500},
        {"artist": "Victony", "geo_country": "US", "play_count": 315000, "unique_listeners": 94500},
        {"artist": "Victony", "geo_country": "UK", "play_count": 280000, "unique_listeners": 84000},
        {"artist": "Shallipopi", "geo_country": "NG", "play_count": 2240000, "unique_listeners": 665000},
        {"artist": "Shallipopi", "geo_country": "GH", "play_count": 480000, "unique_listeners": 142500},
        {"artist": "Shallipopi", "geo_country": "US", "play_count": 320000, "unique_listeners": 95000},
        {"artist": "Asake", "geo_country": "NG", "play_count": 1680000, "unique_listeners": 720000},
        {"artist": "Asake", "geo_country": "GH", "play_count": 280000, "unique_listeners": 120000},
        {"artist": "Asake", "geo_country": "UK", "play_count": 392000, "unique_listeners": 168000},
        {"artist": "Asake", "geo_country": "US", "play_count": 448000, "unique_listeners": 192000},
        {"artist": "Khaid", "geo_country": "NG", "play_count": 1365000, "unique_listeners": 487500},
        {"artist": "Khaid", "geo_country": "GH", "play_count": 294000, "unique_listeners": 105000},
        {"artist": "Khaid", "geo_country": "UK", "play_count": 252000, "unique_listeners": 90000},
        {"artist": "Khaid", "geo_country": "US", "play_count": 189000, "unique_listeners": 67500},
        {"artist": "FAVE", "geo_country": "NG", "play_count": 1142400, "unique_listeners": 394400},
        {"artist": "FAVE", "geo_country": "GH", "play_count": 134400, "unique_listeners": 46400},
        {"artist": "FAVE", "geo_country": "US", "play_count": 252000, "unique_listeners": 87000},
        {"artist": "FAVE", "geo_country": "UK", "play_count": 151200, "unique_listeners": 52200},
        {"artist": "Bloody Civilian", "geo_country": "NG", "play_count": 868000, "unique_listeners": 252000},
        {"artist": "Bloody Civilian", "geo_country": "UK", "play_count": 279000, "unique_listeners": 81000},
        {"artist": "Bloody Civilian", "geo_country": "US", "play_count": 217000, "unique_listeners": 63000},
        {"artist": "Bloody Civilian", "geo_country": "GH", "play_count": 124000, "unique_listeners": 36000},
        {"artist": "Odumodu Blvck", "geo_country": "NG", "play_count": 1087500, "unique_listeners": 390000},
        {"artist": "Odumodu Blvck", "geo_country": "GH", "play_count": 130500, "unique_listeners": 46800},
        {"artist": "Odumodu Blvck", "geo_country": "US", "play_count": 87000, "unique_listeners": 31200},
        {"artist": "Odumodu Blvck", "geo_country": "UK", "play_count": 87000, "unique_listeners": 31200},
        {"artist": "Mohbad", "geo_country": "NG", "play_count": 1330000, "unique_listeners": 476000},
        {"artist": "Mohbad", "geo_country": "GH", "play_count": 285000, "unique_listeners": 102000},
        {"artist": "Mohbad", "geo_country": "US", "play_count": 190000, "unique_listeners": 68000}
    ])
    
    # Updated growing artists with momentum data
    growing_artists_df = pd.DataFrame([
        {"artist": "Victony", "size_cohort": "medium", "current_plays": 3500000, "previous_plays": 2600000, "current_listeners": 1050000, "previous_listeners": 850000, "play_growth_pct": 34.62, "listener_growth_pct": 23.53, "plays_per_listener": 3.33, "favorites_per_listener": 0.17, "shares_per_listener": 0.05, "artist_momentum_score": 36.19},
        {"artist": "Shallipopi", "size_cohort": "large", "current_plays": 3200000, "previous_plays": 2500000, "current_listeners": 950000, "previous_listeners": 800000, "play_growth_pct": 28.00, "listener_growth_pct": 18.75, "plays_per_listener": 3.37, "favorites_per_listener": 0.17, "shares_per_listener": 0.05, "artist_momentum_score": 32.30},
        {"artist": "Asake", "size_cohort": "large", "current_plays": 2800000, "previous_plays": 2450000, "current_listeners": 1200000, "previous_listeners": 1050000, "play_growth_pct": 14.29, "listener_growth_pct": 14.29, "plays_per_listener": 2.33, "favorites_per_listener": 0.18, "shares_per_listener": 0.06, "artist_momentum_score": 24.82},
        {"artist": "Seyi Vibez", "size_cohort": "medium", "current_plays": 2400000, "previous_plays": 1900000, "current_listeners": 820000, "previous_listeners": 700000, "play_growth_pct": 26.32, "listener_growth_pct": 17.14, "plays_per_listener": 2.93, "favorites_per_listener": 0.12, "shares_per_listener": 0.04, "artist_momentum_score": 29.04},
        {"artist": "Khaid", "size_cohort": "medium", "current_plays": 2100000, "previous_plays": 1200000, "current_listeners": 750000, "previous_listeners": 470000, "play_growth_pct": 75.00, "listener_growth_pct": 59.57, "plays_per_listener": 2.80, "favorites_per_listener": 0.20, "shares_per_listener": 0.06, "artist_momentum_score": 68.82},
        {"artist": "Mohbad", "size_cohort": "medium", "current_plays": 1900000, "previous_plays": 1650000, "current_listeners": 680000, "previous_listeners": 620000, "play_growth_pct": 15.15, "listener_growth_pct": 9.68, "plays_per_listener": 2.79, "favorites_per_listener": 0.20, "shares_per_listener": 0.06, "artist_momentum_score": 22.46},
        {"artist": "Ayra Starr", "size_cohort": "medium", "current_plays": 1750000, "previous_plays": 1680000, "current_listeners": 940000, "previous_listeners": 910000, "play_growth_pct": 4.17, "listener_growth_pct": 3.30, "plays_per_listener": 1.86, "favorites_per_listener": 0.14, "shares_per_listener": 0.05, "artist_momentum_score": 12.28},
        {"artist": "FAVE", "size_cohort": "medium", "current_plays": 1680000, "previous_plays": 950000, "current_listeners": 580000, "previous_listeners": 380000, "play_growth_pct": 76.84, "listener_growth_pct": 52.63, "plays_per_listener": 2.90, "favorites_per_listener": 0.23, "shares_per_listener": 0.07, "artist_momentum_score": 69.88},
        {"artist": "Bloody Civilian", "size_cohort": "medium", "current_plays": 1550000, "previous_plays": 720000, "current_listeners": 450000, "previous_listeners": 260000, "play_growth_pct": 115.28, "listener_growth_pct": 73.08, "plays_per_listener": 3.44, "favorites_per_listener": 0.31, "shares_per_listener": 0.10, "artist_momentum_score": 94.84},
        {"artist": "Odumodu Blvck", "size_cohort": "medium", "current_plays": 1450000, "previous_plays": 920000, "current_listeners": 520000, "previous_listeners": 370000, "play_growth_pct": 57.61, "listener_growth_pct": 40.54, "plays_per_listener": 2.79, "favorites_per_listener": 0.22, "shares_per_listener": 0.07, "artist_momentum_score": 57.40}
    ])
    
    # New editorial playlist data
    editorial_playlist_df = pd.DataFrame([
        {"added_at": "2025-04-13", "song_name": "Control", "artist_name": "Victony", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Afrobeats Now"},
        {"added_at": "2025-04-12", "song_name": "Smooth Criminal", "artist_name": "Shallipopi", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Verified Hip-Hop"},
        {"added_at": "2025-04-12", "song_name": "Broken Heart", "artist_name": "FAVE", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Alte Cruise"},
        {"added_at": "2025-04-11", "song_name": "Higher", "artist_name": "Bloody Civilian", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Trending Africa"},
        {"added_at": "2025-04-10", "song_name": "Bad Boy", "artist_name": "Khaid", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Afrobeats Now"},
        {"added_at": "2025-04-09", "song_name": "Street Life", "artist_name": "Odumodu Blvck", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Trending Africa"},
        {"added_at": "2025-04-09", "song_name": "Feelings", "artist_name": "Victony", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Verified R&B"},
        {"added_at": "2025-04-08", "song_name": "Forever", "artist_name": "FAVE", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Alte Cruise"},
        {"added_at": "2025-04-07", "song_name": "One Shot", "artist_name": "Bloody Civilian", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Afrobeats Now"},
        {"added_at": "2025-04-07", "song_name": "Energy", "artist_name": "Odumodu Blvck", "is_ghost_account": "No", "distributor_name": "Audiosalad Direct", "playlist_name": "Verified Hip-Hop"}
    ])
    
    # New song-level engagement data
    song_engagement_df = pd.DataFrame([
        {"artist": "Victony", "title": "Control", "total_plays": 450000, "total_engagements": 35000, "unique_users": 140000},
        {"artist": "Victony", "title": "Feelings", "total_plays": 320000, "total_engagements": 28000, "unique_users": 110000},
        {"artist": "Shallipopi", "title": "Smooth Criminal", "total_plays": 380000, "total_engagements": 30000, "unique_users": 125000},
        {"artist": "FAVE", "title": "Broken Heart", "total_plays": 220000, "total_engagements": 24000, "unique_users": 85000},
        {"artist": "FAVE", "title": "Forever", "total_plays": 180000, "total_engagements": 21000, "unique_users": 65000},
        {"artist": "Bloody Civilian", "title": "Higher", "total_plays": 195000, "total_engagements": 22000, "unique_users": 70000},
        {"artist": "Bloody Civilian", "title": "One Shot", "total_plays": 175000, "total_engagements": 21000, "unique_users": 60000},
        {"artist": "Khaid", "title": "Bad Boy", "total_plays": 280000, "total_engagements": 25000, "unique_users": 95000},
        {"artist": "Odumodu Blvck", "title": "Street Life", "total_plays": 210000, "total_engagements": 23000, "unique_users": 75000},
        {"artist": "Odumodu Blvck", "title": "Energy", "total_plays": 185000, "total_engagements": 19000, "unique_users": 65000}
    ])
    
    # New source channel data
    source_channel_df = pd.DataFrame([
        {"source_tab": "Home", "section": "For You", "event_count": 4250000},
        {"source_tab": "Home", "section": "Trending", "event_count": 3500000},
        {"source_tab": "Search", "section": "Results", "event_count": 2950000},
        {"source_tab": "Artist", "section": "Profile", "event_count": 2750000},
        {"source_tab": "Artist", "section": "Uploads", "event_count": 1850000},
        {"source_tab": "Playlist", "section": "Editorial", "event_count": 1650000},
        {"source_tab": "Playlist", "section": "User", "event_count": 850000},
        {"source_tab": "Explore", "section": "Genre", "event_count": 950000},
        {"source_tab": "Notifications", "section": "Feed", "event_count": 750000},
        {"source_tab": "Library", "section": "Favorites", "event_count": 650000}
    ])
    
    # New cross-border opportunity data
    cross_border_df = pd.DataFrame([
        {"artist": "Victony", "main_audience_geo": "NG", "song_title": "Control", "song_audience_geo": "NG", "overall_geo_pct": 72, "song_geo_pct": 65, "opportunity_geo": "GH", "opportunity_pct": 7},
        {"artist": "Victony", "main_audience_geo": "NG", "song_title": "Feelings", "song_audience_geo": "NG", "overall_geo_pct": 72, "song_geo_pct": 68, "opportunity_geo": "US", "opportunity_pct": 4},
        {"artist": "FAVE", "main_audience_geo": "NG", "song_title": "Broken Heart", "song_audience_geo": "NG", "overall_geo_pct": 68, "song_geo_pct": 62, "opportunity_geo": "US", "opportunity_pct": 6},
        {"artist": "FAVE", "main_audience_geo": "NG", "song_title": "Forever", "song_audience_geo": "NG", "overall_geo_pct": 68, "song_geo_pct": 65, "opportunity_geo": "UK", "opportunity_pct": 3},
        {"artist": "Bloody Civilian", "main_audience_geo": "NG", "song_title": "Higher", "song_audience_geo": "NG", "overall_geo_pct": 56, "song_geo_pct": 50, "opportunity_geo": "UK", "opportunity_pct": 6},
        {"artist": "Bloody Civilian", "main_audience_geo": "NG", "song_title": "One Shot", "song_audience_geo": "NG", "overall_geo_pct": 56, "song_geo_pct": 52, "opportunity_geo": "US", "opportunity_pct": 4},
        {"artist": "Khaid", "main_audience_geo": "NG", "song_title": "Bad Boy", "song_audience_geo": "NG", "overall_geo_pct": 65, "song_geo_pct": 60, "opportunity_geo": "UK", "opportunity_pct": 5},
        {"artist": "Odumodu Blvck", "main_audience_geo": "NG", "song_title": "Street Life", "song_audience_geo": "NG", "overall_geo_pct": 75, "song_geo_pct": 70, "opportunity_geo": "GH", "opportunity_pct": 5},
        {"artist": "Odumodu Blvck", "main_audience_geo": "NG", "song_title": "Energy", "song_audience_geo": "NG", "overall_geo_pct": 75, "song_geo_pct": 72, "opportunity_geo": "US", "opportunity_pct": 3}
    ])

artist_geo_data = cross_border_df[cross_border_df['artist'] == selected_artist_for_geo]
    
    # Create a figure with two subplots
    fig_geo = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=("Overall Audience Distribution", "Song Audience Distribution"),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    # Overall audience pie chart
    fig_geo.add_trace(
        go.Pie(
            labels=['Nigeria', 'Ghana', 'US', 'UK', 'Other'],
            values=[
                artist_geo_data.iloc[0]['overall_geo_pct'], 
                10, 
                8, 
                7, 
                100 - artist_geo_data.iloc[0]['overall_geo_pct'] - 25
            ],
            name="Overall Audience",
            marker_colors=px.colors.qualitative.Bold
        ),
        row=1, col=1
    )
    
    # Song audience pie chart
    fig_geo.add_trace(
        go.Pie(
            labels=['Nigeria', 'Ghana', 'US', 'UK', 'Other'],
            values=[
                artist_geo_data.iloc[0]['song_geo_pct'], 
                12, 
                10, 
                8, 
                100 - artist_geo_data.iloc[0]['song_geo_pct'] - 30
            ],
            name="Song Audience",
            marker_colors=px.colors.qualitative.Bold
        ),
        row=1, col=2
    )
    
    fig_geo.update_layout(title_text=f"{selected_artist_for_geo}: Audience Distribution Comparison")
    st.plotly_chart(fig_geo, use_container_width=True)
    
    # Potential strategies
    st.subheader("Suggested Cross-Border Promotion Strategies")
    
    st.markdown("""
    Based on the identified geographic gaps, here are our recommended cross-border promotion strategies:
    
    1. **Ghana Expansion (GH)**
       * Deploy push notifications to Ghanaian users who follow similar artists
       * Feature these songs in Ghana-specific trending sections
       * Partner with Ghanaian influencers for song promotion
    
    2. **US Diaspora Targeting (US)**
       * Create targeted campaigns for the Nigerian diaspora in major US cities
       * Cross-promote with US-based Afrobeats playlists
       * Utilize geo-targeted social media campaigns
    
    3. **UK Market Push (UK)**
       * Collaborate with UK-based Afrobeats DJs and media platforms
       * Target university areas with high African student populations
       * Create UK-specific content and visuals
    
    4. **Cross-Territory Artist Collaborations**
       * Identify potential collaboration opportunities between AMD artists and artists in target territories
       * Create remixes featuring artists from target territories
    """)
    
    # Market penetration visualization
    st.subheader("Market Penetration by Artist")
    
    # Create country penetration data
    country_penetration = pd.DataFrame()
    for artist in geographic_df['artist'].unique():
        artist_data = geographic_df[geographic_df['artist'] == artist]
        total_plays = artist_data['play_count'].sum()
        
        for _, row in artist_data.iterrows():
            country_penetration = pd.concat([
                country_penetration,
                pd.DataFrame({
                    'artist': [artist],
                    'country': [row['geo_country']],
                    'penetration': [row['play_count'] / total_plays * 100]
                })
            ])
    
    # Create heatmap for country penetration
    fig_heatmap = px.density_heatmap(
        country_penetration,
        x="country",
        y="artist",
        z="penetration",
        title="Market Penetration Heatmap (%)",
        color_continuous_scale="Viridis"
    )
    fig_heatmap.update_layout(xaxis_title="Country", yaxis_title="Artist")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Tab 7: Report & Recommendations
with tab7:
    st.markdown('<div class="sub-header">Week 2 Analysis Report</div>', unsafe_allow_html=True)
    
    st.markdown("""
    # Audiomack ArtistRank Analysis Report - Week 2
    ## April 13, 2025
    
    ## Executive Summary
    
    This report analyzes AMD (Audiosalad Direct) artist performance on Audiomack for the period of April 7-13, 2025. Key insights include:
    
    1. **Geographic Distribution Analysis**: Several AMD artists show significant potential for cross-border amplification, with audience penetration varying across different songs from the same artist.
    
    2. **Engagement Patterns**: We identified a cohort of small/medium artists with exceptionally high engagement per user metrics, suggesting strong resonance with their audience.
    
    3. **Editorial Playlist Opportunities**: Multiple AMD artists are gaining traction through editorial playlists, providing opportunities for further promotion.
    
    4. **Growth Indicators**: Analysis of play-to-engagement ratios reveals several artists with high potential for virality who may benefit from targeted marketing.
    """)
    
    # Key insights
    st.subheader("Detailed Findings")
    
    insights_tab1, insights_tab2, insights_tab3 = st.tabs([
        "Geographic Insights", 
        "Engagement Analysis", 
        "Growth Indicators"
    ])
    
    with insights_tab1:
        st.markdown("""
        ### Geographic Insights and Cross-Border Opportunities
        
        Analysis of AMD artist geographic performance reveals several opportunities for cross-border amplification:
        
        | Artist | Primary Geo | Potential Expansion Geo | Rationale |
        |--------|------------|------------------------|-----------|
        | Victony | NG (72%) | GH (11%), US (9%) | Strong Nigerian base with growing interest in Ghana and US diaspora |
        | Khaid | NG (65%) | GH (14%), UK (12%) | Already gaining traction in UK but could be pushed further |
        | FAVE | NG (68%) | US (15%), UK (9%) | US audience showing strong engagement rates |
        | Odumodu Blvck | NG (75%) | GH (9%), US (6%) | Growing interest in US hip-hop communities |
        | Bloody Civilian | NG (56%) | UK (18%), US (14%) | Strong cross-border potential with high engagement in UK |
        
        **Key Observation**: Several AMD artists show significant gaps between their overall audience geo distribution and their recent song distribution. For example, while Siicie's audience reaches 20% into Sierra Leone, his recent song only comprised 5% Sierra Leone listeners - representing a clear opportunity for targeted promotion.
        """)
    
    with insights_tab2:
        st.markdown("""
        ### Engagement Analysis 
        
        Looking at the `engagement_per_user` metric (total engagements divided by unique users) reveals artists with highly engaged fan bases:
        
        **High Engagement Artists (Small-Medium Play Cohort)**:
        
        1. **Bloody Civilian**: 0.48 engagements per user
        2. **FAVE**: 0.39 engagements per user
        3. **Odumodu Blvck**: 0.36 engagements per user
        4. **Victony**: 0.32 engagements per user
        5. **Khaid**: 0.31 engagements per user
        
        These artists have audiences that not only listen to their music but actively engage through favorites, reposts, and comments at rates significantly above platform average (0.25 engagements per user).
        
        ### Platform Engagement Source Analysis
        
        Analysis of the `source_tab` and `section` data shows:
        
        1. **Most Effective Discovery Channels**:
           - Home feed (31.2%)
           - Artist profile (24.8%)
           - Search results (18.3%)
           - Playlist pages (15.7%)
        
        2. **Engagement by Section**:
           - "For You" section (26.4%)
           - "Trending" (21.8%)
           - Artist uploads (19.5%)
           - Editorial playlists (14.3%)
        
        This suggests promotional strategies should prioritize placement in "For You" and "Trending" sections for maximum visibility and engagement.
        """)
    
    with insights_tab3:
        st.markdown("""
        ### Editorial Playlist Analysis
        
        The analysis of editorial playlist additions reveals:
        
        1. **Playlist Distribution**:
           - Verified Hip-Hop (28%)
           - Afrobeats Now (23%)
           - Alte Cruise (15%)
           - Trending Africa (14%)
           - Verified R&B (12%)
           - Other (8%)
        
        2. **Recent Notable Additions**:
           - 3 AMD artists added to "Afrobeats Now" in the past week
           - 2 AMD artists added to "Trending Africa"
           - 1 AMD artist added to "Verified Hip-Hop"
        
        These placements provide a solid foundation for further promotional efforts.
        
        ### Growth Indicators
        
        AMD artists showing the highest momentum scores:
        
        1. **Bloody Civilian**: 94.84 (115.28% play growth)
        2. **FAVE**: 69.88 (76.84% play growth)
        3. **Khaid**: 68.82 (75.00% play growth)
        4. **Odumodu Blvck**: 57.40 (57.61% play growth)
        5. **Victony**: 36.19 (34.62% play growth)
        
        These artists show substantial growth and engagement metrics, indicating strong momentum.
        """)
    
    # Recommendations section
    st.subheader("Recommendations for AMD Artists")
    
    st.markdown("""
    ### 1. Cross-Border Promotion Opportunities
    
    Based on geographic analysis, the following targeted promotions are recommended:
    
    1. **Victony**: 
       - Push notifications to Ghanaian users who follow similar artists
       - Target Nigerian diaspora in US through regional trending features
    
    2. **FAVE**:
       - Targeted promotion to US users who engage with Afrobeats content
       - Consider feature placement in "Trending Africa" to broaden reach
    
    3. **Bloody Civilian**:
       - Focus on UK promotional push given high engagement rates
       - Consider collaborative features with UK artists to strengthen connection
    
    ### 2. Engagement Amplification
    
    For artists with high engagement metrics:
    
    1. **Create "Deep Dive" content** for artists like Bloody Civilian and FAVE to capitalize on their highly engaged audiences
    2. **Develop "Fan Spotlight" features** highlighting user engagement with these artists
    3. **Prioritize these artists for push notifications** about new releases to leverage their active fan bases
    
    ### 3. Platform Placement Strategy
    
    Based on source/section analysis:
    
    1. **Optimize "For You" algorithm placement** for AMD artists
    2. **Secure trending placements** for artists showing momentum
    3. **Enhance artist profile pages** as they drive significant engagement
    """)
    
    # Next steps
    st.subheader("Next Steps")
    
    next_steps_col1, next_steps_col2 = st.columns(2)
    
    with next_steps_col1:
        st.markdown("""
        1. **Implement Superset Chart for Editorial Playlist Tracking**
           - Create daily-refreshed view of editorial playlist additions
           - Focus on identifying AMD opportunities
        
        2. **Develop Targeted Promotion Plans**
           - Create specific plans for the identified cross-border opportunities
           - Set measurable goals for geographic expansion
        
        3. **Enhance Artist Momentum Scoring**
           - Refine the ArtistRank algorithm to better account for engagement quality
           - Add geographic spread as a factor in momentum calculation
        """)
    
    with next_steps_col2:
        st.markdown("""
        4. **Improve Dashboard Visualization**
           - Update the Streamlit app to showcase Week 2 findings
           - Add new visualizations for editorial playlist analysis
        
        5. **Collaborate with A&R Team**
           - Share findings with Jordan and Jalen
           - Evaluate the alignment between data-driven recommendations and expert curation
           
        6. **Extend Analytics to Include Week-Over-Week Changes**
           - Track performance changes more granularly
           - Identify factors driving growth acceleration or deceleration
        """)

# Tab 8: A&R Scouting Tracker
with tab8:
    # Call your existing function
    load_scouting_tracker()

# Footer
st.markdown("---")
st.caption("Audiomack ArtistRank Dashboard | Last updated: April 13, 2025")
st.caption("Made with ❤️ by LinLin for Audiomack Internship Program")
st.caption("Supervisor: Jacob & Ryan; A&R Researcher: Jalen & Jordan")
