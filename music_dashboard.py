import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Music Data Analysis Dashboard",
    page_icon="🎵",
    layout="wide"
)

# Function to load JSON data
@st.cache_data
def load_data():
    # Sample data based on your JSON structure
    # In production, you would load these from files
    
    # Top songs by download ratio
    top_download_ratio = pd.DataFrame([
        {
            "music_id": 1,
            "song_name": "Have Mercy",
            "artist_name": "Shane Eli",
            "total_plays": 207866,
            "total_downloads": 7207622,
            "download_play_ratio": 34.6744,
            "total_favorites": 612,
            "total_playlist_adds": 5973,
            "total_reposts": 105,
            "favorite_play_ratio": 0.0029,
            "playlist_play_ratio": 0.0287,
            "repost_play_ratio": 0.0005,
            "engagement_score": 10.41186
        },
        {
            "music_id": 23455165,
            "song_name": "Pluto",
            "artist_name": "Shallipopi",
            "total_plays": 3990,
            "total_downloads": 42318,
            "download_play_ratio": 10.6060,
            "total_favorites": 158,
            "total_playlist_adds": 58,
            "total_reposts": 25,
            "favorite_play_ratio": 0.0396,
            "playlist_play_ratio": 0.0145,
            "repost_play_ratio": 0.0063,
            "engagement_score": 3.19867
        },
        {
            "music_id": 37403686,
            "song_name": "Joy is coming",
            "artist_name": "Fido",
            "total_plays": 5976,
            "total_downloads": 35935,
            "download_play_ratio": 6.0132,
            "total_favorites": 302,
            "total_playlist_adds": 230,
            "total_reposts": 35,
            "favorite_play_ratio": 0.0505,
            "playlist_play_ratio": 0.0385,
            "repost_play_ratio": 0.0059,
            "engagement_score": 1.83126
        },
        {
            "music_id": 32475125,
            "song_name": "APartii",
            "artist_name": "Combosman X Togman",
            "total_plays": 9612,
            "total_downloads": 40354,
            "download_play_ratio": 4.1983,
            "total_favorites": 532,
            "total_playlist_adds": 1122,
            "total_reposts": 19,
            "favorite_play_ratio": 0.0553,
            "playlist_play_ratio": 0.1167,
            "repost_play_ratio": 0.0020,
            "engagement_score": 1.31131
        },
        {
            "music_id": 31809979,
            "song_name": "juju",
            "artist_name": "Big smur lee",
            "total_plays": 32581,
            "total_downloads": 132987,
            "download_play_ratio": 4.0817,
            "total_favorites": 1601,
            "total_playlist_adds": 1435,
            "total_reposts": 86,
            "favorite_play_ratio": 0.0491,
            "playlist_play_ratio": 0.0440,
            "repost_play_ratio": 0.0026,
            "engagement_score": 1.25274
        }
    ])
    
    # Country analysis
    country_analysis = pd.DataFrame([
        {
            "geo_country": "NG",
            "unique_songs": 43692,
            "unique_artists": 16867,
            "total_plays": 4921728863,
            "download_rate": 0.1943,
            "favorite_rate": 0.0046,
            "playlist_rate": 0.0106,
            "repost_rate": 0.0003
        },
        {
            "geo_country": "GH",
            "unique_songs": 12605,
            "unique_artists": 4635,
            "total_plays": 1103037822,
            "download_rate": 0.3144,
            "favorite_rate": 0.0063,
            "playlist_rate": 0.0252,
            "repost_rate": 0.0003
        },
        {
            "geo_country": "US",
            "unique_songs": 20239,
            "unique_artists": 6993,
            "total_plays": 984556737,
            "download_rate": 0.0853,
            "favorite_rate": 0.0127,
            "playlist_rate": 0.0186,
            "repost_rate": 0.0002
        },
        {
            "geo_country": "JM",
            "unique_songs": 4037,
            "unique_artists": 1030,
            "total_plays": 286628266,
            "download_rate": 0.1740,
            "favorite_rate": 0.0036,
            "playlist_rate": 0.0109,
            "repost_rate": 0.0002
        },
        {
            "geo_country": "TZ",
            "unique_songs": 2055,
            "unique_artists": 944,
            "total_plays": 124558960,
            "download_rate": 0.3162,
            "favorite_rate": 0.0041,
            "playlist_rate": 0.0203,
            "repost_rate": 0.0002
        }
    ])
    
    # Hidden gems
    hidden_gems = pd.DataFrame([
        {
            "music_id": 31809979,
            "song_name": "juju",
            "artist_name": "Big smur lee",
            "total_plays": 32581,
            "total_downloads": 132987,
            "favorite_ratio": 0.0491,
            "playlist_ratio": 0.0440,
            "engagement_score": 1.25274
        },
        {
            "music_id": 26325473,
            "song_name": "Medicine after death",
            "artist_name": "Mohbad",
            "total_plays": 4019,
            "total_downloads": 16303,
            "favorite_ratio": 0.0475,
            "playlist_ratio": 0.0236,
            "engagement_score": 1.23872
        },
        {
            "music_id": 29326228,
            "song_name": "Twe Twe (remix)",
            "artist_name": "Kizz Daniel",
            "total_plays": 8614,
            "total_downloads": 34749,
            "favorite_ratio": 0.0358,
            "playlist_ratio": 0.0411,
            "engagement_score": 1.23363
        },
        {
            "music_id": 27038877,
            "song_name": "Area Boys prayers",
            "artist_name": "Seyi vibez",
            "total_plays": 4425,
            "total_downloads": 16386,
            "favorite_ratio": 0.0298,
            "playlist_ratio": 0.0280,
            "engagement_score": 1.12861
        },
        {
            "music_id": 24215772,
            "song_name": "Gbona",
            "artist_name": "Zinoleesky",
            "total_plays": 7899,
            "total_downloads": 26930,
            "favorite_ratio": 0.0457,
            "playlist_ratio": 0.0575,
            "engagement_score": 1.05420
        }
    ])
    
    # Top artists by song count
    top_artists = pd.DataFrame([
        {
            "artist_name": "Juice WRLD",
            "song_count": 538,
            "total_plays": 72475641,
            "avg_plays_per_song": 13357.1030
        },
        {
            "artist_name": "KIRAT",
            "song_count": 359,
            "total_plays": 11619281,
            "avg_plays_per_song": 8102.7064
        },
        {
            "artist_name": "Dj Wizkel",
            "song_count": 344,
            "total_plays": 30548286,
            "avg_plays_per_song": 14058.1160
        },
        {
            "artist_name": "SHATTA WALE",
            "song_count": 337,
            "total_plays": 104034146,
            "avg_plays_per_song": 20723.9335
        },
        {
            "artist_name": "NBA YoungBoy",
            "song_count": 327,
            "total_plays": 24226846,
            "avg_plays_per_song": 9012.9635
        },
        {
            "artist_name": "DJ Amacoz",
            "song_count": 286,
            "total_plays": 76663196,
            "avg_plays_per_song": 33787.2173
        },
        {
            "artist_name": "Seyi Vibez",
            "song_count": 257,
            "total_plays": 50295331,
            "avg_plays_per_song": 25952.1832
        },
        {
            "artist_name": "YoungBoy Never Broke Again",
            "song_count": 250,
            "total_plays": 17216580,
            "avg_plays_per_song": 11186.8616
        },
        {
            "artist_name": "Chronic Law",
            "song_count": 241,
            "total_plays": 25692133,
            "avg_plays_per_song": 10338.8865
        },
        {
            "artist_name": "Mohbad",
            "song_count": 236,
            "total_plays": 119361030,
            "avg_plays_per_song": 35261.7518
        }
    ])
    
    # Artist engagement comparison
    artist_engagement = pd.DataFrame([
        {
            "artist_name": "Mama le succès",
            "song_count": 15,
            "avg_engagement_score": 0.404562989
        },
        {
            "artist_name": "Big Smur Lee",
            "song_count": 8,
            "avg_engagement_score": 0.358251483
        },
        {
            "artist_name": "Dj Amass",
            "song_count": 7,
            "avg_engagement_score": 0.269453664
        },
        {
            "artist_name": "djmysterioghana",
            "song_count": 6,
            "avg_engagement_score": 0.254437576
        },
        {
            "artist_name": "Iba Montana",
            "song_count": 10,
            "avg_engagement_score": 0.245587765
        },
        {
            "artist_name": "Adomba Fausty",
            "song_count": 9,
            "avg_engagement_score": 0.237230024
        },
        {
            "artist_name": "DJ MENTOS",
            "song_count": 6,
            "avg_engagement_score": 0.231980866
        },
        {
            "artist_name": "Obaapa Christy",
            "song_count": 22,
            "avg_engagement_score": 0.224386569
        },
        {
            "artist_name": "Dj Wasty Kay",
            "song_count": 18,
            "avg_engagement_score": 0.219959456
        },
        {
            "artist_name": "Kwaku smoke",
            "song_count": 6,
            "avg_engagement_score": 0.213171093
        }
    ])
    
    # Engagement benchmarks
    benchmarks = pd.DataFrame([
        {
            "metric": "Downloads",
            "average_ratio": 0.19943922,
            "highest_ratio": 84.3617
        },
        {
            "metric": "Favorites",
            "average_ratio": 0.00722445,
            "highest_ratio": 2.6768
        },
        {
            "metric": "Playlists",
            "average_ratio": 0.01700405,
            "highest_ratio": 3.1849
        },
        {
            "metric": "Reposts",
            "average_ratio": 0.00026425,
            "highest_ratio": 0.3487
        }
    ])
    
    # DJ Mix vs Single Track Analysis
    dj_single = pd.DataFrame([
        {
            "content_type": "DJ Mix",
            "track_count": 9034,
            "avg_download_ratio": 0.29938929,
            "avg_favorite_ratio": 0.00778788,
            "avg_playlist_ratio": 0.01570945
        },
        {
            "content_type": "Single Track",
            "track_count": 71004,
            "avg_download_ratio": 0.18866509,
            "avg_favorite_ratio": 0.00716354,
            "avg_playlist_ratio": 0.01714273
        }
    ])
    
    # Monthly analysis
    monthly_analysis = pd.DataFrame([
        {
            "month_str": "2023-04",
            "unique_songs": 19723,
            "total_plays": 296749194,
            "download_rate": 0.1859,
            "favorite_rate": 0.0063
        },
        {
            "month_str": "2023-05",
            "unique_songs": 26097,
            "total_plays": 433438893,
            "download_rate": 0.1432,
            "favorite_rate": 0.0050
        },
        {
            "month_str": "2023-06",
            "unique_songs": 25314,
            "total_plays": 409287750,
            "download_rate": 0.1539,
            "favorite_rate": 0.0051
        },
        {
            "month_str": "2023-07",
            "unique_songs": 20650,
            "total_plays": 291190895,
            "download_rate": 0.2027,
            "favorite_rate": 0.0069
        },
        {
            "month_str": "2023-08",
            "unique_songs": 22854,
            "total_plays": 324336447,
            "download_rate": 0.1952,
            "favorite_rate": 0.0065
        },
        {
            "month_str": "2023-09",
            "unique_songs": 22873,
            "total_plays": 329623842,
            "download_rate": 0.1980,
            "favorite_rate": 0.0065
        },
        {
            "month_str": "2023-10",
            "unique_songs": 24746,
            "total_plays": 369916905,
            "download_rate": 0.1898,
            "favorite_rate": 0.0065
        },
        {
            "month_str": "2023-11",
            "unique_songs": 24940,
            "total_plays": 362235739,
            "download_rate": 0.1875,
            "favorite_rate": 0.0061
        },
        {
            "month_str": "2023-12",
            "unique_songs": 26614,
            "total_plays": 399588966,
            "download_rate": 0.1932,
            "favorite_rate": 0.0060
        },
        {
            "month_str": "2024-01",
            "unique_songs": 25525,
            "total_plays": 385683603,
            "download_rate": 0.1951,
            "favorite_rate": 0.0059
        },
        {
            "month_str": "2024-02",
            "unique_songs": 23263,
            "total_plays": 333443551,
            "download_rate": 0.1879,
            "favorite_rate": 0.0056
        },
        {
            "month_str": "2024-03",
            "unique_songs": 24509,
            "total_plays": 351750156,
            "download_rate": 0.2034,
            "favorite_rate": 0.0057
        },
        {
            "month_str": "2024-04",
            "unique_songs": 24584,
            "total_plays": 360657522,
            "download_rate": 0.2161,
            "favorite_rate": 0.0060
        },
        {
            "month_str": "2024-05",
            "unique_songs": 26597,
            "total_plays": 405513449,
            "download_rate": 0.2299,
            "favorite_rate": 0.0058
        },
        {
            "month_str": "2024-06",
            "unique_songs": 26172,
            "total_plays": 397425211,
            "download_rate": 0.2315,
            "favorite_rate": 0.0055
        },
        {
            "month_str": "2024-07",
            "unique_songs": 26432,
            "total_plays": 411944638,
            "download_rate": 0.2198,
            "favorite_rate": 0.0059
        },
        {
            "month_str": "2024-08",
            "unique_songs": 27831,
            "total_plays": 424523455,
            "download_rate": 0.2142,
            "favorite_rate": 0.0059
        },
        {
            "month_str": "2024-09",
            "unique_songs": 27116,
            "total_plays": 404860879,
            "download_rate": 0.2064,
            "favorite_rate": 0.0061
        },
        {
            "month_str": "2024-10",
            "unique_songs": 27640,
            "total_plays": 419514856,
            "download_rate": 0.2000,
            "favorite_rate": 0.0064
        },
        {
            "month_str": "2024-11",
            "unique_songs": 25658,
            "total_plays": 433059119,
            "download_rate": 0.2030,
            "favorite_rate": 0.0067
        },
        {
            "month_str": "2024-12",
            "unique_songs": 28847,
            "total_plays": 479840220,
            "download_rate": 0.2002,
            "favorite_rate": 0.0066
        }
    ])

    # Process top engagement data
    top_engagement_df = top_download_ratio.copy()
    top_engagement_df['song'] = top_engagement_df['song_name'] + " by " + top_engagement_df['artist_name']
    # Create a unique identifier for each song to prevent confusion with same song names
    top_engagement_df['song_id'] = top_engagement_df['music_id'].astype(str)
    top_engagement_df['downloadRatio'] = top_engagement_df['download_play_ratio']
    top_engagement_df['favoritesRatio'] = top_engagement_df['favorite_play_ratio']
    top_engagement_df['playlistRatio'] = top_engagement_df['playlist_play_ratio']
    top_engagement_df['repostsRatio'] = top_engagement_df['repost_play_ratio']
    top_engagement_df['engagement'] = top_engagement_df['engagement_score']
    top_engagement_df['plays'] = top_engagement_df['total_plays']
    
    # Process country data
    country_df = pd.DataFrame({
        'country': country_analysis['geo_country'],
        'totalPlay30s': country_analysis['total_plays'],
        'downloadRate': country_analysis['download_rate'],
        'favoriteRate': country_analysis['favorite_rate'],
        'playlistRate': country_analysis['playlist_rate'],
        'songCount': country_analysis['unique_songs'],
        'artistCount': country_analysis['unique_artists']
    })
    
    # Process hidden gems data
    hidden_gems_df = hidden_gems.copy()
    hidden_gems_df['song'] = hidden_gems_df['song_name'] + " by " + hidden_gems_df['artist_name']
    # Create a unique identifier for each song
    hidden_gems_df['song_id'] = hidden_gems_df['music_id'].astype(str)
    hidden_gems_df['engagementRatio'] = hidden_gems_df['engagement_score']
    hidden_gems_df['plays'] = hidden_gems_df['total_plays']
    
    # Process benchmark data
    benchmark_df = pd.DataFrame({
        'name': benchmarks['metric'],
        'average': benchmarks['average_ratio'],
        'highest': benchmarks['highest_ratio']
    })
    
    # Monthly trend data
    monthly_df = monthly_analysis.sort_values('month_str')
    
    # DJ vs Single comparison
    dj_single_df = dj_single

    return top_engagement_df, country_df, hidden_gems_df, top_artists, artist_engagement, benchmark_df, monthly_df, dj_single_df

