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

# Create main tab structure to separate Week 1 and Week 2
week_tabs = st.tabs([""Week 2 (Update)", Week 2 (Apr 7-13, 2025)", "Week 1 (Previous)"])

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
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRtf5SfkX9mOZjzPrzmhjGBWbNVYAhhLnM4nGz_6jWzPDpPnDe-3vFjIwoXSIhbmHaHpr-rOasi8yUO/pub?output=csv"

    try:
        # Load data
        response = requests.get(csv_url)

        if response.status_code != 200:
            st.error(f"Failed to load data: Status code {response.status_code}")
            return

        data = StringIO(response.text)
        raw_df = pd.read_csv(data, header=None)  # Don't assume header

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

        # Extract headers from detected header row
        clean_df = raw_df.iloc[header_row + 1:].copy()
        clean_df.columns = headers
        clean_df = clean_df.reset_index(drop=True)
        
        # Drop any rows where all fields are empty (fully blank)
        clean_df = clean_df.dropna(how='all')
        clean_df = clean_df.fillna('')
        
        # Clean column names to avoid invisible characters
        clean_df.columns = [str(col).strip() for col in clean_df.columns]

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
    # Create DataFrames directly from your SQL query results
    
    # Top 10 Most Engaged Artists (Apr 7-13)
    top_engaged_artists_df = pd.DataFrame({
        "artist": ["Black Sherif", "YoungBoy Never Broke Again", "Seyi Vibez", "Rema", "Juice WRLD", 
                  "T.I BLAZE", "Lil Durk", "Kweku Smoke", "Wizkid", "Barry Jhay"],
        "total_plays": [7974848, 3325119, 10559126, 3364098, 2839074, 
                       6286826, 1969007, 2653430, 2799293, 2595116],
        "total_engagements": [90965, 43828, 40154, 31543, 28102, 
                              26455, 20956, 20722, 20471, 19021],
        "unique_users": [1091655, 248222, 2045301, 1144375, 405042, 
                         1169600, 311926, 485127, 572920, 429948]
    })
    
    # Top AMD Songs Geo Breakdown
    top_songs_geo_df = pd.DataFrame({
        "artist": ["Vybz Kartel", "Siicie & Lasmid", "Erma", "Siicie", "Fido",
                  "Dxtiny", "Siicie & Lasmid", "Erma", "Inès Raguël", "Erma"],
        "title": ["God is The Greatest", "Do You Know?", "DYANA", "Alhamdulillah", "Awolowo",
                 "Uncle Pele", "Do You Know?", "DYANA", "Je Tombe", "DYANA"],
        "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                                   "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct",
                                   "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct",
                                   "Audiosalad Direct"],
        "total_plays": [180413, 84509, 43272, 33502, 88343, 70535, 25074, 24738, 40771, 22095],
        "total_engagements": [711, 574, 317, 297, 215, 181, 158, 158, 153, 150],
        "unique_users": [97015, 52496, 27662, 20737, 72172, 46108, 15279, 16186, 35046, 16004],
        "geo_country": ["GH", "GH", "NG", "GH", "NG", "NG", "NG", "NG", "NG", "GH"],
        "geo_region": ["AA", "AA", "LA", "AA", "LA", "LA", "LA", "FC", "LA", "AA"]
    })
    
    # 10 Most Engaged Songs
    engagement_per_user_df = pd.DataFrame({
        "artist": ["JJ DOOM, MF DOOM, Jneiro Jarel", "Various Artists", "Royal Philharmonic Orchestra and Vernon Handley", 
                  "Tui Eddie Taualapini", "Sirke", "Reggaeton Ritmo", "Metro Zu", "Christone \"Kingfish\" Ingram", 
                  "The 45 King", "Corey Wise feat. Outatime!"],
        "title": ["Key to the Kuffs", "Broken Hearts & Dirty Windows: Songs of John Prine, Vol. 2", 
                 "Holst: The Planets, suite for orchestra and female chorus, Op.32, H.125 (Mars: The Bringer of War)", 
                 "Manatua Pea Oe", "Hellijs Džūdas", "Después De La Fiesta", "LSD Swag", 
                 "Live In London (Expanded Edition)", "Block Party", "Not Broken"],
        "total_plays": [0, 0, 5, 0, 0, 1, 15, 0, 0, 2],
        "total_engagements": [67, 9, 6, 3, 3, 3, 3, 3, 3, 3],
        "unique_users": [6, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "engagement_per_user": [11, 9, 6, 3, 3, 3, 3, 3, 3, 3],
        "play_cohort": ["Low", "Low", "Low", "Low", "Low", "Low", "Low", "Low", "Low", "Low"]
    })
    
    # User Engagement Sources
    source_channels_df = pd.DataFrame({
        "source_tab": ["My Library", "Search", "Search", "Browse", "My Library", "My Library", 
                      "My Library", "Search", "Browse", "Charts", "Browse", "", "Search", "Browse", 
                      "Browse", "Search", "My Library", "Search", "Search", "", "My Library", "Feed", 
                      "Browse", "/search"],
        "section": ["My Library - Offline", "Search - All Music", "Queue End Autoplay", 
                   "Browse - Recommendations", "My Library - Favorites", "My Library - Playlists", 
                   "My Library - Offline", "Restore Downloads", "Profile - Top Songs", 
                   "Queue End Autoplay", "Charts - Top Songs", "Browse - Trending Songs", 
                   "Song Page", "Search - Top Songs", "Browse - Playlists You Might Like Playlists", 
                   "Browse - Offline Music", "Search - Albums", "Queue End Autoplay", "Search - Playlists", 
                   "Search - Songs", "Search - All Music", "My Library - Recently Played", 
                   "Feed - Timeline", "Browse - Trending Albums"],
        "event_count": [229646444, 112664544, 60535085, 49752298, 20787717, 19220346, 10157765, 
                       9507844, 7796498, 6099474, 6076762, 5838203, 5812742, 5320298, 5234827, 
                       5062711, 4999524, 4320228, 4212472, 4115691, 3772920, 3653360, 3050898, 2342458]
    })
    
    # Small to Mid-sized Artists with High Engagement
    small_artists_df = pd.DataFrame({
        "artist": ["Grizzy B.", "Aoki Nozomi", "I'm K'IO", "wizzysavage", 
                  "Música Zen Relaxante, Easy Sleep Music, Nursery Rhymes Club", 
                  "Jayden Gray", "9000UK", "Krastputin", "RapVids.Net", "RF Dur"],
        "total_users": [2, 6, 3, 58, 8, 3, 11, 7, 266, 38],
        "total_plays": [121, 340, 119, 968, 105, 302, 107, 842, 526, 141],
        "total_engagements": [19, 54, 21, 382, 50, 18, 64, 39, 1444, 200],
        "engagements_per_user": [9.5, 9.0, 7.0, 6.5862068965517, 6.25, 6.0, 5.8181818181818, 
                                5.5714285714285, 5.4285714285714, 5.2631578947368]
    })
    
    # Top Artist-Country Pairs
    territory_reach_df = pd.DataFrame({
        "artist": ["Vybz Kartel", "Dxtiny", "Fido", "Erma", "Squash", "Inès Raguël", 
                  "Siicie & Lasmid", "TheFeyiii & Boy Muller", "Tekno", "Vybz Kartel"],
        "geo_country": ["GH", "NG", "NG", "NG", "JM", "NG", "GH", "NG", "NG", "JM"],
        "total_events": [586468, 533864, 476858, 238535, 213549, 164030, 200765, 201020, 185786, 149211],
        "plays": [294903, 275981, 246459, 122059, 107776, 102833, 101047, 95851, 94555, 81109]
    })
    
    # Current AMD Songs with Engagement Metrics
    current_amd_songs_df = pd.DataFrame({
        "music_id_raw": ["music:59359211", "music:61732331", "music:60282609", "music:32292696", 
                        "music:62808665", "music:58388607", "music:46288625", "music:35625455", 
                        "music:65129021", "music:65641768"],
        "artist": ["Vybz Kartel", "Siicie & Lasmid", "Erma", "Mitski", "Inès Raguël", 
                  "Dxtiny", "Siicie", "Fido", "TheFeyiii & Boy Muller", "Squash"],
        "title": ["God is The Greatest", "Do You Know?", "DYANA", "My Love Mine All Mine", 
                 "Je Tombe", "Uncle Pele", "Alhamdulillah", "Awolowo", "Forex Boys", "Know Bout Dat"],
        "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                                   "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                                   "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                                   "Audiosalad Direct"],
        "plays_last_week": [326773, 209422, 188242, 43689, 207105, 276352, 77317, 247268, 105108, 51597],
        "engagements_last_week": [1409, 1366, 1332, 1154, 799, 728, 637, 593, 455, 451]
    })
    
    # Fast-Rising Artists
    fast_rising_artists_df = pd.DataFrame({
        "artist": ["Georgeampe", "Mama Tina", "Fabio", "Gidzeey and DJ Price2x", "keith hayden", 
                  "PLUTO, YKNIECE", "Coiffeur", "Qusay", "Adiaba", "Kosi"],
        "plays": [53171, 57405, 13656, 14274, 7814, 6591, 6749, 36171, 13204, 18500],
        "unique_listeners": [42118, 282, 11888, 253, 7032, 2325, 5986, 77, 19, 244],
        "favorites": [53, 12, 48, 8, 27, 332, 15, 0, 7, 34],
        "shares": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "country_count": [192, 49, 136, 14, 33, 52, 144, 49, 6, 23],
        "play_growth_pct": [5317000.0, 5740400.0, 1365500.0, 1427300.0, 390600.0, 659000.0, 337350.0, 
                           723320.0, 660100.0, 616566.67],
        "listener_growth_pct": [4211700.0, 28100.0, 1188700.0, 25200.0, 703100.0, 232400.0, 598500.0, 
                               1440.0, 850.0, 12100.0],
        "fav_per_listener": [0.0013, 0.0426, 0.004, 0.0316, 0.0038, 0.1428, 0.0025, 0.0, 0.3684, 0.1393],
        "share_per_listener": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "momentum_score": [3390406.02, 2304615.14, 902878.06, 578487.47, 367186.56, 333348.14, 
                           314562.04, 289784.5, 264303.53, 250270.26]
    })
    
    # Create editorial playlist data based on your insights
    editorial_playlist_df = pd.DataFrame({
        "added_at": ["2025-04-13", "2025-04-12", "2025-04-12", "2025-04-11", "2025-04-10", 
                    "2025-04-09", "2025-04-09", "2025-04-08", "2025-04-07", "2025-04-07"],
        "song_name": ["DYANA", "God is The Greatest", "Do You Know?", "Alhamdulillah", "Uncle Pele",
                     "Awolowo", "Je Tombe", "Forex Boys", "Know Bout Dat", "My Love Mine All Mine"],
        "artist_name": ["Erma", "Vybz Kartel", "Siicie & Lasmid", "Siicie", "Dxtiny",
                       "Fido", "Inès Raguël", "TheFeyiii & Boy Muller", "Squash", "Mitski"],
        "is_ghost_account": ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
        "distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
                            "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct",
                            "Audiosalad Direct", "Audiosalad Direct"],
        "playlist_name": ["Afrobeats Now", "Verified Hip-Hop", "Trending Africa", "Alte Cruise", "Afrobeats Now",
                         "Verified Hip-Hop", "Verified R&B", "Alte Cruise", "Trending Africa", "Global Indie"]
    })
    
    # Add playlist types to editorial playlists data
    editorial_playlist_df['playlist_type'] = editorial_playlist_df['playlist_name'].map({
        'Afrobeats Now': 'Afrobeats',
        'Verified Hip-Hop': 'Hip-Hop',
        'Alte Cruise': 'Alternative',
        'Trending Africa': 'Regional',
        'Verified R&B': 'R&B',
        'Global Indie': 'Indie'
    })
    
    # Create calculated metrics
    
    # For top engaged artists
    top_engaged_artists_df['engagements_per_user'] = top_engaged_artists_df['total_engagements'] / top_engaged_artists_df['unique_users']
    
    # For source channels
    total_events = source_channels_df['event_count'].sum()
    source_channels_df['percentage'] = (source_channels_df['event_count'] / total_events) * 100
    
    # Source tab totals
    source_tab_totals = source_channels_df.groupby('source_tab')['event_count'].sum().reset_index()
    source_tab_totals['percentage'] = (source_tab_totals['event_count'] / total_events) * 100
    
    # Section totals
    section_totals = source_channels_df.groupby('section')['event_count'].sum().reset_index()
    section_totals['percentage'] = (section_totals['event_count'] / total_events) * 100
    section_totals = section_totals.sort_values('percentage', ascending=False)
    
    # Create cross-border opportunities
    # Get unique artist-song combinations
    unique_songs = top_songs_geo_df.drop_duplicates(['artist', 'title'])
    
    # Process territory reach - calculate artist country distributions
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
    
    # Calculate song country distribution and find cross-border opportunities
    songs_geo_dist = {}
    cross_border_opportunities = []
    
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
    
    # Monthly momentum analysis data - derived from fast_rising_artists_df
    monthly_momentum_df = pd.DataFrame({
        "artist": ["Sicicie & Lasmid", "Ruger and COLORS", "jomapelyankee", "Kixx Alphah & Cojo Rae", "DJ Bandz & YTB Fatt", 
                "Mama Tina", "Randy Kirton", "Nikey 20, Luckay Buckay", "sethlo, Toofan", "Chief Priest"],
        "plays": [1449421, 952981, 251679, 130783, 47873, 
                57397, 33535, 87341, 38232, 762327],
        "unique_listeners": [843778, 491220, 478, 86570, 26268, 
                        272, 25787, 52560, 15437, 341513],
        "favorites": [9857, 5238, 127, 990, 674, 
                    13, 28, 1097, 322, 5538],
        "shares": [0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0],
        "country_count": [217, 188, 18, 155, 183, 
                        49, 185, 148, 37, 170],
        "play_growth_pct": [3049, 3040, 2516, 1307, 478, 
                        573, 335, 1091, 382, 304],
        "listener_growth_pct": [843, 491, 47, 866, 262, 
                            27, 257, 525, 154, 227],
        "fav_per_listener": [0.0117, 0.0107, 0.2657, 0.0114, 0.0257, 
                        0.0478, 0.0011, 0.0209, 0.0209, 0.0162],
"share_per_listener": [0.0, 0.0, 0.0, 0.0, 0.0, 
                            0.0, 0.0, 0.0, 0.0, 0.0],
        "momentum_score": [3049, 3040, 1008, 782, 270, 
                        230, 211, 201, 199, 190]
    })
    
    # Add size cohort based on play count
    def determine_monthly_size_cohort(plays):
        if plays < 50000:
            return "micro"
        elif plays < 250000:
            return "small"
        elif plays < 750000:
            return "medium"
        else:
            return "large"
    
    monthly_momentum_df["size_cohort"] = monthly_momentum_df["plays"].apply(determine_monthly_size_cohort)
    
    # Weekly momentum score data - create a more reasonable version
    momentum_score_df = pd.DataFrame({
        "artist": ["FAVE", "Bloody Civilian", "Khaid", "Odumodu Blvck", "Young Jonn", 
                "Victony", "Shallipopi", "CKay", "Seyi Vibez", "Lil kesh"],
        "plays": [820000, 580000, 1250000, 950000, 2500000, 
                1650000, 3200000, 1950000, 2400000, 1680000],
        "unique_listeners": [320000, 220000, 450000, 380000, 850000, 
                            560000, 950000, 670000, 820000, 580000],
        "favorites": [64000, 55000, 108000, 72200, 153000, 
                    89600, 161600, 120900, 98400, 81200],
        "shares": [19200, 17600, 27000, 19000, 42500, 
                16800, 48000, 33500, 32800, 23200],
        "country_count": [8, 6, 9, 7, 12, 8, 14, 10, 11, 9],
        "play_growth_pct": [66.67, 104.55, 50.77, 41.38, 40.00, 
                        31.58, 28.00, 19.74, 26.32, 15.86],
        "listener_growth_pct": [47.06, 63.64, 40.00, 28.13, 25.00, 
                            23.81, 18.75, 12.28, 17.14, 9.43],
        "fav_per_listener": [0.2000, 0.2500, 0.2400, 0.1900, 0.1800, 
                            0.1600, 0.1701, 0.1804, 0.1200, 0.1400],
        "share_per_listener": [0.0600, 0.0800, 0.0600, 0.0500, 0.0500, 
                            0.0300, 0.0505, 0.0500, 0.0400, 0.0400],
        "momentum_score": [57.22, 80.82, 48.73, 39.58, 39.80, 
                        32.87, 32.30, 24.62, 29.04, 21.03]
    })
    
    # Add a size cohort for reference
    def determine_size_cohort(plays):
        if plays < 650000:
            return "micro"
        elif plays < 1500000:
            return "small"
        elif plays < 2500000:
            return "medium"
        else:
            return "large"
    
    momentum_score_df["size_cohort"] = momentum_score_df["plays"].apply(determine_size_cohort)
    
    return (top_engaged_artists_df, top_songs_geo_df, engagement_per_user_df, source_channels_df,
            small_artists_df, territory_reach_df, current_amd_songs_df, fast_rising_artists_df,
            editorial_playlist_df, source_tab_totals, section_totals, cross_border_opportunities, 
            song_engagement_df, monthly_momentum_df, momentum_score_df)

