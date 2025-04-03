import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from streamlit_gsheets import GSheetsConnection
import json

# Set page configuration
st.set_page_config(
    page_title="Audiomack ArtistRank Dashboard",
    page_icon="🎵",
    layout="wide"
)

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

# Create tabs
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     "Overview", 
#     "Engagement Analysis", 
#     "Geographic Insights", 
#     "Growing Artists", 
#     "Recommendations",
#     "Methodology & Explanations"
# ])
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
    2. **Mian thing: Recommend artists & Artist Momentum Score methodology and its components**
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


with tab7:
    st.header("A&R Scouting Tracker")
    st.write("View of Jordan and Jalen's AMD A&R scouting selections")
    
    # Direct link to the published CSV version of the sheet
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2Q-L96f18C7C-EMCzIoCxR8bdphMkPNcpske5xGYzr6lmztcsqaJgmyTFmXHhu7mjrqvR8MsgfWJT/pub?output=csv"
    
    # Load the data
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_scouting_data():
        try:
            df = pd.read_csv(csv_url)
            return df
        except Exception as e:
            st.error(f"Error loading scouting data: {e}")
            return pd.DataFrame()
    
    scouting_df = load_scouting_data()
    
    # Display a message if the sheet is not found or empty
    if scouting_df.empty:
        st.warning("No data available in the scouting tracker")
    else:
        # Clean and prepare the data
        # Skip header rows if needed (adjust based on your sheet structure)
        if len(scouting_df) > 2:
            # Assuming row 3 contains column headers and data starts from row 4
            column_names = scouting_df.iloc[2].tolist()
            scouting_df = scouting_df.iloc[3:].reset_index(drop=True)
            scouting_df.columns = column_names
        
        # Filter out empty rows
        scouting_df = scouting_df.dropna(how='all')
        
        # Display filters
        st.subheader("Filter Tracks")
        
        # Genre filter
        available_genres = scouting_df['Genre'].dropna().unique()
        selected_genres = st.multiselect(
            "Select Genres",
            options=available_genres,
            default=available_genres
        )
        
        # Geography filter
        available_geos = scouting_df['Geo'].dropna().unique()
        selected_geos = st.multiselect(
            "Select Geographies",
            options=available_geos,
            default=available_geos
        )
        
        # On Platform filter
        platform_options = ['Y', 'N']
        selected_platform = st.multiselect(
            "On Audiomack Platform",
            options=platform_options,
            default=platform_options
        )
        
        # Apply filters
        filtered_df = scouting_df.copy()
        
        if selected_genres:
            filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
        
        if selected_geos:
            filtered_df = filtered_df[filtered_df['Geo'].isin(selected_geos)]
        
        if selected_platform:
            filtered_df = filtered_df[filtered_df['On Platform'].isin(selected_platform)]
        
        # Display the filtered data
        st.subheader("Scouting Results")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Analytics
        st.subheader("Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tracks Scouted", len(filtered_df))
        
        with col2:
            if 'Genre' in filtered_df.columns:
                genre_count = filtered_df['Genre'].nunique()
                st.metric("Unique Genres", genre_count)
        
        with col3:
            if 'Geo' in filtered_df.columns:
                geo_count = filtered_df['Geo'].nunique()
                st.metric("Geographic Regions", geo_count)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Genre' in filtered_df.columns and not filtered_df['Genre'].isna().all():
                genre_counts = filtered_df['Genre'].value_counts().reset_index()
                genre_counts.columns = ['Genre', 'Count']
                
                fig = px.pie(
                    genre_counts,
                    values='Count',
                    names='Genre',
                    title="Genre Distribution",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Geo' in filtered_df.columns and not filtered_df['Geo'].isna().all():
                geo_counts = filtered_df['Geo'].value_counts().reset_index()
                geo_counts.columns = ['Geography', 'Count']
                
                fig = px.bar(
                    geo_counts,
                    x='Geography',
                    y='Count',
                    title="Geographic Distribution",
                    color='Count'
                )
                st.plotly_chart(fig, use_container_width=True)





# Footer
st.markdown("---")
st.caption("Audiomack ArtistRank Dashboard | Last updated: April 3, 2025")
st.caption("Made with ❤️ by LinLin for Audiomack Internship Program")
st.caption("Supervisor: Jacob & Ryan; A&R Researcher: Jalen & Jordan")

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import json

# # Set page configuration
# st.set_page_config(
#     page_title="Audiomack ArtistRank Dashboard",
#     page_icon="🎵",
#     layout="wide"
# )

# # Function to load CSV data
# @st.cache_data
# def load_data():
#     # In a real implementation, this would read actual CSV files
#     # For now, we'll create DataFrames with sample data based on your file structure
    
#     # Event type counts
#     event_type_df = pd.DataFrame([
#         {"event_type": "play", "event_count": 15000000, "unique_users": 2500000},
#         {"event_type": "favorite", "event_count": 750000, "unique_users": 500000},
#         {"event_type": "share", "event_count": 250000, "unique_users": 200000},
#         {"event_type": "download", "event_count": 3000000, "unique_users": 1800000},
#         {"event_type": "playlist_add", "event_count": 450000, "unique_users": 300000},
#         {"event_type": "comment", "event_count": 180000, "unique_users": 95000},
#         {"event_type": "profile_view", "event_count": 900000, "unique_users": 650000}
#     ])
    
#     # Music engagement metrics
#     music_engagement_df = pd.DataFrame([
#         {"artist": "Shallipopi", "total_plays": 3200000, "unique_listeners": 950000},
#         {"artist": "Asake", "total_plays": 2800000, "unique_listeners": 1200000},
#         {"artist": "Seyi Vibez", "total_plays": 2400000, "unique_listeners": 820000},
#         {"artist": "Young Jonn", "total_plays": 2100000, "unique_listeners": 750000},
#         {"artist": "Mohbad", "total_plays": 1900000, "unique_listeners": 680000},
#         {"artist": "Ayra Starr", "total_plays": 1750000, "unique_listeners": 940000},
#         {"artist": "Burna Boy", "total_plays": 1650000, "unique_listeners": 1050000},
#         {"artist": "Davido", "total_plays": 1550000, "unique_listeners": 980000},
#         {"artist": "Wizkid", "total_plays": 1450000, "unique_listeners": 920000},
#         {"artist": "Rema", "total_plays": 1350000, "unique_listeners": 860000}
#     ])
    
#     # Engagement ratios for artists
#     engagement_ratios_df = pd.DataFrame([
#         {"artist": "Shallipopi", "plays": 3200000, "favorites": 160000, "shares": 48000, "unique_users": 950000, "favorite_to_play_ratio": 0.050},
#         {"artist": "Asake", "plays": 2800000, "favorites": 210000, "shares": 70000, "unique_users": 1200000, "favorite_to_play_ratio": 0.075},
#         {"artist": "Seyi Vibez", "plays": 2400000, "favorites": 96000, "shares": 36000, "unique_users": 820000, "favorite_to_play_ratio": 0.040},
#         {"artist": "Young Jonn", "plays": 2100000, "favorites": 147000, "shares": 31500, "unique_users": 750000, "favorite_to_play_ratio": 0.070},
#         {"artist": "Mohbad", "plays": 1900000, "favorites": 133000, "shares": 38000, "unique_users": 680000, "favorite_to_play_ratio": 0.070},
#         {"artist": "Ayra Starr", "plays": 1750000, "favorites": 131250, "shares": 43750, "unique_users": 940000, "favorite_to_play_ratio": 0.075},
#         {"artist": "Burna Boy", "plays": 1650000, "favorites": 123750, "shares": 33000, "unique_users": 1050000, "favorite_to_play_ratio": 0.075},
#         {"artist": "Davido", "plays": 1550000, "favorites": 108500, "shares": 38750, "unique_users": 980000, "favorite_to_play_ratio": 0.070},
#         {"artist": "Wizkid", "plays": 1450000, "favorites": 116000, "shares": 36250, "unique_users": 920000, "favorite_to_play_ratio": 0.080},
#         {"artist": "Rema", "plays": 1350000, "favorites": 94500, "shares": 27000, "unique_users": 860000, "favorite_to_play_ratio": 0.070}
#     ])
    
#     # Geographic analysis
#     geographic_df = pd.DataFrame([
#         {"artist": "Shallipopi", "geo_country": "NG", "play_count": 2240000, "unique_listeners": 665000},
#         {"artist": "Shallipopi", "geo_country": "GH", "play_count": 480000, "unique_listeners": 142500},
#         {"artist": "Shallipopi", "geo_country": "US", "play_count": 320000, "unique_listeners": 95000},
#         {"artist": "Asake", "geo_country": "NG", "play_count": 1680000, "unique_listeners": 720000},
#         {"artist": "Asake", "geo_country": "GH", "play_count": 280000, "unique_listeners": 120000},
#         {"artist": "Asake", "geo_country": "UK", "play_count": 392000, "unique_listeners": 168000},
#         {"artist": "Asake", "geo_country": "US", "play_count": 448000, "unique_listeners": 192000},
#         {"artist": "Seyi Vibez", "geo_country": "NG", "play_count": 1680000, "unique_listeners": 574000},
#         {"artist": "Seyi Vibez", "geo_country": "GH", "play_count": 360000, "unique_listeners": 123000},
#         {"artist": "Seyi Vibez", "geo_country": "US", "play_count": 240000, "unique_listeners": 82000},
#         {"artist": "Mohbad", "geo_country": "NG", "play_count": 1330000, "unique_listeners": 476000},
#         {"artist": "Mohbad", "geo_country": "GH", "play_count": 285000, "unique_listeners": 102000},
#         {"artist": "Mohbad", "geo_country": "US", "play_count": 190000, "unique_listeners": 68000},
#         {"artist": "Wizkid", "geo_country": "NG", "play_count": 725000, "unique_listeners": 460000},
#         {"artist": "Wizkid", "geo_country": "GH", "play_count": 217500, "unique_listeners": 138000},
#         {"artist": "Wizkid", "geo_country": "UK", "play_count": 217500, "unique_listeners": 138000},
#         {"artist": "Wizkid", "geo_country": "US", "play_count": 290000, "unique_listeners": 184000}
#     ])
    
#     # Growing artists with momentum
#     growing_artists_df = pd.DataFrame([
#         {"artist": "Young Jonn", "size_cohort": "medium", "current_plays": 2100000, "previous_plays": 1500000, "current_listeners": 750000, "previous_listeners": 600000, "play_growth_pct": 40.00, "listener_growth_pct": 25.00, "plays_per_listener": 3, "favorites_per_listener": 0.2, "shares_per_listener": 0.04, "artist_momentum_score": 39.80},
#         {"artist": "Shallipopi", "size_cohort": "large", "current_plays": 3200000, "previous_plays": 2500000, "current_listeners": 950000, "previous_listeners": 800000, "play_growth_pct": 28.00, "listener_growth_pct": 18.75, "plays_per_listener": 3, "favorites_per_listener": 0.17, "shares_per_listener": 0.05, "artist_momentum_score": 32.30},
#         {"artist": "Seyi Vibez", "size_cohort": "medium", "current_plays": 2400000, "previous_plays": 1900000, "current_listeners": 820000, "previous_listeners": 700000, "play_growth_pct": 26.32, "listener_growth_pct": 17.14, "plays_per_listener": 3, "favorites_per_listener": 0.12, "shares_per_listener": 0.04, "artist_momentum_score": 29.04},
#         {"artist": "Khaid", "size_cohort": "small", "current_plays": 980000, "previous_plays": 650000, "current_listeners": 350000, "previous_listeners": 250000, "play_growth_pct": 50.77, "listener_growth_pct": 40.00, "plays_per_listener": 3, "favorites_per_listener": 0.23, "shares_per_listener": 0.06, "artist_momentum_score": 48.73},
#         {"artist": "Odumodu Blvck", "size_cohort": "small", "current_plays": 820000, "previous_plays": 580000, "current_listeners": 410000, "previous_listeners": 320000, "play_growth_pct": 41.38, "listener_growth_pct": 28.13, "plays_per_listener": 2, "favorites_per_listener": 0.19, "shares_per_listener": 0.05, "artist_momentum_score": 39.58},
#         {"artist": "Victony", "size_cohort": "medium", "current_plays": 1250000, "previous_plays": 950000, "current_listeners": 520000, "previous_listeners": 420000, "play_growth_pct": 31.58, "listener_growth_pct": 23.81, "plays_per_listener": 2, "favorites_per_listener": 0.16, "shares_per_listener": 0.03, "artist_momentum_score": 32.87},
#         {"artist": "FAVE", "size_cohort": "micro", "current_plays": 650000, "previous_plays": 390000, "current_listeners": 250000, "previous_listeners": 170000, "play_growth_pct": 66.67, "listener_growth_pct": 47.06, "plays_per_listener": 3, "favorites_per_listener": 0.24, "shares_per_listener": 0.07, "artist_momentum_score": 57.22},
#         {"artist": "Lil kesh", "size_cohort": "medium", "current_plays": 1680000, "previous_plays": 1450000, "current_listeners": 580000, "previous_listeners": 530000, "play_growth_pct": 15.86, "listener_growth_pct": 9.43, "plays_per_listener": 3, "favorites_per_listener": 0.14, "shares_per_listener": 0.04, "artist_momentum_score": 21.03},
#         {"artist": "CKay", "size_cohort": "medium", "current_plays": 1820000, "previous_plays": 1520000, "current_listeners": 640000, "previous_listeners": 570000, "play_growth_pct": 19.74, "listener_growth_pct": 12.28, "plays_per_listener": 3, "favorites_per_listener": 0.18, "shares_per_listener": 0.05, "artist_momentum_score": 24.62},
#         {"artist": "Bloody Civilian", "size_cohort": "micro", "current_plays": 450000, "previous_plays": 220000, "current_listeners": 180000, "previous_listeners": 110000, "play_growth_pct": 104.55, "listener_growth_pct": 63.64, "plays_per_listener": 3, "favorites_per_listener": 0.25, "shares_per_listener": 0.08, "artist_momentum_score": 80.82}
#     ])
    
#     # Add calculated fields
#     # Plays per user ratio for engagement analysis
#     music_engagement_df['plays_per_user'] = music_engagement_df['total_plays'] / music_engagement_df['unique_listeners']
    
#     # Add geographic distribution percentages
#     total_plays_by_artist = {}
#     for artist in geographic_df['artist'].unique():
#         artist_plays = geographic_df[geographic_df['artist'] == artist]['play_count'].sum()
#         total_plays_by_artist[artist] = artist_plays
    
#     geographic_df['play_percentage'] = geographic_df.apply(
#         lambda row: (row['play_count'] / total_plays_by_artist[row['artist']]) * 100 if row['artist'] in total_plays_by_artist else 0,
#         axis=1
#     )
    
#     # Process engagement ratios data for visualization
#     engagement_analysis_df = engagement_ratios_df.copy()
#     engagement_analysis_df['favorite_ratio'] = engagement_analysis_df['favorites'] / engagement_analysis_df['plays']
#     engagement_analysis_df['share_ratio'] = engagement_analysis_df['shares'] / engagement_analysis_df['plays']
#     engagement_analysis_df['engagement_score'] = (engagement_analysis_df['favorite_ratio'] * 10) + (engagement_analysis_df['share_ratio'] * 5)
    
#     # Add growth indication
#     growing_artists_df['growth_indicator'] = growing_artists_df['play_growth_pct'].apply(
#         lambda x: '🔥 High Growth' if x > 40 else ('📈 Moderate Growth' if x > 20 else '➖ Stable')
#     )
    
#     return event_type_df, music_engagement_df, engagement_analysis_df, geographic_df, growing_artists_df

# # Load data
# try:
#     event_type_df, music_engagement_df, engagement_analysis_df, geographic_df, growing_artists_df = load_data()
#     data_loaded = True
# except Exception as e:
#     st.error(f"Error loading data: {e}")
#     data_loaded = False

# # Dashboard title and description
# st.title("🎵 Audiomack ArtistRank Dashboard")
# st.write("Analysis dashboard for the ArtistRank tool development - Week 1") 
# # st.write("Time Period: All metrics reflect the last 30 days (March 4 - April 3, 2025) compared against the previous 30 days (February 2 - March 3, 2025)")
# # st.write("Data Sources: Audiomack platform events database (dw01.events and dw01.music tables)")
# # st.write("Event Types: Plays (30+ seconds), favorites, shares, downloads, playlist adds")
# # st.write("Geographic Scope: Global data with country-specific breakdowns for Nigeria, Ghana, US, UK, and other key markets")

# # Create sidebar for filtering
# st.sidebar.header("Filters")
# selected_size_cohort = st.sidebar.multiselect(
#     "Artist Size Cohort",
#     options=growing_artists_df['size_cohort'].unique(),
#     default=growing_artists_df['size_cohort'].unique()
# )

# selected_countries = st.sidebar.multiselect(
#     "Countries",
#     options=geographic_df['geo_country'].unique(),
#     default=['NG', 'GH', 'US']
# )

# # About section in sidebar
# st.sidebar.markdown("---")
# st.sidebar.header("About ArtistRank")
# st.sidebar.info(
#     """
#     ArtistRank is a tool for surfacing songs and artists 
#     best situated to gain traction and success on and 
#     off the platform.
    
#     This dashboard provides insights into engagement metrics, 
#     geographic distribution, and growth trends to support 
#     A&R decisions.
#     """
# )

# # Create tabs
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "Overview", 
#     "Engagement Analysis", 
#     "Geographic Insights", 
#     "Growing Artists", 
#     "Recommendations"
# ])

# # Tab 1: Overview
# with tab1:
#     st.header("Platform Event Overview")
    
#     # Create metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     total_plays = event_type_df[event_type_df['event_type'] == 'play']['event_count'].sum()
#     total_favorites = event_type_df[event_type_df['event_type'] == 'favorite']['event_count'].sum()
#     total_shares = event_type_df[event_type_df['event_type'] == 'share']['event_count'].sum()
#     total_downloads = event_type_df[event_type_df['event_type'] == 'download']['event_count'].sum()
    
#     col1.metric("Total Plays", f"{total_plays:,}")
#     col2.metric("Total Favorites", f"{total_favorites:,}")
#     col3.metric("Total Shares", f"{total_shares:,}")
#     col4.metric("Total Downloads", f"{total_downloads:,}")
    
#     # Create event type distribution chart
#     st.subheader("Event Type Distribution")
    
#     fig1 = px.bar(
#         event_type_df,
#         x="event_type",
#         y="event_count",
#         title="Events by Type",
#         color="event_type",
#         labels={"event_count": "Number of Events", "event_type": "Event Type"},
#         color_discrete_sequence=px.colors.qualitative.Bold
#     )
#     fig1.update_layout(xaxis={'categoryorder':'total descending'})
#     st.plotly_chart(fig1, use_container_width=True)
    
#     # Create unique users by event type
#     st.subheader("User Engagement by Event Type")
    
#     fig2 = go.Figure()
#     fig2.add_trace(go.Bar(
#         x=event_type_df["event_type"],
#         y=event_type_df["unique_users"],
#         name="Unique Users",
#         marker_color="#FF6B6B"
#     ))
#     fig2.update_layout(
#         title="Unique Users by Event Type",
#         xaxis_title="Event Type",
#         yaxis_title="Number of Unique Users",
#         xaxis={'categoryorder':'total descending'}
#     )
#     st.plotly_chart(fig2, use_container_width=True)
    
#     # Top artists by plays
#     st.subheader("Top Artists by Plays")
    
#     fig3 = px.bar(
#         music_engagement_df.sort_values('total_plays', ascending=False).head(10),
#         x="artist",
#         y="total_plays",
#         title="Top 10 Artists by Total Plays",
#         color_discrete_sequence=["#4ECDC4"],
#         hover_data=["unique_listeners", "plays_per_user"]
#     )
#     fig3.update_layout(xaxis_title="Artist", yaxis_title="Total Plays")
#     st.plotly_chart(fig3, use_container_width=True)

# # Tab 2: Engagement Analysis
# with tab2:
#     st.header("Artist Engagement Analysis")
    
#     # Create engagement metrics visualization
#     st.subheader("Engagement Metrics by Artist")
    
#     metrics_df = engagement_analysis_df.melt(
#         id_vars=["artist"],
#         value_vars=["favorite_ratio", "share_ratio"],
#         var_name="Metric",
#         value_name="Value"
#     )
    
#     metrics_df["Metric"] = metrics_df["Metric"].map({
#         "favorite_ratio": "Favorites Ratio",
#         "share_ratio": "Shares Ratio"
#     })
    
#     fig4 = px.bar(
#         metrics_df,
#         x="artist",
#         y="Value",
#         color="Metric",
#         barmode="group",
#         title="Engagement Ratios by Artist",
#         color_discrete_map={
#             "Favorites Ratio": "#FF9F1C",
#             "Shares Ratio": "#E71D36"
#         }
#     )
#     fig4.update_layout(xaxis_title="Artist", yaxis_title="Ratio Value")
#     st.plotly_chart(fig4, use_container_width=True)
    
#     # Create plays per user chart
#     st.subheader("Plays per Unique Listener")
    
#     fig5 = px.bar(
#         music_engagement_df.sort_values('plays_per_user', ascending=False),
#         x="artist",
#         y="plays_per_user",
#         title="Average Plays per Unique Listener",
#         color_discrete_sequence=["#2EC4B6"],
#         hover_data=["total_plays", "unique_listeners"]
#     )
#     fig5.update_layout(xaxis_title="Artist", yaxis_title="Plays per Listener")
#     st.plotly_chart(fig5, use_container_width=True)
    
#     # Create composite engagement score chart
#     st.subheader("Composite Engagement Score")
    
#     fig6 = px.bar(
#         engagement_analysis_df.sort_values('engagement_score', ascending=False),
#         x="artist",
#         y="engagement_score",
#         title="Composite Engagement Score (Favorites + Shares Weighted)",
#         color_discrete_sequence=["#FF6B6B"],
#         hover_data=["favorite_ratio", "share_ratio"]
#     )
#     fig6.update_layout(xaxis_title="Artist", yaxis_title="Engagement Score")
#     st.plotly_chart(fig6, use_container_width=True)

# # Tab 3: Geographic Insights
# with tab3:
#     st.header("Geographic Analysis")
    
#     # Filter by selected countries
#     filtered_geo_df = geographic_df[geographic_df['geo_country'].isin(selected_countries)]
    
#     # Create country comparison chart
#     st.subheader("Artist Performance by Country")
    
#     fig7 = px.bar(
#         filtered_geo_df,
#         x="artist",
#         y="play_count",
#         color="geo_country",
#         title="Play Counts by Artist and Country",
#         barmode="group",
#         color_discrete_sequence=px.colors.qualitative.Set3
#     )
#     fig7.update_layout(xaxis_title="Artist", yaxis_title="Play Count")
#     st.plotly_chart(fig7, use_container_width=True)
    
#     # Create percentage distribution chart
#     st.subheader("Geographic Distribution of Plays")
    
#     fig8 = px.bar(
#         filtered_geo_df,
#         x="artist",
#         y="play_percentage",
#         color="geo_country",
#         title="Percentage Distribution of Plays by Country",
#         barmode="stack",
#         color_discrete_sequence=px.colors.qualitative.Bold
#     )
#     fig8.update_layout(xaxis_title="Artist", yaxis_title="Percentage of Total Plays (%)")
#     st.plotly_chart(fig8, use_container_width=True)
    
#     # Create unique listeners map
#     st.subheader("Unique Listeners by Country")
    
#     unique_by_country = filtered_geo_df.groupby('geo_country')['unique_listeners'].sum().reset_index()
    
#     fig9 = px.choropleth(
#         unique_by_country,
#         locations="geo_country",
#         locationmode="ISO-3",
#         color="unique_listeners",
#         hover_name="geo_country",
#         color_continuous_scale=px.colors.sequential.Viridis,
#         title="Unique Listeners by Country"
#     )
#     st.plotly_chart(fig9, use_container_width=True)

# # Tab 4: Growing Artists
# with tab4:
#     st.header("Artist Growth Analysis")
    
#     # Filter by selected size cohorts
#     filtered_growing_df = growing_artists_df[growing_artists_df['size_cohort'].isin(selected_size_cohort)]
    
#     # Add a selection widget for the growth metric
#     growth_metric = st.radio(
#         "Select Growth Metric",
#         ["play_growth_pct", "listener_growth_pct", "artist_momentum_score"],
#         format_func=lambda x: {
#             "play_growth_pct": "Play Count Growth %",
#             "listener_growth_pct": "Listener Growth %",
#             "artist_momentum_score": "Artist Momentum Score"
#         }[x],
#         horizontal=True
#     )
    
#     # Create growth metric chart
#     st.subheader("Artist Growth Metrics")
    
#     fig10 = px.bar(
#         filtered_growing_df.sort_values(growth_metric, ascending=False),
#         x="artist",
#         y=growth_metric,
#         color="size_cohort",
#         title="Artist Growth by Size Cohort",
#         labels={
#             "play_growth_pct": "Play Count Growth %",
#             "listener_growth_pct": "Listener Growth %",
#             "artist_momentum_score": "Artist Momentum Score"
#         },
#         hover_data=["plays_per_listener", "favorites_per_listener", "shares_per_listener"],
#         color_discrete_sequence=px.colors.qualitative.Safe
#     )
#     fig10.update_layout(xaxis_title="Artist", yaxis_title="Growth Metric")
#     st.plotly_chart(fig10, use_container_width=True)
    
#     # Create side-by-side comparison of current vs previous metrics
#     st.subheader("Current vs Previous Period Comparison")
    
#     # Select an artist for detailed view
#     selected_artist = st.selectbox(
#         "Select Artist for Detailed Comparison",
#         options=filtered_growing_df['artist'].tolist()
#     )
    
#     artist_data = filtered_growing_df[filtered_growing_df['artist'] == selected_artist].iloc[0]
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Current metrics
#         st.subheader("Current Period")
#         st.metric("Plays", f"{artist_data['current_plays']:,}")
#         st.metric("Unique Listeners", f"{artist_data['current_listeners']:,}")
#         st.metric("Plays per Listener", f"{artist_data['plays_per_listener']:.2f}")
#         st.metric("Favorites per Listener", f"{artist_data['favorites_per_listener']:.2f}")
#         st.metric("Shares per Listener", f"{artist_data['shares_per_listener']:.2f}")
    
#     with col2:
#         # Previous metrics with growth indicators
#         st.subheader("Growth Metrics")
#         st.metric("Previous Plays", f"{artist_data['previous_plays']:,}", 
#                  delta=f"{artist_data['play_growth_pct']:.1f}%")
#         st.metric("Previous Listeners", f"{artist_data['previous_listeners']:,}", 
#                  delta=f"{artist_data['listener_growth_pct']:.1f}%")
#         st.metric("Growth Indicator", artist_data['growth_indicator'])
#         st.metric("Size Cohort", artist_data['size_cohort'].capitalize())
#         st.metric("Momentum Score", f"{artist_data['artist_momentum_score']:.2f}")
    
#     # Show comparison chart
#     metrics_to_compare = {
#         'plays': ['current_plays', 'previous_plays'],
#         'listeners': ['current_listeners', 'previous_listeners']
#     }
    
#     metric_choice = st.radio(
#         "Compare Metric",
#         list(metrics_to_compare.keys()),
#         horizontal=True
#     )
    
#     current_col, prev_col = metrics_to_compare[metric_choice]
    
#     comparison_data = pd.DataFrame({
#         'period': ['Current', 'Previous'],
#         'value': [artist_data[current_col], artist_data[prev_col]]
#     })
    
#     fig11 = px.bar(
#         comparison_data,
#         x="period",
#         y="value",
#         title=f"{selected_artist}: {metric_choice.capitalize()} Comparison",
#         color="period",
#         color_discrete_map={
#             "Current": "#00A878",
#             "Previous": "#5F4B8B"
#         }
#     )
#     st.plotly_chart(fig11, use_container_width=True)

# # Tab 5: Recommendations
# with tab5:
#     st.header("ArtistRank Recommendations")
    
#     # Identifying potential emerging artists
#     st.subheader("Emerging Artists to Watch")
    
#     # Combine growth and engagement data
#     emerging_artists = growing_artists_df[
#         (growing_artists_df['play_growth_pct'] > 30) & 
#         (growing_artists_df['size_cohort'].isin(['micro', 'small']))
#     ].sort_values('artist_momentum_score', ascending=False).head(5)
    
#     for i, artist in enumerate(emerging_artists['artist'].tolist()):
#         col_left, col_right = st.columns([1, 3])
        
#         with col_left:
#             st.subheader(f"{i+1}. {artist}")
#             st.caption(f"Size: {emerging_artists.iloc[i]['size_cohort'].capitalize()}")
#             st.caption(f"Growth: {emerging_artists.iloc[i]['play_growth_pct']:.1f}%")
            
#         with col_right:
#             st.write(f"**Momentum Score:** {emerging_artists.iloc[i]['artist_momentum_score']:.2f}")
#             st.write(f"**Growth Indicator:** {emerging_artists.iloc[i]['growth_indicator']}")
#             st.write(f"**Current Plays:** {emerging_artists.iloc[i]['current_plays']:,} | **Previous:** {emerging_artists.iloc[i]['previous_plays']:,}")
#             st.write(f"**Current Listeners:** {emerging_artists.iloc[i]['current_listeners']:,} | **Previous:** {emerging_artists.iloc[i]['previous_listeners']:,}")
        
#         st.markdown("---")
    
#     # Key metrics for ArtistRank algorithm
#     st.subheader("Recommended Key Metrics for ArtistRank Algorithm")
    
#     st.markdown("""
#     Based on the analysis, these metrics should be prioritized in the ArtistRank algorithm:
    
#     1. **Growth Rate Metrics:**
#        - Play count growth percentage (week-over-week)
#        - Unique listener growth percentage
       
#     2. **Engagement Quality Metrics:**
#        - Favorites per listener ratio
#        - Shares per listener ratio
#        - Plays per listener ratio
       
#     3. **Geographic Expansion Indicators:**
#        - Multi-country presence (weighted by market importance)
#        - Growth in secondary markets
       
#     4. **Size-Relative Performance:**
#        - Performance relative to size cohort (micro, small, medium, large)
#        - Above-average engagement within cohort
#     """)
    
#     # Visualization of key recommendation factors
#     st.subheader("Visualization of Recommended Weighting")
    
#     weights_data = pd.DataFrame([
#         {"factor": "Play Growth %", "weight": 0.40},
#         {"factor": "Listener Growth %", "weight": 0.30},
#         {"factor": "Favorites/Listener", "weight": 0.15},
#         {"factor": "Shares/Listener", "weight": 0.10},
#         {"factor": "Geographic Spread", "weight": 0.05}
#     ])
    
#     fig12 = px.pie(
#         weights_data,
#         values="weight",
#         names="factor",
#         title="Recommended Weighting for ArtistRank Algorithm",
#         color_discrete_sequence=px.colors.qualitative.Bold,
#         hole=0.4
#     )
#     fig12.update_traces(textposition='inside', textinfo='percent+label')
#     st.plotly_chart(fig12, use_container_width=True)
    
#     # SQL implementation suggestions
#     st.subheader("SQL Implementation Recommendations")
    
#     st.code('''
# -- Core ArtistRank query incorporating all recommended factors
# WITH current_period AS (
#     SELECT 
#         m.artist,
#         COUNT(*) as plays,
#         COUNT(DISTINCT e.actor_id) as unique_listeners,
#         SUM(CASE WHEN e.type = 'favorite' THEN 1 ELSE 0 END) as favorites,
#         SUM(CASE WHEN e.type = 'share' THEN 1 ELSE 0 END) as shares,
#         COUNT(DISTINCT e.geo_country) as country_count
#     FROM dw01.events e
#     JOIN dw01.music m ON e.object_id = m.music_id_raw
#     WHERE e.event_date >= CAST((CURRENT_DATE - INTERVAL '30' DAY) AS VARCHAR)
#     AND e.type IN ('play', 'favorite', 'share')
#     AND m.status = 'complete'
#     GROUP BY m.artist
# ),
# previous_period AS (
#     SELECT 
#         m.artist,
#         COUNT(*) as plays,
#         COUNT(DISTINCT e.actor_id) as unique_listeners
#     FROM dw01.events e
#     JOIN dw01.music m ON e.object_id = m.music_id_raw
#     WHERE e.event_date >= CAST((CURRENT_DATE - INTERVAL '60' DAY) AS VARCHAR)
#     AND e.event_date < CAST((CURRENT_DATE - INTERVAL '30' DAY) AS VARCHAR)
#     AND e.type = 'play'
#     AND m.status = 'complete'
#     GROUP BY m.artist
# ),
# -- Create size cohorts based on play volume
# artist_sizes AS (
#     SELECT
#         artist,
#         CASE 
#             WHEN plays < 1000 THEN 'micro'
#             WHEN plays < 10000 THEN 'small'
#             WHEN plays < 100000 THEN 'medium'
#             ELSE 'large'
#         END as size_cohort,
#         plays,
#         unique_listeners,
#         favorites,
#         shares,
#         country_count,
#         CASE WHEN unique_listeners > 0 
#              THEN CAST(favorites AS DECIMAL) / unique_listeners 
#              ELSE 0 
#         END as favorites_per_listener,
#         CASE WHEN unique_listeners > 0 
#              THEN CAST(shares AS DECIMAL) / unique_listeners 
#              ELSE 0 
#         END as shares_per_listener
#     FROM current_period
# )
# SELECT
#     a.artist,
#     a.size_cohort,
#     a.plays as current_plays,
#     p.plays as previous_plays,
#     a.unique_listeners as current_listeners,
#     p.unique_listeners as previous_listeners,
#     a.country_count,
#     -- Growth metrics
#     CAST((a.plays - p.plays) * 100.0 / NULLIF(p.plays, 0) AS DECIMAL(10,2)) as play_growth_pct,
#     CAST((a.unique_listeners - p.unique_listeners) * 100.0 / NULLIF(p.unique_listeners, 0) AS DECIMAL(10,2)) as listener_growth_pct,
#     -- Engagement quality metrics
#     a.favorites_per_listener,
#     a.shares_per_listener,
#     -- Composite score calculation with recommended weights
#     (CAST((a.plays - p.plays) * 100.0 / NULLIF(p.plays, 0) AS DECIMAL(10,2)) * 0.4) + 
#     (CAST((a.unique_listeners - p.unique_listeners) * 100.0 / NULLIF(p.unique_listeners, 0) AS DECIMAL(10,2)) * 0.3) +
#     (a.favorites_per_listener * 15.0) +
#     (a.shares_per_listener * 10.0) +
#     (a.country_count * 0.5) as artist_momentum_score
# FROM artist_sizes a
# JOIN previous_period p ON a.artist = p.artist
# WHERE p.plays > 100 -- Minimum threshold for previous period
# ORDER BY
#     a.size_cohort,
#     artist_momentum_score DESC
# LIMIT 100;
#     ''', language='sql')
    
#     # Next steps for ArtistRank development
#     st.subheader("Next Steps for ArtistRank Development")
    
#     st.markdown("""
#     ### Week 2 Development Priorities:
    
#     1. **Testing & Validation:**
#        - Test the above SQL with actual platform data
#        - Compare results with previous A&R picks to validate effectiveness
#        - Adjust weight coefficients based on findings
    
#     2. **Integration with Superset:**
#        - Create visualizations based on this dashboard
#        - Set up scheduled queries to update data daily
#        - Create alerts for high momentum score artists
    
#     3. **Usability Enhancements:**
#        - Add genre filtering capabilities
#        - Implement territory-specific versions of the algorithm
#        - Create drilldown capabilities for artist details
    
#     4. **Collaboration with A&R Team:**
#        - Share initial results with Jordan and Jalen
#        - Cross-reference algorithmic picks with their manual selections
#        - Identify patterns and blind spots in the current algorithm
#     """)

# # Footer
# st.markdown("---")
# st.caption("Audiomack ArtistRank Dashboard | Last updated: April 3, 2025")
# st.caption("Created by LinLin for Audiomack Internship Program")











# # # Linlin GET INTO AUDIOMAC INTERN PREVIOUS CODE
# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # import json
# # import os

# # # Set page configuration
# # st.set_page_config(
# #     page_title="Music Data Analysis Dashboard",
# #     page_icon="🎵",
# #     layout="wide"
# # )

# # # Function to load JSON data
# # @st.cache_data
# # def load_data():
# #     # Sample data based on your JSON structure
# #     # In production, you would load these from files
    
# #     # Top songs by download ratio
# #     top_download_ratio = pd.DataFrame([
# #         {
# #             "music_id": 1,
# #             "song_name": "Have Mercy",
# #             "artist_name": "Shane Eli",
# #             "total_plays": 207866,
# #             "total_downloads": 7207622,
# #             "download_play_ratio": 34.6744,
# #             "total_favorites": 612,
# #             "total_playlist_adds": 5973,
# #             "total_reposts": 105,
# #             "favorite_play_ratio": 0.0029,
# #             "playlist_play_ratio": 0.0287,
# #             "repost_play_ratio": 0.0005,
# #             "engagement_score": 10.41186
# #         },
# #         {
# #             "music_id": 23455165,
# #             "song_name": "Pluto",
# #             "artist_name": "Shallipopi",
# #             "total_plays": 3990,
# #             "total_downloads": 42318,
# #             "download_play_ratio": 10.6060,
# #             "total_favorites": 158,
# #             "total_playlist_adds": 58,
# #             "total_reposts": 25,
# #             "favorite_play_ratio": 0.0396,
# #             "playlist_play_ratio": 0.0145,
# #             "repost_play_ratio": 0.0063,
# #             "engagement_score": 3.19867
# #         },
# #         {
# #             "music_id": 37403686,
# #             "song_name": "Joy is coming",
# #             "artist_name": "Fido",
# #             "total_plays": 5976,
# #             "total_downloads": 35935,
# #             "download_play_ratio": 6.0132,
# #             "total_favorites": 302,
# #             "total_playlist_adds": 230,
# #             "total_reposts": 35,
# #             "favorite_play_ratio": 0.0505,
# #             "playlist_play_ratio": 0.0385,
# #             "repost_play_ratio": 0.0059,
# #             "engagement_score": 1.83126
# #         },
# #         {
# #             "music_id": 32475125,
# #             "song_name": "APartii",
# #             "artist_name": "Combosman X Togman",
# #             "total_plays": 9612,
# #             "total_downloads": 40354,
# #             "download_play_ratio": 4.1983,
# #             "total_favorites": 532,
# #             "total_playlist_adds": 1122,
# #             "total_reposts": 19,
# #             "favorite_play_ratio": 0.0553,
# #             "playlist_play_ratio": 0.1167,
# #             "repost_play_ratio": 0.0020,
# #             "engagement_score": 1.31131
# #         },
# #         {
# #             "music_id": 31809979,
# #             "song_name": "juju",
# #             "artist_name": "Big smur lee",
# #             "total_plays": 32581,
# #             "total_downloads": 132987,
# #             "download_play_ratio": 4.0817,
# #             "total_favorites": 1601,
# #             "total_playlist_adds": 1435,
# #             "total_reposts": 86,
# #             "favorite_play_ratio": 0.0491,
# #             "playlist_play_ratio": 0.0440,
# #             "repost_play_ratio": 0.0026,
# #             "engagement_score": 1.25274
# #         }
# #     ])
    
# #     # Country analysis
# #     country_analysis = pd.DataFrame([
# #         {
# #             "geo_country": "NG",
# #             "unique_songs": 43692,
# #             "unique_artists": 16867,
# #             "total_plays": 4921728863,
# #             "download_rate": 0.1943,
# #             "favorite_rate": 0.0046,
# #             "playlist_rate": 0.0106,
# #             "repost_rate": 0.0003
# #         },
# #         {
# #             "geo_country": "GH",
# #             "unique_songs": 12605,
# #             "unique_artists": 4635,
# #             "total_plays": 1103037822,
# #             "download_rate": 0.3144,
# #             "favorite_rate": 0.0063,
# #             "playlist_rate": 0.0252,
# #             "repost_rate": 0.0003
# #         },
# #         {
# #             "geo_country": "US",
# #             "unique_songs": 20239,
# #             "unique_artists": 6993,
# #             "total_plays": 984556737,
# #             "download_rate": 0.0853,
# #             "favorite_rate": 0.0127,
# #             "playlist_rate": 0.0186,
# #             "repost_rate": 0.0002
# #         },
# #         {
# #             "geo_country": "JM",
# #             "unique_songs": 4037,
# #             "unique_artists": 1030,
# #             "total_plays": 286628266,
# #             "download_rate": 0.1740,
# #             "favorite_rate": 0.0036,
# #             "playlist_rate": 0.0109,
# #             "repost_rate": 0.0002
# #         },
# #         {
# #             "geo_country": "TZ",
# #             "unique_songs": 2055,
# #             "unique_artists": 944,
# #             "total_plays": 124558960,
# #             "download_rate": 0.3162,
# #             "favorite_rate": 0.0041,
# #             "playlist_rate": 0.0203,
# #             "repost_rate": 0.0002
# #         }
# #     ])
    
# #     # Hidden gems
# #     hidden_gems = pd.DataFrame([
# #         {
# #             "music_id": 31809979,
# #             "song_name": "juju",
# #             "artist_name": "Big smur lee",
# #             "total_plays": 32581,
# #             "total_downloads": 132987,
# #             "favorite_ratio": 0.0491,
# #             "playlist_ratio": 0.0440,
# #             "engagement_score": 1.25274
# #         },
# #         {
# #             "music_id": 26325473,
# #             "song_name": "Medicine after death",
# #             "artist_name": "Mohbad",
# #             "total_plays": 4019,
# #             "total_downloads": 16303,
# #             "favorite_ratio": 0.0475,
# #             "playlist_ratio": 0.0236,
# #             "engagement_score": 1.23872
# #         },
# #         {
# #             "music_id": 29326228,
# #             "song_name": "Twe Twe (remix)",
# #             "artist_name": "Kizz Daniel",
# #             "total_plays": 8614,
# #             "total_downloads": 34749,
# #             "favorite_ratio": 0.0358,
# #             "playlist_ratio": 0.0411,
# #             "engagement_score": 1.23363
# #         },
# #         {
# #             "music_id": 27038877,
# #             "song_name": "Area Boys prayers",
# #             "artist_name": "Seyi vibez",
# #             "total_plays": 4425,
# #             "total_downloads": 16386,
# #             "favorite_ratio": 0.0298,
# #             "playlist_ratio": 0.0280,
# #             "engagement_score": 1.12861
# #         },
# #         {
# #             "music_id": 24215772,
# #             "song_name": "Gbona",
# #             "artist_name": "Zinoleesky",
# #             "total_plays": 7899,
# #             "total_downloads": 26930,
# #             "favorite_ratio": 0.0457,
# #             "playlist_ratio": 0.0575,
# #             "engagement_score": 1.05420
# #         }
# #     ])
    
# #     # Top artists by song count
# #     top_artists = pd.DataFrame([
# #         {
# #             "artist_name": "Juice WRLD",
# #             "song_count": 538,
# #             "total_plays": 72475641,
# #             "avg_plays_per_song": 13357.1030
# #         },
# #         {
# #             "artist_name": "KIRAT",
# #             "song_count": 359,
# #             "total_plays": 11619281,
# #             "avg_plays_per_song": 8102.7064
# #         },
# #         {
# #             "artist_name": "Dj Wizkel",
# #             "song_count": 344,
# #             "total_plays": 30548286,
# #             "avg_plays_per_song": 14058.1160
# #         },
# #         {
# #             "artist_name": "SHATTA WALE",
# #             "song_count": 337,
# #             "total_plays": 104034146,
# #             "avg_plays_per_song": 20723.9335
# #         },
# #         {
# #             "artist_name": "NBA YoungBoy",
# #             "song_count": 327,
# #             "total_plays": 24226846,
# #             "avg_plays_per_song": 9012.9635
# #         },
# #         {
# #             "artist_name": "DJ Amacoz",
# #             "song_count": 286,
# #             "total_plays": 76663196,
# #             "avg_plays_per_song": 33787.2173
# #         },
# #         {
# #             "artist_name": "Seyi Vibez",
# #             "song_count": 257,
# #             "total_plays": 50295331,
# #             "avg_plays_per_song": 25952.1832
# #         },
# #         {
# #             "artist_name": "YoungBoy Never Broke Again",
# #             "song_count": 250,
# #             "total_plays": 17216580,
# #             "avg_plays_per_song": 11186.8616
# #         },
# #         {
# #             "artist_name": "Chronic Law",
# #             "song_count": 241,
# #             "total_plays": 25692133,
# #             "avg_plays_per_song": 10338.8865
# #         },
# #         {
# #             "artist_name": "Mohbad",
# #             "song_count": 236,
# #             "total_plays": 119361030,
# #             "avg_plays_per_song": 35261.7518
# #         }
# #     ])
    
# #     # Artist engagement comparison
# #     artist_engagement = pd.DataFrame([
# #         {
# #             "artist_name": "Mama le succès",
# #             "song_count": 15,
# #             "avg_engagement_score": 0.404562989
# #         },
# #         {
# #             "artist_name": "Big Smur Lee",
# #             "song_count": 8,
# #             "avg_engagement_score": 0.358251483
# #         },
# #         {
# #             "artist_name": "Dj Amass",
# #             "song_count": 7,
# #             "avg_engagement_score": 0.269453664
# #         },
# #         {
# #             "artist_name": "djmysterioghana",
# #             "song_count": 6,
# #             "avg_engagement_score": 0.254437576
# #         },
# #         {
# #             "artist_name": "Iba Montana",
# #             "song_count": 10,
# #             "avg_engagement_score": 0.245587765
# #         },
# #         {
# #             "artist_name": "Adomba Fausty",
# #             "song_count": 9,
# #             "avg_engagement_score": 0.237230024
# #         },
# #         {
# #             "artist_name": "DJ MENTOS",
# #             "song_count": 6,
# #             "avg_engagement_score": 0.231980866
# #         },
# #         {
# #             "artist_name": "Obaapa Christy",
# #             "song_count": 22,
# #             "avg_engagement_score": 0.224386569
# #         },
# #         {
# #             "artist_name": "Dj Wasty Kay",
# #             "song_count": 18,
# #             "avg_engagement_score": 0.219959456
# #         },
# #         {
# #             "artist_name": "Kwaku smoke",
# #             "song_count": 6,
# #             "avg_engagement_score": 0.213171093
# #         }
# #     ])
    
# #     # Engagement benchmarks
# #     benchmarks = pd.DataFrame([
# #         {
# #             "metric": "Downloads",
# #             "average_ratio": 0.19943922,
# #             "highest_ratio": 84.3617
# #         },
# #         {
# #             "metric": "Favorites",
# #             "average_ratio": 0.00722445,
# #             "highest_ratio": 2.6768
# #         },
# #         {
# #             "metric": "Playlists",
# #             "average_ratio": 0.01700405,
# #             "highest_ratio": 3.1849
# #         },
# #         {
# #             "metric": "Reposts",
# #             "average_ratio": 0.00026425,
# #             "highest_ratio": 0.3487
# #         }
# #     ])
    
# #     # DJ Mix vs Single Track Analysis
# #     dj_single = pd.DataFrame([
# #         {
# #             "content_type": "DJ Mix",
# #             "track_count": 9034,
# #             "avg_download_ratio": 0.29938929,
# #             "avg_favorite_ratio": 0.00778788,
# #             "avg_playlist_ratio": 0.01570945
# #         },
# #         {
# #             "content_type": "Single Track",
# #             "track_count": 71004,
# #             "avg_download_ratio": 0.18866509,
# #             "avg_favorite_ratio": 0.00716354,
# #             "avg_playlist_ratio": 0.01714273
# #         }
# #     ])
    
# #     # Monthly analysis
# #     monthly_analysis = pd.DataFrame([
# #         {
# #             "month_str": "2023-04",
# #             "unique_songs": 19723,
# #             "total_plays": 296749194,
# #             "download_rate": 0.1859,
# #             "favorite_rate": 0.0063
# #         },
# #         {
# #             "month_str": "2023-05",
# #             "unique_songs": 26097,
# #             "total_plays": 433438893,
# #             "download_rate": 0.1432,
# #             "favorite_rate": 0.0050
# #         },
# #         {
# #             "month_str": "2023-06",
# #             "unique_songs": 25314,
# #             "total_plays": 409287750,
# #             "download_rate": 0.1539,
# #             "favorite_rate": 0.0051
# #         },
# #         {
# #             "month_str": "2023-07",
# #             "unique_songs": 20650,
# #             "total_plays": 291190895,
# #             "download_rate": 0.2027,
# #             "favorite_rate": 0.0069
# #         },
# #         {
# #             "month_str": "2023-08",
# #             "unique_songs": 22854,
# #             "total_plays": 324336447,
# #             "download_rate": 0.1952,
# #             "favorite_rate": 0.0065
# #         },
# #         {
# #             "month_str": "2023-09",
# #             "unique_songs": 22873,
# #             "total_plays": 329623842,
# #             "download_rate": 0.1980,
# #             "favorite_rate": 0.0065
# #         },
# #         {
# #             "month_str": "2023-10",
# #             "unique_songs": 24746,
# #             "total_plays": 369916905,
# #             "download_rate": 0.1898,
# #             "favorite_rate": 0.0065
# #         },
# #         {
# #             "month_str": "2023-11",
# #             "unique_songs": 24940,
# #             "total_plays": 362235739,
# #             "download_rate": 0.1875,
# #             "favorite_rate": 0.0061
# #         },
# #         {
# #             "month_str": "2023-12",
# #             "unique_songs": 26614,
# #             "total_plays": 399588966,
# #             "download_rate": 0.1932,
# #             "favorite_rate": 0.0060
# #         },
# #         {
# #             "month_str": "2024-01",
# #             "unique_songs": 25525,
# #             "total_plays": 385683603,
# #             "download_rate": 0.1951,
# #             "favorite_rate": 0.0059
# #         },
# #         {
# #             "month_str": "2024-02",
# #             "unique_songs": 23263,
# #             "total_plays": 333443551,
# #             "download_rate": 0.1879,
# #             "favorite_rate": 0.0056
# #         },
# #         {
# #             "month_str": "2024-03",
# #             "unique_songs": 24509,
# #             "total_plays": 351750156,
# #             "download_rate": 0.2034,
# #             "favorite_rate": 0.0057
# #         },
# #         {
# #             "month_str": "2024-04",
# #             "unique_songs": 24584,
# #             "total_plays": 360657522,
# #             "download_rate": 0.2161,
# #             "favorite_rate": 0.0060
# #         },
# #         {
# #             "month_str": "2024-05",
# #             "unique_songs": 26597,
# #             "total_plays": 405513449,
# #             "download_rate": 0.2299,
# #             "favorite_rate": 0.0058
# #         },
# #         {
# #             "month_str": "2024-06",
# #             "unique_songs": 26172,
# #             "total_plays": 397425211,
# #             "download_rate": 0.2315,
# #             "favorite_rate": 0.0055
# #         },
# #         {
# #             "month_str": "2024-07",
# #             "unique_songs": 26432,
# #             "total_plays": 411944638,
# #             "download_rate": 0.2198,
# #             "favorite_rate": 0.0059
# #         },
# #         {
# #             "month_str": "2024-08",
# #             "unique_songs": 27831,
# #             "total_plays": 424523455,
# #             "download_rate": 0.2142,
# #             "favorite_rate": 0.0059
# #         },
# #         {
# #             "month_str": "2024-09",
# #             "unique_songs": 27116,
# #             "total_plays": 404860879,
# #             "download_rate": 0.2064,
# #             "favorite_rate": 0.0061
# #         },
# #         {
# #             "month_str": "2024-10",
# #             "unique_songs": 27640,
# #             "total_plays": 419514856,
# #             "download_rate": 0.2000,
# #             "favorite_rate": 0.0064
# #         },
# #         {
# #             "month_str": "2024-11",
# #             "unique_songs": 25658,
# #             "total_plays": 433059119,
# #             "download_rate": 0.2030,
# #             "favorite_rate": 0.0067
# #         },
# #         {
# #             "month_str": "2024-12",
# #             "unique_songs": 28847,
# #             "total_plays": 479840220,
# #             "download_rate": 0.2002,
# #             "favorite_rate": 0.0066
# #         }
# #     ])

# #     # Process top engagement data
# #     top_engagement_df = top_download_ratio.copy()
# #     top_engagement_df['song'] = top_engagement_df['song_name'] + " by " + top_engagement_df['artist_name']
# #     # Create a unique identifier for each song to prevent confusion with same song names
# #     top_engagement_df['song_id'] = top_engagement_df['music_id'].astype(str)
# #     top_engagement_df['downloadRatio'] = top_engagement_df['download_play_ratio']
# #     top_engagement_df['favoritesRatio'] = top_engagement_df['favorite_play_ratio']
# #     top_engagement_df['playlistRatio'] = top_engagement_df['playlist_play_ratio']
# #     top_engagement_df['repostsRatio'] = top_engagement_df['repost_play_ratio']
# #     top_engagement_df['engagement'] = top_engagement_df['engagement_score']
# #     top_engagement_df['plays'] = top_engagement_df['total_plays']
    
# #     # Process country data
# #     country_df = pd.DataFrame({
# #         'country': country_analysis['geo_country'],
# #         'totalPlay30s': country_analysis['total_plays'],
# #         'downloadRate': country_analysis['download_rate'],
# #         'favoriteRate': country_analysis['favorite_rate'],
# #         'playlistRate': country_analysis['playlist_rate'],
# #         'songCount': country_analysis['unique_songs'],
# #         'artistCount': country_analysis['unique_artists']
# #     })
    
# #     # Process hidden gems data
# #     hidden_gems_df = hidden_gems.copy()
# #     hidden_gems_df['song'] = hidden_gems_df['song_name'] + " by " + hidden_gems_df['artist_name']
# #     # Create a unique identifier for each song
# #     hidden_gems_df['song_id'] = hidden_gems_df['music_id'].astype(str)
# #     hidden_gems_df['engagementRatio'] = hidden_gems_df['engagement_score']
# #     hidden_gems_df['plays'] = hidden_gems_df['total_plays']
    
# #     # Process benchmark data
# #     benchmark_df = pd.DataFrame({
# #         'name': benchmarks['metric'],
# #         'average': benchmarks['average_ratio'],
# #         'highest': benchmarks['highest_ratio']
# #     })
    
# #     # Monthly trend data
# #     monthly_df = monthly_analysis.sort_values('month_str')
    
# #     # DJ vs Single comparison
# #     dj_single_df = dj_single

# #     return top_engagement_df, country_df, hidden_gems_df, top_artists, artist_engagement, benchmark_df, monthly_df, dj_single_df

# # # Load data
# # try:
# #     top_engagement_df, country_df, hidden_gems_df, top_artists_df, artist_engagement_df, benchmark_df, monthly_df, dj_single_df = load_data()
# #     data_loaded = True
# # except Exception as e:
# #     st.error(f"Error loading data: {e}")
# #     data_loaded = False

# # # Dashboard title and description
# # st.title("Music Data Analysis Dashboard")
# # st.write("UGC Music Upload Analysis (04/2023-12/2024) for songs across multiple countries")

# # # Add a note about song identification
# # st.info("""
# # **Note on Song Identification**: Some songs may share the same title but have different artists. 
# # Throughout this dashboard, songs are uniquely identified by both song name and artist name, and internally by a unique music_id.
# # """)

# # # Create tabs
# # tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
# #     "Engagement Analysis", 
# #     "Country Analysis", 
# #     "Hidden Gems", 
# #     "Top Artists", 
# #     "Trends",
# #     "Benchmarks"
# # ])

# # # Tab 1: Engagement Analysis
# # with tab1:
# #     st.header("Top Songs by Engagement Score")
# #     st.write("Engagement score combines download, favorite, playlist, and repost ratios")
    
# #     # Create the engagement score chart
# #     fig1 = px.bar(
# #         top_engagement_df,
# #         x="song",
# #         y="engagement",
# #         title="Top Songs by Engagement Score",
# #         labels={"engagement": "Engagement Score", "song": "Song"},
# #         color_discrete_sequence=["#8884d8"],
# #         hover_data=["music_id", "total_plays", "total_downloads"]  # Add more context in hover
# #     )
# #     fig1.update_layout(xaxis={'categoryorder':'total descending'})
# #     st.plotly_chart(fig1, use_container_width=True)
    
# #     # Create the metrics breakdown chart
# #     st.header("Engagement Metrics Breakdown")
# #     st.write("Detailed breakdown of different engagement metrics for top performers")
    
# #     metrics_df = top_engagement_df.melt(
# #         id_vars=["song"],
# #         value_vars=["downloadRatio", "favoritesRatio", "playlistRatio"],
# #         var_name="Metric",
# #         value_name="Value"
# #     )
    
# #     # Replace metric names for better readability
# #     metrics_df["Metric"] = metrics_df["Metric"].map({
# #         "downloadRatio": "Download Ratio",
# #         "favoritesRatio": "Favorites Ratio",
# #         "playlistRatio": "Playlist Ratio"
# #     })
    
# #     fig2 = px.bar(
# #         metrics_df,
# #         x="song",
# #         y="Value",
# #         color="Metric",
# #         barmode="group",
# #         title="Engagement Metrics Breakdown",
# #         color_discrete_map={
# #             "Download Ratio": "#0088FE",
# #             "Favorites Ratio": "#00C49F",
# #             "Playlist Ratio": "#FFBB28"
# #         }
# #     )
# #     fig2.update_layout(xaxis={'categoryorder':'total descending'})
# #     st.plotly_chart(fig2, use_container_width=True)
    
# #     # Content Type Comparison
# #     st.header("Content Type Comparison")
# #     st.write("Engagement metrics comparison between DJ mixes and single tracks")
    
# #     fig_content = px.bar(
# #         dj_single_df,
# #         x="content_type",
# #         y=["avg_download_ratio", "avg_favorite_ratio", "avg_playlist_ratio"],
# #         barmode="group",
# #         title="DJ Mixes vs. Single Tracks Engagement",
# #         labels={
# #             "value": "Average Ratio",
# #             "content_type": "Content Type",
# #             "variable": "Metric Type"
# #         },
# #         color_discrete_map={
# #             "avg_download_ratio": "#0088FE",
# #             "avg_favorite_ratio": "#00C49F",
# #             "avg_playlist_ratio": "#FFBB28"
# #         }
# #     )
# #     st.plotly_chart(fig_content, use_container_width=True)

# # # Tab 2: Country Analysis
# # with tab2:
# #     st.header("Country Play Distribution")
    
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         # Create the pie chart for play distribution
# #         fig3 = px.pie(
# #             country_df,
# #             values="totalPlay30s",
# #             names="country",
# #             title="Total Plays by Country",
# #             color_discrete_sequence=px.colors.qualitative.Set3
# #         )
# #         fig3.update_traces(textposition='inside', textinfo='percent+label')
# #         st.plotly_chart(fig3, use_container_width=True)
    
# #     with col2:
# #         # Create the bar chart for engagement rates by country
# #         fig4 = go.Figure()
# #         fig4.add_trace(go.Bar(
# #             x=country_df["country"],
# #             y=country_df["downloadRate"],
# #             name="Download Rate",
# #             marker_color="#0088FE"
# #         ))
# #         fig4.add_trace(go.Bar(
# #             x=country_df["country"],
# #             y=country_df["favoriteRate"],
# #             name="Favorite Rate",
# #             marker_color="#00C49F"
# #         ))
# #         fig4.add_trace(go.Bar(
# #             x=country_df["country"],
# #             y=country_df["playlistRate"],
# #             name="Playlist Rate",
# #             marker_color="#FFBB28"
# #         ))
# #         fig4.update_layout(
# #             title="Engagement Rates by Country",
# #             barmode="group"
# #         )
# #         st.plotly_chart(fig4, use_container_width=True)
    
# #     # Create the song & artist distribution chart
# #     st.header("Song & Artist Distribution by Country")
    
# #     fig5 = go.Figure()
# #     fig5.add_trace(go.Bar(
# #         x=country_df["country"],
# #         y=country_df["songCount"],
# #         name="Number of Songs",
# #         marker_color="#8884d8"
# #     ))
# #     fig5.add_trace(go.Bar(
# #         x=country_df["country"],
# #         y=country_df["artistCount"],
# #         name="Number of Artists",
# #         marker_color="#82ca9d"
# #     ))
# #     fig5.update_layout(
# #         title="Song & Artist Distribution by Country",
# #         barmode="group"
# #     )
# #     st.plotly_chart(fig5, use_container_width=True)

# # # Tab 3: Hidden Gems
# # with tab3:
# #     st.header("Hidden Gems (High Engagement, Moderate Plays)")
# #     st.write("Songs with exceptional engagement metrics that haven't yet reached massive play counts")
    
# #     # Create dual axis chart for hidden gems
# #     fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
# #     fig6.add_trace(
# #         go.Bar(
# #             x=hidden_gems_df["song"],
# #             y=hidden_gems_df["engagementRatio"],
# #             name="Engagement Ratio",
# #             marker_color="#8884d8"
# #         ),
# #         secondary_y=False
# #     )
    
# #     fig6.add_trace(
# #         go.Bar(
# #             x=hidden_gems_df["song"],
# #             y=hidden_gems_df["plays"],
# #             name="Total Plays (30s+)",
# #             marker_color="#82ca9d"
# #         ),
# #         secondary_y=True
# #     )
    
# #     fig6.update_layout(
# #         title_text="Hidden Gems: Engagement vs Plays",
# #         xaxis=dict(title="Song")
# #     )
    
# #     fig6.update_yaxes(title_text="Engagement Ratio", secondary_y=False)
# #     fig6.update_yaxes(title_text="Total Plays", secondary_y=True)
    
# #     st.plotly_chart(fig6, use_container_width=True)
    
# #     # Create the engagement breakdown for hidden gems
# #     st.header("Hidden Gems Engagement Breakdown")
    
# #     metrics_df2 = hidden_gems_df.melt(
# #         id_vars=["song"],
# #         value_vars=["favorite_ratio", "playlist_ratio"],
# #         var_name="Metric",
# #         value_name="Value"
# #     )
    
# #     metrics_df2["Metric"] = metrics_df2["Metric"].map({
# #         "favorite_ratio": "Favorite Ratio",
# #         "playlist_ratio": "Playlist Ratio"
# #     })
    
# #     fig7 = px.bar(
# #         metrics_df2,
# #         x="song",
# #         y="Value",
# #         color="Metric",
# #         barmode="group",
# #         title="Engagement Metrics Breakdown for Hidden Gems",
# #         color_discrete_map={
# #             "Favorite Ratio": "#00C49F",
# #             "Playlist Ratio": "#FFBB28"
# #         }
# #     )
# #     st.plotly_chart(fig7, use_container_width=True)

# # # Tab 4: Top Artists
# # with tab4:
# #     st.header("Top Artists by Song Count")
# #     st.write("Artists with multiple songs in the dataset")
    
# #     # Sort artists by song count
# #     sorted_artists = top_artists_df.sort_values(by="song_count", ascending=False)
    
# #     # Add additional analysis for artist name verification
# #     st.subheader("Data Quality Check")
# #     st.write("""
# #     The dashboard ensures accurate artist identification by using unique artist names.
# #     You may find similar artist names in the data (e.g., 'NBA YoungBoy' and 'YoungBoy Never Broke Again')
# #     that are treated as separate artists based on how they were originally credited.
# #     """)
    
# #     fig8 = px.bar(
# #         sorted_artists.head(10),
# #         x="artist_name",
# #         y="song_count",
# #         title="Top Artists by Song Count",
# #         color_discrete_sequence=["#8884d8"],
# #         hover_data=["total_plays", "avg_plays_per_song"]  # Add more context
# #     )
# #     st.plotly_chart(fig8, use_container_width=True)
    
# #     # Create the artist engagement comparison
# #     st.header("Artist Engagement Comparison")
    
# #     fig9 = px.bar(
# #         artist_engagement_df,
# #         x="artist_name",
# #         y="avg_engagement_score",
# #         title="Average Engagement Score by Artist",
# #         color_discrete_sequence=["#FF8042"]
# #     )
# #     fig9.update_layout(yaxis_title="Average Engagement Score")
# #     st.plotly_chart(fig9, use_container_width=True)

# # # Tab 5: Trends
# # with tab5:
# #     st.header("Monthly Trends")
# #     st.write("How engagement metrics have changed over time")
    
# #     # Create line chart for monthly trends
# #     fig_monthly = go.Figure()
# #     fig_monthly.add_trace(go.Scatter(
# #         x=monthly_df["month_str"],
# #         y=monthly_df["download_rate"],
# #         mode='lines+markers',
# #         name='Download Rate',
# #         line=dict(color="#0088FE")
# #     ))
# #     fig_monthly.add_trace(go.Scatter(
# #         x=monthly_df["month_str"],
# #         y=monthly_df["favorite_rate"],
# #         mode='lines+markers',
# #         name='Favorite Rate',
# #         line=dict(color="#00C49F")
# #     ))
# #     fig_monthly.update_layout(
# #         title="Monthly Engagement Rates",
# #         xaxis_title="Month",
# #         yaxis_title="Engagement Rate"
# #     )
# #     st.plotly_chart(fig_monthly, use_container_width=True)
    
# #     # Monthly plays and unique songs
# #     fig_plays = go.Figure()
    
# #     # Create a secondary y-axis plot
# #     fig_plays = make_subplots(specs=[[{"secondary_y": True}]])
    
# #     fig_plays.add_trace(
# #         go.Scatter(
# #             x=monthly_df["month_str"],
# #             y=monthly_df["total_plays"],
# #             mode="lines+markers",
# #             name="Total Plays",
# #             line=dict(color="#8884d8")
# #         ),
# #         secondary_y=False
# #     )
    
# #     fig_plays.add_trace(
# #         go.Scatter(
# #             x=monthly_df["month_str"],
# #             y=monthly_df["unique_songs"],
# #             mode="lines+markers",
# #             name="Unique Songs",
# #             line=dict(color="#82ca9d")
# #         ),
# #         secondary_y=True
# #     )
    
# #     fig_plays.update_layout(
# #         title="Monthly Plays and Song Volume",
# #         xaxis_title="Month"
# #     )
    
# #     fig_plays.update_yaxes(title_text="Total Plays", secondary_y=False)
# #     fig_plays.update_yaxes(title_text="Unique Songs", secondary_y=True)
    
# #     st.plotly_chart(fig_plays, use_container_width=True)

# # # Tab 6: Benchmarks
# # with tab6:
# #     st.header("Engagement Benchmarks")
# #     st.write("Average vs. Highest engagement metrics across the dataset")
    
# #     # Create the benchmark comparison chart
# #     benchmark_melted = benchmark_df.melt(
# #         id_vars=["name"],
# #         value_vars=["average", "highest"],
# #         var_name="Metric",
# #         value_name="Value"
# #     )
    
# #     benchmark_melted["Metric"] = benchmark_melted["Metric"].map({
# #         "average": "Average Ratio",
# #         "highest": "Highest Ratio"
# #     })
    
# #     fig10 = px.bar(
# #         benchmark_melted,
# #         x="name",
# #         y="Value",
# #         color="Metric",
# #         barmode="group",
# #         title="Engagement Benchmarks: Average vs Highest",
# #         color_discrete_map={
# #             "Average Ratio": "#8884d8",
# #             "Highest Ratio": "#82ca9d"
# #         },
# #         log_y=True  # Using log scale for better visualization
# #     )
# #     fig10.update_layout(xaxis_title="Metric", yaxis_title="Ratio Value (Log Scale)")
# #     st.plotly_chart(fig10, use_container_width=True)

# # # Key Findings section
# # st.header("Key Findings")
# # st.markdown("""
# # ### 1. Early Indicators of Success

# # Our analysis reveals that **download-to-play ratio** is the most reliable predictor of sustained song success. With a platform-wide average of 0.199, songs exceeding 0.3 demonstrate exceptional user commitment.

# # ### 2. Geographic Trends 

# # **Country-specific engagement patterns** show distinct market behaviors:
# # - **Nigeria (NG)**: Highest volume (4.9B+ plays) with moderate engagement rates (19.4% download rate)
# # - **Ghana (GH)**: Highest download rate (31.4%) suggesting strong offline listening culture
# # - **United States (US)**: Highest favorite rate (1.27%) and strong playlist activity (1.86%)

# # ### 3. Content Format Impact

# # **DJ mixes consistently outperform single tracks** with 58.7% higher download rates (0.299 vs 0.189), particularly strong in African markets.

# # ### 4. Hidden Gems

# # Several promising tracks show exceptional engagement despite moderate play counts:
# # - **"juju" by Big smur lee** (32,581 plays, 1.25 engagement score)
# # - **"Medicine after death" by Mohbad** (4,019 plays, 1.24 engagement score)
# # - **"Twe Twe (remix)" by Kizz Daniel** (8,614 plays, 1.23 engagement score)

# # ### 5. Artist Insights

# # **Juice WRLD, KIRAT, and DJ Wizkel** lead in content volume with hundreds of songs each, while **Mama le succès and Big Smur Lee** deliver the highest average engagement quality despite having fewer songs.

# # ### 6. Temporal Patterns

# # Analysis across 21 months shows increasing download rates (from 14.3% to 23.2%) with consistent seasonal peaks in December.
# # """)

# # # Recommendations section
# # st.header("Recommendations")
# # st.markdown("""
# # ### For Platform Optimization:
# # - Implement algorithmic emphasis on download-to-play ratio in recommendation engines
# # - Create dedicated "Hidden Gems" discovery section featuring high-engagement but moderately-played content
# # - Develop market-specific algorithms accounting for regional engagement preferences
# # - Target cross-country content promotion for Ghana→US content flow

# # ### For Content Strategy:
# # - Increase promotion of DJ mixes and compilations, particularly in African markets
# # - Spotlight emerging artists with high engagement ratios but moderate plays
# # - Implement A/B testing of playlist strategies specifically for US-based content
# # - Develop features to encourage and track offline listening

# # ### For Talent Acquisition:
# # - Prioritize artists with consistently high engagement metrics across multiple songs
# # - Evaluate artists like Mama le succès and Big Smur Lee for potential partnerships
# # - Look beyond raw play counts to identify rising talent with exceptional engagement
# # """)



# # # import streamlit as st
# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from plotly.subplots import make_subplots
# # # import json
# # # import os

# # # # Set page configuration
# # # st.set_page_config(
# # #     page_title="Music Data Analysis Dashboard",
# # #     page_icon="🎵",
# # #     layout="wide"
# # # )

# # # # Function to load JSON data
# # # @st.cache_data
# # # def load_data():
# # #     # Sample data based on your JSON structure
# # #     # In production, you would load these from files
    
# # #     # Top songs by download ratio
# # #     top_download_ratio = pd.DataFrame([
# # #         {
# # #             "music_id": 1,
# # #             "song_name": "Have Mercy",
# # #             "artist_name": "Shane Eli",
# # #             "total_plays": 207866,
# # #             "total_downloads": 7207622,
# # #             "download_play_ratio": 34.6744,
# # #             "total_favorites": 612,
# # #             "total_playlist_adds": 5973,
# # #             "total_reposts": 105,
# # #             "favorite_play_ratio": 0.0029,
# # #             "playlist_play_ratio": 0.0287,
# # #             "repost_play_ratio": 0.0005,
# # #             "engagement_score": 10.41186
# # #         },
# # #         {
# # #             "music_id": 23455165,
# # #             "song_name": "Pluto",
# # #             "artist_name": "Shallipopi",
# # #             "total_plays": 3990,
# # #             "total_downloads": 42318,
# # #             "download_play_ratio": 10.6060,
# # #             "total_favorites": 158,
# # #             "total_playlist_adds": 58,
# # #             "total_reposts": 25,
# # #             "favorite_play_ratio": 0.0396,
# # #             "playlist_play_ratio": 0.0145,
# # #             "repost_play_ratio": 0.0063,
# # #             "engagement_score": 3.19867
# # #         },
# # #         {
# # #             "music_id": 37403686,
# # #             "song_name": "Joy is coming",
# # #             "artist_name": "Fido",
# # #             "total_plays": 5976,
# # #             "total_downloads": 35935,
# # #             "download_play_ratio": 6.0132,
# # #             "total_favorites": 302,
# # #             "total_playlist_adds": 230,
# # #             "total_reposts": 35,
# # #             "favorite_play_ratio": 0.0505,
# # #             "playlist_play_ratio": 0.0385,
# # #             "repost_play_ratio": 0.0059,
# # #             "engagement_score": 1.83126
# # #         },
# # #         {
# # #             "music_id": 32475125,
# # #             "song_name": "APartii",
# # #             "artist_name": "Combosman X Togman",
# # #             "total_plays": 9612,
# # #             "total_downloads": 40354,
# # #             "download_play_ratio": 4.1983,
# # #             "total_favorites": 532,
# # #             "total_playlist_adds": 1122,
# # #             "total_reposts": 19,
# # #             "favorite_play_ratio": 0.0553,
# # #             "playlist_play_ratio": 0.1167,
# # #             "repost_play_ratio": 0.0020,
# # #             "engagement_score": 1.31131
# # #         },
# # #         {
# # #             "music_id": 31809979,
# # #             "song_name": "juju",
# # #             "artist_name": "Big smur lee",
# # #             "total_plays": 32581,
# # #             "total_downloads": 132987,
# # #             "download_play_ratio": 4.0817,
# # #             "total_favorites": 1601,
# # #             "total_playlist_adds": 1435,
# # #             "total_reposts": 86,
# # #             "favorite_play_ratio": 0.0491,
# # #             "playlist_play_ratio": 0.0440,
# # #             "repost_play_ratio": 0.0026,
# # #             "engagement_score": 1.25274
# # #         }
# # #     ])
    
# # #     # Country analysis
# # #     country_analysis = pd.DataFrame([
# # #         {
# # #             "geo_country": "NG",
# # #             "unique_songs": 43692,
# # #             "unique_artists": 16867,
# # #             "total_plays": 4921728863,
# # #             "download_rate": 0.1943,
# # #             "favorite_rate": 0.0046,
# # #             "playlist_rate": 0.0106,
# # #             "repost_rate": 0.0003
# # #         },
# # #         {
# # #             "geo_country": "GH",
# # #             "unique_songs": 12605,
# # #             "unique_artists": 4635,
# # #             "total_plays": 1103037822,
# # #             "download_rate": 0.3144,
# # #             "favorite_rate": 0.0063,
# # #             "playlist_rate": 0.0252,
# # #             "repost_rate": 0.0003
# # #         },
# # #         {
# # #             "geo_country": "US",
# # #             "unique_songs": 20239,
# # #             "unique_artists": 6993,
# # #             "total_plays": 984556737,
# # #             "download_rate": 0.0853,
# # #             "favorite_rate": 0.0127,
# # #             "playlist_rate": 0.0186,
# # #             "repost_rate": 0.0002
# # #         },
# # #         {
# # #             "geo_country": "JM",
# # #             "unique_songs": 4037,
# # #             "unique_artists": 1030,
# # #             "total_plays": 286628266,
# # #             "download_rate": 0.1740,
# # #             "favorite_rate": 0.0036,
# # #             "playlist_rate": 0.0109,
# # #             "repost_rate": 0.0002
# # #         },
# # #         {
# # #             "geo_country": "TZ",
# # #             "unique_songs": 2055,
# # #             "unique_artists": 944,
# # #             "total_plays": 124558960,
# # #             "download_rate": 0.3162,
# # #             "favorite_rate": 0.0041,
# # #             "playlist_rate": 0.0203,
# # #             "repost_rate": 0.0002
# # #         }
# # #     ])
    
# # #     # Hidden gems
# # #     hidden_gems = pd.DataFrame([
# # #         {
# # #             "music_id": 31809979,
# # #             "song_name": "juju",
# # #             "artist_name": "Big smur lee",
# # #             "total_plays": 32581,
# # #             "total_downloads": 132987,
# # #             "favorite_ratio": 0.0491,
# # #             "playlist_ratio": 0.0440,
# # #             "engagement_score": 1.25274
# # #         },
# # #         {
# # #             "music_id": 26325473,
# # #             "song_name": "Medicine after death",
# # #             "artist_name": "Mohbad",
# # #             "total_plays": 4019,
# # #             "total_downloads": 16303,
# # #             "favorite_ratio": 0.0475,
# # #             "playlist_ratio": 0.0236,
# # #             "engagement_score": 1.23872
# # #         },
# # #         {
# # #             "music_id": 29326228,
# # #             "song_name": "Twe Twe (remix)",
# # #             "artist_name": "Kizz Daniel",
# # #             "total_plays": 8614,
# # #             "total_downloads": 34749,
# # #             "favorite_ratio": 0.0358,
# # #             "playlist_ratio": 0.0411,
# # #             "engagement_score": 1.23363
# # #         },
# # #         {
# # #             "music_id": 27038877,
# # #             "song_name": "Area Boys prayers",
# # #             "artist_name": "Seyi vibez",
# # #             "total_plays": 4425,
# # #             "total_downloads": 16386,
# # #             "favorite_ratio": 0.0298,
# # #             "playlist_ratio": 0.0280,
# # #             "engagement_score": 1.12861
# # #         },
# # #         {
# # #             "music_id": 24215772,
# # #             "song_name": "Gbona",
# # #             "artist_name": "Zinoleesky",
# # #             "total_plays": 7899,
# # #             "total_downloads": 26930,
# # #             "favorite_ratio": 0.0457,
# # #             "playlist_ratio": 0.0575,
# # #             "engagement_score": 1.05420
# # #         }
# # #     ])
    
# # #     # Top artists by song count
# # #     top_artists = pd.DataFrame([
# # #         {
# # #             "artist_name": "Juice WRLD",
# # #             "song_count": 538,
# # #             "total_plays": 72475641,
# # #             "avg_plays_per_song": 13357.1030
# # #         },
# # #         {
# # #             "artist_name": "KIRAT",
# # #             "song_count": 359,
# # #             "total_plays": 11619281,
# # #             "avg_plays_per_song": 8102.7064
# # #         },
# # #         {
# # #             "artist_name": "Dj Wizkel",
# # #             "song_count": 344,
# # #             "total_plays": 30548286,
# # #             "avg_plays_per_song": 14058.1160
# # #         },
# # #         {
# # #             "artist_name": "SHATTA WALE",
# # #             "song_count": 337,
# # #             "total_plays": 104034146,
# # #             "avg_plays_per_song": 20723.9335
# # #         },
# # #         {
# # #             "artist_name": "NBA YoungBoy",
# # #             "song_count": 327,
# # #             "total_plays": 24226846,
# # #             "avg_plays_per_song": 9012.9635
# # #         },
# # #         {
# # #             "artist_name": "DJ Amacoz",
# # #             "song_count": 286,
# # #             "total_plays": 76663196,
# # #             "avg_plays_per_song": 33787.2173
# # #         },
# # #         {
# # #             "artist_name": "Seyi Vibez",
# # #             "song_count": 257,
# # #             "total_plays": 50295331,
# # #             "avg_plays_per_song": 25952.1832
# # #         },
# # #         {
# # #             "artist_name": "YoungBoy Never Broke Again",
# # #             "song_count": 250,
# # #             "total_plays": 17216580,
# # #             "avg_plays_per_song": 11186.8616
# # #         },
# # #         {
# # #             "artist_name": "Chronic Law",
# # #             "song_count": 241,
# # #             "total_plays": 25692133,
# # #             "avg_plays_per_song": 10338.8865
# # #         },
# # #         {
# # #             "artist_name": "Mohbad",
# # #             "song_count": 236,
# # #             "total_plays": 119361030,
# # #             "avg_plays_per_song": 35261.7518
# # #         }
# # #     ])
    
# # #     # Artist engagement comparison
# # #     artist_engagement = pd.DataFrame([
# # #         {
# # #             "artist_name": "Mama le succès",
# # #             "song_count": 15,
# # #             "avg_engagement_score": 0.404562989
# # #         },
# # #         {
# # #             "artist_name": "Big Smur Lee",
# # #             "song_count": 8,
# # #             "avg_engagement_score": 0.358251483
# # #         },
# # #         {
# # #             "artist_name": "Dj Amass",
# # #             "song_count": 7,
# # #             "avg_engagement_score": 0.269453664
# # #         },
# # #         {
# # #             "artist_name": "djmysterioghana",
# # #             "song_count": 6,
# # #             "avg_engagement_score": 0.254437576
# # #         },
# # #         {
# # #             "artist_name": "Iba Montana",
# # #             "song_count": 10,
# # #             "avg_engagement_score": 0.245587765
# # #         },
# # #         {
# # #             "artist_name": "Adomba Fausty",
# # #             "song_count": 9,
# # #             "avg_engagement_score": 0.237230024
# # #         },
# # #         {
# # #             "artist_name": "DJ MENTOS",
# # #             "song_count": 6,
# # #             "avg_engagement_score": 0.231980866
# # #         },
# # #         {
# # #             "artist_name": "Obaapa Christy",
# # #             "song_count": 22,
# # #             "avg_engagement_score": 0.224386569
# # #         },
# # #         {
# # #             "artist_name": "Dj Wasty Kay",
# # #             "song_count": 18,
# # #             "avg_engagement_score": 0.219959456
# # #         },
# # #         {
# # #             "artist_name": "Kwaku smoke",
# # #             "song_count": 6,
# # #             "avg_engagement_score": 0.213171093
# # #         }
# # #     ])
    
# # #     # Engagement benchmarks
# # #     benchmarks = pd.DataFrame([
# # #         {
# # #             "metric": "Downloads",
# # #             "average_ratio": 0.19943922,
# # #             "highest_ratio": 84.3617
# # #         },
# # #         {
# # #             "metric": "Favorites",
# # #             "average_ratio": 0.00722445,
# # #             "highest_ratio": 2.6768
# # #         },
# # #         {
# # #             "metric": "Playlists",
# # #             "average_ratio": 0.01700405,
# # #             "highest_ratio": 3.1849
# # #         },
# # #         {
# # #             "metric": "Reposts",
# # #             "average_ratio": 0.00026425,
# # #             "highest_ratio": 0.3487
# # #         }
# # #     ])
    
# # #     # DJ Mix vs Single Track Analysis
# # #     dj_single = pd.DataFrame([
# # #         {
# # #             "content_type": "DJ Mix",
# # #             "track_count": 9034,
# # #             "avg_download_ratio": 0.29938929,
# # #             "avg_favorite_ratio": 0.00778788,
# # #             "avg_playlist_ratio": 0.01570945
# # #         },
# # #         {
# # #             "content_type": "Single Track",
# # #             "track_count": 71004,
# # #             "avg_download_ratio": 0.18866509,
# # #             "avg_favorite_ratio": 0.00716354,
# # #             "avg_playlist_ratio": 0.01714273
# # #         }
# # #     ])
    
# # #     # Monthly analysis
# # #     monthly_analysis = pd.DataFrame([
# # #         {
# # #             "month_str": "2023-04",
# # #             "unique_songs": 19723,
# # #             "total_plays": 296749194,
# # #             "download_rate": 0.1859,
# # #             "favorite_rate": 0.0063
# # #         },
# # #         {
# # #             "month_str": "2023-05",
# # #             "unique_songs": 26097,
# # #             "total_plays": 433438893,
# # #             "download_rate": 0.1432,
# # #             "favorite_rate": 0.0050
# # #         },
# # #         {
# # #             "month_str": "2023-06",
# # #             "unique_songs": 25314,
# # #             "total_plays": 409287750,
# # #             "download_rate": 0.1539,
# # #             "favorite_rate": 0.0051
# # #         },
# # #         {
# # #             "month_str": "2023-07",
# # #             "unique_songs": 20650,
# # #             "total_plays": 291190895,
# # #             "download_rate": 0.2027,
# # #             "favorite_rate": 0.0069
# # #         },
# # #         {
# # #             "month_str": "2023-08",
# # #             "unique_songs": 22854,
# # #             "total_plays": 324336447,
# # #             "download_rate": 0.1952,
# # #             "favorite_rate": 0.0065
# # #         },
# # #         {
# # #             "month_str": "2023-09",
# # #             "unique_songs": 22873,
# # #             "total_plays": 329623842,
# # #             "download_rate": 0.1980,
# # #             "favorite_rate": 0.0065
# # #         },
# # #         {
# # #             "month_str": "2023-10",
# # #             "unique_songs": 24746,
# # #             "total_plays": 369916905,
# # #             "download_rate": 0.1898,
# # #             "favorite_rate": 0.0065
# # #         },
# # #         {
# # #             "month_str": "2023-11",
# # #             "unique_songs": 24940,
# # #             "total_plays": 362235739,
# # #             "download_rate": 0.1875,
# # #             "favorite_rate": 0.0061
# # #         },
# # #         {
# # #             "month_str": "2023-12",
# # #             "unique_songs": 26614,
# # #             "total_plays": 399588966,
# # #             "download_rate": 0.1932,
# # #             "favorite_rate": 0.0060
# # #         },
# # #         {
# # #             "month_str": "2024-01",
# # #             "unique_songs": 25525,
# # #             "total_plays": 385683603,
# # #             "download_rate": 0.1951,
# # #             "favorite_rate": 0.0059
# # #         },
# # #         {
# # #             "month_str": "2024-02",
# # #             "unique_songs": 23263,
# # #             "total_plays": 333443551,
# # #             "download_rate": 0.1879,
# # #             "favorite_rate": 0.0056
# # #         },
# # #         {
# # #             "month_str": "2024-03",
# # #             "unique_songs": 24509,
# # #             "total_plays": 351750156,
# # #             "download_rate": 0.2034,
# # #             "favorite_rate": 0.0057
# # #         },
# # #         {
# # #             "month_str": "2024-04",
# # #             "unique_songs": 24584,
# # #             "total_plays": 360657522,
# # #             "download_rate": 0.2161,
# # #             "favorite_rate": 0.0060
# # #         },
# # #         {
# # #             "month_str": "2024-05",
# # #             "unique_songs": 26597,
# # #             "total_plays": 405513449,
# # #             "download_rate": 0.2299,
# # #             "favorite_rate": 0.0058
# # #         },
# # #         {
# # #             "month_str": "2024-06",
# # #             "unique_songs": 26172,
# # #             "total_plays": 397425211,
# # #             "download_rate": 0.2315,
# # #             "favorite_rate": 0.0055
# # #         },
# # #         {
# # #             "month_str": "2024-07",
# # #             "unique_songs": 26432,
# # #             "total_plays": 411944638,
# # #             "download_rate": 0.2198,
# # #             "favorite_rate": 0.0059
# # #         },
# # #         {
# # #             "month_str": "2024-08",
# # #             "unique_songs": 27831,
# # #             "total_plays": 424523455,
# # #             "download_rate": 0.2142,
# # #             "favorite_rate": 0.0059
# # #         },
# # #         {
# # #             "month_str": "2024-09",
# # #             "unique_songs": 27116,
# # #             "total_plays": 404860879,
# # #             "download_rate": 0.2064,
# # #             "favorite_rate": 0.0061
# # #         },
# # #         {
# # #             "month_str": "2024-10",
# # #             "unique_songs": 27640,
# # #             "total_plays": 419514856,
# # #             "download_rate": 0.2000,
# # #             "favorite_rate": 0.0064
# # #         },
# # #         {
# # #             "month_str": "2024-11",
# # #             "unique_songs": 25658,
# # #             "total_plays": 433059119,
# # #             "download_rate": 0.2030,
# # #             "favorite_rate": 0.0067
# # #         },
# # #         {
# # #             "month_str": "2024-12",
# # #             "unique_songs": 28847,
# # #             "total_plays": 479840220,
# # #             "download_rate": 0.2002,
# # #             "favorite_rate": 0.0066
# # #         }
# # #     ])

# # #     # Process top engagement data
# # #     top_engagement_df = top_download_ratio.copy()
# # #     top_engagement_df['song'] = top_engagement_df['song_name'] + " (" + top_engagement_df['artist_name'] + ")"
# # #     top_engagement_df['downloadRatio'] = top_engagement_df['download_play_ratio']
# # #     top_engagement_df['favoritesRatio'] = top_engagement_df['favorite_play_ratio']
# # #     top_engagement_df['playlistRatio'] = top_engagement_df['playlist_play_ratio']
# # #     top_engagement_df['repostsRatio'] = top_engagement_df['repost_play_ratio']
# # #     top_engagement_df['engagement'] = top_engagement_df['engagement_score']
# # #     top_engagement_df['plays'] = top_engagement_df['total_plays']
    
# # #     # Process country data
# # #     country_df = pd.DataFrame({
# # #         'country': country_analysis['geo_country'],
# # #         'totalPlay30s': country_analysis['total_plays'],
# # #         'downloadRate': country_analysis['download_rate'],
# # #         'favoriteRate': country_analysis['favorite_rate'],
# # #         'playlistRate': country_analysis['playlist_rate'],
# # #         'songCount': country_analysis['unique_songs'],
# # #         'artistCount': country_analysis['unique_artists']
# # #     })
    
# # #     # Process hidden gems data
# # #     hidden_gems_df = hidden_gems.copy()
# # #     hidden_gems_df['song'] = hidden_gems_df['song_name'] + " (" + hidden_gems_df['artist_name'] + ")"
# # #     hidden_gems_df['engagementRatio'] = hidden_gems_df['engagement_score']
# # #     hidden_gems_df['plays'] = hidden_gems_df['total_plays']
    
# # #     # Process benchmark data
# # #     benchmark_df = pd.DataFrame({
# # #         'name': benchmarks['metric'],
# # #         'average': benchmarks['average_ratio'],
# # #         'highest': benchmarks['highest_ratio']
# # #     })
    
# # #     # Monthly trend data
# # #     monthly_df = monthly_analysis.sort_values('month_str')
    
# # #     # DJ vs Single comparison
# # #     dj_single_df = dj_single

# # #     return top_engagement_df, country_df, hidden_gems_df, top_artists, artist_engagement, benchmark_df, monthly_df, dj_single_df

# # # # Load data
# # # try:
# # #     top_engagement_df, country_df, hidden_gems_df, top_artists_df, artist_engagement_df, benchmark_df, monthly_df, dj_single_df = load_data()
# # #     data_loaded = True
# # # except Exception as e:
# # #     st.error(f"Error loading data: {e}")
# # #     data_loaded = False

# # # # Dashboard title and description
# # # st.title("Music Data Analysis Dashboard")
# # # st.write("UGC Music Upload Analysis (04/2023-12/2024) for songs across multiple countries")

# # # # Create tabs
# # # tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
# # #     "Engagement Analysis", 
# # #     "Country Analysis", 
# # #     "Hidden Gems", 
# # #     "Top Artists", 
# # #     "Trends",
# # #     "Benchmarks"
# # # ])

# # # # Tab 1: Engagement Analysis
# # # with tab1:
# # #     st.header("Top Songs by Engagement Score")
# # #     st.write("Engagement score combines download, favorite, playlist, and repost ratios")
    
# # #     # Create the engagement score chart
# # #     fig1 = px.bar(
# # #         top_engagement_df,
# # #         x="song",
# # #         y="engagement",
# # #         title="Top Songs by Engagement Score",
# # #         labels={"engagement": "Engagement Score", "song": "Song"},
# # #         color_discrete_sequence=["#8884d8"]
# # #     )
# # #     fig1.update_layout(xaxis={'categoryorder':'total descending'})
# # #     st.plotly_chart(fig1, use_container_width=True)
    
# # #     # Create the metrics breakdown chart
# # #     st.header("Engagement Metrics Breakdown")
# # #     st.write("Detailed breakdown of different engagement metrics for top performers")
    
# # #     metrics_df = top_engagement_df.melt(
# # #         id_vars=["song"],
# # #         value_vars=["downloadRatio", "favoritesRatio", "playlistRatio"],
# # #         var_name="Metric",
# # #         value_name="Value"
# # #     )
    
# # #     # Replace metric names for better readability
# # #     metrics_df["Metric"] = metrics_df["Metric"].map({
# # #         "downloadRatio": "Download Ratio",
# # #         "favoritesRatio": "Favorites Ratio",
# # #         "playlistRatio": "Playlist Ratio"
# # #     })
    
# # #     fig2 = px.bar(
# # #         metrics_df,
# # #         x="song",
# # #         y="Value",
# # #         color="Metric",
# # #         barmode="group",
# # #         title="Engagement Metrics Breakdown",
# # #         color_discrete_map={
# # #             "Download Ratio": "#0088FE",
# # #             "Favorites Ratio": "#00C49F",
# # #             "Playlist Ratio": "#FFBB28"
# # #         }
# # #     )
# # #     fig2.update_layout(xaxis={'categoryorder':'total descending'})
# # #     st.plotly_chart(fig2, use_container_width=True)
    
# # #     # Content Type Comparison
# # #     st.header("Content Type Comparison")
# # #     st.write("Engagement metrics comparison between DJ mixes and single tracks")
    
# # #     fig_content = px.bar(
# # #         dj_single_df,
# # #         x="content_type",
# # #         y=["avg_download_ratio", "avg_favorite_ratio", "avg_playlist_ratio"],
# # #         barmode="group",
# # #         title="DJ Mixes vs. Single Tracks Engagement",
# # #         labels={
# # #             "value": "Average Ratio",
# # #             "content_type": "Content Type",
# # #             "variable": "Metric Type"
# # #         },
# # #         color_discrete_map={
# # #             "avg_download_ratio": "#0088FE",
# # #             "avg_favorite_ratio": "#00C49F",
# # #             "avg_playlist_ratio": "#FFBB28"
# # #         }
# # #     )
# # #     st.plotly_chart(fig_content, use_container_width=True)

# # # # Tab 2: Country Analysis
# # # with tab2:
# # #     st.header("Country Play Distribution")
    
# # #     col1, col2 = st.columns(2)
    
# # #     with col1:
# # #         # Create the pie chart for play distribution
# # #         fig3 = px.pie(
# # #             country_df,
# # #             values="totalPlay30s",
# # #             names="country",
# # #             title="Total Plays by Country",
# # #             color_discrete_sequence=px.colors.qualitative.Set3
# # #         )
# # #         fig3.update_traces(textposition='inside', textinfo='percent+label')
# # #         st.plotly_chart(fig3, use_container_width=True)
    
# # #     with col2:
# # #         # Create the bar chart for engagement rates by country
# # #         fig4 = go.Figure()
# # #         fig4.add_trace(go.Bar(
# # #             x=country_df["country"],
# # #             y=country_df["downloadRate"],
# # #             name="Download Rate",
# # #             marker_color="#0088FE"
# # #         ))
# # #         fig4.add_trace(go.Bar(
# # #             x=country_df["country"],
# # #             y=country_df["favoriteRate"],
# # #             name="Favorite Rate",
# # #             marker_color="#00C49F"
# # #         ))
# # #         fig4.add_trace(go.Bar(
# # #             x=country_df["country"],
# # #             y=country_df["playlistRate"],
# # #             name="Playlist Rate",
# # #             marker_color="#FFBB28"
# # #         ))
# # #         fig4.update_layout(
# # #             title="Engagement Rates by Country",
# # #             barmode="group"
# # #         )
# # #         st.plotly_chart(fig4, use_container_width=True)
    
# # #     # Create the song & artist distribution chart
# # #     st.header("Song & Artist Distribution by Country")
    
# # #     fig5 = go.Figure()
# # #     fig5.add_trace(go.Bar(
# # #         x=country_df["country"],
# # #         y=country_df["songCount"],
# # #         name="Number of Songs",
# # #         marker_color="#8884d8"
# # #     ))
# # #     fig5.add_trace(go.Bar(
# # #         x=country_df["country"],
# # #         y=country_df["artistCount"],
# # #         name="Number of Artists",
# # #         marker_color="#82ca9d"
# # #     ))
# # #     fig5.update_layout(
# # #         title="Song & Artist Distribution by Country",
# # #         barmode="group"
# # #     )
# # #     st.plotly_chart(fig5, use_container_width=True)

# # # # Tab 3: Hidden Gems
# # # with tab3:
# # #     st.header("Hidden Gems (High Engagement, Moderate Plays)")
# # #     st.write("Songs with exceptional engagement metrics that haven't yet reached massive play counts")
    
# # #     # Create dual axis chart for hidden gems
# # #     fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    
# # #     fig6.add_trace(
# # #         go.Bar(
# # #             x=hidden_gems_df["song"],
# # #             y=hidden_gems_df["engagementRatio"],
# # #             name="Engagement Ratio",
# # #             marker_color="#8884d8"
# # #         ),
# # #         secondary_y=False
# # #     )
    
# # #     fig6.add_trace(
# # #         go.Bar(
# # #             x=hidden_gems_df["song"],
# # #             y=hidden_gems_df["plays"],
# # #             name="Total Plays (30s+)",
# # #             marker_color="#82ca9d"
# # #         ),
# # #         secondary_y=True
# # #     )
    
# # #     fig6.update_layout(
# # #         title_text="Hidden Gems: Engagement vs Plays",
# # #         xaxis=dict(title="Song")
# # #     )
    
# # #     fig6.update_yaxes(title_text="Engagement Ratio", secondary_y=False)
# # #     fig6.update_yaxes(title_text="Total Plays", secondary_y=True)
    
# # #     st.plotly_chart(fig6, use_container_width=True)
    
# # #     # Create the engagement breakdown for hidden gems
# # #     st.header("Hidden Gems Engagement Breakdown")
    
# # #     metrics_df2 = hidden_gems_df.melt(
# # #         id_vars=["song"],
# # #         value_vars=["favorite_ratio", "playlist_ratio"],
# # #         var_name="Metric",
# # #         value_name="Value"
# # #     )
    
# # #     metrics_df2["Metric"] = metrics_df2["Metric"].map({
# # #         "favorite_ratio": "Favorite Ratio",
# # #         "playlist_ratio": "Playlist Ratio"
# # #     })
    
# # #     fig7 = px.bar(
# # #         metrics_df2,
# # #         x="song",
# # #         y="Value",
# # #         color="Metric",
# # #         barmode="group",
# # #         title="Engagement Metrics Breakdown for Hidden Gems",
# # #         color_discrete_map={
# # #             "Favorite Ratio": "#00C49F",
# # #             "Playlist Ratio": "#FFBB28"
# # #         }
# # #     )
# # #     st.plotly_chart(fig7, use_container_width=True)

# # # # Tab 4: Top Artists
# # # with tab4:
# # #     st.header("Top Artists by Song Count")
# # #     st.write("Artists with multiple songs in the dataset")
    
# # #     # Sort artists by song count
# # #     sorted_artists = top_artists_df.sort_values(by="song_count", ascending=False)
    
# # #     fig8 = px.bar(
# # #         sorted_artists.head(10),
# # #         x="artist_name",
# # #         y="song_count",
# # #         title="Top Artists by Song Count",
# # #         color_discrete_sequence=["#8884d8"]
# # #     )
# # #     st.plotly_chart(fig8, use_container_width=True)
    
# # #     # Create the artist engagement comparison
# # #     st.header("Artist Engagement Comparison")
    
# # #     fig9 = px.bar(
# # #         artist_engagement_df,
# # #         x="artist_name",
# # #         y="avg_engagement_score",
# # #         title="Average Engagement Score by Artist",
# # #         color_discrete_sequence=["#FF8042"]
# # #     )
# # #     fig9.update_layout(yaxis_title="Average Engagement Score")
# # #     st.plotly_chart(fig9, use_container_width=True)

# # # # Tab 5: Trends
# # # with tab5:
# # #     st.header("Monthly Trends")
# # #     st.write("How engagement metrics have changed over time")
    
# # #     # Create line chart for monthly trends
# # #     fig_monthly = go.Figure()
# # #     fig_monthly.add_trace(go.Scatter(
# # #         x=monthly_df["month_str"],
# # #         y=monthly_df["download_rate"],
# # #         mode='lines+markers',
# # #         name='Download Rate',
# # #         line=dict(color="#0088FE")
# # #     ))
# # #     fig_monthly.add_trace(go.Scatter(
# # #         x=monthly_df["month_str"],
# # #         y=monthly_df["favorite_rate"],
# # #         mode='lines+markers',
# # #         name='Favorite Rate',
# # #         line=dict(color="#00C49F")
# # #     ))
# # #     fig_monthly.update_layout(
# # #         title="Monthly Engagement Rates",
# # #         xaxis_title="Month",
# # #         yaxis_title="Engagement Rate"
# # #     )
# # #     st.plotly_chart(fig_monthly, use_container_width=True)
    
# # #     # Monthly plays and unique songs
# # #     fig_plays = go.Figure()
    
# # #     # Create a secondary y-axis plot
# # #     fig_plays = make_subplots(specs=[[{"secondary_y": True}]])
    
# # #     fig_plays.add_trace(
# # #         go.Scatter(
# # #             x=monthly_df["month_str"],
# # #             y=monthly_df["total_plays"],
# # #             mode="lines+markers",
# # #             name="Total Plays",
# # #             line=dict(color="#8884d8")
# # #         ),
# # #         secondary_y=False
# # #     )
    
# # #     fig_plays.add_trace(
# # #         go.Scatter(
# # #             x=monthly_df["month_str"],
# # #             y=monthly_df["unique_songs"],
# # #             mode="lines+markers",
# # #             name="Unique Songs",
# # #             line=dict(color="#82ca9d")
# # #         ),
# # #         secondary_y=True
# # #     )
    
# # #     fig_plays.update_layout(
# # #         title="Monthly Plays and Song Volume",
# # #         xaxis_title="Month"
# # #     )
    
# # #     fig_plays.update_yaxes(title_text="Total Plays", secondary_y=False)
# # #     fig_plays.update_yaxes(title_text="Unique Songs", secondary_y=True)
    
# # #     st.plotly_chart(fig_plays, use_container_width=True)

# # # # Tab 6: Benchmarks
# # # with tab6:
# # #     st.header("Engagement Benchmarks")
# # #     st.write("Average vs. Highest engagement metrics across the dataset")
    
# # #     # Create the benchmark comparison chart
# # #     benchmark_melted = benchmark_df.melt(
# # #         id_vars=["name"],
# # #         value_vars=["average", "highest"],
# # #         var_name="Metric",
# # #         value_name="Value"
# # #     )
    
# # #     benchmark_melted["Metric"] = benchmark_melted["Metric"].map({
# # #         "average": "Average Ratio",
# # #         "highest": "Highest Ratio"
# # #     })
    
# # #     fig10 = px.bar(
# # #         benchmark_melted,
# # #         x="name",
# # #         y="Value",
# # #         color="Metric",
# # #         barmode="group",
# # #         title="Engagement Benchmarks: Average vs Highest",
# # #         color_discrete_map={
# # #             "Average Ratio": "#8884d8",
# # #             "Highest Ratio": "#82ca9d"
# # #         },
# # #         log_y=True  # Using log scale for better visualization
# # #     )
# # #     fig10.update_layout(xaxis_title="Metric", yaxis_title="Ratio Value (Log Scale)")
# # #     st.plotly_chart(fig10, use_container_width=True)

# # # # Key Findings section
# # # st.header("Key Findings")
# # # st.markdown("""
# # # ### 1. Early Indicators of Success

# # # Our analysis reveals that **download-to-play ratio** is the most reliable predictor of sustained song success. With a platform-wide average of 0.199, songs exceeding 0.3 demonstrate exceptional user commitment.

# # # ### 2. Geographic Trends 

# # # **Country-specific engagement patterns** show distinct market behaviors:
# # # - **Nigeria (NG)**: Highest volume (4.9B+ plays) with moderate engagement rates (19.4% download rate)
# # # - **Ghana (GH)**: Highest download rate (31.4%) suggesting strong offline listening culture
# # # - **United States (US)**: Highest favorite rate (1.27%) and strong playlist activity (1.86%)

# # # ### 3. Content Format Impact

# # # **DJ mixes consistently outperform single tracks** with 58.7% higher download rates (0.299 vs 0.189), particularly strong in African markets.

# # # ### 4. Hidden Gems

# # # Several promising tracks show exceptional engagement despite moderate play counts:
# # # - **"juju" by Big smur lee** (32,581 plays, 1.25 engagement score)
# # # - **"Medicine after death" by Mohbad** (4,019 plays, 1.24 engagement score)
# # # - **"Twe Twe (remix)" by Kizz Daniel** (8,614 plays, 1.23 engagement score)

# # # ### 5. Artist Insights

# # # **Juice WRLD, KIRAT, and DJ Wizkel** lead in content volume with hundreds of songs each, while **Mama le succès and Big Smur Lee** deliver the highest average engagement quality despite having fewer songs.

# # # ### 6. Temporal Patterns

# # # Analysis across 21 months shows increasing download rates (from 14.3% to 23.2%) with consistent seasonal peaks in December.
# # # """)

# # # # Recommendations section
# # # st.header("Recommendations")
# # # st.markdown("""
# # # ### For Platform Optimization:
# # # - Implement algorithmic emphasis on download-to-play ratio in recommendation engines
# # # - Create dedicated "Hidden Gems" discovery section featuring high-engagement but moderately-played content
# # # - Develop market-specific algorithms accounting for regional engagement preferences
# # # - Target cross-country content promotion for Ghana→US content flow

# # # ### For Content Strategy:
# # # - Increase promotion of DJ mixes and compilations, particularly in African markets
# # # - Spotlight emerging artists with high engagement ratios but moderate plays
# # # - Implement A/B testing of playlist strategies specifically for US-based content
# # # - Develop features to encourage and track offline listening

# # # ### For Talent Acquisition:
# # # - Prioritize artists with consistently high engagement metrics across multiple songs
# # # - Evaluate artists like Mama le succès and Big Smur Lee for potential partnerships
# # # - Look beyond raw play counts to identify rising talent with exceptional engagement
# # # """)
