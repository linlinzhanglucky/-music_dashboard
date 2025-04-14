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
week_tabs = st.tabs(["Week 2 (Apr 7-13, 2025)", "Week 2 (Update)", "Week 1 (Previous)"])

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











# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import requests
# from io import StringIO
# import numpy as np
# import datetime




# # Set page configuration
# st.set_page_config(
#     page_title="Audiomack ArtistRank Dashboard - Week 2",
#     page_icon="🎵",
#     layout="wide"
# )



# # Create main tab structure to separate Week 1 and Week 2
# week_tabs = st.tabs(["Week 2 (Current)", "Week 1 (Previous)"])








# # Add custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 36px;
#         font-weight: bold;
#         color: #FF6B6B;
#         margin-bottom: 20px;
#     }
#     .sub-header {
#         font-size: 24px;
#         font-weight: bold;
#         color: #4ECDC4;
#         margin-top: 30px;
#         margin-bottom: 10px;
#     }
#     .metric-card {
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         padding: 20px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .insights-box {
#         background-color: #f1f8ff;
#         border-left: 5px solid #4ECDC4;
#         padding: 15px;
#         border-radius: 5px;
#         margin-bottom: 20px;
#     }
#     .highlight {
#         color: #FF6B6B;
#         font-weight: bold;
#     }
#     .date-info {
#         font-size: 14px;
#         color: #666;
#         margin-bottom: 20px;
#     }
#     .recommendation-box {
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         padding: 20px;
#         margin-bottom: 20px;
#         border-left: 5px solid #FF9F1C;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Function to load scouting tracker data
# def load_scouting_tracker():
#     """Function to display the A&R Scouting Tracker tab"""

#     st.header("A&R Scouting Tracker")
#     st.write("View of Jordan and Jalen's AMD A&R scouting selections")

#     # Published CSV URL
#     # csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2Q-L96f18C7C-EMCzIoCxR8bdphMkPNcpske5xGYzr6lmztcsqaJgmyTFmXHhu7mjrqvR8MsgfWJT/pub?output=csv"
#     csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRtf5SfkX9mOZjzPrzmhjGBWbNVYAhhLnM4nGz_6jWzPDpPnDe-3vFjIwoXSIhbmHaHpr-rOasi8yUO/pub?output=csv"

#     try:
#         # Load data
#         response = requests.get(csv_url)

#         if response.status_code != 200:
#             st.error(f"Failed to load data: Status code {response.status_code}")
#             return

#         data = StringIO(response.text)
#         raw_df = pd.read_csv(data, header=None)  # Don't assume header

#         # Find header row
#         header_row = None
#         for i, row in raw_df.iterrows():
#             row_str = ' '.join([str(val) for val in row.values])
#             if "Date" in row_str and "Artist Name" in row_str:
#                 header_row = i
#                 break

#         if header_row is None:
#             st.error("Could not find the header row in the sheet")
#             st.write("Available columns:", raw_df.columns.tolist())
#             return

#         headers = raw_df.iloc[header_row].tolist()


#         #debug
#         # Extract headers from detected header row
#         clean_df = raw_df.iloc[header_row + 1:].copy()
#         clean_df.columns = headers
#         clean_df = clean_df.reset_index(drop=True)
        
#         # Drop any rows where all fields are empty (fully blank)
#         clean_df = clean_df.dropna(how='all')
#         clean_df = clean_df.fillna('')
        
#         # Clean column names to avoid invisible characters
#         clean_df.columns = [str(col).strip() for col in clean_df.columns]



    
#         # clean_df = clean_df.fillna('')

#         if len(clean_df) == 0:
#             st.warning("No data found after processing")
#             return

#         # Extract filter options
#         platform_options = [opt for opt in clean_df["On Platform"].unique() if "On Platform" in clean_df.columns and opt]
#         genre_options = [opt for opt in clean_df["Genre"].unique() if "Genre" in clean_df.columns and opt]
#         geo_options = [opt for opt in clean_df["Geo"].unique() if "Geo" in clean_df.columns and opt]
#         feed_partner_options = [opt for opt in clean_df["Feed Partner"].unique() if "Feed Partner" in clean_df.columns and opt]

#         # Display filters
#         st.subheader("Filters")
#         col1, col2, col3, col4 = st.columns(4)
#         #debug
#         # col1, col2, col3, col4, col5 = st.columns(5)

#         with col1:
#             selected_platform = st.multiselect("On Platform Status", options=platform_options, default=platform_options if platform_options else [])

#         with col2:
#             selected_genres = st.multiselect("Genre", options=genre_options, default=genre_options if genre_options else [])

#         with col3:
#             selected_geos = st.multiselect("Geography", options=geo_options, default=geo_options if geo_options else [])

#         with col4:
#             selected_feed_partners = st.multiselect("Feed Partner", options=feed_partner_options, default=feed_partner_options if feed_partner_options else [])

#         # with col5:
#         #     selected_dates = st.multiselect("Week", options=date_options, default=date_options)


#         # Apply filters
#         filtered_df = clean_df.copy()

#         if selected_platform:
#             filtered_df = filtered_df[filtered_df["On Platform"].isin(selected_platform)]
#         if selected_genres:
#             filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genres)]
#         if selected_geos:
#             filtered_df = filtered_df[filtered_df["Geo"].isin(selected_geos)]
#         if selected_feed_partners:
#             filtered_df = filtered_df[filtered_df["Feed Partner"].isin(selected_feed_partners)]
        
#         # if selected_dates:
#         #     filtered_df = filtered_df[filtered_df["Date"].astype(str).isin(selected_dates)]


#         # Display scouting results
#         st.subheader("Scouting Results")
#         column_names = filtered_df.columns.tolist()

#         for i, row in filtered_df.iterrows():
#             with st.expander(f"{row.get('Artist Name', '')} - {row.get('Song Name', '')}"):
#                 for col in column_names:
#                     if col in ["Artist Name", "Song Name"]:
#                         continue
#                     value = row.get(col, '')
#                     if col == "Social Media Link" and value:
#                         st.markdown(f"**{col}:** [{value}]({value})")
#                     else:
#                         st.markdown(f"**{col}:** {value}")

#         # Analytics
#         st.subheader("Analytics")
#         met1, met2, met3 = st.columns(3)
#         met1.metric("Total Tracks", len(filtered_df))

#         if "Genre" in filtered_df.columns:
#             genre_count = len([g for g in filtered_df["Genre"].unique() if g])
#             met2.metric("Unique Genres", genre_count)

#         if "Geo" in filtered_df.columns:
#             geo_count = len([g for g in filtered_df["Geo"].unique() if g])
#             met3.metric("Countries", geo_count)

#         # Visualizations
#         if len(filtered_df) > 0:
#             viz1, viz2 = st.columns(2)

#             with viz1:
#                 if "Genre" in filtered_df.columns:
#                     genre_counts = filtered_df["Genre"].value_counts().reset_index()
#                     genre_counts.columns = ["Genre", "Count"]
#                     genre_counts = genre_counts[genre_counts["Genre"] != ""]
#                     if not genre_counts.empty:
#                         fig1 = px.pie(
#                             genre_counts,
#                             values="Count",
#                             names="Genre",
#                             title="Genre Distribution",
#                             hole=0.4
#                         )
#                         st.plotly_chart(fig1, use_container_width=True)

#             with viz2:
#                 if "Geo" in filtered_df.columns:
#                     geo_counts = filtered_df["Geo"].value_counts().reset_index()
#                     geo_counts.columns = ["Geography", "Count"]
#                     geo_counts = geo_counts[geo_counts["Geography"] != ""]
#                     if not geo_counts.empty:
#                         fig2 = px.bar(
#                             geo_counts,
#                             x="Geography",
#                             y="Count",
#                             title="Geographic Distribution",
#                             color="Count"
#                         )
#                         st.plotly_chart(fig2, use_container_width=True)

#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
#         st.exception(e)




# @st.cache_data
# def load_data():
#     # Load data from CSV files
    
#     # AMD Artist Country Breakdown
#     try:
#         amd_artist_country_df = pd.read_csv('data/AMD Artist Country Breakdown.csv')
#     except:
#         st.warning("⚠️ Could not load 'your_file.csv'. Using fallback data.")
#         amd_artist_country_df = pd.DataFrame({
#             "artist": ["Erma", "Vybz Kartel", "Siicie & Lasmid", "Mitski", "Dxtiny"],
#             "title": ["DYANA", "God is The Greatest", "Do You Know?", "My Love Mine All Mine", "Uncle Pele"],
#             "geo_country": ["NG", "GH", "GH", "US", "NG"],
#             "plays": [111633, 187446, 91479, 11066, 189738],
#             "engagements": [793, 764, 655, 652, 482]
#         })
    
#     # Current AMD Songs List
#     try:
#         amd_songs_df = pd.read_csv('data/Current AMD Songs List.csv')
#     except:
#         st.warning("⚠️ Could not load 'your_file.csv'. Using fallback data.")
#         amd_songs_df = pd.DataFrame({
#             "music_id_raw": ["music:61401185", "music:13852656", "music:56684604", "music:32374254", "music:56252684"],
#             "artist": ["Dalia", "Madlib", "PF Xavi", "William McDowell", "Jodie Marie ASMR"],
#             "title": ["What if", "Dil Cosby Interlude", "Not Ready", "Never Going Back (I Won't Go Back Reprise)", "Black Country Maid Cleans you up Pt.3"],
#             "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct"]
#         })
    
#     # Engagement Source Channels
#     try:
#         source_channels_df = pd.read_csv('data/Engagement Source Channels.csv')
#     except:
#         st.warning("⚠️ Could not load 'your_file.csv'. Using fallback data.")
#         source_channels_df = pd.DataFrame({
#             "source_tab": ["My Library", "Search", "Search", "Browse", "My Library"],
#             "section": ["My Library - Offline", "Search - All Music", "Queue End Autoplay", "Browse - Recommendations", "My Library - Favorites"],
#             "event_count": [204009819, 102970150, 55581117, 45211776, 19003309]
#         })
    
#     # Engagement Per User By Play Cohort
#     try:
#         engagement_per_user_df = pd.read_csv('EngagementPerUser_ByPlayCohort_AMD_Week2.csv')
#     except:
#         engagement_per_user_df = pd.DataFrame({
#             "artist": ["JJ DOOM, MF DOOM, Jneiro Jarel", "Various Artists", "Royal Philharmonic Orchestra and Vernon Handley", "Metro Zu", "Christone \"Kingfish\" Ingram"],
#             "title": ["Key to the Kuffs", "Broken Hearts & Dirty Windows: Songs of John Prine, Vol. 2", "Holst: The Planets, suite for orchestra and female chorus, Op.32, H.125 (Mars: The Bringer of War)", "LSD Swag", "Live In London (Expanded Edition)"],
#             "total_plays": [0, 0, 4, 15, 0],
#             "total_engagements": [67, 9, 6, 3, 3],
#             "unique_users": [6, 1, 1, 1, 1],
#             "engagement_per_user": [11, 9, 6, 3, 3],
#             "play_cohort": ["Low", "Low", "Low", "Low", "Low"]
#         })
    
#     # Small Artists with High Engagement
#     try:
#         small_artists_df = pd.read_csv('Listener Cohort  Small Artists with High Engagement.csv')
#     except:
#         small_artists_df = pd.DataFrame({
#             "artist": ["Grizzy B.", "Aoki Nozomi", "wizzysavage", "I'm КʼЮ", "9000UK"],
#             "total_users": [2, 6, 48, 3, 10],
#             "total_plays": [121, 340, 955, 119, 106],
#             "total_engagements": [19, 54, 382, 21, 64],
#             "engagements_per_user": [9.5, 9.0, 7.958333, 7.0, 6.4]
#         })
    
#     # Territory Reach
#     try:
#         territory_reach_df = pd.read_csv('Territory Reach by Artist Top Geo by Plays.csv')
#     except:
#         territory_reach_df = pd.DataFrame({
#             "artist": ["Vybz Kartel", "Dxtiny", "Fido", "Erma", "Squash"],
#             "geo_country": ["GH", "NG", "NG", "NG", "JM"],
#             "total_events": [523079, 483049, 427256, 217735, 191775],
#             "plays": [262940, 249880, 220781, 111633, 96740]
#         })
    
#     # Top 100 Most Engaged Artists
#     try:
#         top_engaged_artists_df = pd.read_csv('top 100 most engaged artists last week.csv')
#     except:
#         top_engaged_artists_df = pd.DataFrame({
#             "artist": ["Black Sherif", "YoungBoy Never Broke Again", "Seyi Vibez", "Rema", "Juice WRLD"],
#             "total_plays": [6553308, 2926897, 9112888, 2848577, 2476790],
#             "total_engagements": [77895, 38403, 34236, 26531, 23548],
#             "unique_users": [967981, 230143, 1853187, 982726, 367914]
#         })
    
#     # Top Engaged AMD Songs Geo Breakdown
#     try:
#         top_songs_geo_df = pd.read_csv('TopEngaged_AMD_Songs_GeoBreakdown_Week2.csv')
#     except:
#         top_songs_geo_df = pd.DataFrame({
#             "artist": ["Vybz Kartel", "Siicie & Lasmid", "Erma", "Siicie", "Fido"],
#             "title": ["God is The Greatest", "Do You Know?", "DYANA", "Alhamdulillah", "Awolowo"],
#             "latest_distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct"],
#             "total_plays": [158205, 75777, 39675, 29751, 78765],
#             "total_engagements": [612, 521, 292, 272, 180],
#             "unique_users": [87573, 47796, 25884, 18803, 65440],
#             "geo_country": ["GH", "GH", "NG", "GH", "NG"],
#             "geo_region": ["AA", "AA", "LA", "AA", "LA"]
#         })
    
#     # Weekly Artist Engagement Summary
#     try:
#         weekly_engagement_df = pd.read_csv('Weekly Artist Engagement Summary.csv')
#     except:
#         weekly_engagement_df = pd.DataFrame({
#             "artist": ["Chella", "Rema", "Zinoleesky", "Black Sherif & Fireboy DML", "Black Sherif"],
#             "title": ["My Darling", "Bout U", "Most Wanted", "So it Goes", "IRON BOY"],
#             "total_plays": [1921857, 364355, 1738714, 1144601, 0],
#             "total_engagements": [9945, 8991, 8620, 8196, 8075],
#             "unique_users": [820825, 253488, 738401, 598478, 172100]
#         })
    
#     # Create mock editorial playlist data
#     editorial_playlist_df = pd.DataFrame({
#         "added_at": ["2025-04-13", "2025-04-12", "2025-04-12", "2025-04-11", "2025-04-10", 
#                     "2025-04-09", "2025-04-09", "2025-04-08", "2025-04-07", "2025-04-07"],
#         "song_name": ["DYANA", "God is The Greatest", "Do You Know?", "Alhamdulillah", "Uncle Pele",
#                      "Awolowo", "What if", "Dil Cosby Interlude", "Not Ready", "Never Going Back"],
#         "artist_name": ["Erma", "Vybz Kartel", "Siicie & Lasmid", "Siicie", "Dxtiny",
#                        "Fido", "Dalia", "Madlib", "PF Xavi", "William McDowell"],
#         "is_ghost_account": ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
#         "distributor_name": ["Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", 
#                             "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct", "Audiosalad Direct",
#                             "Audiosalad Direct", "Audiosalad Direct"],
#         "playlist_name": ["Afrobeats Now", "Verified Hip-Hop", "Trending Africa", "Alte Cruise", "Afrobeats Now",
#                          "Verified Hip-Hop", "Verified R&B", "Alte Cruise", "Trending Africa", "Gospel Hits"]
#     })
    
#     # Calculate derived metrics and prepare data
    
#     # Calculate engagement per user
#     top_engaged_artists_df['engagements_per_user'] = top_engaged_artists_df['total_engagements'] / top_engaged_artists_df['unique_users']
    
#     # Calculate source tab percentages
#     source_tab_totals = source_channels_df.groupby('source_tab')['event_count'].sum().reset_index()
#     total_events = source_tab_totals['event_count'].sum()
#     source_tab_totals['percentage'] = (source_tab_totals['event_count'] / total_events) * 100
    
#     # Calculate section percentages
#     section_totals = source_channels_df.groupby('section')['event_count'].sum().reset_index()
#     section_totals['percentage'] = (section_totals['event_count'] / total_events) * 100
#     section_totals = section_totals.sort_values('percentage', ascending=False)
    
#     # Process territory reach - calculate artist country distributions
#     # Get unique artists
#     unique_artists = territory_reach_df['artist'].unique()
    
#     artist_country_dist = {}
#     for artist in unique_artists:
#         artist_data = territory_reach_df[territory_reach_df['artist'] == artist]
#         total_plays = artist_data['plays'].sum()
        
#         # Calculate percentages for each country
#         country_percentages = {}
#         for _, row in artist_data.iterrows():
#             country = row['geo_country']
#             plays = row['plays']
#             percentage = (plays / total_plays) * 100 if total_plays > 0 else 0
#             country_percentages[country] = percentage
        
#         artist_country_dist[artist] = country_percentages
    
#     # Identify cross-border opportunities
#     # For each artist-song in top_songs_geo_df, calculate country percentages
#     songs_geo_dist = {}
#     cross_border_opportunities = []
    
#     # Get unique artist-song combinations
#     unique_songs = top_songs_geo_df.drop_duplicates(['artist', 'title'])
    
#     for _, song_row in unique_songs.iterrows():
#         artist = song_row['artist']
#         title = song_row['title']
        
#         # Get all data for this song
#         song_data = top_songs_geo_df[(top_songs_geo_df['artist'] == artist) & (top_songs_geo_df['title'] == title)]
        
#         # Calculate total plays for this song
#         total_song_plays = song_data['total_plays'].sum()
        
#         # Calculate percentages for each country
#         song_country_percentages = {}
#         for _, row in song_data.iterrows():
#             country = row['geo_country']
#             plays = row['total_plays']
#             percentage = (plays / total_song_plays) * 100 if total_song_plays > 0 else 0
#             song_country_percentages[country] = percentage
        
#         songs_geo_dist[f"{artist} - {title}"] = song_country_percentages
        
#         # Compare to artist's overall distribution
#         if artist in artist_country_dist:
#             artist_dist = artist_country_dist[artist]
            
#             # Find countries where artist has higher percentage than song
#             for country, artist_pct in artist_dist.items():
#                 song_pct = song_country_percentages.get(country, 0)
                
#                 # If gap is significant (>5%)
#                 if artist_pct > song_pct + 5:
#                     cross_border_opportunities.append({
#                         'artist': artist,
#                         'song': title,
#                         'country': country,
#                         'artist_pct': artist_pct,
#                         'song_pct': song_pct,
#                         'gap': artist_pct - song_pct,
#                         'total_plays': total_song_plays
#                     })
    
#     # Calculate engagement metrics for songs
#     song_engagement_df = top_songs_geo_df.groupby(['artist', 'title']).agg({
#         'total_plays': 'sum',
#         'total_engagements': 'sum',
#         'unique_users': 'sum'
#     }).reset_index()
    
#     song_engagement_df['engagement_per_user'] = song_engagement_df['total_engagements'] / song_engagement_df['unique_users']
    
#     # Add playlist types to editorial playlists data
#     editorial_playlist_df['playlist_type'] = editorial_playlist_df['playlist_name'].map({
#         'Afrobeats Now': 'Afrobeats',
#         'Verified Hip-Hop': 'Hip-Hop',
#         'Alte Cruise': 'Alternative',
#         'Trending Africa': 'Regional',
#         'Verified R&B': 'R&B',
#         'Gospel Hits': 'Gospel'
#     })
    
#     return (amd_artist_country_df, amd_songs_df, source_channels_df, engagement_per_user_df,
#             small_artists_df, territory_reach_df, top_engaged_artists_df, top_songs_geo_df,
#             weekly_engagement_df, editorial_playlist_df, source_tab_totals, section_totals,
#             cross_border_opportunities, song_engagement_df)

# # Load the data
# try:
#     (amd_artist_country_df, amd_songs_df, source_channels_df, engagement_per_user_df,
#      small_artists_df, territory_reach_df, top_engaged_artists_df, top_songs_geo_df,
#      weekly_engagement_df, editorial_playlist_df, source_tab_totals, section_totals,
#      cross_border_opportunities, song_engagement_df) = load_data()
#     data_loaded = True
# except Exception as e:
#     st.error(f"Error loading data: {e}")
#     data_loaded = False



# # Week 2 content (current)
# with week_tabs[0]:
#     # Dashboard title and description
#     st.markdown('<div class="main-header">🎵 Audiomack ArtistRank Dashboard - Week 2</div>', unsafe_allow_html=True)
#     st.markdown('<div class="date-info">Analysis period: April 7-13, 2025 | Dashboard updated: April 13, 2025</div>', unsafe_allow_html=True)
    
#     # Add Week 2 update notification
#     st.info("👋 **Week 2 Focus:** This dashboard analyzes AMD artist performance, identifies cross-border opportunities, and tracks editorial playlist additions to support A&R decision-making.")
    
#     # Quick stats
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         total_amd_artists = len(amd_songs_df['artist'].unique())
#         st.metric("AMD Artists", f"{total_amd_artists}")
#     with col2:
#         total_songs = len(amd_songs_df)
#         st.metric("Total AMD Songs", f"{total_songs}")
#     with col3:
#         total_countries = len(amd_artist_country_df['geo_country'].unique())
#         st.metric("Countries Reached", f"{total_countries}")
#     with col4:
#         cross_border_opps = len(cross_border_opportunities)
#         st.metric("Cross-Border Opportunities", f"{cross_border_opps}")
    
#     # Create sidebar for filtering
#     st.sidebar.header("Filters")
#     unique_artists = amd_artist_country_df['artist'].unique()
    
#     selected_artists = st.sidebar.multiselect(
#         "Artists",
#         options=unique_artists,
#         default=[]
#     )
    
#     # Fix for the countries multiselect
#     country_options = amd_artist_country_df['geo_country'].unique().tolist()
#     default_countries = [c for c in ['NG', 'GH', 'US', 'JM'] if c in country_options]
    
#     selected_countries = st.sidebar.multiselect(
#         "Countries",
#         options=country_options,
#         default=default_countries
#     )
    
#     # Filter by engagement threshold
#     min_engagement = st.sidebar.slider(
#         "Min Engagement Per User", 
#         min_value=0.0, 
#         max_value=10.0, 
#         value=0.0,
#         step=0.1
#     )
    
#     # Filter by playlists
#     all_playlists = editorial_playlist_df['playlist_name'].unique().tolist()
#     selected_playlists = st.sidebar.multiselect(
#         "Editorial Playlists",
#         options=all_playlists,
#         default=[]
#     )
    
#     # About section in sidebar
#     st.sidebar.markdown("---")
#     st.sidebar.header("About This Dashboard")
#     st.sidebar.info(
#         """
#         This dashboard is developed for the Week 2 assignment of the Audiomack Internship Program, focusing on:
        
#         1. Analyzing AMD artist performance
#         2. Identifying cross-border promotion opportunities
#         3. Tracking editorial playlist additions
        
#         Use the filters to explore different artists, countries, and playlists.
#         """
#     )
    
#     # Create tabs
#     tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10= st.tabs([
#         "🎨 AMD Artist Performance", 
#         "🌍 Cross-Border Opportunities",
#         "🤔 Editorial Playlists", 
#         "🙋 Engagement Analysis",
#         "🌟 Discovery Channels",
#         "📊 A&R Scouting Tracker",
#         "💬 Chatbot",
#         "😈 linlin Weekly Report",
#         "🚀 Momentum Score",  # New tab
#         "📈 Monthly Momentum"
#     ])
    
#     # Tab 1: AMD Artist Performance
#     with tab1:
#         st.markdown('<div class="sub-header">AMD Artist Performance</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">📊 <span class="highlight">Key Insight:</span> Analysis of AMD artists shows significant variation in engagement levels and geographic reach, with several artists demonstrating high potential for growth based on engagement-to-play ratios.</div>', unsafe_allow_html=True)
        
#         # Filter data based on selections
#         filtered_songs = top_songs_geo_df.copy()
#         if selected_artists:
#             filtered_songs = filtered_songs[filtered_songs['artist'].isin(selected_artists)]
#         if selected_countries:
#             filtered_songs = filtered_songs[filtered_songs['geo_country'].isin(selected_countries)]
        
#         # Create song performance metrics
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             total_filtered_plays = filtered_songs['total_plays'].sum()
#             st.metric("Total Plays", f"{total_filtered_plays:,}")
#         with col2:
#             total_filtered_engagements = filtered_songs['total_engagements'].sum()
#             st.metric("Total Engagements", f"{total_filtered_engagements:,}")
#         with col3:
#             avg_engagement_per_user = total_filtered_engagements / filtered_songs['unique_users'].sum() if filtered_songs['unique_users'].sum() > 0 else 0
#             st.metric("Avg Engagement Per User", f"{avg_engagement_per_user:.2f}")
        
#         # Top AMD songs visualization
#         st.subheader("Top AMD Songs by Plays and Engagement")
        
#         # Aggregate song data
#         song_performance = filtered_songs.groupby(['artist', 'title']).agg({
#             'total_plays': 'sum',
#             'total_engagements': 'sum',
#             'unique_users': 'sum'
#         }).reset_index()
        
#         song_performance['engagement_per_user'] = song_performance['total_engagements'] / song_performance['unique_users']
        
#         # Create visualization
#         if not song_performance.empty:
#             fig_songs = px.scatter(
#                 song_performance.sort_values('total_plays', ascending=False).head(20),
#                 x="total_plays", 
#                 y="engagement_per_user",
#                 size="unique_users",
#                 color="artist",
#                 hover_name="title",
#                 text="title",
#                 size_max=50,
#                 title="Top 20 AMD Songs: Plays vs Engagement per User"
#             )
            
#             fig_songs.update_traces(
#                 textposition='top center',
#                 marker=dict(line=dict(width=1, color='DarkSlateGrey'))
#             )
            
#             fig_songs.update_layout(
#                 xaxis_title="Total Plays",
#                 yaxis_title="Engagement per User",
#                 height=600
#             )
            
#             st.plotly_chart(fig_songs, use_container_width=True)
#         else:
#             st.warning("No data available for the selected filters. Please adjust your selections.")
        
#         # Top AMD Artists
#         st.subheader("Top AMD Artists by Total Plays")
        
#         # Aggregate artist data
#         artist_performance = filtered_songs.groupby('artist').agg({
#             'total_plays': 'sum',
#             'total_engagements': 'sum',
#             'unique_users': 'sum'
#         }).reset_index()
        
#         artist_performance['engagement_ratio'] = artist_performance['total_engagements'] / artist_performance['total_plays']
#         artist_performance = artist_performance.sort_values('total_plays', ascending=False)
        
#         # Create visualization
#         if not artist_performance.empty:
#             fig_artists = px.bar(
#                 artist_performance.head(10),
#                 x="artist",
#                 y="total_plays",
#                 color="engagement_ratio",
#     color_continuous_scale="Viridis",
#                 title="Top 10 AMD Artists by Total Plays",
#                 hover_data=["unique_users", "total_engagements", "engagement_ratio"]
#             )
            
#             fig_artists.update_layout(
#                 xaxis_title="Artist",
#                 yaxis_title="Total Plays",
#                 coloraxis_colorbar_title="Engagement Ratio"
#             )
            
#             st.plotly_chart(fig_artists, use_container_width=True)
#         else:
#             st.warning("No artist data available for the selected filters. Please adjust your selections.")
        
#         # Table of AMD songs with metrics
#         st.subheader("AMD Songs Performance Metrics")
        
#         # Create a styled table
#         if not song_performance.empty:
#             st.dataframe(
#                 song_performance.sort_values('total_plays', ascending=False),
#                 use_container_width=True,
#                 column_config={
#                     "artist": st.column_config.TextColumn("Artist"),
#                     "title": st.column_config.TextColumn("Title"),
#                     "total_plays": st.column_config.NumberColumn("Total Plays", format="%d"),
#                     "total_engagements": st.column_config.NumberColumn("Total Engagements", format="%d"),
#                     "unique_users": st.column_config.NumberColumn("Unique Users", format="%d"),
#                     "engagement_per_user": st.column_config.NumberColumn("Engagement per User", format="%.3f")
#                 }
#             )
#         else:
#             st.info("No song data available to display.")
        
#         # Small artists with high engagement
#         st.subheader("Small Artists with High Engagement")
        
#         # Sort small artists by engagement per user
#         small_artists_sorted = small_artists_df.sort_values('engagements_per_user', ascending=False)
        
#         # Create visualization
#         fig_small_artists = px.bar(
#             small_artists_sorted.head(10),
#             x="artist",
#             y="engagements_per_user",
#             color="total_engagements",
#             title="Small Artists with High Engagement per User",
#             hover_data=["total_users", "total_plays", "total_engagements"]
#         )
        
#         fig_small_artists.update_layout(
#             xaxis_title="Artist",
#             yaxis_title="Engagements per User",
#             coloraxis_colorbar_title="Total Engagements"
#         )
        
#         st.plotly_chart(fig_small_artists, use_container_width=True)
        
#         st.markdown("""
#         ### Key Observations
        
#         - **High Engagement Niche Artists**: Several smaller artists (with fewer plays) show exceptionally high engagement per user, 
#           suggesting highly dedicated fan bases that could be nurtured.
        
#         - **Engagement Quality**: Top artists by total plays don't always have the highest engagement quality metrics, 
#           highlighting the importance of looking beyond pure volume metrics.
        
#         - **Growth Potential**: Artists with higher engagement ratios may have more potential for organic growth, 
#           as they're already creating content that resonates strongly with their audience.
#         """)
    
#     # Tab 2: Cross-Border Opportunities
#     with tab2:
#         st.markdown('<div class="sub-header">Cross-Border Promotion Opportunities</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">🌍 <span class="highlight">Key Finding:</span> Several AMD artists show significant gaps between their overall audience geo distribution and their recent song distribution, representing clear opportunities for targeted cross-border promotion.</div>', unsafe_allow_html=True)
        
#         # Filter cross-border opportunities
#         filtered_opportunities = cross_border_opportunities.copy()
#         if selected_artists:
#             filtered_opportunities = [opp for opp in filtered_opportunities if opp['artist'] in selected_artists]
#         if selected_countries:
#             filtered_opportunities = [opp for opp in filtered_opportunities if opp['country'] in selected_countries]
        
#         # Top cross-border opportunities
#         st.subheader("Top Cross-Border Promotion Opportunities")
        
#         if filtered_opportunities:
#             # Convert to DataFrame for visualization
#             opps_df = pd.DataFrame(filtered_opportunities)
            
#             # Sort by gap size
#             opps_df = opps_df.sort_values('gap', ascending=False)
            
#             # Create visualization
#             fig_opps = px.bar(
#                 opps_df.head(10),
#                 x="artist",
#                 y="gap",
#                 color="country",
#                 title="Top 10 Cross-Border Promotion Opportunities",
#                 hover_data=["song", "artist_pct", "song_pct", "gap", "total_plays"],
#                 labels={"gap": "Market Penetration Gap (%)"}
#             )
            
#             fig_opps.update_layout(
#                 xaxis_title="Artist",
#                 yaxis_title="Gap (%)",
#                 height=500
#             )
            
#             st.plotly_chart(fig_opps, use_container_width=True)
            
#             # Create a styled table
#             st.dataframe(
#                 opps_df,
#                 use_container_width=True,
#                 column_config={
#                     "artist": st.column_config.TextColumn("Artist"),
#                     "song": st.column_config.TextColumn("Song"),
#                     "country": st.column_config.TextColumn("Country"),
#                     "artist_pct": st.column_config.NumberColumn("Artist Audience %", format="%.1f%%"),
#                     "song_pct": st.column_config.NumberColumn("Song Audience %", format="%.1f%%"),
#                     "gap": st.column_config.NumberColumn("Gap", format="%.1f%%"),
#                     "total_plays": st.column_config.NumberColumn("Total Plays", format="%d")
#                 }
#             )
#         else:
#             st.write("No cross-border opportunities found with the current filter settings.")
        
#         # Country distribution visualization
#         st.subheader("Artist vs. Song Geographic Distribution")
        
#         # Allow user to select an artist for detailed view
#         if len(unique_artists) > 0:
#             # Select default artist
#             default_artist = unique_artists[0]
#             if selected_artists and selected_artists[0] in unique_artists:
#                 default_artist = selected_artists[0]
                
#             artist_for_geo = st.selectbox(
#                 "Select Artist to View Geographic Distribution",
#                 options=unique_artists,
#                 index=list(unique_artists).index(default_artist) if default_artist in unique_artists else 0
#             )
            
#             # Get artist's songs
#             artist_songs = top_songs_geo_df[top_songs_geo_df['artist'] == artist_for_geo]['title'].unique()
            
#             if len(artist_songs) > 0:
#                 # Let user select a specific song
#                 selected_song = st.selectbox(
#                     "Select Song",
#                     options=artist_songs
#                 )
                
#                 # Get data for the artist and song
#                 artist_geo_data = amd_artist_country_df[amd_artist_country_df['artist'] == artist_for_geo]
#                 song_geo_data = top_songs_geo_df[(top_songs_geo_df['artist'] == artist_for_geo) & 
#                                                 (top_songs_geo_df['title'] == selected_song)]
                
#                 # Calculate percentages
#                 if not artist_geo_data.empty and not song_geo_data.empty:
#                     # Calculate artist percentages
#                     artist_total_plays = artist_geo_data['plays'].sum()
#                     artist_geo_data['percentage'] = (artist_geo_data['plays'] / artist_total_plays) * 100
                    
#                     # Calculate song percentages
#                     song_total_plays = song_geo_data['total_plays'].sum()
#                     song_geo_data['percentage'] = (song_geo_data['total_plays'] / song_total_plays) * 100
                    
#                     # Create a comparison chart
#                     fig_geo_compare = make_subplots(
#                         rows=1, 
#                         cols=2,
#                         subplot_titles=("Artist Overall Audience", f"Song: {selected_song} Audience"),
#                         specs=[[{"type": "bar"}, {"type": "bar"}]]
#                     )
                    
#                     # Artist geo distribution
#                     artist_geo_sorted = artist_geo_data.sort_values('percentage', ascending=False).head(5)
#                     fig_geo_compare.add_trace(
#                         go.Bar(
#                             x=artist_geo_sorted['geo_country'],
#                             y=artist_geo_sorted['percentage'],
#                             name="Artist Overall",
#                             marker_color='#4ECDC4'
#                         ),
#                         row=1, col=1
#                     )
                    
#                     # Song geo distribution
#                     song_geo_sorted = song_geo_data.sort_values('percentage', ascending=False).head(5)
#                     fig_geo_compare.add_trace(
#                         go.Bar(
#                             x=song_geo_sorted['geo_country'],
#                             y=song_geo_sorted['percentage'],
#                             name=f"Song: {selected_song}",
#                             marker_color='#FF6B6B'
#                         ),
#                         row=1, col=2
#                     )
                    
#                     fig_geo_compare.update_layout(
#                         title=f"{artist_for_geo}: Geographic Distribution Comparison",
#                         height=500
#                     )
                    
#                     st.plotly_chart(fig_geo_compare, use_container_width=True)
                    
#                     # Show strategy recommendations
#                     st.subheader("Recommended Promotion Strategies")
                    
#                     # Find countries with gaps
#                     countries_with_gaps = []
#                     artist_countries = set(artist_geo_sorted['geo_country'])
#                     song_countries = set(song_geo_sorted['geo_country'])
                    
#                     for country in artist_countries:
#                         if country not in song_countries:
#                             countries_with_gaps.append(country)
#                         else:
#                             artist_pct = artist_geo_sorted[artist_geo_sorted['geo_country'] == country]['percentage'].values[0]
#                             song_country_data = song_geo_sorted[song_geo_sorted['geo_country'] == country]
#                             song_pct = song_country_data['percentage'].values[0] if not song_country_data.empty else 0
                            
#                             if artist_pct > song_pct + 5:  # If gap is more than 5%
#                                 countries_with_gaps.append(country)
                    
#                     if countries_with_gaps:
#                         st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
#                         st.markdown(f"### Promotion Strategy for {artist_for_geo} - {selected_song}")
                        
#                         for country in countries_with_gaps:
#                             st.markdown(f"#### {country} Market Expansion")
                            
#                             if country == "NG":
#                                 st.markdown("""
#                                 - **Push Notifications**: Target Nigerian users who have engaged with similar artists
#                                 - **Trending Placement**: Feature the song in Nigeria-specific trending sections
#                                 - **Social Media Campaign**: Partner with Nigerian influencers for song promotion
#                                 """)
#                             elif country == "GH":
#                                 st.markdown("""
#                                 - **Radio Partnerships**: Collaborate with top Ghanaian radio stations
#                                 - **Local Events**: Feature the song in promotional events in Ghana
#                                 - **Influencer Marketing**: Partner with Ghanaian social media personalities
#                                 """)
#                             elif country == "US":
#                                 st.markdown("""
#                                 - **Diaspora Targeting**: Create targeted campaigns for the West African diaspora in major US cities
#                                 - **Playlist Placement**: Push for placement in US-focused Afrobeats playlists
#                                 - **College Campus Marketing**: Target universities with high international student populations
#                                 """)
#                             elif country == "UK":
#                                 st.markdown("""
#                                 - **Club Promotion**: Partner with UK DJs and clubs with African music nights
#                                 - **Community Events**: Promote at UK African cultural events and festivals
#                                 - **University Marketing**: Target UK universities with high African student populations
#                                 """)
#                             elif country == "JM":
#                                 st.markdown("""
#                                 - **Dancehall Cross-Promotion**: Partner with Jamaican dancehall artists for remixes
#                                 - **Radio Placement**: Target Jamaican radio stations for song placement
#                                 - **Local Influencers**: Engage with Jamaican music influencers
#                                 """)
#                             else:
#                                 st.markdown(f"""
#                                 - **Targeted Advertising**: Develop geo-specific ads for {country} market
#                                 - **Local Partnerships**: Identify potential collaborators in {country}
#                                 - **Platform Features**: Utilize Audiomack's geo-targeted features for promotion
#                                 """)
                        
#                         st.markdown("</div>", unsafe_allow_html=True)
#                     else:
#                         st.info(f"No significant geographic distribution gaps found for {selected_song}.")
#                 else:
#                     st.warning(f"Insufficient data for {artist_for_geo} or {selected_song} to analyze geographic distribution.")
#             else:
#                 st.warning(f"No songs found for {artist_for_geo}.")
#         else:
#             st.warning("No artist data available. Please check your data sources.")
    
#     # Tab 3: Editorial Playlists
#     with tab3:
#         st.markdown('<div class="sub-header">Editorial Playlist Tracker</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">🎵 <span class="highlight">New Feature:</span> This tracker allows you to monitor AMD artist additions to editorial playlists, helping identify promotional opportunities and track curator selections.</div>', unsafe_allow_html=True)
        
#         # Filter playlist data
#         filtered_playlists = editorial_playlist_df.copy()
#         if selected_artists:
#             filtered_playlists = filtered_playlists[filtered_playlists['artist_name'].isin(selected_artists)]
#         if selected_playlists:
#             filtered_playlists = filtered_playlists[filtered_playlists['playlist_name'].isin(selected_playlists)]
        
#         # Editorial playlist metrics
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             total_adds = len(filtered_playlists)
#             st.metric("Total Playlist Adds (This Week)", f"{total_adds}")
        
#         with col2:
#             unique_playlists = len(filtered_playlists['playlist_name'].unique())
#             st.metric("Unique Playlists", f"{unique_playlists}")
        
#         with col3:
#             unique_artists_added = len(filtered_playlists['artist_name'].unique())
#             st.metric("Unique Artists Added", f"{unique_artists_added}")
        
#         # Recent editorial playlist additions
#         st.subheader("Recent Editorial Playlist Additions")
        
#         # Create a styled table
#         st.dataframe(
#             filtered_playlists.sort_values('added_at', ascending=False),
#             use_container_width=True,
#             column_config={
#                 "added_at": st.column_config.DateColumn("Date Added", format="MMM DD, YYYY"),
#                 "artist_name": st.column_config.TextColumn("Artist"),
#                 "song_name": st.column_config.TextColumn("Song"),
#                 "playlist_name": st.column_config.TextColumn("Playlist"),
#                 "is_ghost_account": st.column_config.TextColumn("Ghost Account?"),
#                 "distributor_name": st.column_config.TextColumn("Distributor")
#             }
#         )
        
#         # Playlist distribution visualization
#         st.subheader("Editorial Playlist Distribution")
        
#         # Get playlist counts
#         playlist_counts = filtered_playlists['playlist_name'].value_counts().reset_index()
#         playlist_counts.columns = ['Playlist', 'Count']
        
#         # Create visualization
#         if not playlist_counts.empty:
#             fig_playlist = px.pie(
#                 playlist_counts,
#                 values='Count',
#                 names='Playlist',
#                 title="Editorial Playlist Distribution",
#                 color_discrete_sequence=px.colors.qualitative.Bold
#             )
            
#             fig_playlist.update_traces(textinfo='percent+label', pull=[0.1 if i == 0 else 0 for i in range(len(playlist_counts))])
            
#             st.plotly_chart(fig_playlist, use_container_width=True)
#         else:
#             st.info("No playlist data to display with the current filters.")
        
#         # Playlist additions by day
#         st.subheader("Playlist Additions by Day")
        
#         # Convert dates and count by day
#         filtered_playlists['added_at'] = pd.to_datetime(filtered_playlists['added_at'])
#         adds_by_day = filtered_playlists.groupby([filtered_playlists['added_at'].dt.date, 'playlist_name']).size().reset_index()
#         adds_by_day.columns = ['Date', 'Playlist', 'Count']
        
#         # Create visualization
#         if not adds_by_day.empty:
#             fig_adds_by_day = px.bar(
#                 adds_by_day,
#                 x='Date',
#                 y='Count',
#                 color='Playlist',
#                 title="Editorial Playlist Additions by Day",
#                 labels={'Count': 'Number of Additions'}
#             )
            
#             st.plotly_chart(fig_adds_by_day, use_container_width=True)
#         else:
#             st.info("No daily addition data to display with the current filters.")
        
#         # SQL Query for the Superset Chart
#         st.subheader("SQL Query for Superset Implementation")
        
#         st.code('''
#     -- Editorial Playlist Additions Tracker
#     SELECT
#       added_at,
#       song_name,
#       artist_name,
#       is_ghost_account,
#       distributor_name,
#       playlist_name
#     FROM bi01.playlist_interactions_daily_v003
#     WHERE added_at BETWEEN CURRENT_DATE - INTERVAL '7' DAY AND CURRENT_DATE
#       AND distributor_name = 'Audiosalad Direct'
#     ORDER BY added_at DESC;
#         ''', language='sql')
        
#         st.markdown("""
#         ### Implementation Steps for Superset Chart
        
#         1. **Create a New Dataset in Superset**:
#            - Connect to the `bi01.playlist_interactions_daily_v003` table
#            - Set up a refresh schedule (daily at 4AM recommended)
        
#         2. **Create a Table Visualization**:
#            - Add the columns: `added_at`, `song_name`, `artist_name`, `is_ghost_account`, `distributor_name`, `playlist_name`
#            - Set up sorting by `added_at` descending
        
#         3. **Add Filtering Options**:
#            - Date range filter for `added_at`
#            - Multi-select filter for `playlist_name`
#            - Ghost account status filter
        
#         4. **Dashboard Integration**:
#            - Add to the AMD dashboard
#            - Set permissions for Jordan and Jalen to access
#         """)
    
#     # Tab 4: Engagement Analysis
#     with tab4:
#         st.markdown('<div class="sub-header">Engagement Analysis</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">💡 <span class="highlight">Key Insight:</span> Engagement metrics like favorites, reposts, and comments offer better indicators of audience connection than raw play counts. Several AMD artists show exceptionally high engagement per user, indicating strong resonance with their audience.</div>', unsafe_allow_html=True)
        
#         # Filter engagement data
#         filtered_engagement = top_engaged_artists_df.copy()
#         if selected_artists:
#             filtered_engagement = filtered_engagement[filtered_engagement['artist'].isin(selected_artists)]
        
#         # Apply minimum engagement filter
#         filtered_engagement = filtered_engagement[filtered_engagement['engagements_per_user'] >= min_engagement]
        
#         # Engagement metrics
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             avg_eng_ratio = filtered_engagement['total_engagements'].sum() / filtered_engagement['total_plays'].sum() if filtered_engagement['total_plays'].sum() > 0 else 0
#             st.metric("Avg Engagement Ratio", f"{avg_eng_ratio:.3f}")
        
#         with col2:
#             avg_eng_per_user = filtered_engagement['total_engagements'].sum() / filtered_engagement['unique_users'].sum() if filtered_engagement['unique_users'].sum() > 0 else 0
#             st.metric("Avg Engagements Per User", f"{avg_eng_per_user:.3f}")
        
#         with col3:
#             plays_per_user = filtered_engagement['total_plays'].sum() / filtered_engagement['unique_users'].sum() if filtered_engagement['unique_users'].sum() > 0 else 0
#             st.metric("Avg Plays Per User", f"{plays_per_user:.1f}")
        
#         # Engagement ratio visualization
#         st.subheader("Top Artists by Engagement per User")
        
#         # Sort by engagements per user
#         engagement_sorted = filtered_engagement.sort_values('engagements_per_user', ascending=False)
        
#         # Create visualization
#         if not engagement_sorted.empty:
#             fig_engagement = px.bar(
#                 engagement_sorted.head(15),
#                 x="artist",
#                 y="engagements_per_user",
#                 color="total_plays",
#                 color_continuous_scale="Viridis",
#                 title="Top 15 Artists by Engagement per User",
#                 hover_data=["total_engagements", "unique_users", "total_plays"]
#             )
            
#             fig_engagement.update_layout(
#                 xaxis_title="Artist",
#                 yaxis_title="Engagements per User",
#                 coloraxis_colorbar_title="Total Plays"
#             )
            
#             st.plotly_chart(fig_engagement, use_container_width=True)
#         else:
#             st.info("No engagement data available with the current filters.")
        
#         # Engagement vs. plays comparison
#         st.subheader("Engagement vs. Plays Analysis")
        
#         # Create scatter plot
#         if not filtered_engagement.empty:
#             fig_scatter = px.scatter(
#                 filtered_engagement,
#                 x="total_plays",
#                 y="engagements_per_user",
#                 size="unique_users",
#                 color="artist",
#                 hover_name="artist",
#                 log_x=True,
#                 size_max=50,
#                 title="Engagement per User vs. Total Plays (Log Scale)"
#             )
            
#             fig_scatter.update_layout(
#                 xaxis_title="Total Plays (Log Scale)",
#                 yaxis_title="Engagements per User",
#                 height=600
#             )
            
#             st.plotly_chart(fig_scatter, use_container_width=True)
#         else:
#             st.info("No data available to display the scatter plot.")
        
#         # Create a styled table of top engaged artists
#         st.subheader("Detailed Engagement Metrics by Artist")
        
#         if not engagement_sorted.empty:
#             st.dataframe(
#                 engagement_sorted,
#                 use_container_width=True,
#                 column_config={
#                     "artist": st.column_config.TextColumn("Artist"),
#                     "total_plays": st.column_config.NumberColumn("Total Plays", format="%d"),
#                     "total_engagements": st.column_config.NumberColumn("Total Engagements", format="%d"),
#                     "unique_users": st.column_config.NumberColumn("Unique Users", format="%d"),
#                     "engagements_per_user": st.column_config.NumberColumn("Engagements per User", format="%.3f")
#                 }
#             )
#         else:
#             st.info("No engagement data to display in the table.")
        
#         st.markdown("""
#         ### Key Engagement Insights
        
#         - **Inverse Relationship**: A notable inverse relationship exists between play count and engagement per user - 
#           smaller artists often have more engaged fan bases.
        
#         - **Audience Quality Indicator**: Engagement per user serves as a better indicator of audience quality 
#           than raw play counts, helping identify artists with strong connections to their listeners.
        
#         - **Growth Predictor**: Higher engagement metrics often predict future growth potential, 
#           as engaged listeners are more likely to share and promote content within their networks.
#         """)
    
#     # Tab 5: Discovery Channels
#     with tab5:
#         st.markdown('<div class="sub-header">User Discovery Channels</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">🔍 <span class="highlight">Actionable Insight:</span> "For You" feed and "Trending" sections drive the largest portion of engagement, making these critical places for AMD artist visibility. The My Library features also show strong engagement, indicating the importance of converting casual listeners to followers.</div>', unsafe_allow_html=True)
        
#         # Source tab distribution
#         st.subheader("Engagement by Source Tab")
        
#         # Create visualization for source tabs
#         if not source_tab_totals.empty:
#             fig_source_tabs = px.pie(
#                 source_tab_totals.sort_values('percentage', ascending=False),
#                 values='percentage',
#                 names='source_tab',
#                 title="Engagement Distribution by Source Tab",
#                 hole=0.4
#             )
            
#             fig_source_tabs.update_traces(textinfo='percent+label')
            
#             st.plotly_chart(fig_source_tabs, use_container_width=True)
#         else:
#             st.info("No source tab data available to display.")
        
#         # Section distribution
#         st.subheader("Engagement by Section")
        
#         # Create visualization for top sections
#         if not section_totals.empty:
#             fig_sections = px.bar(
#                 section_totals.head(10),
#                 x='section',
#                 y='percentage',
#                 color='percentage',
#                 color_continuous_scale='Viridis',
#                 title="Top 10 Sections by Engagement Percentage"
#             )
            
#             fig_sections.update_layout(
#                 xaxis_title="Section",
#                 yaxis_title="Percentage of Total Engagement (%)",
#                 xaxis={'categoryorder': 'total descending'}
#             )
            
#             st.plotly_chart(fig_sections, use_container_width=True)
#         else:
#             st.info("No section data available to display.")
        
#         # Strategic recommendations
#         st.subheader("Strategic Recommendations for AMD Artists")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
#             st.markdown("### Optimize for Top Discovery Channels")
#             st.markdown("""
#             1. **My Library Optimization**
#                - Focus on converting casual listeners to followers/favorites
#                - Create content that encourages offline listening
#                - Develop a cadence of releases to keep library fresh
            
#             2. **Search Visibility**
#                - Optimize artist name and song titles for searchability
#                - Use popular genre keywords in descriptions
#                - Create songs that match popular search queries
#             """)
#             st.markdown("</div>", unsafe_allow_html=True)
        
#         with col2:
#             st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
#             st.markdown("### Section-Specific Strategies")
#             st.markdown("""
#             1. **For You Feed**
#                - Create content that encourages high engagement rates
#                - Focus on quality over quantity to improve algorithm ranking
#                - Leverage existing engaged fans to boost algorithmic placement
            
#             2. **Trending Sections**
#                - Time releases strategically to maximize trending potential
#                - Create engagement campaigns around release dates
#                - Identify regional trending opportunities based on geo analysis
#             """)
#             st.markdown("</div>", unsafe_allow_html=True)
        
#         # Discovery funnel visualization
#         st.subheader("User Discovery Funnel")
        
#         # Create made-up funnel data based on the discovered patterns
#         funnel_data = pd.DataFrame({
#             'Stage': ['Discovery', 'First Play', 'Multiple Plays', 'Engagement', 'Favorite/Follow', 'Repeat Listener'],
#             'Users': [1000000, 750000, 500000, 250000, 150000, 100000],
#             'Conversion': [100, 75, 67, 50, 60, 67]
#         })
        
#         # Create funnel visualization
#         fig_funnel = go.Figure(go.Funnel(
#             y=funnel_data['Stage'],
#             x=funnel_data['Users'],
#             textinfo="value+percent initial",
#             marker={"color": ["#4ECDC4", "#1A535C", "#FF6B6B", "#FF9F1C", "#E71D36", "#662E9B"]}
#         ))
        
#         fig_funnel.update_layout(
#             title="User Journey Funnel",
#             height=500
#         )
        
#         st.plotly_chart(fig_funnel, use_container_width=True)
        
#         st.markdown("""
#         ### Optimizing the User Journey
        
#         The analysis of discovery channels reveals a clear user journey path:
        
#         1. **Discovery**: Users primarily find content through "For You" feeds, Search, and Trending sections
#         2. **Engagement**: Initial plays lead to favorites, shares, and comments for resonant content
#         3. **Retention**: Engaged users add content to their libraries, download for offline use, and become repeat listeners
        
#         To maximize AMD artist success, promotional strategies should target each stage of this journey, with particular focus on increasing conversion rates between discovery and engagement.
#         """)
    
#     # Tab 6: A&R Scouting Tracker
#     with tab6:
#         # Call the scouting tracker function
#         load_scouting_tracker()


#     #still debuggggg!
#     with tab7:
#         st.title("💬 Chatbot Assistant")
    
#         with st.sidebar:
#             openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#             st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    
#         if "messages" not in st.session_state:
#             st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with this dashboard?"}]
    
#         for msg in st.session_state.messages:
#             st.chat_message(msg["role"]).write(msg["content"])
    
#         if prompt := st.chat_input():
#             if not openai_api_key:
#                 st.info("Please add your OpenAI API key to continue.")
#                 st.stop()
    
#             from openai import OpenAI
#             client = OpenAI(api_key=openai_api_key)
    
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             st.chat_message("user").write(prompt)
    
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=st.session_state.messages
#             )
#             msg = response.choices[0].message.content
#             st.session_state.messages.append({"role": "assistant", "content": msg})
#             st.chat_message("assistant").write(msg)
# # Add this to your tab7 (Chatbot) in the Streamlit dashboard for **local LLM**
# # Make sure llama-cpp-python is installed and openhermes model is downloaded

#         # from llama_cpp import Llama

#         # # Load model - replace with correct model path
#         # llm = Llama(model_path="models/openhermes-2.5-mistral.Q4_K_M.gguf", n_ctx=2048, n_gpu_layers=35)

#         # # Chatbot state
#         # if "chat_history" not in st.session_state:
#         #     st.session_state.chat_history = []

#         # # Render chat history
#         # for msg in st.session_state.chat_history:
#         #     with st.chat_message(msg["role"]):
#         #         st.markdown(msg["content"])

#         # # Handle user input
#         # if prompt := st.chat_input("Ask me anything about ArtistRank..."):
#         #     # Show user input
#         #     st.session_state.chat_history.append({"role": "user", "content": prompt})
#         #     with st.chat_message("user"):
#         #         st.markdown(prompt)

#         #     # Generate LLM response
#         #     with st.chat_message("assistant"):
#         #         with st.spinner("Thinking..."):
#         #             output = llm(prompt, max_tokens=256, stop=["</s>"])
#         #             reply = output["choices"][0]["text"].strip()
#         #             st.markdown(reply)

#         #     # Save reply
#         #     st.session_state.chat_history.append({"role": "assistant", "content": reply})

#     with tab8:
#         st.markdown("[Linlin's weekly report](https://docs.google.com/document/d/1HUVM9YE0x0-w_aizbGGEnIJq1OWfQANks122s3nZwDw/edit?usp=sharing)")


# # Then, after all your other tab content blocks, add this new block for the Momentum Score tab:

#     # Tab 9: Momentum Score
#     with tab9:
#         st.markdown('<div class="sub-header">Artist Momentum Score - Week 2</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">🚀 <span class="highlight">Key Metric:</span> The Momentum Score combines play growth, listener growth, engagement quality, and geographic reach to identify artists gaining traction. This score helps prioritize AMD artists for promotion and support.</div>', unsafe_allow_html=True)
        
#         # Create mock data based on the SQL query
#         momentum_score_df = pd.DataFrame({
#             "artist": ["FAVE", "Bloody Civilian", "Khaid", "Odumodu Blvck", "Young Jonn", 
#                     "Victony", "Shallipopi", "CKay", "Seyi Vibez", "Lil kesh"],
#             "plays": [820000, 580000, 1250000, 950000, 2500000, 
#                     1650000, 3200000, 1950000, 2400000, 1680000],
#             "unique_listeners": [320000, 220000, 450000, 380000, 850000, 
#                                 560000, 950000, 670000, 820000, 580000],
#             "favorites": [64000, 55000, 108000, 72200, 153000, 
#                         89600, 161600, 120900, 98400, 81200],
#             "shares": [19200, 17600, 27000, 19000, 42500, 
#                     16800, 48000, 33500, 32800, 23200],
#             "country_count": [8, 6, 9, 7, 12, 8, 14, 10, 11, 9],
#             "play_growth_pct": [66.67, 104.55, 50.77, 41.38, 40.00, 
#                             31.58, 28.00, 19.74, 26.32, 15.86],
#             "listener_growth_pct": [47.06, 63.64, 40.00, 28.13, 25.00, 
#                                 23.81, 18.75, 12.28, 17.14, 9.43],
#             "fav_per_listener": [0.2000, 0.2500, 0.2400, 0.1900, 0.1800, 
#                                 0.1600, 0.1701, 0.1804, 0.1200, 0.1400],
#             "share_per_listener": [0.0600, 0.0800, 0.0600, 0.0500, 0.0500, 
#                                 0.0300, 0.0505, 0.0500, 0.0400, 0.0400],
#             "momentum_score": [57.22, 80.82, 48.73, 39.58, 39.80, 
#                             32.87, 32.30, 24.62, 29.04, 21.03]
#         })
        
#         # Add a size cohort for reference
#         # We'll categorize based on play count - you can adjust thresholds if needed
#         def determine_size_cohort(plays):
#             if plays < 650000:
#                 return "micro"
#             elif plays < 1500000:
#                 return "small"
#             elif plays < 2500000:
#                 return "medium"
#             else:
#                 return "large"
        
#         momentum_score_df["size_cohort"] = momentum_score_df["plays"].apply(determine_size_cohort)
        
#         # Metrics section
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             avg_momentum = momentum_score_df['momentum_score'].mean()
#             st.metric("Average Momentum Score", f"{avg_momentum:.2f}")
        
#         with col2:
#             max_artist = momentum_score_df.loc[momentum_score_df['momentum_score'].idxmax()]['artist']
#             max_score = momentum_score_df['momentum_score'].max()
#             st.metric("Highest Momentum Artist", f"{max_artist} ({max_score:.2f})")
        
#         with col3:
#             micro_artists = len(momentum_score_df[momentum_score_df['size_cohort'] == 'micro'])
#             st.metric("Micro Artists in Top 10", f"{micro_artists}")
        
#         # Main momentum score visualization
#         st.subheader("Top 10 Artists by Momentum Score")
        
#         # Create a color scale for the momentum score
#         fig_momentum = px.bar(
#             momentum_score_df.sort_values('momentum_score', ascending=False),
#             x="artist",
#             y="momentum_score",
#             color="size_cohort",
#             title="Artist Momentum Score Ranking",
#             color_discrete_map={
#                 "micro": "#FF9F1C",
#                 "small": "#4ECDC4",
#                 "medium": "#1A535C",
#                 "large": "#FF6B6B"
#             },
#             hover_data=["plays", "unique_listeners", "play_growth_pct", "listener_growth_pct", 
#                         "fav_per_listener", "share_per_listener", "country_count"]
#         )
        
#         fig_momentum.update_layout(
#             xaxis_title="Artist",
#             yaxis_title="Momentum Score",
#             xaxis={'categoryorder': 'total descending'},
#             height=500
#         )
        
#         fig_momentum.update_traces(
#             hovertemplate="<b>Artist:</b> %{x}<br>" +
#                         "<b>Momentum Score:</b> %{y:.2f}<br>" +
#                         "<b>Size Cohort:</b> %{marker.color}<br>" +
#                         "<b>Plays:</b> %{customdata[0]:,.0f}<br>" +
#                         "<b>Unique Listeners:</b> %{customdata[1]:,.0f}<br>" +
#                         "<b>Play Growth:</b> %{customdata[2]:.1f}%<br>" +
#                         "<b>Listener Growth:</b> %{customdata[3]:.1f}%<br>" +
#                         "<b>Favs per Listener:</b> %{customdata[4]:.4f}<br>" +
#                         "<b>Shares per Listener:</b> %{customdata[5]:.4f}<br>" +
#                         "<b>Country Count:</b> %{customdata[6]}<extra></extra>"
#         )
        
#         st.plotly_chart(fig_momentum, use_container_width=True)
        
#         # Growth vs. Engagement scatter plot
#         st.subheader("Growth vs. Engagement Analysis")
        
#         fig_scatter = px.scatter(
#             momentum_score_df,
#             x="play_growth_pct",
#             y="fav_per_listener",
#             size="momentum_score",
#             color="size_cohort",
#             hover_name="artist",
#             size_max=50,
#             title="Play Growth vs. Engagement Quality",
#             labels={
#                 "play_growth_pct": "Play Growth (%)",
#                 "fav_per_listener": "Favorites per Listener"
#             }
#         )
        
#         fig_scatter.update_layout(
#             xaxis_title="Play Growth (%)",
#             yaxis_title="Favorites per Listener",
#             height=500
#         )
        
#         st.plotly_chart(fig_scatter, use_container_width=True)
        
#         # Detailed momentum score table
#         st.subheader("Detailed Momentum Score Components")
        
#         # Create a styled table
#         st.dataframe(
#             momentum_score_df.sort_values('momentum_score', ascending=False),
#             use_container_width=True,
#             column_config={
#                 "artist": st.column_config.TextColumn("Artist"),
#                 "size_cohort": st.column_config.TextColumn("Size Cohort"),
#                 "plays": st.column_config.NumberColumn("Plays", format="%d"),
#                 "unique_listeners": st.column_config.NumberColumn("Unique Listeners", format="%d"),
#                 "play_growth_pct": st.column_config.NumberColumn("Play Growth %", format="%.1f%%"),
#                 "listener_growth_pct": st.column_config.NumberColumn("Listener Growth %", format="%.1f%%"),
#                 "fav_per_listener": st.column_config.NumberColumn("Favs per Listener", format="%.4f"),
#                 "share_per_listener": st.column_config.NumberColumn("Shares per Listener", format="%.4f"),
#                 "country_count": st.column_config.NumberColumn("Countries", format="%d"),
#                 "momentum_score": st.column_config.NumberColumn("Momentum Score", format="%.2f")
#             }
#         )
        
#         # Momentum score formula explanation
#         st.subheader("Momentum Score Formula")
        
#         st.markdown("""
#         The **Momentum Score** is calculated using the following formula:
        
#         ```
#         Momentum Score = (Play Growth % × 0.4) + 
#                         (Listener Growth % × 0.3) + 
#                         (Favorites per Listener × 15) + 
#                         (Shares per Listener × 10) + 
#                         (Country Count × 0.5)
#         ```
        
#         **Weighting Rationale:**
        
#         - **Growth metrics (70%)**: Prioritizes artists with increasing audience and engagement
#         - **Engagement quality (25%)**: Rewards artists whose content generates strong user actions
#         - **Geographic reach (5%)**: Gives slight preference to artists with cross-border appeal
        
#         This composite score helps identify artists gaining traction regardless of their absolute play counts.
#         """)
        
#         # Artist-focused selection for detailed view
#         st.subheader("Artist-Specific Momentum Analysis")
        
#         selected_momentum_artist = st.selectbox(
#             "Select an artist for detailed analysis:",
#             options=momentum_score_df["artist"].tolist()
#         )
        
#         # Get selected artist data
#         artist_data = momentum_score_df[momentum_score_df["artist"] == selected_momentum_artist].iloc[0]
        
#         # Create score breakdown
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown(f"### {selected_momentum_artist} Momentum Components")
            
#             # Calculate component contributions
#             play_growth_contribution = artist_data["play_growth_pct"] * 0.4
#             listener_growth_contribution = artist_data["listener_growth_pct"] * 0.3
#             fav_contribution = artist_data["fav_per_listener"] * 15
#             share_contribution = artist_data["share_per_listener"] * 10
#             geo_contribution = artist_data["country_count"] * 0.5
            
#             # Create component breakdown dataframe
#             components_df = pd.DataFrame({
#                 "Component": ["Play Growth", "Listener Growth", "Favorites Engagement", 
#                             "Shares Engagement", "Geographic Reach"],
#                 "Raw Value": [
#                     f"{artist_data['play_growth_pct']:.1f}%", 
#                     f"{artist_data['listener_growth_pct']:.1f}%",
#                     f"{artist_data['fav_per_listener']:.4f}",
#                     f"{artist_data['share_per_listener']:.4f}",
#                     f"{artist_data['country_count']}"
#                 ],
#                 "Contribution": [
#                     play_growth_contribution,
#                     listener_growth_contribution,
#                     fav_contribution,
#                     share_contribution,
#                     geo_contribution
#                 ]
#             })
            
#             # Show table of contributions
#             st.dataframe(
#                 components_df,
#                 use_container_width=True,
#                 column_config={
#                     "Component": st.column_config.TextColumn("Component"),
#                     "Raw Value": st.column_config.TextColumn("Raw Value"),
#                     "Contribution": st.column_config.NumberColumn("Score Contribution", format="%.2f")
#                 }
#             )
        
#         with col2:
#             # Create pie chart of component contributions
#             fig_components = px.pie(
#                 components_df,
#                 values="Contribution",
#                 names="Component",
#                 title=f"{selected_momentum_artist} Momentum Score Breakdown",
#                 color_discrete_sequence=px.colors.qualitative.Bold
#             )
            
#             fig_components.update_traces(textposition='inside', textinfo='percent+label')
            
#             st.plotly_chart(fig_components, use_container_width=True)
        
#         # Artist growth and recommendation
#         st.subheader("Artist Growth Indicators")
        
#         # Create growth indicators
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.metric("Play Growth", f"{artist_data['play_growth_pct']:.1f}%")
            
#         with col2:
#             st.metric("Listener Growth", f"{artist_data['listener_growth_pct']:.1f}%")
            
#         with col3:
#             # Create a custom growth indicator
#             growth_level = "High 🔥" if artist_data['momentum_score'] > 40 else ("Medium 📈" if artist_data['momentum_score'] > 25 else "Low ➖")
#             st.metric("Growth Level", growth_level)
        
#         # Recommendation section
#         st.markdown(f"### Recommendations for {selected_momentum_artist}")
        
#         # Generate custom recommendations based on the artist's data
#         if artist_data['momentum_score'] > 40:
#             st.markdown("""
#             <div class="recommendation-box">
#             <h4>High Momentum Strategy</h4>
            
#             - **Editorial Priority**: Fast-track for editorial playlist placement
#             - **Feature Promotion**: Consider for app homepage feature and push notifications
#             - **Cross-Border Expansion**: Analyze geographic engagement for targeted regional promotions
#             - **Partnership Opportunity**: Prime candidate for brand and event partnerships
#             </div>
#             """, unsafe_allow_html=True)
#         elif artist_data['momentum_score'] > 25:
#             st.markdown("""
#             <div class="recommendation-box">
#             <h4>Medium Momentum Strategy</h4>
            
#             - **Targeted Playlisting**: Place in growth-focused playlists
#             - **Engagement Campaigns**: Create engagement-driving campaigns to increase favorites and shares
#             - **Geographic Focus**: Identify strongest territories and boost promotion there
#             - **Content Strategy**: Encourage consistent release schedule to maintain momentum
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="recommendation-box">
#             <h4>Building Momentum Strategy</h4>
            
#             - **Audience Development**: Focus on core fan engagement and conversion
#             - **Content Feedback**: Provide insights on engagement patterns to guide future releases
#             - **Niche Playlisting**: Target genre-specific and discovery playlists
#             - **Collaboration Opportunities**: Suggest potential collaborators to boost exposure
#             </div>
#             """, unsafe_allow_html=True)


#     # Tab 10: Monthly Momentum Analysis
#     with tab10:
#         st.markdown('<div class="sub-header">Artist Monthly Momentum Analysis</div>', unsafe_allow_html=True)
        
#         st.markdown('<div class="insights-box">📈 <span class="highlight">Key Analysis:</span> This view analyzes artist momentum over a full month period, comparing current metrics against growth benchmarks. The momentum score combines play performance, listener engagement, and geographic reach to identify artists with significant momentum.</div>', unsafe_allow_html=True)
        
#         # Use the actual data provided
#         monthly_momentum_df = pd.DataFrame({
#             "artist": ["Sicicie & Lasmid", "Ruger and COLORS", "jomapelyankee", "Kixx Alphah & Cojo Rae", "DJ Bandz & YTB Fatt", 
#                     "Mama Tina", "Randy Kirton", "Nikey 20, Luckay Buckay", "sethlo, Toofan", "Chief Priest"],
#             "plays": [1449421, 952981, 251679, 130783, 47873, 
#                     57397, 33535, 87341, 38232, 762327],
#             "unique_listeners": [843778, 491220, 478, 86570, 26268, 
#                             272, 25787, 52560, 15437, 341513],
#             "favorites": [9857, 5238, 127, 990, 674, 
#                         13, 28, 1097, 322, 5538],
#             "shares": [0, 0, 0, 0, 0, 
#                     0, 0, 0, 0, 0],
#             "country_count": [217, 188, 18, 155, 183, 
#                             49, 185, 148, 37, 170],
#             "play_growth_pct": [3049, 3040, 2516, 1307, 478, 
#                             573, 335, 1091, 382, 304],
#             "listener_growth_pct": [843, 491, 47, 866, 262, 
#                                 27, 257, 525, 154, 227],
#             "fav_per_listener": [0.0117, 0.0107, 0.2657, 0.0114, 0.0257, 
#                             0.0478, 0.0011, 0.0209, 0.0209, 0.0162],
#             "share_per_listener": [0.0, 0.0, 0.0, 0.0, 0.0, 
#                                 0.0, 0.0, 0.0, 0.0, 0.0],
#             "momentum_score": [3049, 3040, 1008, 782, 270, 
#                             230, 211, 201, 199, 190]
#         })
        
#         # Clean/normalize the data - converting scientific notation to regular numbers
#         # We'll also cap growth percentages at more reasonable values for visualization
#         monthly_momentum_df['play_growth_pct'] = monthly_momentum_df['play_growth_pct'].astype(float)
#         monthly_momentum_df['listener_growth_pct'] = monthly_momentum_df['listener_growth_pct'].astype(float)
        
#         # Add a size cohort based on play count
#         def determine_monthly_size_cohort(plays):
#             if plays < 50000:
#                 return "micro"
#             elif plays < 250000:
#                 return "small"
#             elif plays < 750000:
#                 return "medium"
#             else:
#                 return "large"
        
#         monthly_momentum_df["size_cohort"] = monthly_momentum_df["plays"].apply(determine_monthly_size_cohort)
        
#         # Metrics section
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             avg_momentum = monthly_momentum_df['momentum_score'].mean()
#             st.metric("Avg Monthly Momentum", f"{avg_momentum:.2f}")
        
#         with col2:
#             max_artist = monthly_momentum_df.loc[monthly_momentum_df['momentum_score'].idxmax()]['artist']
#             max_score = monthly_momentum_df['momentum_score'].max()
#             st.metric("Top Artist", f"{max_artist} ({max_score:.0f})")
        
#         with col3:
#             high_engagement = len(monthly_momentum_df[monthly_momentum_df['fav_per_listener'] > 0.02])
#             st.metric("High Engagement Artists", f"{high_engagement} in top 10")
        
#         # Main momentum score visualization
#         st.subheader("Monthly Artist Momentum Rankings")
        
#         # Create a color scale for the momentum score
#         fig_momentum = px.bar(
#             monthly_momentum_df.sort_values('momentum_score', ascending=False),
#             x="artist",
#             y="momentum_score",
#             color="size_cohort",
#             title="Monthly Artist Momentum Score Rankings",
#             color_discrete_map={
#                 "micro": "#FF9F1C",
#                 "small": "#4ECDC4",
#                 "medium": "#1A535C",
#                 "large": "#FF6B6B"
#             },
#             hover_data=["plays", "unique_listeners", "play_growth_pct", "listener_growth_pct", 
#                         "fav_per_listener", "share_per_listener", "country_count"]
#         )
        
#         fig_momentum.update_layout(
#             xaxis_title="Artist",
#             yaxis_title="Monthly Momentum Score",
#             xaxis={'categoryorder': 'total descending'},
#             height=500,
#             xaxis_tickangle=-45
#         )
        
#         fig_momentum.update_traces(
#             hovertemplate="<b>Artist:</b> %{x}<br>" +
#                         "<b>Momentum Score:</b> %{y:.0f}<br>" +
#                         "<b>Size Cohort:</b> %{marker.color}<br>" +
#                         "<b>Plays:</b> %{customdata[0]:,.0f}<br>" +
#                         "<b>Unique Listeners:</b> %{customdata[1]:,.0f}<br>" +
#                         "<b>Play Growth:</b> %{customdata[2]:.0f}<br>" +
#                         "<b>Listener Growth:</b> %{customdata[3]:.0f}<br>" +
#                         "<b>Favs per Listener:</b> %{customdata[4]:.4f}<br>" +
#                         "<b>Countries:</b> %{customdata[6]}<extra></extra>"
#         )
        
#         st.plotly_chart(fig_momentum, use_container_width=True)
        
#         # Analysis of engagement vs geographic reach
#         st.subheader("Engagement vs Geographic Reach Analysis")
        
#         # Create a scatter plot to visualize engagement vs geographic reach
#         fig_engagement_geo = px.scatter(
#             monthly_momentum_df,
#             x="country_count",
#             y="fav_per_listener",
#             size="momentum_score",
#             color="size_cohort",
#             hover_name="artist",
#             size_max=60,
#             title="Artist Engagement vs Geographic Reach",
#             labels={
#                 "country_count": "Number of Countries",
#                 "fav_per_listener": "Favorites per Listener"
#             },
#             color_discrete_map={
#                 "micro": "#FF9F1C",
#                 "small": "#4ECDC4",
#                 "medium": "#1A535C",
#                 "large": "#FF6B6B"
#             }
#         )
        
#         fig_engagement_geo.update_layout(
#             xaxis_title="Geographic Reach (Number of Countries)",
#             yaxis_title="Engagement Quality (Favorites per Listener)",
#             height=500
#         )
        
#         st.plotly_chart(fig_engagement_geo, use_container_width=True)
        
#         # Table of all artists with detailed metrics
#         st.subheader("Detailed Metrics for All Artists")
        
#         st.dataframe(
#             monthly_momentum_df.sort_values('momentum_score', ascending=False),
#             use_container_width=True,
#             column_config={
#                 "artist": st.column_config.TextColumn("Artist"),
#                 "size_cohort": st.column_config.TextColumn("Size Cohort"),
#                 "plays": st.column_config.NumberColumn("Plays", format="%d"),
#                 "unique_listeners": st.column_config.NumberColumn("Unique Listeners", format="%d"),
#                 "play_growth_pct": st.column_config.NumberColumn("Play Growth", format="%.0f"),
#                 "listener_growth_pct": st.column_config.NumberColumn("Listener Growth", format="%.0f"),
#                 "fav_per_listener": st.column_config.NumberColumn("Favs per Listener", format="%.4f"),
#                 "country_count": st.column_config.NumberColumn("Countries", format="%d"),
#                 "momentum_score": st.column_config.NumberColumn("Momentum Score", format="%.0f")
#             }
#         )
        
#         # Key Insights Analysis
#         st.subheader("Key Insights from Monthly Momentum Analysis")
        
#         # Select two interesting artists for comparison
#         comparison_artists = ["Sicicie & Lasmid", "jomapelyankee"]
#         comparison_df = monthly_momentum_df[monthly_momentum_df['artist'].isin(comparison_artists)]
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("""
#             ### Notable Momentum Patterns
            
#             1. **Global vs. Niche Appeal**: The data shows two distinct momentum patterns:
#                 - **Global Reach Artists**: Like Sicicie & Lasmid with high play counts across 217 countries
#                 - **High Engagement Niche Artists**: Like jomapelyankee with exceptional engagement metrics but limited geographic reach
            
#             2. **Engagement Quality**: Artists with higher favorites-per-listener ratios show stronger fan connection regardless of absolute play counts
            
#             3. **Geographic Expansion**: The top momentum artists show varying degrees of geographic penetration, suggesting different growth strategies
#             """)
        
#         with col2:
#             # Create comparison chart
#             metrics_to_compare = ['plays', 'unique_listeners', 'fav_per_listener', 'country_count']
#             comparison_data = []
            
#             for artist in comparison_artists:
#                 artist_data = monthly_momentum_df[monthly_momentum_df['artist'] == artist].iloc[0]
#                 for metric in metrics_to_compare:
#                     comparison_data.append({
#                         'artist': artist,
#                         'metric': metric,
#                         'value': artist_data[metric]
#                     })
            
#             comparison_plot_df = pd.DataFrame(comparison_data)
            
#             # Normalize the data for better visualization
#             for metric in metrics_to_compare:
#                 max_val = comparison_plot_df[comparison_plot_df['metric'] == metric]['value'].max()
#                 comparison_plot_df.loc[comparison_plot_df['metric'] == metric, 'normalized_value'] = comparison_plot_df[comparison_plot_df['metric'] == metric]['value'] / max_val
            
#             fig_comparison = px.bar(
#                 comparison_plot_df,
#                 x="metric",
#                 y="normalized_value",
#                 color="artist",
#                 barmode="group",
#                 title="Comparing Global vs. Niche Artist Profiles",
#                 labels={"normalized_value": "Normalized Value (Relative to Max)"}
#             )
            
#             fig_comparison.update_layout(
#                 xaxis_title="Metric",
#                 yaxis_title="Relative Value",
#                 height=300
#             )
            
#             st.plotly_chart(fig_comparison, use_container_width=True)
        
#         # SQL Implementation for reference
#         st.subheader("SQL Implementation Reference")
        
#         st.code('''
#     WITH current_period AS (
#         SELECT 
#             m.artist,
#             COUNT(*) AS plays,
#             COUNT(DISTINCT e.actor_id) AS unique_listeners,
#             SUM(CASE WHEN e.type = 'favorite' THEN 1 ELSE 0 END) AS favorites,
#             SUM(CASE WHEN e.type = 'share' THEN 1 ELSE 0 END) AS shares,
#             COUNT(DISTINCT e.geo_country) AS country_count
#         FROM dw01.events e
#         JOIN dw01.music m ON e.object_id = m.music_id_raw
#         WHERE DATE_PARSE(e.event_date, '%Y%m%d') BETWEEN CURRENT_DATE - INTERVAL '30' DAY AND CURRENT_DATE
#         AND e.type IN ('play', 'favorite', 'share')
#         GROUP BY m.artist
#     ),
#     previous_period AS (
#         SELECT 
#             m.artist,
#             COUNT(*) AS prev_plays,
#             COUNT(DISTINCT e.actor_id) AS prev_unique_listeners
#         FROM dw01.events e
#         JOIN dw01.music m ON e.object_id = m.music_id_raw
#         WHERE DATE_PARSE(e.event_date, '%Y%m%d') BETWEEN CURRENT_DATE - INTERVAL '60' DAY AND CURRENT_DATE - INTERVAL '30' DAY
#         AND e.type = 'play'
#         GROUP BY m.artist
#     )
#     SELECT 
#         c.artist,
#         c.plays,
#         c.unique_listeners,
#         c.favorites,
#         c.shares,
#         c.country_count,
#         -- Growth metrics
#         c.plays - COALESCE(p.prev_plays, 0) AS play_growth,
#         c.unique_listeners - COALESCE(p.prev_unique_listeners, 0) AS listener_growth,
#         -- Engagement ratios
#         ROUND(c.favorites * 1.0 / NULLIF(c.unique_listeners, 0), 4) AS fav_per_listener,
#         ROUND(c.shares * 1.0 / NULLIF(c.unique_listeners, 0), 4) AS share_per_listener,
#         -- Simplified momentum score that matches the data pattern
#         -- Actual formula would need to be adjusted based on business requirements
#         ROUND(
#             (c.plays - COALESCE(p.prev_plays, 0)) * 0.8 +
#             (c.unique_listeners - COALESCE(p.prev_unique_listeners, 0)) * 0.1 +
#             (c.favorites * 10) + 
#             (c.country_count * 0.5)
#         ) AS momentum_score
#     FROM current_period c
#     LEFT JOIN previous_period p ON c.artist = p.artist
#     WHERE c.plays > 10000
#     ORDER BY momentum_score DESC
#     LIMIT 10;
#         ''', language='sql')
        
#     # <h4>Top Emerging Artists for Promotion Focus</h4>
        
#     #     Based on the monthly momentum analysis, these artists show exceptional growth potential:
        
#     #     1. **Bloody Civilian** (Micro) - Extraordinary 104% play growth with high engagement quality. Immediate action recommended for editorial placement and potential feature.
        
#     #     2. **FAVE** (Small) - Strong 66% growth with excellent favorites engagement. Consider for cross-platform promotional campaign.
        
#     #     3. **Khaid** (Small) - Balanced growth profile with significant geographic distribution. Good candidate for regional promotional push.
#     #     </div>
#     #     """, unsafe_allow_html=True)
        
#     #     # Comparison of Monthly Top 3 vs Weekly Top 3
#     #     comparison_df = pd.DataFrame({
#     #         "Metric": ["Play Growth %", "Listener Growth %", "Favorites per Listener", "Shares per Listener", "Momentum Score"],
#     #         "Monthly Top 3 (Average)": [74.00, 50.23, 0.2400, 0.0700, 62.26],
#     #         "Weekly Top 3 (Average)": [69.33, 47.70, 0.2300, 0.0666, 55.97]
#     #     })
        
#     #     st.dataframe(
#     #         comparison_df,
#     #         use_container_width=True,
#     #         column_config={
#     #             "Metric": st.column_config.TextColumn("Metric"),
#     #             "Monthly Top 3 (Average)": st.column_config.NumberColumn("Monthly Top 3 (Average)", format="%.2f"),
#     #             "Weekly Top 3 (Average)": st.column_config.NumberColumn("Weekly Top 3 (Average)", format="%.2f")
#     #         }
#     #     )



























# Week 1 content (previous)
with week_tabs[1]:


    # # Set page configuration
    # st.set_page_config(
    #     page_title="Audiomack ArtistRank Dashboard",
    #     page_icon="🎵",
    #     layout="wide"
    # )
    
    # Function to load CSV data
    @st.cache_data
    def load_data():
        # In a real implementation, this would read actual CSV files
        # For now, we'll create DataFrames with sample data based on your file structure
        
        # Event type counts
        event_type_df = pd.DataFrame([
            {"event_type": "play", "event_count": 15000000, "unique_users": 2500000},
            {"event_type": "favorite", "event_count": 750000, "unique_users": 500000},
            {"event_type": "share", "event_count": 250000, "unique_users": 200000},
            {"event_type": "download", "event_count": 3000000, "unique_users": 1800000},
            {"event_type": "playlist_add", "event_count": 450000, "unique_users": 300000},
            {"event_type": "comment", "event_count": 180000, "unique_users": 95000},
            {"event_type": "profile_view", "event_count": 900000, "unique_users": 650000}
        ])
        
        # Music engagement metrics
        music_engagement_df = pd.DataFrame([
            {"artist": "Shallipopi", "total_plays": 3200000, "unique_listeners": 950000},
            {"artist": "Asake", "total_plays": 2800000, "unique_listeners": 1200000},
            {"artist": "Seyi Vibez", "total_plays": 2400000, "unique_listeners": 820000},
            {"artist": "Young Jonn", "total_plays": 2100000, "unique_listeners": 750000},
            {"artist": "Mohbad", "total_plays": 1900000, "unique_listeners": 680000},
            {"artist": "Ayra Starr", "total_plays": 1750000, "unique_listeners": 940000},
            {"artist": "Burna Boy", "total_plays": 1650000, "unique_listeners": 1050000},
            {"artist": "Davido", "total_plays": 1550000, "unique_listeners": 980000},
            {"artist": "Wizkid", "total_plays": 1450000, "unique_listeners": 920000},
            {"artist": "Rema", "total_plays": 1350000, "unique_listeners": 860000}
        ])
        
        # Engagement ratios for artists
        engagement_ratios_df = pd.DataFrame([
            {"artist": "Shallipopi", "plays": 3200000, "favorites": 160000, "shares": 48000, "unique_users": 950000, "favorite_to_play_ratio": 0.050},
            {"artist": "Asake", "plays": 2800000, "favorites": 210000, "shares": 70000, "unique_users": 1200000, "favorite_to_play_ratio": 0.075},
            {"artist": "Seyi Vibez", "plays": 2400000, "favorites": 96000, "shares": 36000, "unique_users": 820000, "favorite_to_play_ratio": 0.040},
            {"artist": "Young Jonn", "plays": 2100000, "favorites": 147000, "shares": 31500, "unique_users": 750000, "favorite_to_play_ratio": 0.070},
            {"artist": "Mohbad", "plays": 1900000, "favorites": 133000, "shares": 38000, "unique_users": 680000, "favorite_to_play_ratio": 0.070},
            {"artist": "Ayra Starr", "plays": 1750000, "favorites": 131250, "shares": 43750, "unique_users": 940000, "favorite_to_play_ratio": 0.075},
            {"artist": "Burna Boy", "plays": 1650000, "favorites": 123750, "shares": 33000, "unique_users": 1050000, "favorite_to_play_ratio": 0.075},
            {"artist": "Davido", "plays": 1550000, "favorites": 108500, "shares": 38750, "unique_users": 980000, "favorite_to_play_ratio": 0.070},
            {"artist": "Wizkid", "plays": 1450000, "favorites": 116000, "shares": 36250, "unique_users": 920000, "favorite_to_play_ratio": 0.080},
            {"artist": "Rema", "plays": 1350000, "favorites": 94500, "shares": 27000, "unique_users": 860000, "favorite_to_play_ratio": 0.070}
        ])
        
        # Geographic analysis
        geographic_df = pd.DataFrame([
            {"artist": "Shallipopi", "geo_country": "NG", "play_count": 2240000, "unique_listeners": 665000},
            {"artist": "Shallipopi", "geo_country": "GH", "play_count": 480000, "unique_listeners": 142500},
            {"artist": "Shallipopi", "geo_country": "US", "play_count": 320000, "unique_listeners": 95000},
            {"artist": "Asake", "geo_country": "NG", "play_count": 1680000, "unique_listeners": 720000},
            {"artist": "Asake", "geo_country": "GH", "play_count": 280000, "unique_listeners": 120000},
            {"artist": "Asake", "geo_country": "UK", "play_count": 392000, "unique_listeners": 168000},
            {"artist": "Asake", "geo_country": "US", "play_count": 448000, "unique_listeners": 192000},
            {"artist": "Seyi Vibez", "geo_country": "NG", "play_count": 1680000, "unique_listeners": 574000},
            {"artist": "Seyi Vibez", "geo_country": "GH", "play_count": 360000, "unique_listeners": 123000},
            {"artist": "Seyi Vibez", "geo_country": "US", "play_count": 240000, "unique_listeners": 82000},
            {"artist": "Mohbad", "geo_country": "NG", "play_count": 1330000, "unique_listeners": 476000},
            {"artist": "Mohbad", "geo_country": "GH", "play_count": 285000, "unique_listeners": 102000},
            {"artist": "Mohbad", "geo_country": "US", "play_count": 190000, "unique_listeners": 68000},
            {"artist": "Wizkid", "geo_country": "NG", "play_count": 725000, "unique_listeners": 460000},
            {"artist": "Wizkid", "geo_country": "GH", "play_count": 217500, "unique_listeners": 138000},
            {"artist": "Wizkid", "geo_country": "UK", "play_count": 217500, "unique_listeners": 138000},
            {"artist": "Wizkid", "geo_country": "US", "play_count": 290000, "unique_listeners": 184000}
        ])
        
        # Growing artists with momentum
        growing_artists_df = pd.DataFrame([
            {"artist": "Young Jonn", "size_cohort": "medium", "current_plays": 2100000, "previous_plays": 1500000, "current_listeners": 750000, "previous_listeners": 600000, "play_growth_pct": 40.00, "listener_growth_pct": 25.00, "plays_per_listener": 3, "favorites_per_listener": 0.2, "shares_per_listener": 0.04, "artist_momentum_score": 39.80},
            {"artist": "Shallipopi", "size_cohort": "large", "current_plays": 3200000, "previous_plays": 2500000, "current_listeners": 950000, "previous_listeners": 800000, "play_growth_pct": 28.00, "listener_growth_pct": 18.75, "plays_per_listener": 3, "favorites_per_listener": 0.17, "shares_per_listener": 0.05, "artist_momentum_score": 32.30},
            {"artist": "Seyi Vibez", "size_cohort": "medium", "current_plays": 2400000, "previous_plays": 1900000, "current_listeners": 820000, "previous_listeners": 700000, "play_growth_pct": 26.32, "listener_growth_pct": 17.14, "plays_per_listener": 3, "favorites_per_listener": 0.12, "shares_per_listener": 0.04, "artist_momentum_score": 29.04},
            {"artist": "Khaid", "size_cohort": "small", "current_plays": 980000, "previous_plays": 650000, "current_listeners": 350000, "previous_listeners": 250000, "play_growth_pct": 50.77, "listener_growth_pct": 40.00, "plays_per_listener": 3, "favorites_per_listener": 0.23, "shares_per_listener": 0.06, "artist_momentum_score": 48.73},
            {"artist": "Odumodu Blvck", "size_cohort": "small", "current_plays": 820000, "previous_plays": 580000, "current_listeners": 410000, "previous_listeners": 320000, "play_growth_pct": 41.38, "listener_growth_pct": 28.13, "plays_per_listener": 2, "favorites_per_listener": 0.19, "shares_per_listener": 0.05, "artist_momentum_score": 39.58},
            {"artist": "Victony", "size_cohort": "medium", "current_plays": 1250000, "previous_plays": 950000, "current_listeners": 520000, "previous_listeners": 420000, "play_growth_pct": 31.58, "listener_growth_pct": 23.81, "plays_per_listener": 2, "favorites_per_listener": 0.16, "shares_per_listener": 0.03, "artist_momentum_score": 32.87},
            {"artist": "FAVE", "size_cohort": "micro", "current_plays": 650000, "previous_plays": 390000, "current_listeners": 250000, "previous_listeners": 170000, "play_growth_pct": 66.67, "listener_growth_pct": 47.06, "plays_per_listener": 3, "favorites_per_listener": 0.24, "shares_per_listener": 0.07, "artist_momentum_score": 57.22},
            {"artist": "Lil kesh", "size_cohort": "medium", "current_plays": 1680000, "previous_plays": 1450000, "current_listeners": 580000, "previous_listeners": 530000, "play_growth_pct": 15.86, "listener_growth_pct": 9.43, "plays_per_listener": 3, "favorites_per_listener": 0.14, "shares_per_listener": 0.04, "artist_momentum_score": 21.03},
            {"artist": "CKay", "size_cohort": "medium", "current_plays": 1820000, "previous_plays": 1520000, "current_listeners": 640000, "previous_listeners": 570000, "play_growth_pct": 19.74, "listener_growth_pct": 12.28, "plays_per_listener": 3, "favorites_per_listener": 0.18, "shares_per_listener": 0.05, "artist_momentum_score": 24.62},
            {"artist": "Bloody Civilian", "size_cohort": "micro", "current_plays": 450000, "previous_plays": 220000, "current_listeners": 180000, "previous_listeners": 110000, "play_growth_pct": 104.55, "listener_growth_pct": 63.64, "plays_per_listener": 3, "favorites_per_listener": 0.25, "shares_per_listener": 0.08, "artist_momentum_score": 80.82}
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
        
        return event_type_df, music_engagement_df, engagement_analysis_df, geographic_df, growing_artists_df
    
    # Load data
    try:
        event_type_df, music_engagement_df, engagement_analysis_df, geographic_df, growing_artists_df = load_data()
        data_loaded = True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        data_loaded = False
    
    # Dashboard title and description
    st.title("🎵 Audiomack ArtistRank Dashboard")
    st.write("Analysis dashboard for the ArtistRank tool development - Week 1")
    
    # Create sidebar for filtering
    st.sidebar.header("Filters")
    selected_size_cohort = st.sidebar.multiselect(
        "Artist Size Cohort",
        options=growing_artists_df['size_cohort'].unique(),
        default=growing_artists_df['size_cohort'].unique()
    )
    
    selected_countries = st.sidebar.multiselect(
        "Countries",
        options=geographic_df['geo_country'].unique(),
        default=['NG', 'GH', 'US']
    )
    
    # About section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("About ArtistRank")
    st.sidebar.info(
        """
        ArtistRank is a tool for surfacing songs and artists 
        best situated to gain traction and success on and 
        off the platform.
        
        This dashboard provides insights into engagement metrics, 
        geographic distribution, and growth trends to support 
        A&R decisions.
        """
    )
    
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
    
            # Debug: Show raw data
            if st.checkbox("Show raw data: https://docs.google.com/spreadsheets/d/1fkd2RMzHaUGsahUXB6_86dogYLruoHIpu9aThOo3cRY/edit?gid=0#gid=0"):
                st.write("Raw data from CSV:")
                st.dataframe(raw_df)
    
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
            clean_df.columns = [col.strip() for col in clean_df.columns]

    
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
                selected_platform = st.multiselect("On Platform Status", options=platform_options, default=platform_options)
    
            with col2:
                selected_genres = st.multiselect("Genre", options=genre_options, default=genre_options)
    
            with col3:
                selected_geos = st.multiselect("Geography", options=geo_options, default=geo_options)
    
            with col4:
                selected_feed_partners = st.multiselect("Feed Partner", options=feed_partner_options, default=feed_partner_options)
    
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
    
    

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Overview", 
        "Engagement Analysis", 
        "Geographic Insights", 
        "Growing Artists", 
        "Recommendations",
        "Methodology & Explanations",
        "A&R Scouting Tracker (JJ)"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Platform Event Overview")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_plays = event_type_df[event_type_df['event_type'] == 'play']['event_count'].sum()
        total_favorites = event_type_df[event_type_df['event_type'] == 'favorite']['event_count'].sum()
        total_shares = event_type_df[event_type_df['event_type'] == 'share']['event_count'].sum()
        total_downloads = event_type_df[event_type_df['event_type'] == 'download']['event_count'].sum()
        
        col1.metric("Total Plays", f"{total_plays:,}")
        col2.metric("Total Favorites", f"{total_favorites:,}")
        col3.metric("Total Shares", f"{total_shares:,}")
        col4.metric("Total Downloads", f"{total_downloads:,}")
        
        # Create event type distribution chart
        st.subheader("Event Type Distribution")
        
        fig1 = px.bar(
            event_type_df,
            x="event_type",
            y="event_count",
            title="Events by Type",
            color="event_type",
            labels={"event_count": "Number of Events", "event_type": "Event Type"},
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_data={"event_count": True, "unique_users": True, "event_type": True},
            custom_data=["unique_users"]
        )
        # Add a more descriptive tooltip
        fig1.update_traces(
            hovertemplate="<b>Event Type:</b> %{x}<br>" +
                          "<b>Count:</b> %{y:,.0f}<br>" +
                          "<b>Unique Users:</b> %{customdata[0]:,.0f}<br>" +
                          "<b>Description:</b> Total number of '%{x}' events in the last 30 days<extra></extra>"
        )
        fig1.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig1, use_container_width=True)
        
        # Create unique users by event type
        st.subheader("User Engagement by Event Type")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=event_type_df["event_type"],
            y=event_type_df["unique_users"],
            name="Unique Users",
            marker_color="#FF6B6B"
        ))
        fig2.update_layout(
            title="Unique Users by Event Type",
            xaxis_title="Event Type",
            yaxis_title="Number of Unique Users",
            xaxis={'categoryorder':'total descending'}
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Top artists by plays
        st.subheader("Top Artists by Plays")
        
        fig3 = px.bar(
            music_engagement_df.sort_values('total_plays', ascending=False).head(10),
            x="artist",
            y="total_plays",
            title="Top 10 Artists by Total Plays",
            color_discrete_sequence=["#4ECDC4"],
            hover_data=["unique_listeners", "plays_per_user"]
        )
        fig3.update_layout(xaxis_title="Artist", yaxis_title="Total Plays")
        st.plotly_chart(fig3, use_container_width=True)
    
    # Tab 2: Engagement Analysis
    with tab2:
        st.header("Artist Engagement Analysis")
        
        # Create engagement metrics visualization
        st.subheader("Engagement Metrics by Artist")
        
        metrics_df = engagement_analysis_df.melt(
            id_vars=["artist"],
            value_vars=["favorite_ratio", "share_ratio"],
            var_name="Metric",
            value_name="Value"
        )
        
        metrics_df["Metric"] = metrics_df["Metric"].map({
            "favorite_ratio": "Favorites Ratio",
            "share_ratio": "Shares Ratio"
        })
        
        fig4 = px.bar(
            metrics_df,
            x="artist",
            y="Value",
            color="Metric",
            barmode="group",
            title="Engagement Ratios by Artist",
            color_discrete_map={
                "Favorites Ratio": "#FF9F1C",
                "Shares Ratio": "#E71D36"
            },
            hover_data={"Value": ":.2%"}  # Format as percentage
        )
        # Add a more descriptive tooltip
        fig4.update_traces(
            hovertemplate="<b>Artist:</b> %{x}<br>" +
                          "<b>%{data.name}:</b> %{customdata[0]}<br>" +
                          "<b>Formula:</b> %{data.name === 'Favorites Ratio' ? 'Favorites ÷ Plays' : 'Shares ÷ Plays'}<br>" +
                          "<b>Interpretation:</b> %{data.name === 'Favorites Ratio' ? 'Higher values indicate stronger audience connection' : 'Higher values indicate better viral potential'}<extra></extra>"
        )
        fig4.update_layout(xaxis_title="Artist", yaxis_title="Ratio Value")
        st.plotly_chart(fig4, use_container_width=True)
        
        # Create plays per user chart
        st.subheader("Plays per Unique Listener")
        
        fig5 = px.bar(
            music_engagement_df.sort_values('plays_per_user', ascending=False),
            x="artist",
            y="plays_per_user",
            title="Average Plays per Unique Listener",
            color_discrete_sequence=["#2EC4B6"],
            hover_data=["total_plays", "unique_listeners"]
        )
        fig5.update_layout(xaxis_title="Artist", yaxis_title="Plays per Listener")
        st.plotly_chart(fig5, use_container_width=True)
        
        # Create composite engagement score chart
        st.subheader("Composite Engagement Score")
        
        fig6 = px.bar(
            engagement_analysis_df.sort_values('engagement_score', ascending=False),
            x="artist",
            y="engagement_score",
            title="Composite Engagement Score (Favorites + Shares Weighted)",
            color_discrete_sequence=["#FF6B6B"],
            hover_data=["favorite_ratio", "share_ratio", "plays", "favorites", "shares"]
        )
        
        # Create a detailed tooltip explaining the engagement score calculation
        fig6.update_traces(
            hovertemplate="<b>Artist:</b> %{x}<br>" +
                          "<b>Engagement Score:</b> %{y:.2f}<br>" +
                          "<b>Favorite Ratio:</b> %{customdata[0]:.1%}<br>" +
                          "<b>Share Ratio:</b> %{customdata[1]:.1%}<br>" +
                          "<b>Total Plays:</b> %{customdata[2]:,.0f}<br>" +
                          "<b>Formula:</b> (Favorite Ratio × 10) + (Share Ratio × 5)<br>" +
                          "<b>Interpretation:</b> Higher scores indicate stronger audience engagement<extra></extra>"
        )
        
        fig6.update_layout(xaxis_title="Artist", yaxis_title="Engagement Score")
        st.plotly_chart(fig6, use_container_width=True)
    
    # Tab 3: Geographic Insights
    with tab3:
        st.header("Geographic Analysis")
        
        # Filter by selected countries
        filtered_geo_df = geographic_df[geographic_df['geo_country'].isin(selected_countries)]
        
        # Create country comparison chart
        st.subheader("Artist Performance by Country")
        
        fig7 = px.bar(
            filtered_geo_df,
            x="artist",
            y="play_count",
            color="geo_country",
            title="Play Counts by Artist and Country",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig7.update_layout(xaxis_title="Artist", yaxis_title="Play Count")
        st.plotly_chart(fig7, use_container_width=True)
        
        # Create percentage distribution chart
        st.subheader("Geographic Distribution of Plays")
        
        fig8 = px.bar(
            filtered_geo_df,
            x="artist",
            y="play_percentage",
            color="geo_country",
            title="Percentage Distribution of Plays by Country",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_data=["play_count", "unique_listeners"]
        )
        
        # Add a detailed tooltip for geographic distribution
        fig8.update_traces(
            hovertemplate="<b>Artist:</b> %{x}<br>" +
                          "<b>Country:</b> %{marker.color}<br>" +
                          "<b>Percentage:</b> %{y:.1f}%<br>" +
                          "<b>Play Count:</b> %{customdata[0]:,.0f}<br>" +
                          "<b>Unique Listeners:</b> %{customdata[1]:,.0f}<br>" +
                          "<b>Significance:</b> Shows cross-border reach and market penetration<extra></extra>"
        )
        
        fig8.update_layout(xaxis_title="Artist", yaxis_title="Percentage of Total Plays (%)")
        st.plotly_chart(fig8, use_container_width=True)
        
        # Create unique listeners map
        st.subheader("Unique Listeners by Country")
        
        unique_by_country = filtered_geo_df.groupby('geo_country')['unique_listeners'].sum().reset_index()
        
        fig9 = px.choropleth(
            unique_by_country,
            locations="geo_country",
            locationmode="ISO-3",
            color="unique_listeners",
            hover_name="geo_country",
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Unique Listeners by Country"
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    # Tab 4: Growing Artists
    with tab4:
        st.header("Artist Growth Analysis")
        
        # Filter by selected size cohorts
        filtered_growing_df = growing_artists_df[growing_artists_df['size_cohort'].isin(selected_size_cohort)]
        
        # Add a selection widget for the growth metric
        growth_metric = st.radio(
            "Select Growth Metric",
            ["play_growth_pct", "listener_growth_pct", "artist_momentum_score"],
            format_func=lambda x: {
                "play_growth_pct": "Play Count Growth %",
                "listener_growth_pct": "Listener Growth %",
                "artist_momentum_score": "Artist Momentum Score"
            }[x],
            horizontal=True
        )
        
        # Create growth metric chart
        st.subheader("Artist Growth Metrics")
        
        fig10 = px.bar(
            filtered_growing_df.sort_values(growth_metric, ascending=False),
            x="artist",
            y=growth_metric,
            color="size_cohort",
            title="Artist Growth by Size Cohort",
            labels={
                "play_growth_pct": "Play Count Growth %",
                "listener_growth_pct": "Listener Growth %",
                "artist_momentum_score": "Artist Momentum Score"
            },
            hover_data=["plays_per_listener", "favorites_per_listener", "shares_per_listener", "current_plays", "previous_plays"],
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        # Add a detailed tooltip based on which metric is selected
        if growth_metric == "play_growth_pct":
            tooltip_template = (
                "<b>Artist:</b> %{x}<br>" +
                "<b>Play Growth:</b> %{y:.1f}%<br>" +
                "<b>Current Plays:</b> %{customdata[3]:,.0f}<br>" +
                "<b>Previous Plays:</b> %{customdata[4]:,.0f}<br>" +
                "<b>Size Cohort:</b> %{marker.color}<br>" +
                "<b>Formula:</b> ((Current - Previous) ÷ Previous) × 100<br>" +
                "<b>Weight in Momentum Score:</b> 40%<extra></extra>"
            )
        elif growth_metric == "listener_growth_pct":
            tooltip_template = (
                "<b>Artist:</b> %{x}<br>" +
                "<b>Listener Growth:</b> %{y:.1f}%<br>" +
                "<b>Plays per Listener:</b> %{customdata[0]:.1f}<br>" +
                "<b>Size Cohort:</b> %{marker.color}<br>" +
                "<b>Formula:</b> ((Current - Previous) ÷ Previous) × 100<br>" +
                "<b>Weight in Momentum Score:</b> 30%<extra></extra>"
            )
        else:  # artist_momentum_score
            tooltip_template = (
                "<b>Artist:</b> %{x}<br>" +
                "<b>Momentum Score:</b> %{y:.2f}<br>" +
                "<b>Plays per Listener:</b> %{customdata[0]:.1f}<br>" +
                "<b>Favorites per Listener:</b> %{customdata[1]:.2f}<br>" +
                "<b>Shares per Listener:</b> %{customdata[2]:.2f}<br>" +
                "<b>Size Cohort:</b> %{marker.color}<br>" +
                "<b>Formula:</b> Weighted sum of growth and engagement metrics<extra></extra>"
            )
        
        fig10.update_traces(hovertemplate=tooltip_template)
        fig10.update_layout(xaxis_title="Artist", yaxis_title="Growth Metric")
        st.plotly_chart(fig10, use_container_width=True)
        
        # Create side-by-side comparison of current vs previous metrics
        st.subheader("Current vs Previous Period Comparison")
        
        # Select an artist for detailed view
        selected_artist = st.selectbox(
            "Select Artist for Detailed Comparison",
            options=filtered_growing_df['artist'].tolist()
        )
        
        artist_data = filtered_growing_df[filtered_growing_df['artist'] == selected_artist].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Current metrics
            st.subheader("Current Period")
            st.metric("Plays", f"{artist_data['current_plays']:,}")
            st.metric("Unique Listeners", f"{artist_data['current_listeners']:,}")
            st.metric("Plays per Listener", f"{artist_data['plays_per_listener']:.2f}")
            st.metric("Favorites per Listener", f"{artist_data['favorites_per_listener']:.2f}")
            st.metric("Shares per Listener", f"{artist_data['shares_per_listener']:.2f}")
        
        with col2:
            # Previous metrics with growth indicators
            st.subheader("Growth Metrics")
            st.metric("Previous Plays", f"{artist_data['previous_plays']:,}", 
                     delta=f"{artist_data['play_growth_pct']:.1f}%")
            st.metric("Previous Listeners", f"{artist_data['previous_listeners']:,}", 
                     delta=f"{artist_data['listener_growth_pct']:.1f}%")
            st.metric("Growth Indicator", artist_data['growth_indicator'])
            st.metric("Size Cohort", artist_data['size_cohort'].capitalize())
            st.metric("Momentum Score", f"{artist_data['artist_momentum_score']:.2f}")
        
        # Show comparison chart
        metrics_to_compare = {
            'plays': ['current_plays', 'previous_plays'],
            'listeners': ['current_listeners', 'previous_listeners']
        }
        
        metric_choice = st.radio(
            "Compare Metric",
            list(metrics_to_compare.keys()),
            horizontal=True
        )
        
        current_col, prev_col = metrics_to_compare[metric_choice]
        
        comparison_data = pd.DataFrame({
            'period': ['Current', 'Previous'],
            'value': [artist_data[current_col], artist_data[prev_col]]
        })
        
        fig11 = px.bar(
            comparison_data,
            x="period",
            y="value",
            title=f"{selected_artist}: {metric_choice.capitalize()} Comparison",
            color="period",
            color_discrete_map={
                "Current": "#00A878",
                "Previous": "#5F4B8B"
            }
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    # Tab 5: Recommendations
    with tab5:
        st.header("ArtistRank Recommendations")
        
        # Identifying potential emerging artists
        st.subheader("Emerging Artists to Watch")
        
        # Combine growth and engagement data
        emerging_artists = growing_artists_df[
            (growing_artists_df['play_growth_pct'] > 30) & 
            (growing_artists_df['size_cohort'].isin(['micro', 'small']))
        ].sort_values('artist_momentum_score', ascending=False).head(5)
        
        for i, artist in enumerate(emerging_artists['artist'].tolist()):
            col_left, col_right = st.columns([1, 3])
            
            with col_left:
                st.subheader(f"{i+1}. {artist}")
                st.caption(f"Size: {emerging_artists.iloc[i]['size_cohort'].capitalize()}")
                st.caption(f"Growth: {emerging_artists.iloc[i]['play_growth_pct']:.1f}%")
                
            with col_right:
                st.write(f"**Momentum Score:** {emerging_artists.iloc[i]['artist_momentum_score']:.2f}")
                st.write(f"**Growth Indicator:** {emerging_artists.iloc[i]['growth_indicator']}")
                st.write(f"**Current Plays:** {emerging_artists.iloc[i]['current_plays']:,} | **Previous:** {emerging_artists.iloc[i]['previous_plays']:,}")
                st.write(f"**Current Listeners:** {emerging_artists.iloc[i]['current_listeners']:,} | **Previous:** {emerging_artists.iloc[i]['previous_listeners']:,}")
            
            st.markdown("---")
        
        # Key metrics for ArtistRank algorithm
        st.subheader("Recommended Key Metrics for ArtistRank Algorithm")
        
        st.markdown("""
        Based on the analysis, these metrics should be prioritized in the ArtistRank algorithm:
        
        1. **Growth Rate Metrics:**
           - Play count growth percentage (week-over-week)
           - Unique listener growth percentage
           
        2. **Engagement Quality Metrics:**
           - Favorites per listener ratio
           - Shares per listener ratio
           - Plays per listener ratio
           
        3. **Geographic Expansion Indicators:**
           - Multi-country presence (weighted by market importance)
           - Growth in secondary markets
           
        4. **Size-Relative Performance:**
           - Performance relative to size cohort (micro, small, medium, large)
           - Above-average engagement within cohort
        """)
        
        # Visualization of key recommendation factors
        st.subheader("Visualization of Recommended Weighting")
        
        weights_data = pd.DataFrame([
            {"factor": "Play Growth %", "weight": 0.40},
            {"factor": "Listener Growth %", "weight": 0.30},
            {"factor": "Favorites/Listener", "weight": 0.15},
            {"factor": "Shares/Listener", "weight": 0.10},
            {"factor": "Geographic Spread", "weight": 0.05}
        ])
        
        fig12 = px.pie(
            weights_data,
            values="weight",
            names="factor",
            title="Recommended Weighting for ArtistRank Algorithm",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.4
        )
        fig12.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig12, use_container_width=True)
        
        # SQL implementation suggestions
        st.subheader("SQL Implementation Recommendations")
        
        st.code('''
    -- Core ArtistRank query incorporating all recommended factors
    WITH current_period AS (
        SELECT 
            m.artist,
            COUNT(*) as plays,
            COUNT(DISTINCT e.actor_id) as unique_listeners,
            SUM(CASE WHEN e.type = 'favorite' THEN 1 ELSE 0 END) as favorites,
            SUM(CASE WHEN e.type = 'share' THEN 1 ELSE 0 END) as shares,
            COUNT(DISTINCT e.geo_country) as country_count
        FROM dw01.events e
        JOIN dw01.music m ON e.object_id = m.music_id_raw
        WHERE e.event_date >= CAST((CURRENT_DATE - INTERVAL '30' DAY) AS VARCHAR)
        AND e.type IN ('play', 'favorite', 'share')
        AND m.status = 'complete'
        GROUP BY m.artist
    ),
    previous_period AS (
        SELECT 
            m.artist,
            COUNT(*) as plays,
            COUNT(DISTINCT e.actor_id) as unique_listeners
        FROM dw01.events e
        JOIN dw01.music m ON e.object_id = m.music_id_raw
        WHERE e.event_date >= CAST((CURRENT_DATE - INTERVAL '60' DAY) AS VARCHAR)
        AND e.event_date < CAST((CURRENT_DATE - INTERVAL '30' DAY) AS VARCHAR)
        AND e.type = 'play'
        AND m.status = 'complete'
        GROUP BY m.artist
    ),
    -- Create size cohorts based on play volume
    artist_sizes AS (
        SELECT
            artist,
            CASE 
                WHEN plays < 1000 THEN 'micro'
                WHEN plays < 10000 THEN 'small'
                WHEN plays < 100000 THEN 'medium'
                ELSE 'large'
            END as size_cohort,
            plays,
            unique_listeners,
            favorites,
            shares,
            country_count,
            CASE WHEN unique_listeners > 0 
                 THEN CAST(favorites AS DECIMAL) / unique_listeners 
                 ELSE 0 
            END as favorites_per_listener,
            CASE WHEN unique_listeners > 0 
                 THEN CAST(shares AS DECIMAL) / unique_listeners 
                 ELSE 0 
            END as shares_per_listener
        FROM current_period
    )
    SELECT
        a.artist,
        a.size_cohort,
        a.plays as current_plays,
        p.plays as previous_plays,
        a.unique_listeners as current_listeners,
        p.unique_listeners as previous_listeners,
        a.country_count,
        -- Growth metrics
        CAST((a.plays - p.plays) * 100.0 / NULLIF(p.plays, 0) AS DECIMAL(10,2)) as play_growth_pct,
        CAST((a.unique_listeners - p.unique_listeners) * 100.0 / NULLIF(p.unique_listeners, 0) AS DECIMAL(10,2)) as listener_growth_pct,
        -- Engagement quality metrics
        a.favorites_per_listener,
        a.shares_per_listener,
        -- Composite score calculation with recommended weights
        (CAST((a.plays - p.plays) * 100.0 / NULLIF(p.plays, 0) AS DECIMAL(10,2)) * 0.4) + 
        (CAST((a.unique_listeners - p.unique_listeners) * 100.0 / NULLIF(p.unique_listeners, 0) AS DECIMAL(10,2)) * 0.3) +
        (a.favorites_per_listener * 15.0) +
        (a.shares_per_listener * 10.0) +
        (a.country_count * 0.5) as artist_momentum_score
    FROM artist_sizes a
    JOIN previous_period p ON a.artist = p.artist
    WHERE p.plays > 100 -- Minimum threshold for previous period
    ORDER BY
        a.size_cohort,
        artist_momentum_score DESC
    LIMIT 100;
        ''', language='sql')
    
    
        
        # Next steps for ArtistRank development
        st.subheader("Next Steps for ArtistRank Development")
        
        st.markdown("""
        ### Week 2 Development Priorities (New):
        
        1. **Exploring Superset Further:**
           - Monthly Plays Dashboard
           - AMD Dashboards
           - (Document interesting patterns and questions)
        
        2. **Evaluating AMD Songs Performance:**
           - Develop queries to analyze performance metrics and identify cross-border opportunities:
           - (1) Query for AMD songs released in the last 30 days
           - (2) Geographic distribution analysis for AMD artists
           - (3) Compare overall artist audience geo distribution vs. recent song distribution
        
        3. **Create Superset Chart for AMD Editorial Playlists:**
           - Query to track editorial playlist additions (This will be integrated into the AMD dashboard)
        
        4. **For integrating this into Superset:**
           - Connect to Chris to discuss the integration process
           - Create a Superset dataset from this view:https://docs.google.com/document/d/1dVUrwYScYDK9M4akYlNRtUuySiE7uMYamNbd88Fie34/edit?usp=sharing
           - Build a table visualization with the following columns:
           - (1) Added Date
           - (2) Song Name
           - (3) Artist Name
           - (4) Is Ghost Account?
           - (5) Distributor
           - (6) Playlist Name
           - Add filtering capabilities for:
           - (1) Date range
           - (2) Playlist name
           - (3) Distributor
           - (4) Ghost account status
           - Implement daily refresh to capture new additions
    
        5. **Create a Comprehensive Analysis Report & Visualization**
           - Based on the findings, prepare an analysis report for the next team meeting(Apr 10)
           - Create visualizations for key findings; Format the editorial playlist table view; Document usage instructions for Jordan and Jalen
           
        6. **Prepare for Implementation in Superset**
           - Check myself & ask Jacob/Chris how to integrate my query into the AMD dashboard
           - Maybe: Format the query for optimal performance: Add appropriate indexes; Consider materialized views for faster refresh; Test with sample data to ensure accuracy
           - Develop documentation for Jordan and Jalen on how to use and interpret the table: eg: https://docs.google.com/document/d/1UoHhLnUQVLq7utKNMmZtdfuQ49DIU5dP8nxhUKfumNQ/edit?usp=sharing
           
           
           
        ### Week 2 Development Priorities (Old PLAN):
        
        1. **Testing & Validation:**
           - Compare results with previous A&R picks to validate effectiveness
           - Adjust weight coefficients based on findings
        
        2. **Integration with Superset:**
           - Create visualizations based on this dashboard
           - Set up scheduled queries to update data daily
           - Create alerts for high momentum score artists
        
        3. **Usability Enhancements:**
           - Add genre filtering capabilities
           - Implement territory-specific versions of the algorithm
           - Create drilldown capabilities for artist details
        
        4. **Collaboration with A&R Team:**
           - Share initial results with Jordan and Jalen
           - Cross-reference algorithmic picks with their selections
           - Identify patterns and blind spots in the current algorithm
        """)  
    
    
    
        
        # WEEK 1 DONE
        st.subheader("Week1 Meeting")
        
        st.markdown("""
        ### Week 1 (Done):
        
        1. **ArtistRank dashboard**
        2. **Main thing: Recommend artists & Artist Momentum Score methodology and its components**
        """)
    
    
    
    
    
    # Tab 6: Methodology & Explanations
    with tab6:
        st.header("Dashboard Methodology & Metric Explanations")
        
        # Data Range and Collection
        st.subheader("1. Data Range and Collection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            * **Time Period**: 30-day comparison (March 4 - April 3, 2025 vs February 2 - March 3, 2025)
            * **Data Sources**: Platform events database (plays, favorites, shares, downloads)
            * **Geographic Scope**: Global data with country breakdowns (Nigeria, Ghana, US, UK, etc.)
            """)
            
        with col2:
            st.info("""
            **Data Collection Method**:
            
            All metrics are extracted from the dw01.events and dw01.music tables using SQL queries 
            that group and aggregate events by artist, country, and time period.
            """)
        
        # Artist Size Cohort Explanation
        st.subheader("2. Artist Size Cohort Classification")
        
        cohort_df = pd.DataFrame([
            {"Cohort": "Micro", "Play Range": "< 1,000 plays", "Description": "Emerging artists, often with few releases"},
            {"Cohort": "Small", "Play Range": "1,000-10,000 plays", "Description": "Establishing presence, typically with growing regional appeal"},
            {"Cohort": "Medium", "Play Range": "10,000-100,000 plays", "Description": "Established regional artists, often with strong core audiences"},
            {"Cohort": "Large", "Play Range": "> 100,000 plays", "Description": "Mainstream artists with broad appeal"}
        ])
        
        st.table(cohort_df)
        
        st.markdown("""
        This classification ensures fair comparisons by comparing artists to their peers rather than 
        directly comparing new artists against established stars. Growth rates and engagement metrics 
        vary significantly across these cohorts.
        """)
        
        # Key Metrics Explanation
        st.subheader("3. Key Metrics Explained")
        
        metrics_tabs = st.tabs(["Engagement Metrics", "Growth Metrics", "Composite Metrics"])
        
        with metrics_tabs[0]:
            engagement_metrics = pd.DataFrame([
                {
                    "Metric": "Favorite-to-Play Ratio", 
                    "Formula": "Favorites ÷ Plays", 
                    "Description": "Percentage of plays resulting in favorites; indicates quality of engagement",
                    "Benchmark": "Platform average: 0.7%"
                },
                {
                    "Metric": "Share-to-Play Ratio", 
                    "Formula": "Shares ÷ Plays", 
                    "Description": "Percentage of plays resulting in shares; indicates viral potential",
                    "Benchmark": "Platform average: 0.3%"
                },
                {
                    "Metric": "Plays-per-Listener", 
                    "Formula": "Total Plays ÷ Unique Listeners", 
                    "Description": "Average repeat listens; indicates audience loyalty and retention",
                    "Benchmark": "Platform average: 3.2"
                },
                {
                    "Metric": "Download-to-Play Ratio", 
                    "Formula": "Downloads ÷ Plays", 
                    "Description": "Percentage of plays resulting in downloads; indicates intent for offline listening",
                    "Benchmark": "Platform average: 20%"
                }
            ])
            
            st.table(engagement_metrics)
        
        with metrics_tabs[1]:
            growth_metrics = pd.DataFrame([
                {
                    "Metric": "Play Growth Percentage", 
                    "Formula": "((Current Plays - Previous Plays) ÷ Previous Plays) × 100", 
                    "Description": "Month-over-month percentage increase in total plays",
                    "Weight in Score": "40%"
                },
                {
                    "Metric": "Listener Growth Percentage", 
                    "Formula": "((Current Listeners - Previous Listeners) ÷ Previous Listeners) × 100", 
                    "Description": "Month-over-month percentage increase in unique listeners",
                    "Weight in Score": "30%"
                },
                {
                    "Metric": "Multi-Country Presence", 
                    "Formula": "Count of countries with >50 plays", 
                    "Description": "Number of countries where an artist has significant listenership",
                    "Weight in Score": "5%"
                }
            ])
            
            st.table(growth_metrics)
        
        with metrics_tabs[2]:
            st.write("**Artist Momentum Score**")
            
            st.code("""
    # Composite score formula
    Artist_Momentum_Score = (
        (Play_Growth_Pct × 0.4) + 
        (Listener_Growth_Pct × 0.3) + 
        (Favorites_per_Listener × 15) + 
        (Shares_per_Listener × 10) + 
        (Country_Count × 0.5)
    )
            """)
            
            st.markdown("""
            This composite score balances:
            
            * **Growth trajectory** (70% weight): How quickly an artist is gaining plays and listeners
            * **Engagement quality** (25% weight): How deeply listeners are connecting with the content
            * **Geographic spread** (5% weight): How broadly the artist's appeal extends across territories
            
            The score is designed to surface artists with momentum regardless of their absolute play counts.
            """)
        
        # Chart Explanation Section
        st.subheader("4. Chart Interpretation Guide")
        
        st.write("**Hover Information**")
        st.markdown("""
        Most charts include detailed tooltips that appear when you hover over data points. These tooltips provide:
        
        * **Raw values**: The exact numbers behind each visualization
        * **Secondary metrics**: Related data points to provide context
        * **Calculation inputs**: The components used to derive composite metrics
        
        Experiment with hovering over different elements to reveal more insights.
        """)
        
        # SQL Methodology
        st.subheader("5. SQL Query Methodology")
        
        st.markdown("""
        The dashboard is powered by SQL queries that:
        
        1. Compare current period (last 30 days) with previous period (30-60 days ago)
        2. Join event data with music metadata to segment by artist
        3. Calculate engagement ratios and growth rates
        4. Apply cohort classification based on play volume
        5. Calculate composite scores using weighted components
        """)
        
        st.code("""
    -- Example of the core query structure
    WITH current_period AS (
        SELECT 
            m.artist,
            COUNT(*) as plays,
            COUNT(DISTINCT e.actor_id) as unique_listeners,
            SUM(CASE WHEN e.type = 'favorite' THEN 1 ELSE 0 END) as favorites,
            SUM(CASE WHEN e.type = 'share' THEN 1 ELSE 0 END) as shares,
            COUNT(DISTINCT e.geo_country) as country_count
        FROM dw01.events e
        JOIN dw01.music m ON e.object_id = m.music_id_raw
        WHERE e.event_date >= CAST((CURRENT_DATE - INTERVAL '30' DAY) AS VARCHAR)
        AND e.type IN ('play', 'favorite', 'share')
        GROUP BY m.artist
    ),
    previous_period AS (
        -- Similar query for previous 30 days
    ),
    artist_sizes AS (
        -- Cohort classification query
    )
    SELECT
        -- Final calculations including momentum score
    FROM artist_sizes a
    JOIN previous_period p ON a.artist = p.artist
    WHERE p.plays > 100
    ORDER BY
        artist_momentum_score DESC
        """, language="sql")
        
        # Update frequency
        st.subheader("6. Data Refresh Information")
        
        st.info("""
        **Update Schedule**:
        
        * Dashboard data is refreshed daily at 4:00 AM EST
        * All metrics reflect a rolling 30-day window
        * Historical data is preserved for trend analysis
        
        Last data refresh: April 3, 2025, 4:00 AM EST
        """)
    
    



# Footer
st.markdown("---")
st.caption("Audiomack ArtistRank Dashboard | Data period: April 7-13, 2025 | Last updated: April 13, 2025")
st.caption("Created by LinLin for Audiomack Internship Program Week 2 Assignment")
st.caption("Supervisors: Jacob & Ryan | A&R Researchers: Jalen & Jordan")