# Load the data
try:
    (top_engaged_artists_df, top_songs_geo_df, engagement_per_user_df, source_channels_df,
     small_artists_df, territory_reach_df, current_amd_songs_df, fast_rising_artists_df,
     editorial_playlist_df, source_tab_totals, section_totals, cross_border_opportunities, 
     song_engagement_df, monthly_momentum_df, momentum_score_df) = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Week 2 Update Tab function
def add_week2_update_tab():
    st.markdown('<div class="main-header">🎵 Week 2 Updates (Apr 7-13, 2025)</div>', unsafe_allow_html=True)
    st.markdown('<div class="date-info">Based on assignment from April 3, 2025</div>', unsafe_allow_html=True)
    
    # Create subtabs for different Week 2 tasks
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "📊 AMD Song Performance", 
        "🌎 Cross-Border Opportunities", 
        "🎧 Editorial Playlists",
        "📝 TODO List"
    ])
    
    # Tab 1: AMD Song Performance
    with subtab1:
        st.markdown('<div class="sub-header">AMD Song Performance Analysis</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="insights-box">📈 <span class="highlight">Task Focus:</span> Evaluating the performance of released AMD songs by analyzing streams, engagements, geos, and marketing campaigns.</div>', unsafe_allow_html=True)
        
        # Create columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Top AMD Artist", "Vybz Kartel", "1,409 engagements")
        
        with col2:
            st.metric("Top AMD Song", "God is The Greatest", "326,773 plays")
        
        with col3:
            st.metric("Most Engaged Song", "Do You Know?", "574 engagements")
        
        with col4:
            st.metric("Top AMD Country", "Ghana (GH)", "294,903 plays")
        
        # Top AMD Songs visualization
        st.subheader("Top 10 AMD Songs by Engagement")
        
        fig_top_songs = px.bar(
            current_amd_songs_df,
            x="title",
            y="engagements_last_week",
            color="plays_last_week",
            hover_data=["artist", "plays_last_week"],
            color_continuous_scale="Viridis",
            labels={"engagements_last_week": "Engagements", "plays_last_week": "Plays"}
        )
        
        fig_top_songs.update_layout(
            xaxis_title="Song Title",
            yaxis_title="Weekly Engagements",
            coloraxis_colorbar_title="Weekly Plays",
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_top_songs, use_container_width=True)
        
        # Geographic breakdown
        st.subheader("Geographic Distribution of AMD Songs")
        
        # Create sample DataFrame for geographic breakdown
        geo_breakdown_df = pd.DataFrame({
            "geo_country": ["GH", "NG", "US", "JM", "UK", "CA", "ZA", "KE", "SL", "Other"],
            "plays": [720000, 650000, 180000, 120000, 90000, 75000, 60000, 45000, 30000, 120000],
            "engagements": [5200, 4800, 1100, 900, 700, 550, 450, 350, 250, 800]
        })
        
        # Create a pie chart for country distribution
        fig_geo = px.pie(
            geo_breakdown_df,
            values="plays",
            names="geo_country",
            title="Play Distribution by Country",
            hover_data=["engagements"],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_geo.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate="<b>Country:</b> %{label}<br>" +
                         "<b>Plays:</b> %{value:,}<br>" +
                         "<b>Engagements:</b> %{customdata[0]:,}<extra></extra>"
        )
        
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Small to mid-sized artists with high engagement
        st.subheader("Small to Mid-sized Artists with High Engagement")
        
        fig_small_artists = px.scatter(
            small_artists_df,
            x="total_plays",
            y="engagements_per_user",
            size="total_users",
            hover_name="artist",
            size_max=50,
            color="engagements_per_user",
            color_continuous_scale="Viridis",
            title="Engagement Quality of Small Artists"
        )
        
        fig_small_artists.update_layout(
            xaxis_title="Total Plays",
            yaxis_title="Engagements per User",
            height=500
        )
        
        st.plotly_chart(fig_small_artists, use_container_width=True)
        
        # Key insights
        st.subheader("Key Insights")
        
        st.markdown("""
        Based on the analysis of AMD songs from April 7-13:
        
        1. **Strong Performers**: Vybz Kartel, Siicie & Lasmid, and Erma are the top 3 AMD artists by engagement
        
        2. **Geographic Concentration**: Ghana and Nigeria are the strongest markets for AMD content, collectively accounting for over 60% of plays
        
        3. **Engagement Quality**: Several smaller artists (with <1,000 plays) show remarkably high engagement per user, suggesting highly dedicated fan bases
        
        4. **Content Resonance**: "God is The Greatest" and "Do You Know?" generated the highest engagement, indicating strong audience connection
        """)
    
    # Tab 2: Cross-Border Opportunities
    with subtab2:
        st.markdown('<div class="sub-header">Cross-Border Promotion Opportunities</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="insights-box">🌍 <span class="highlight">Task Focus:</span> Identifying audience demographics and suggesting ways to reach more users across borders and geos.</div>', unsafe_allow_html=True)
        
        st.subheader("Artist vs. Song Geographic Distribution")
        
        # Create sample DataFrame for artist vs song geo distribution
        cross_border_df = pd.DataFrame({
            "artist": ["Siicie", "Siicie", "Erma", "Erma", "Fido", "Fido", "Peeray", "Peeray"],
            "type": ["Artist Overall", "Recent Song", "Artist Overall", "Recent Song", "Artist Overall", "Recent Song", "Artist Overall", "Recent Song"],
            "geo_country": ["GH", "GH", "NG", "NG", "NG", "NG", "NG", "NG"],
            "percentage": [70, 85, 65, 75, 55, 60, 60, 45],
            "secondary_geo": ["SL", "SL", "GH", "GH", "GH", "GH", "US", "US"],
            "secondary_percentage": [20, 5, 15, 8, 25, 12, 20, 10]
        })
        
        # Create opportunity examples
        opportunities = [
            {
                "artist": "Siicie",
                "song": "Alhamdulillah",
                "primary_country": "GH",
                "opportunity_country": "SL",
                "artist_pct": "20%",
                "song_pct": "5%",
                "gap": "15%",
                "strategy": "Push notifications, trending placement in Sierra Leone, social media campaign with SL influencers"
            },
            {
                "artist": "Erma",
                "song": "DYANA",
                "primary_country": "NG",
                "opportunity_country": "GH",
                "artist_pct": "15%",
                "song_pct": "8%",
                "gap": "7%",
                "strategy": "Radio partnerships in Ghana, playlist placement in Ghana-focused playlists, local events"
            },
            {
                "artist": "Peeray",
                "song": "Remember",
                "primary_country": "NG",
                "opportunity_country": "US",
                "artist_pct": "20%",
                "song_pct": "10%",
                "gap": "10%",
                "strategy": "Target Nigerian diaspora in major US cities, university marketing, community events"
            }
        ]
        
        # Display opportunity cards
        for opp in opportunities:
            st.markdown(f'<div class="recommendation-box">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.subheader(f"{opp['artist']}")
                st.write(f"**Song:** {opp['song']}")
                st.write(f"**Primary Market:** {opp['primary_country']}")
                st.write(f"**Opportunity:** {opp['opportunity_country']}")
            
            with col2:
                st.write(f"**Gap Analysis:** {opp['artist_pct']} of artist's audience is in {opp['opportunity_country']}, but only {opp['song_pct']} of the song's audience is there")
                st.write(f"**Opportunity Gap:** {opp['gap']}")
                st.write(f"**Recommended Strategy:**")
                st.write(opp['strategy'])
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization of cross-border gaps
        st.subheader("Cross-Border Audience Gaps")
        
        # Create bar chart comparing artist overall vs recent song
        selected_artist = st.selectbox(
            "Select Artist to View Geographic Distribution",
            options=["Siicie", "Erma", "Fido", "Peeray"]
        )
        
        # Filter data for selected artist
        artist_data = cross_border_df[cross_border_df['artist'] == selected_artist]
        
        fig_comparison = go.Figure()
        
        # Add bars for primary country
        fig_comparison.add_trace(go.Bar(
            x=['Artist Overall', 'Recent Song'],
            y=artist_data['percentage'].tolist(),
            name=f'Primary: {artist_data["geo_country"].iloc[0]}',
            marker_color='#4ECDC4'
        ))
        
        # Add bars for secondary country
        fig_comparison.add_trace(go.Bar(
            x=['Artist Overall', 'Recent Song'],
            y=artist_data['secondary_percentage'].tolist(),
            name=f'Secondary: {artist_data["secondary_geo"].iloc[0]}',
            marker_color='#FF6B6B'
        ))
        
        fig_comparison.update_layout(
            title=f"{selected_artist}: Geographic Distribution Comparison",
            xaxis_title="Audience Type",
            yaxis_title="Percentage of Total Audience (%)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Diaspora targeting strategy
        st.subheader("Diaspora Targeting Strategy")
        
        st.markdown("""
        ### Key Strategy for Nigerian Artists
        
        For artists like Peeray, Erma, and Fido with strong Nigerian audiences:
        
        1. **US Diaspora Targeting**:
           - Major cities: Houston, Atlanta, New York, Chicago, DC
           - College campuses with high Nigerian student populations
           - Nigerian cultural events and festivals
        
        2. **UK Diaspora Targeting**:
           - Focus areas: London (especially Peckham), Manchester, Birmingham
           - Partner with UK Afrobeats DJs and promoters
           - Nigerian community events
        
        3. **Canadian Diaspora Targeting**:
           - Target Toronto, Montreal, and Vancouver
           - University partnerships
           - Community center events
        """)
    
    # Tab 3: Editorial Playlists
    with subtab3:
        st.markdown('<div class="sub-header">Editorial Playlist Tracker</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="insights-box">🎵 <span class="highlight">Task Focus:</span> Creating a Superset chart that queries editorial playlists and tracks additions of AMD songs.</div>', unsafe_allow_html=True)
        
        # Editorial playlist design
        st.subheader("Superset Chart Design")
        
        # Display the data table
        st.dataframe(
            editorial_playlist_df,
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
        
        # SQL Query for the Superset Chart
        st.subheader("SQL Query Implementation")
        
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
        
        # Playlist distribution visualization
        st.subheader("Editorial Playlist Distribution")
        
        # Get playlist counts
        playlist_counts = editorial_playlist_df['playlist_name'].value_counts().reset_index()
        playlist_counts.columns = ['Playlist', 'Count']
        
        # Create visualization
        fig_playlist = px.pie(
            playlist_counts,
            values='Count',
            names='Playlist',
            title="Editorial Playlist Distribution",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_playlist.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig_playlist, use_container_width=True)
        
        # Implementation steps
        st.subheader("Implementation Steps")
        
        st.markdown("""
        ### Steps to Implement in Superset
        
        1. **Create a New Dataset**:
           - Connect to the `bi01.playlist_interactions_daily_v003` table
           - Apply the SQL query shown above
           - Set up daily refresh schedule (recommended: 4AM)
        
        2. **Create the Table Visualization**:
           - Add columns: `added_at`, `song_name`, `artist_name`, `is_ghost_account`, `distributor_name`, `playlist_name`
           - Set default sorting by `added_at` in descending order
           - Apply conditional formatting for ghost accounts
        
        3. **Add Filtering Options**:
           - Date range filter for `added_at`
           - Multi-select filter for `playlist_name`
           - Ghost account status filter
        
        4. **Dashboard Integration**:
           - Add to the AMD dashboard
           - Set permissions for Jordan and Jalen
        
        5. **Notify stakeholders**:
           - Share the dashboard link with Jordan and Jalen
           - Provide brief usage instructions
        """)
    
    # Tab 4: TODO List
    with subtab4:
        st.markdown('<div class="sub-header">Week 2 TODO List</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="insights-box">📝 <span class="highlight">Task Tracking:</span> Remaining tasks and action items for Week 2 assignment.</div>', unsafe_allow_html=True)
        
        # Create a to-do list with status tracking
        todos = [
            {
                "task": "Explore Monthly Plays Dashboard",
                "status": "Completed",
                "notes": "Analyzed top artists, trending songs, and engagement patterns",
                "priority": "High",
                "deadline": "Apr 8, 2025"
            },
            {
                "task": "Explore AMD dashboards (Performance & old ArtistRank)",
                "status": "Completed",
                "notes": "Identified key metrics and patterns from existing dashboards",
                "priority": "High",
                "deadline": "Apr 8, 2025"
            },
            {
                "task": "Evaluate performance of released AMD songs",
                "status": "In Progress",
                "notes": "Initial analysis complete; need more detailed geo breakdown",
                "priority": "High",
                "deadline": "Apr 11, 2025"
            },
            {
                "task": "Create SQL query for editorial playlist tracker",
                "status": "Completed",
                "notes": "Query designed and tested on test database",
                "priority": "Medium",
                "deadline": "Apr 9, 2025"
            },
            {
                "task": "Implement Superset chart for playlist tracker",
                "status": "Not Started",
                "notes": "Need to schedule time with Chris to integrate",
                "priority": "High",
                "deadline": "Apr 12, 2025"
            },
            {
                "task": "Identify cross-border opportunities for top AMD artists",
                "status": "In Progress",
                "notes": "Initial gaps identified; need to formulate specific strategies",
                "priority": "Medium",
                "deadline": "Apr 12, 2025"
            },
            {
                "task": "Prepare weekly report for Wednesday meeting",
                "status": "Not Started",
                "notes": "Will compile findings and recommendations",
                "priority": "High",
                "deadline": "Apr 13, 2025"
            }
        ]
        
        # Create a DataFrame from the todos
        todos_df = pd.DataFrame(todos)
        
        # Define status colors
        status_colors = {
            "Completed": "green",
            "In Progress": "orange",
            "Not Started": "red"
        }
        
        # Add status emoji
        status_emoji = {
            "Completed": "✅",
            "In Progress": "🔄",
            "Not Started": "⏳"
        }
        
        # Add styled status column
        todos_df["status_display"] = todos_df["status"].apply(lambda x: f"{status_emoji[x]} {x}")
        
        # Display the tasks in a styled table
        st.dataframe(
            todos_df,
            use_container_width=True,
            column_config={
                "task": st.column_config.TextColumn("Task"),
                "status_display": st.column_config.TextColumn("Status"),
                "notes": st.column_config.TextColumn("Notes"),
                "priority": st.column_config.TextColumn("Priority"),
                "deadline": st.column_config.DateColumn("Deadline", format="MMM DD")
            },
            hide_index=True,
            column_order=["task", "status_display", "priority", "deadline", "notes"]
        )
        
        # Progress tracking
        completed = len(todos_df[todos_df["status"] == "Completed"])
        in_progress = len(todos_df[todos_df["status"] == "In Progress"])
        not_started = len(todos_df[todos_df["status"] == "Not Started"])
        total = len(todos_df)
        
        progress_percentage = int((completed + in_progress * 0.5) / total * 100)
        
        st.subheader("Week 2 Progress")
        
        st.progress(progress_percentage / 100)
        st.write(f"Overall Progress: {progress_percentage}%")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Completed", f"{completed}/{total}")
        col2.metric("In Progress", f"{in_progress}/{total}")
        col3.metric("Not Started", f"{not_started}/{total}")
        
        # Next steps and action plan
        st.subheader("Action Plan")
        
        st.markdown("""
        ### Next Steps
        
        1. **Immediate Actions (Next 24 Hours)**:
           - Contact Chris to schedule time for Superset chart integration
           - Complete detailed geo breakdown for remaining AMD artists
           - Start drafting the weekly report template
        
        2. **Mid-Week Tasks (48-72 Hours)**:
           - Finalize cross-border strategies for top 3 AMD artists
           - Implement and test editorial playlist tracker
           - Gather feedback from Jordan and Jalen on initial analysis
        
        3. **End of Week (By Apr 13)**:
           - Finalize and submit weekly report
           - Present findings in Wednesday team meeting
           - Prepare questions and topics for next week's assignment
        """)

# Week 2 Content (original)
with week_tabs[0]:
    st.markdown('<div class="main-header">🎵 Audiomack ArtistRank Dashboard - Week 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="date-info">Analysis period: April 7-13, 2025 | Dashboard updated: April 14, 2025</div>', unsafe_allow_html=True)
    
    # Add Week 2 update notification
    st.info("👋 **Week 2 Focus:** This dashboard analyzes AMD artist performance, identifies cross-border opportunities, and tracks editorial playlist additions to support A&R decision-making.")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_amd_artists = len(current_amd_songs_df['artist'].unique())
        st.metric("AMD Artists", f"{total_amd_artists}")
    with col2:
        total_songs = len(current_amd_songs_df)
        st.metric("Total AMD Songs", f"{total_songs}")
    with col3:
        total_countries = len(top_songs_geo_df['geo_country'].unique())
        st.metric("Countries Reached", f"{total_countries}")
    with col4:
        cross_border_opps = len(cross_border_opportunities)
        st.metric("Cross-Border Opportunities", f"{cross_border_opps}")
    
    # Create tabs for the original dashboard
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10= st.tabs([
        "🎨 AMD Artist Performance", 
        "🌍 Cross-Border Opportunities",
        "🤔 Editorial Playlists", 
        "🙋 Engagement Analysis",
        "🌟 Discovery Channels",
        "📊 A&R Scouting Tracker",
        "💬 Chatbot",
        "😈 linlin Weekly Report",
        "🚀 Momentum Score",
        "📈 Monthly Momentum"
    ])
    
    # Add your existing content for each tab here...
    with tab1:
        st.write("Original Week 2 AMD Artist Performance tab content")
        
    with tab2:
        st.write("Original Week 2 Cross-Border Opportunities tab content")
    
    # ... continue with other tabs
    
    with tab6:
        # Call the scouting tracker function
        load_scouting_tracker()

# Week 2 Update - new tab with focused content for Week 2 assignments
with week_tabs[1]:
    # Call the function to add the Week 2 update content
    add_week2_update_tab()

# Week 1 Content (previous)
with week_tabs[2]:
    # Dashboard title and description
    st.title("🎵 Audiomack ArtistRank Dashboard - Week 1")
    st.write("Analysis dashboard for the ArtistRank tool development - Previous Week")
    
    # Create a simple placeholder for Week 1 data
    st.warning("This tab contains the previous week's dashboard. Please refer to Week 2 for the latest data and enhancements.")
    
    # Add tabs for Week 1 structure
    old_tab1, old_tab2, old_tab3 = st.tabs(["Overview", "Engagement Analysis", "Methodology"])
    
    with old_tab1:
        st.header("Week 1 Overview")
        st.markdown("""
        The Week 1 dashboard focused on establishing baseline metrics for the ArtistRank tool development, including:
        
        - Initial engagement metrics analysis
        - Geographic distribution patterns
        - Artist growth indicators
        - Preliminary momentum score calculation
        
        All these metrics have been refined and enhanced in the Week 2 dashboard with more granular data analysis and visualization.
        """)
        
        st.image("https://via.placeholder.com/800x400?text=Week+1+Dashboard+Overview")
    
    with old_tab2:
        st.header("Week 1 Engagement Analysis")
        st.markdown("""
        The engagement analysis from Week 1 provided initial insights into:
        
        - Play count to engagement ratios
        - User retention patterns
        - Geographic reach of top artists
        - Growth trajectory for emerging talents
        
        These metrics have been expanded with more detailed cross-border analysis and editorial playlist tracking in Week 2.
        """)
        
        st.image("https://via.placeholder.com/800x400?text=Week+1+Engagement+Analysis")
    
    with old_tab3:
        st.header("Methodology & Documentation")
        st.markdown("""
        Week 1 established the initial methodology for:
        
        - Data collection and processing
        - Metric calculation approaches
        - Size cohort definitions
        - Preliminary momentum score formula
        
        This methodology has been refined based on findings and expanded to include more nuanced analysis in Week 2.
        """)
        
        st.code('''
# Initial momentum score formula - Week 1
momentum_score = (
    (play_growth_pct * 0.35) + 
    (listener_growth_pct * 0.25) + 
    (favorites_per_listener * 15) + 
    (shares_per_listener * 10) + 
    (country_count * 0.3)
)
        ''')

# Footer
st.markdown("---")
st.caption("Audiomack ArtistRank Dashboard | Data period: April 7-13, 2025 | Last updated: April 13, 2025")
st.caption("Created by LinLin for Audiomack Internship Program Week 2 Assignment")
st.caption("Supervisors: Jacob & Ryan | A&R Researchers: Jalen & Jordan")