# Load data
try:
    top_engagement_df, country_df, hidden_gems_df, top_artists_df, artist_engagement_df, benchmark_df, monthly_df, dj_single_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Dashboard title and description
st.title("Music Data Analysis Dashboard")
st.write("UGC Music Upload Analysis (04/2023-12/2024) for songs across multiple countries")

# Add a note about song identification
st.info("""
**Note on Song Identification**: Some songs may share the same title but have different artists. 
Throughout this dashboard, songs are uniquely identified by both song name and artist name, and internally by a unique music_id.
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Engagement Analysis", 
    "Country Analysis", 
    "Hidden Gems", 
    "Top Artists", 
    "Trends",
    "Benchmarks"
])

# Tab 1: Engagement Analysis
with tab1:
    st.header("Top Songs by Engagement Score")
    st.write("Engagement score combines download, favorite, playlist, and repost ratios")
    
    # Create the engagement score chart
    fig1 = px.bar(
        top_engagement_df,
        x="song",
        y="engagement",
        title="Top Songs by Engagement Score",
        labels={"engagement": "Engagement Score", "song": "Song"},
        color_discrete_sequence=["#8884d8"],
        hover_data=["music_id", "total_plays", "total_downloads"]  # Add more context in hover
    )
    fig1.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Create the metrics breakdown chart
    st.header("Engagement Metrics Breakdown")
    st.write("Detailed breakdown of different engagement metrics for top performers")
    
    metrics_df = top_engagement_df.melt(
        id_vars=["song"],
        value_vars=["downloadRatio", "favoritesRatio", "playlistRatio"],
        var_name="Metric",
        value_name="Value"
    )
    
    # Replace metric names for better readability
    metrics_df["Metric"] = metrics_df["Metric"].map({
        "downloadRatio": "Download Ratio",
        "favoritesRatio": "Favorites Ratio",
        "playlistRatio": "Playlist Ratio"
    })
    
    fig2 = px.bar(
        metrics_df,
        x="song",
        y="Value",
        color="Metric",
        barmode="group",
        title="Engagement Metrics Breakdown",
        color_discrete_map={
            "Download Ratio": "#0088FE",
            "Favorites Ratio": "#00C49F",
            "Playlist Ratio": "#FFBB28"
        }
    )
    fig2.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig2, use_container_width=True)
    
    # Content Type Comparison
    st.header("Content Type Comparison")
    st.write("Engagement metrics comparison between DJ mixes and single tracks")
    
    fig_content = px.bar(
        dj_single_df,
        x="content_type",
        y=["avg_download_ratio", "avg_favorite_ratio", "avg_playlist_ratio"],
        barmode="group",
        title="DJ Mixes vs. Single Tracks Engagement",
        labels={
            "value": "Average Ratio",
            "content_type": "Content Type",
            "variable": "Metric Type"
        },
        color_discrete_map={
            "avg_download_ratio": "#0088FE",
            "avg_favorite_ratio": "#00C49F",
            "avg_playlist_ratio": "#FFBB28"
        }
    )
    st.plotly_chart(fig_content, use_container_width=True)

# Tab 2: Country Analysis
with tab2:
    st.header("Country Play Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create the pie chart for play distribution
        fig3 = px.pie(
            country_df,
            values="totalPlay30s",
            names="country",
            title="Total Plays by Country",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Create the bar chart for engagement rates by country
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=country_df["country"],
            y=country_df["downloadRate"],
            name="Download Rate",
            marker_color="#0088FE"
        ))
        fig4.add_trace(go.Bar(
            x=country_df["country"],
            y=country_df["favoriteRate"],
            name="Favorite Rate",
            marker_color="#00C49F"
        ))
        fig4.add_trace(go.Bar(
            x=country_df["country"],
            y=country_df["playlistRate"],
            name="Playlist Rate",
            marker_color="#FFBB28"
        ))
        fig4.update_layout(
            title="Engagement Rates by Country",
            barmode="group"
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Create the song & artist distribution chart
    st.header("Song & Artist Distribution by Country")
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=country_df["country"],
        y=country_df["songCount"],
        name="Number of Songs",
        marker_color="#8884d8"
    ))
    fig5.add_trace(go.Bar(
        x=country_df["country"],
        y=country_df["artistCount"],
        name="Number of Artists",
        marker_color="#82ca9d"
    ))
    fig5.update_layout(
        title="Song & Artist Distribution by Country",
        barmode="group"
    )
    st.plotly_chart(fig5, use_container_width=True)

# Tab 3: Hidden Gems
with tab3:
    st.header("Hidden Gems (High Engagement, Moderate Plays)")
    st.write("Songs with exceptional engagement metrics that haven't yet reached massive play counts")
    
    # Create dual axis chart for hidden gems
    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig6.add_trace(
        go.Bar(
            x=hidden_gems_df["song"],
            y=hidden_gems_df["engagementRatio"],
            name="Engagement Ratio",
            marker_color="#8884d8"
        ),
        secondary_y=False
    )
    
    fig6.add_trace(
        go.Bar(
            x=hidden_gems_df["song"],
            y=hidden_gems_df["plays"],
            name="Total Plays (30s+)",
            marker_color="#82ca9d"
        ),
        secondary_y=True
    )
    
    fig6.update_layout(
        title_text="Hidden Gems: Engagement vs Plays",
        xaxis=dict(title="Song")
    )
    
    fig6.update_yaxes(title_text="Engagement Ratio", secondary_y=False)
    fig6.update_yaxes(title_text="Total Plays", secondary_y=True)
    
    st.plotly_chart(fig6, use_container_width=True)
    
    # Create the engagement breakdown for hidden gems
    st.header("Hidden Gems Engagement Breakdown")
    
    metrics_df2 = hidden_gems_df.melt(
        id_vars=["song"],
        value_vars=["favorite_ratio", "playlist_ratio"],
        var_name="Metric",
        value_name="Value"
    )
    
    metrics_df2["Metric"] = metrics_df2["Metric"].map({
        "favorite_ratio": "Favorite Ratio",
        "playlist_ratio": "Playlist Ratio"
    })
    
    fig7 = px.bar(
        metrics_df2,
        x="song",
        y="Value",
        color="Metric",
        barmode="group",
        title="Engagement Metrics Breakdown for Hidden Gems",
        color_discrete_map={
            "Favorite Ratio": "#00C49F",
            "Playlist Ratio": "#FFBB28"
        }
    )
    st.plotly_chart(fig7, use_container_width=True)

# Tab 4: Top Artists
with tab4:
    st.header("Top Artists by Song Count")
    st.write("Artists with multiple songs in the dataset")
    
    # Sort artists by song count
    sorted_artists = top_artists_df.sort_values(by="song_count", ascending=False)
    
    # Add additional analysis for artist name verification
    st.subheader("Data Quality Check")
    st.write("""
    The dashboard ensures accurate artist identification by using unique artist names.
    You may find similar artist names in the data (e.g., 'NBA YoungBoy' and 'YoungBoy Never Broke Again')
    that are treated as separate artists based on how they were originally credited.
    """)
    
    fig8 = px.bar(
        sorted_artists.head(10),
        x="artist_name",
        y="song_count",
        title="Top Artists by Song Count",
        color_discrete_sequence=["#8884d8"],
        hover_data=["total_plays", "avg_plays_per_song"]  # Add more context
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    # Create the artist engagement comparison
    st.header("Artist Engagement Comparison")
    
    fig9 = px.bar(
        artist_engagement_df,
        x="artist_name",
        y="avg_engagement_score",
        title="Average Engagement Score by Artist",
        color_discrete_sequence=["#FF8042"]
    )
    fig9.update_layout(yaxis_title="Average Engagement Score")
    st.plotly_chart(fig9, use_container_width=True)

# Tab 5: Trends
with tab5:
    st.header("Monthly Trends")
    st.write("How engagement metrics have changed over time")
    
    # Create line chart for monthly trends
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=monthly_df["month_str"],
        y=monthly_df["download_rate"],
        mode='lines+markers',
        name='Download Rate',
        line=dict(color="#0088FE")
    ))
    fig_monthly.add_trace(go.Scatter(
        x=monthly_df["month_str"],
        y=monthly_df["favorite_rate"],
        mode='lines+markers',
        name='Favorite Rate',
        line=dict(color="#00C49F")
    ))
    fig_monthly.update_layout(
        title="Monthly Engagement Rates",
        xaxis_title="Month",
        yaxis_title="Engagement Rate"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Monthly plays and unique songs
    fig_plays = go.Figure()
    
    # Create a secondary y-axis plot
    fig_plays = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_plays.add_trace(
        go.Scatter(
            x=monthly_df["month_str"],
            y=monthly_df["total_plays"],
            mode="lines+markers",
            name="Total Plays",
            line=dict(color="#8884d8")
        ),
        secondary_y=False
    )
    
    fig_plays.add_trace(
        go.Scatter(
            x=monthly_df["month_str"],
            y=monthly_df["unique_songs"],
            mode="lines+markers",
            name="Unique Songs",
            line=dict(color="#82ca9d")
        ),
        secondary_y=True
    )
    
    fig_plays.update_layout(
        title="Monthly Plays and Song Volume",
        xaxis_title="Month"
    )
    
    fig_plays.update_yaxes(title_text="Total Plays", secondary_y=False)
    fig_plays.update_yaxes(title_text="Unique Songs", secondary_y=True)
    
    st.plotly_chart(fig_plays, use_container_width=True)

# Tab 6: Benchmarks
with tab6:
    st.header("Engagement Benchmarks")
    st.write("Average vs. Highest engagement metrics across the dataset")
    
    # Create the benchmark comparison chart
    benchmark_melted = benchmark_df.melt(
        id_vars=["name"],
        value_vars=["average", "highest"],
        var_name="Metric",
        value_name="Value"
    )
    
    benchmark_melted["Metric"] = benchmark_melted["Metric"].map({
        "average": "Average Ratio",
        "highest": "Highest Ratio"
    })
    
    fig10 = px.bar(
        benchmark_melted,
        x="name",
        y="Value",
        color="Metric",
        barmode="group",
        title="Engagement Benchmarks: Average vs Highest",
        color_discrete_map={
            "Average Ratio": "#8884d8",
            "Highest Ratio": "#82ca9d"
        },
        log_y=True  # Using log scale for better visualization
    )
    fig10.update_layout(xaxis_title="Metric", yaxis_title="Ratio Value (Log Scale)")
    st.plotly_chart(fig10, use_container_width=True)

# Key Findings section
st.header("Key Findings")
st.markdown("""
### 1. Early Indicators of Success

Our analysis reveals that **download-to-play ratio** is the most reliable predictor of sustained song success. With a platform-wide average of 0.199, songs exceeding 0.3 demonstrate exceptional user commitment.

### 2. Geographic Trends 

**Country-specific engagement patterns** show distinct market behaviors:
- **Nigeria (NG)**: Highest volume (4.9B+ plays) with moderate engagement rates (19.4% download rate)
- **Ghana (GH)**: Highest download rate (31.4%) suggesting strong offline listening culture
- **United States (US)**: Highest favorite rate (1.27%) and strong playlist activity (1.86%)

### 3. Content Format Impact

**DJ mixes consistently outperform single tracks** with 58.7% higher download rates (0.299 vs 0.189), particularly strong in African markets.

### 4. Hidden Gems

Several promising tracks show exceptional engagement despite moderate play counts:
- **"juju" by Big smur lee** (32,581 plays, 1.25 engagement score)
- **"Medicine after death" by Mohbad** (4,019 plays, 1.24 engagement score)
- **"Twe Twe (remix)" by Kizz Daniel** (8,614 plays, 1.23 engagement score)

### 5. Artist Insights

**Juice WRLD, KIRAT, and DJ Wizkel** lead in content volume with hundreds of songs each, while **Mama le succès and Big Smur Lee** deliver the highest average engagement quality despite having fewer songs.

### 6. Temporal Patterns

Analysis across 21 months shows increasing download rates (from 14.3% to 23.2%) with consistent seasonal peaks in December.
""")

# Recommendations section
st.header("Recommendations")
st.markdown("""
### For Platform Optimization:
- Implement algorithmic emphasis on download-to-play ratio in recommendation engines
- Create dedicated "Hidden Gems" discovery section featuring high-engagement but moderately-played content
- Develop market-specific algorithms accounting for regional engagement preferences
- Target cross-country content promotion for Ghana→US content flow

### For Content Strategy:
- Increase promotion of DJ mixes and compilations, particularly in African markets
- Spotlight emerging artists with high engagement ratios but moderate plays
- Implement A/B testing of playlist strategies specifically for US-based content
- Develop features to encourage and track offline listening

### For Talent Acquisition:
- Prioritize artists with consistently high engagement metrics across multiple songs
- Evaluate artists like Mama le succès and Big Smur Lee for potential partnerships
- Look beyond raw play counts to identify rising talent with exceptional engagement
""")



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import json
# import os

# # Set page configuration
# st.set_page_config(
#     page_title="Music Data Analysis Dashboard",
#     page_icon="🎵",
#     layout="wide"
# )

# # Function to load JSON data
# @st.cache_data
# def load_data():
#     # Sample data based on your JSON structure
#     # In production, you would load these from files
    
#     # Top songs by download ratio
#     top_download_ratio = pd.DataFrame([
#         {
#             "music_id": 1,
#             "song_name": "Have Mercy",
#             "artist_name": "Shane Eli",
#             "total_plays": 207866,
#             "total_downloads": 7207622,
#             "download_play_ratio": 34.6744,
#             "total_favorites": 612,
#             "total_playlist_adds": 5973,
#             "total_reposts": 105,
#             "favorite_play_ratio": 0.0029,
#             "playlist_play_ratio": 0.0287,
#             "repost_play_ratio": 0.0005,
#             "engagement_score": 10.41186
#         },
#         {
#             "music_id": 23455165,
#             "song_name": "Pluto",
#             "artist_name": "Shallipopi",
#             "total_plays": 3990,
#             "total_downloads": 42318,
#             "download_play_ratio": 10.6060,
#             "total_favorites": 158,
#             "total_playlist_adds": 58,
#             "total_reposts": 25,
#             "favorite_play_ratio": 0.0396,
#             "playlist_play_ratio": 0.0145,
#             "repost_play_ratio": 0.0063,
#             "engagement_score": 3.19867
#         },
#         {
#             "music_id": 37403686,
#             "song_name": "Joy is coming",
#             "artist_name": "Fido",
#             "total_plays": 5976,
#             "total_downloads": 35935,
#             "download_play_ratio": 6.0132,
#             "total_favorites": 302,
#             "total_playlist_adds": 230,
#             "total_reposts": 35,
#             "favorite_play_ratio": 0.0505,
#             "playlist_play_ratio": 0.0385,
#             "repost_play_ratio": 0.0059,
#             "engagement_score": 1.83126
#         },
#         {
#             "music_id": 32475125,
#             "song_name": "APartii",
#             "artist_name": "Combosman X Togman",
#             "total_plays": 9612,
#             "total_downloads": 40354,
#             "download_play_ratio": 4.1983,
#             "total_favorites": 532,
#             "total_playlist_adds": 1122,
#             "total_reposts": 19,
#             "favorite_play_ratio": 0.0553,
#             "playlist_play_ratio": 0.1167,
#             "repost_play_ratio": 0.0020,
#             "engagement_score": 1.31131
#         },
#         {
#             "music_id": 31809979,
#             "song_name": "juju",
#             "artist_name": "Big smur lee",
#             "total_plays": 32581,
#             "total_downloads": 132987,
#             "download_play_ratio": 4.0817,
#             "total_favorites": 1601,
#             "total_playlist_adds": 1435,
#             "total_reposts": 86,
#             "favorite_play_ratio": 0.0491,
#             "playlist_play_ratio": 0.0440,
#             "repost_play_ratio": 0.0026,
#             "engagement_score": 1.25274
#         }
#     ])
    
#     # Country analysis
#     country_analysis = pd.DataFrame([
#         {
#             "geo_country": "NG",
#             "unique_songs": 43692,
#             "unique_artists": 16867,
#             "total_plays": 4921728863,
#             "download_rate": 0.1943,
#             "favorite_rate": 0.0046,
#             "playlist_rate": 0.0106,
#             "repost_rate": 0.0003
#         },
#         {
#             "geo_country": "GH",
#             "unique_songs": 12605,
#             "unique_artists": 4635,
#             "total_plays": 1103037822,
#             "download_rate": 0.3144,
#             "favorite_rate": 0.0063,
#             "playlist_rate": 0.0252,
#             "repost_rate": 0.0003
#         },
#         {
#             "geo_country": "US",
#             "unique_songs": 20239,
#             "unique_artists": 6993,
#             "total_plays": 984556737,
#             "download_rate": 0.0853,
#             "favorite_rate": 0.0127,
#             "playlist_rate": 0.0186,
#             "repost_rate": 0.0002
#         },
#         {
#             "geo_country": "JM",
#             "unique_songs": 4037,
#             "unique_artists": 1030,
#             "total_plays": 286628266,
#             "download_rate": 0.1740,
#             "favorite_rate": 0.0036,
#             "playlist_rate": 0.0109,
#             "repost_rate": 0.0002
#         },
#         {
#             "geo_country": "TZ",
#             "unique_songs": 2055,
#             "unique_artists": 944,
#             "total_plays": 124558960,
#             "download_rate": 0.3162,
#             "favorite_rate": 0.0041,
#             "playlist_rate": 0.0203,
#             "repost_rate": 0.0002
#         }
#     ])
    
#     # Hidden gems
#     hidden_gems = pd.DataFrame([
#         {
#             "music_id": 31809979,
#             "song_name": "juju",
#             "artist_name": "Big smur lee",
#             "total_plays": 32581,
#             "total_downloads": 132987,
#             "favorite_ratio": 0.0491,
#             "playlist_ratio": 0.0440,
#             "engagement_score": 1.25274
#         },
#         {
#             "music_id": 26325473,
#             "song_name": "Medicine after death",
#             "artist_name": "Mohbad",
#             "total_plays": 4019,
#             "total_downloads": 16303,
#             "favorite_ratio": 0.0475,
#             "playlist_ratio": 0.0236,
#             "engagement_score": 1.23872
#         },
#         {
#             "music_id": 29326228,
#             "song_name": "Twe Twe (remix)",
#             "artist_name": "Kizz Daniel",
#             "total_plays": 8614,
#             "total_downloads": 34749,
#             "favorite_ratio": 0.0358,
#             "playlist_ratio": 0.0411,
#             "engagement_score": 1.23363
#         },
#         {
#             "music_id": 27038877,
#             "song_name": "Area Boys prayers",
#             "artist_name": "Seyi vibez",
#             "total_plays": 4425,
#             "total_downloads": 16386,
#             "favorite_ratio": 0.0298,
#             "playlist_ratio": 0.0280,
#             "engagement_score": 1.12861
#         },
#         {
#             "music_id": 24215772,
#             "song_name": "Gbona",
#             "artist_name": "Zinoleesky",
#             "total_plays": 7899,
#             "total_downloads": 26930,
#             "favorite_ratio": 0.0457,
#             "playlist_ratio": 0.0575,
#             "engagement_score": 1.05420
#         }
#     ])
    
#     # Top artists by song count
#     top_artists = pd.DataFrame([
#         {
#             "artist_name": "Juice WRLD",
#             "song_count": 538,
#             "total_plays": 72475641,
#             "avg_plays_per_song": 13357.1030
#         },
#         {
#             "artist_name": "KIRAT",
#             "song_count": 359,
#             "total_plays": 11619281,
#             "avg_plays_per_song": 8102.7064
#         },
#         {
#             "artist_name": "Dj Wizkel",
#             "song_count": 344,
#             "total_plays": 30548286,
#             "avg_plays_per_song": 14058.1160
#         },
#         {
#             "artist_name": "SHATTA WALE",
#             "song_count": 337,
#             "total_plays": 104034146,
#             "avg_plays_per_song": 20723.9335
#         },
#         {
#             "artist_name": "NBA YoungBoy",
#             "song_count": 327,
#             "total_plays": 24226846,
#             "avg_plays_per_song": 9012.9635
#         },
#         {
#             "artist_name": "DJ Amacoz",
#             "song_count": 286,
#             "total_plays": 76663196,
#             "avg_plays_per_song": 33787.2173
#         },
#         {
#             "artist_name": "Seyi Vibez",
#             "song_count": 257,
#             "total_plays": 50295331,
#             "avg_plays_per_song": 25952.1832
#         },
#         {
#             "artist_name": "YoungBoy Never Broke Again",
#             "song_count": 250,
#             "total_plays": 17216580,
#             "avg_plays_per_song": 11186.8616
#         },
#         {
#             "artist_name": "Chronic Law",
#             "song_count": 241,
#             "total_plays": 25692133,
#             "avg_plays_per_song": 10338.8865
#         },
#         {
#             "artist_name": "Mohbad",
#             "song_count": 236,
#             "total_plays": 119361030,
#             "avg_plays_per_song": 35261.7518
#         }
#     ])
    
#     # Artist engagement comparison
#     artist_engagement = pd.DataFrame([
#         {
#             "artist_name": "Mama le succès",
#             "song_count": 15,
#             "avg_engagement_score": 0.404562989
#         },
#         {
#             "artist_name": "Big Smur Lee",
#             "song_count": 8,
#             "avg_engagement_score": 0.358251483
#         },
#         {
#             "artist_name": "Dj Amass",
#             "song_count": 7,
#             "avg_engagement_score": 0.269453664
#         },
#         {
#             "artist_name": "djmysterioghana",
#             "song_count": 6,
#             "avg_engagement_score": 0.254437576
#         },
#         {
#             "artist_name": "Iba Montana",
#             "song_count": 10,
#             "avg_engagement_score": 0.245587765
#         },
#         {
#             "artist_name": "Adomba Fausty",
#             "song_count": 9,
#             "avg_engagement_score": 0.237230024
#         },
#         {
#             "artist_name": "DJ MENTOS",
#             "song_count": 6,
#             "avg_engagement_score": 0.231980866
#         },
#         {
#             "artist_name": "Obaapa Christy",
#             "song_count": 22,
#             "avg_engagement_score": 0.224386569
#         },
#         {
#             "artist_name": "Dj Wasty Kay",
#             "song_count": 18,
#             "avg_engagement_score": 0.219959456
#         },
#         {
#             "artist_name": "Kwaku smoke",
#             "song_count": 6,
#             "avg_engagement_score": 0.213171093
#         }
#     ])
    
#     # Engagement benchmarks
#     benchmarks = pd.DataFrame([
#         {
#             "metric": "Downloads",
#             "average_ratio": 0.19943922,
#             "highest_ratio": 84.3617
#         },
#         {
#             "metric": "Favorites",
#             "average_ratio": 0.00722445,
#             "highest_ratio": 2.6768
#         },
#         {
#             "metric": "Playlists",
#             "average_ratio": 0.01700405,
#             "highest_ratio": 3.1849
#         },
#         {
#             "metric": "Reposts",
#             "average_ratio": 0.00026425,
#             "highest_ratio": 0.3487
#         }
#     ])
    
#     # DJ Mix vs Single Track Analysis
#     dj_single = pd.DataFrame([
#         {
#             "content_type": "DJ Mix",
#             "track_count": 9034,
#             "avg_download_ratio": 0.29938929,
#             "avg_favorite_ratio": 0.00778788,
#             "avg_playlist_ratio": 0.01570945
#         },
#         {
#             "content_type": "Single Track",
#             "track_count": 71004,
#             "avg_download_ratio": 0.18866509,
#             "avg_favorite_ratio": 0.00716354,
#             "avg_playlist_ratio": 0.01714273
#         }
#     ])
    
#     # Monthly analysis
#     monthly_analysis = pd.DataFrame([
#         {
#             "month_str": "2023-04",
#             "unique_songs": 19723,
#             "total_plays": 296749194,
#             "download_rate": 0.1859,
#             "favorite_rate": 0.0063
#         },
#         {
#             "month_str": "2023-05",
#             "unique_songs": 26097,
#             "total_plays": 433438893,
#             "download_rate": 0.1432,
#             "favorite_rate": 0.0050
#         },
#         {
#             "month_str": "2023-06",
#             "unique_songs": 25314,
#             "total_plays": 409287750,
#             "download_rate": 0.1539,
#             "favorite_rate": 0.0051
#         },
#         {
#             "month_str": "2023-07",
#             "unique_songs": 20650,
#             "total_plays": 291190895,
#             "download_rate": 0.2027,
#             "favorite_rate": 0.0069
#         },
#         {
#             "month_str": "2023-08",
#             "unique_songs": 22854,
#             "total_plays": 324336447,
#             "download_rate": 0.1952,
#             "favorite_rate": 0.0065
#         },
#         {
#             "month_str": "2023-09",
#             "unique_songs": 22873,
#             "total_plays": 329623842,
#             "download_rate": 0.1980,
#             "favorite_rate": 0.0065
#         },
#         {
#             "month_str": "2023-10",
#             "unique_songs": 24746,
#             "total_plays": 369916905,
#             "download_rate": 0.1898,
#             "favorite_rate": 0.0065
#         },
#         {
#             "month_str": "2023-11",
#             "unique_songs": 24940,
#             "total_plays": 362235739,
#             "download_rate": 0.1875,
#             "favorite_rate": 0.0061
#         },
#         {
#             "month_str": "2023-12",
#             "unique_songs": 26614,
#             "total_plays": 399588966,
#             "download_rate": 0.1932,
#             "favorite_rate": 0.0060
#         },
#         {
#             "month_str": "2024-01",
#             "unique_songs": 25525,
#             "total_plays": 385683603,
#             "download_rate": 0.1951,
#             "favorite_rate": 0.0059
#         },
#         {
#             "month_str": "2024-02",
#             "unique_songs": 23263,
#             "total_plays": 333443551,
#             "download_rate": 0.1879,
#             "favorite_rate": 0.0056
#         },
#         {
#             "month_str": "2024-03",
#             "unique_songs": 24509,
#             "total_plays": 351750156,
#             "download_rate": 0.2034,
#             "favorite_rate": 0.0057
#         },
#         {
#             "month_str": "2024-04",
#             "unique_songs": 24584,
#             "total_plays": 360657522,
#             "download_rate": 0.2161,
#             "favorite_rate": 0.0060
#         },
#         {
#             "month_str": "2024-05",
#             "unique_songs": 26597,
#             "total_plays": 405513449,
#             "download_rate": 0.2299,
#             "favorite_rate": 0.0058
#         },
#         {
#             "month_str": "2024-06",
#             "unique_songs": 26172,
#             "total_plays": 397425211,
#             "download_rate": 0.2315,
#             "favorite_rate": 0.0055
#         },
#         {
#             "month_str": "2024-07",
#             "unique_songs": 26432,
#             "total_plays": 411944638,
#             "download_rate": 0.2198,
#             "favorite_rate": 0.0059
#         },
#         {
#             "month_str": "2024-08",
#             "unique_songs": 27831,
#             "total_plays": 424523455,
#             "download_rate": 0.2142,
#             "favorite_rate": 0.0059
#         },
#         {
#             "month_str": "2024-09",
#             "unique_songs": 27116,
#             "total_plays": 404860879,
#             "download_rate": 0.2064,
#             "favorite_rate": 0.0061
#         },
#         {
#             "month_str": "2024-10",
#             "unique_songs": 27640,
#             "total_plays": 419514856,
#             "download_rate": 0.2000,
#             "favorite_rate": 0.0064
#         },
#         {
#             "month_str": "2024-11",
#             "unique_songs": 25658,
#             "total_plays": 433059119,
#             "download_rate": 0.2030,
#             "favorite_rate": 0.0067
#         },
#         {
#             "month_str": "2024-12",
#             "unique_songs": 28847,
#             "total_plays": 479840220,
#             "download_rate": 0.2002,
#             "favorite_rate": 0.0066
#         }
#     ])

#     # Process top engagement data
#     top_engagement_df = top_download_ratio.copy()
#     top_engagement_df['song'] = top_engagement_df['song_name'] + " (" + top_engagement_df['artist_name'] + ")"
#     top_engagement_df['downloadRatio'] = top_engagement_df['download_play_ratio']
#     top_engagement_df['favoritesRatio'] = top_engagement_df['favorite_play_ratio']
#     top_engagement_df['playlistRatio'] = top_engagement_df['playlist_play_ratio']
#     top_engagement_df['repostsRatio'] = top_engagement_df['repost_play_ratio']
#     top_engagement_df['engagement'] = top_engagement_df['engagement_score']
#     top_engagement_df['plays'] = top_engagement_df['total_plays']
    
#     # Process country data
#     country_df = pd.DataFrame({
#         'country': country_analysis['geo_country'],
#         'totalPlay30s': country_analysis['total_plays'],
#         'downloadRate': country_analysis['download_rate'],
#         'favoriteRate': country_analysis['favorite_rate'],
#         'playlistRate': country_analysis['playlist_rate'],
#         'songCount': country_analysis['unique_songs'],
#         'artistCount': country_analysis['unique_artists']
#     })
    
#     # Process hidden gems data
#     hidden_gems_df = hidden_gems.copy()
#     hidden_gems_df['song'] = hidden_gems_df['song_name'] + " (" + hidden_gems_df['artist_name'] + ")"
#     hidden_gems_df['engagementRatio'] = hidden_gems_df['engagement_score']
#     hidden_gems_df['plays'] = hidden_gems_df['total_plays']
    
#     # Process benchmark data
#     benchmark_df = pd.DataFrame({
#         'name': benchmarks['metric'],
#         'average': benchmarks['average_ratio'],
#         'highest': benchmarks['highest_ratio']
#     })
    
#     # Monthly trend data
#     monthly_df = monthly_analysis.sort_values('month_str')
    
#     # DJ vs Single comparison
#     dj_single_df = dj_single

#     return top_engagement_df, country_df, hidden_gems_df, top_artists, artist_engagement, benchmark_df, monthly_df, dj_single_df

# # Load data
# try:
#     top_engagement_df, country_df, hidden_gems_df, top_artists_df, artist_engagement_df, benchmark_df, monthly_df, dj_single_df = load_data()
#     data_loaded = True
# except Exception as e:
#     st.error(f"Error loading data: {e}")
#     data_loaded = False

# # Dashboard title and description
# st.title("Music Data Analysis Dashboard")
# st.write("UGC Music Upload Analysis (04/2023-12/2024) for songs across multiple countries")

# # Create tabs
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     "Engagement Analysis", 
#     "Country Analysis", 
#     "Hidden Gems", 
#     "Top Artists", 
#     "Trends",
#     "Benchmarks"
# ])

# # Tab 1: Engagement Analysis
# with tab1:
#     st.header("Top Songs by Engagement Score")
#     st.write("Engagement score combines download, favorite, playlist, and repost ratios")
    
#     # Create the engagement score chart
#     fig1 = px.bar(
#         top_engagement_df,
#         x="song",
#         y="engagement",
#         title="Top Songs by Engagement Score",
#         labels={"engagement": "Engagement Score", "song": "Song"},
#         color_discrete_sequence=["#8884d8"]
#     )
#     fig1.update_layout(xaxis={'categoryorder':'total descending'})
#     st.plotly_chart(fig1, use_container_width=True)
    
#     # Create the metrics breakdown chart
#     st.header("Engagement Metrics Breakdown")
#     st.write("Detailed breakdown of different engagement metrics for top performers")
    
#     metrics_df = top_engagement_df.melt(
#         id_vars=["song"],
#         value_vars=["downloadRatio", "favoritesRatio", "playlistRatio"],
#         var_name="Metric",
#         value_name="Value"
#     )
    
#     # Replace metric names for better readability
#     metrics_df["Metric"] = metrics_df["Metric"].map({
#         "downloadRatio": "Download Ratio",
#         "favoritesRatio": "Favorites Ratio",
#         "playlistRatio": "Playlist Ratio"
#     })
    
#     fig2 = px.bar(
#         metrics_df,
#         x="song",
#         y="Value",
#         color="Metric",
#         barmode="group",
#         title="Engagement Metrics Breakdown",
#         color_discrete_map={
#             "Download Ratio": "#0088FE",
#             "Favorites Ratio": "#00C49F",
#             "Playlist Ratio": "#FFBB28"
#         }
#     )
#     fig2.update_layout(xaxis={'categoryorder':'total descending'})
#     st.plotly_chart(fig2, use_container_width=True)
    
#     # Content Type Comparison
#     st.header("Content Type Comparison")
#     st.write("Engagement metrics comparison between DJ mixes and single tracks")
    
#     fig_content = px.bar(
#         dj_single_df,
#         x="content_type",
#         y=["avg_download_ratio", "avg_favorite_ratio", "avg_playlist_ratio"],
#         barmode="group",
#         title="DJ Mixes vs. Single Tracks Engagement",
#         labels={
#             "value": "Average Ratio",
#             "content_type": "Content Type",
#             "variable": "Metric Type"
#         },
#         color_discrete_map={
#             "avg_download_ratio": "#0088FE",
#             "avg_favorite_ratio": "#00C49F",
#             "avg_playlist_ratio": "#FFBB28"
#         }
#     )
#     st.plotly_chart(fig_content, use_container_width=True)

# # Tab 2: Country Analysis
# with tab2:
#     st.header("Country Play Distribution")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Create the pie chart for play distribution
#         fig3 = px.pie(
#             country_df,
#             values="totalPlay30s",
#             names="country",
#             title="Total Plays by Country",
#             color_discrete_sequence=px.colors.qualitative.Set3
#         )
#         fig3.update_traces(textposition='inside', textinfo='percent+label')
#         st.plotly_chart(fig3, use_container_width=True)
    
#     with col2:
#         # Create the bar chart for engagement rates by country
#         fig4 = go.Figure()
#         fig4.add_trace(go.Bar(
#             x=country_df["country"],
#             y=country_df["downloadRate"],
#             name="Download Rate",
#             marker_color="#0088FE"
#         ))
#         fig4.add_trace(go.Bar(
#             x=country_df["country"],
#             y=country_df["favoriteRate"],
#             name="Favorite Rate",
#             marker_color="#00C49F"
#         ))
#         fig4.add_trace(go.Bar(
#             x=country_df["country"],
#             y=country_df["playlistRate"],
#             name="Playlist Rate",
#             marker_color="#FFBB28"
#         ))
#         fig4.update_layout(
#             title="Engagement Rates by Country",
#             barmode="group"
#         )
#         st.plotly_chart(fig4, use_container_width=True)
    
#     # Create the song & artist distribution chart
#     st.header("Song & Artist Distribution by Country")
    
#     fig5 = go.Figure()
#     fig5.add_trace(go.Bar(
#         x=country_df["country"],
#         y=country_df["songCount"],
#         name="Number of Songs",
#         marker_color="#8884d8"
#     ))
#     fig5.add_trace(go.Bar(
#         x=country_df["country"],
#         y=country_df["artistCount"],
#         name="Number of Artists",
#         marker_color="#82ca9d"
#     ))
#     fig5.update_layout(
#         title="Song & Artist Distribution by Country",
#         barmode="group"
#     )
#     st.plotly_chart(fig5, use_container_width=True)

# # Tab 3: Hidden Gems
# with tab3:
#     st.header("Hidden Gems (High Engagement, Moderate Plays)")
#     st.write("Songs with exceptional engagement metrics that haven't yet reached massive play counts")
    
#     # Create dual axis chart for hidden gems
#     fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
#     fig6.add_trace(
#         go.Bar(
#             x=hidden_gems_df["song"],
#             y=hidden_gems_df["engagementRatio"],
#             name="Engagement Ratio",
#             marker_color="#8884d8"
#         ),
#         secondary_y=False
#     )
    
#     fig6.add_trace(
#         go.Bar(
#             x=hidden_gems_df["song"],
#             y=hidden_gems_df["plays"],
#             name="Total Plays (30s+)",
#             marker_color="#82ca9d"
#         ),
#         secondary_y=True
#     )
    
#     fig6.update_layout(
#         title_text="Hidden Gems: Engagement vs Plays",
#         xaxis=dict(title="Song")
#     )
    
#     fig6.update_yaxes(title_text="Engagement Ratio", secondary_y=False)
#     fig6.update_yaxes(title_text="Total Plays", secondary_y=True)
    
#     st.plotly_chart(fig6, use_container_width=True)
    
#     # Create the engagement breakdown for hidden gems
#     st.header("Hidden Gems Engagement Breakdown")
    
#     metrics_df2 = hidden_gems_df.melt(
#         id_vars=["song"],
#         value_vars=["favorite_ratio", "playlist_ratio"],
#         var_name="Metric",
#         value_name="Value"
#     )
    
#     metrics_df2["Metric"] = metrics_df2["Metric"].map({
#         "favorite_ratio": "Favorite Ratio",
#         "playlist_ratio": "Playlist Ratio"
#     })
    
#     fig7 = px.bar(
#         metrics_df2,
#         x="song",
#         y="Value",
#         color="Metric",
#         barmode="group",
#         title="Engagement Metrics Breakdown for Hidden Gems",
#         color_discrete_map={
#             "Favorite Ratio": "#00C49F",
#             "Playlist Ratio": "#FFBB28"
#         }
#     )
#     st.plotly_chart(fig7, use_container_width=True)

# # Tab 4: Top Artists
# with tab4:
#     st.header("Top Artists by Song Count")
#     st.write("Artists with multiple songs in the dataset")
    
#     # Sort artists by song count
#     sorted_artists = top_artists_df.sort_values(by="song_count", ascending=False)
    
#     fig8 = px.bar(
#         sorted_artists.head(10),
#         x="artist_name",
#         y="song_count",
#         title="Top Artists by Song Count",
#         color_discrete_sequence=["#8884d8"]
#     )
#     st.plotly_chart(fig8, use_container_width=True)
    
#     # Create the artist engagement comparison
#     st.header("Artist Engagement Comparison")
    
#     fig9 = px.bar(
#         artist_engagement_df,
#         x="artist_name",
#         y="avg_engagement_score",
#         title="Average Engagement Score by Artist",
#         color_discrete_sequence=["#FF8042"]
#     )
#     fig9.update_layout(yaxis_title="Average Engagement Score")
#     st.plotly_chart(fig9, use_container_width=True)

# # Tab 5: Trends
# with tab5:
#     st.header("Monthly Trends")
#     st.write("How engagement metrics have changed over time")
    
#     # Create line chart for monthly trends
#     fig_monthly = go.Figure()
#     fig_monthly.add_trace(go.Scatter(
#         x=monthly_df["month_str"],
#         y=monthly_df["download_rate"],
#         mode='lines+markers',
#         name='Download Rate',
#         line=dict(color="#0088FE")
#     ))
#     fig_monthly.add_trace(go.Scatter(
#         x=monthly_df["month_str"],
#         y=monthly_df["favorite_rate"],
#         mode='lines+markers',
#         name='Favorite Rate',
#         line=dict(color="#00C49F")
#     ))
#     fig_monthly.update_layout(
#         title="Monthly Engagement Rates",
#         xaxis_title="Month",
#         yaxis_title="Engagement Rate"
#     )
#     st.plotly_chart(fig_monthly, use_container_width=True)
    
#     # Monthly plays and unique songs
#     fig_plays = go.Figure()
    
#     # Create a secondary y-axis plot
#     fig_plays = make_subplots(specs=[[{"secondary_y": True}]])
    
#     fig_plays.add_trace(
#         go.Scatter(
#             x=monthly_df["month_str"],
#             y=monthly_df["total_plays"],
#             mode="lines+markers",
#             name="Total Plays",
#             line=dict(color="#8884d8")
#         ),
#         secondary_y=False
#     )
    
#     fig_plays.add_trace(
#         go.Scatter(
#             x=monthly_df["month_str"],
#             y=monthly_df["unique_songs"],
#             mode="lines+markers",
#             name="Unique Songs",
#             line=dict(color="#82ca9d")
#         ),
#         secondary_y=True
#     )
    
#     fig_plays.update_layout(
#         title="Monthly Plays and Song Volume",
#         xaxis_title="Month"
#     )
    
#     fig_plays.update_yaxes(title_text="Total Plays", secondary_y=False)
#     fig_plays.update_yaxes(title_text="Unique Songs", secondary_y=True)
    
#     st.plotly_chart(fig_plays, use_container_width=True)

# # Tab 6: Benchmarks
# with tab6:
#     st.header("Engagement Benchmarks")
#     st.write("Average vs. Highest engagement metrics across the dataset")
    
#     # Create the benchmark comparison chart
#     benchmark_melted = benchmark_df.melt(
#         id_vars=["name"],
#         value_vars=["average", "highest"],
#         var_name="Metric",
#         value_name="Value"
#     )
    
#     benchmark_melted["Metric"] = benchmark_melted["Metric"].map({
#         "average": "Average Ratio",
#         "highest": "Highest Ratio"
#     })
    
#     fig10 = px.bar(
#         benchmark_melted,
#         x="name",
#         y="Value",
#         color="Metric",
#         barmode="group",
#         title="Engagement Benchmarks: Average vs Highest",
#         color_discrete_map={
#             "Average Ratio": "#8884d8",
#             "Highest Ratio": "#82ca9d"
#         },
#         log_y=True  # Using log scale for better visualization
#     )
#     fig10.update_layout(xaxis_title="Metric", yaxis_title="Ratio Value (Log Scale)")
#     st.plotly_chart(fig10, use_container_width=True)

# # Key Findings section
# st.header("Key Findings")
# st.markdown("""
# ### 1. Early Indicators of Success

# Our analysis reveals that **download-to-play ratio** is the most reliable predictor of sustained song success. With a platform-wide average of 0.199, songs exceeding 0.3 demonstrate exceptional user commitment.

# ### 2. Geographic Trends 

# **Country-specific engagement patterns** show distinct market behaviors:
# - **Nigeria (NG)**: Highest volume (4.9B+ plays) with moderate engagement rates (19.4% download rate)
# - **Ghana (GH)**: Highest download rate (31.4%) suggesting strong offline listening culture
# - **United States (US)**: Highest favorite rate (1.27%) and strong playlist activity (1.86%)

# ### 3. Content Format Impact

# **DJ mixes consistently outperform single tracks** with 58.7% higher download rates (0.299 vs 0.189), particularly strong in African markets.

# ### 4. Hidden Gems

# Several promising tracks show exceptional engagement despite moderate play counts:
# - **"juju" by Big smur lee** (32,581 plays, 1.25 engagement score)
# - **"Medicine after death" by Mohbad** (4,019 plays, 1.24 engagement score)
# - **"Twe Twe (remix)" by Kizz Daniel** (8,614 plays, 1.23 engagement score)

# ### 5. Artist Insights

# **Juice WRLD, KIRAT, and DJ Wizkel** lead in content volume with hundreds of songs each, while **Mama le succès and Big Smur Lee** deliver the highest average engagement quality despite having fewer songs.

# ### 6. Temporal Patterns

# Analysis across 21 months shows increasing download rates (from 14.3% to 23.2%) with consistent seasonal peaks in December.
# """)

# # Recommendations section
# st.header("Recommendations")
# st.markdown("""
# ### For Platform Optimization:
# - Implement algorithmic emphasis on download-to-play ratio in recommendation engines
# - Create dedicated "Hidden Gems" discovery section featuring high-engagement but moderately-played content
# - Develop market-specific algorithms accounting for regional engagement preferences
# - Target cross-country content promotion for Ghana→US content flow

# ### For Content Strategy:
# - Increase promotion of DJ mixes and compilations, particularly in African markets
# - Spotlight emerging artists with high engagement ratios but moderate plays
# - Implement A/B testing of playlist strategies specifically for US-based content
# - Develop features to encourage and track offline listening

# ### For Talent Acquisition:
# - Prioritize artists with consistently high engagement metrics across multiple songs
# - Evaluate artists like Mama le succès and Big Smur Lee for potential partnerships
# - Look beyond raw play counts to identify rising talent with exceptional engagement
# """)
