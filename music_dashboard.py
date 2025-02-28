import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Music Data Analysis Dashboard",
    page_icon="🎵",
    layout="wide"
)

# Data
# Top Engagement Songs
top_engagement_data = [
    {
        "song": "Have Mercy (Shane Eli)",
        "downloadRatio": 10.6733,
        "favoritesRatio": 0.0011,
        "playlistRatio": 0.0042,
        "repostsRatio": 0.0005,
        "engagement": 10.6887,
        "plays": 7438
    },
    {
        "song": "juju (Big smur lee)",
        "downloadRatio": 1.2954,
        "favoritesRatio": 0.0524,
        "playlistRatio": 0.0304,
        "repostsRatio": 0.0013,
        "engagement": 1.3612,
        "plays": 12147
    },
    {
        "song": "Area Boys prayers (Seyi vibez)",
        "downloadRatio": 1.0645,
        "favoritesRatio": 0.0298,
        "playlistRatio": 0.0335,
        "repostsRatio": 0.0011,
        "engagement": 1.1286,
        "plays": 4425
    },
    {
        "song": "Gbona (Zinoleesky)",
        "downloadRatio": 0.9954,
        "favoritesRatio": 0.0457,
        "playlistRatio": 0.0130,
        "repostsRatio": 0.0016,
        "engagement": 1.0542,
        "plays": 7899
    },
    {
        "song": "Blacksherif Let Me Go MY Way (Black Sheriff)",
        "downloadRatio": 0.9508,
        "favoritesRatio": 0.0966,
        "playlistRatio": 0.0057,
        "repostsRatio": 0.0007,
        "engagement": 1.0535,
        "plays": 4202
    }
]

# Country Data
country_data = [
    {
        "country": "NG",
        "totalPlay30s": 452678656,
        "downloadRate": 0.192,
        "favoriteRate": 0.005,
        "playlistRate": 0.011,
        "songCount": 17669,
        "artistCount": 7936
    },
    {
        "country": "GH",
        "totalPlay30s": 106642952,
        "downloadRate": 0.315,
        "favoriteRate": 0.006,
        "playlistRate": 0.026,
        "songCount": 5365,
        "artistCount": 2204
    },
    {
        "country": "US",
        "totalPlay30s": 90898517,
        "downloadRate": 0.086,
        "favoriteRate": 0.013,
        "playlistRate": 0.019,
        "songCount": 7349,
        "artistCount": 3206
    },
    {
        "country": "JM",
        "totalPlay30s": 24816983,
        "downloadRate": 0.174,
        "favoriteRate": 0.004,
        "playlistRate": 0.011,
        "songCount": 1478,
        "artistCount": 478
    },
    {
        "country": "TZ",
        "totalPlay30s": 11616569,
        "downloadRate": 0.314,
        "favoriteRate": 0.004,
        "playlistRate": 0.020,
        "songCount": 756,
        "artistCount": 396
    }
]

# Hidden Gems
hidden_gems_data = [
    {
        "song": "Have Mercy (Shane Eli)",
        "engagementRatio": 10.689,
        "favoriteRatio": 0.001,
        "playlistRatio": 0.004,
        "plays": 7438
    },
    {
        "song": "juju (Big smur lee)",
        "engagementRatio": 1.361,
        "favoriteRatio": 0.052,
        "playlistRatio": 0.030,
        "plays": 12147
    },
    {
        "song": "Area Boys prayers (Seyi vibez)",
        "engagementRatio": 1.129,
        "favoriteRatio": 0.030,
        "playlistRatio": 0.034,
        "plays": 4425
    },
    {
        "song": "Gbona (Zinoleesky)",
        "engagementRatio": 1.054,
        "favoriteRatio": 0.046,
        "playlistRatio": 0.013,
        "plays": 7899
    },
    {
        "song": "Blacksherif Let Me Go MY Way (Black Sheriff)",
        "engagementRatio": 1.054,
        "favoriteRatio": 0.097,
        "playlistRatio": 0.006,
        "plays": 4202
    }
]

# Top Artists with Multiple Songs
top_artists_data = [
    {"artist": "Future", "songCount": 483, "avgEngagement": 0.14},
    {"artist": "Juice WRLD", "songCount": 409, "avgEngagement": 0.10},
    {"artist": "Zinoleesky", "songCount": 360, "avgEngagement": 0.22},
    {"artist": "Kodak Black", "songCount": 310, "avgEngagement": 0.09},
    {"artist": "SHATTA WALE", "songCount": 279, "avgEngagement": 0.19},
    {"artist": "Young Thug", "songCount": 236, "avgEngagement": 0.08},
    {"artist": "Lil Durk", "songCount": 232, "avgEngagement": 0.12},
    {"artist": "Otega", "songCount": 230, "avgEngagement": 0.16},
    {"artist": "Mohbad", "songCount": 216, "avgEngagement": 0.18},
    {"artist": "Dax", "songCount": 203, "avgEngagement": 0.13}
]

# Benchmark data
benchmark_data = [
    {"name": "Downloads", "average": 0.202, "highest": 10.673},
    {"name": "Favorites", "average": 0.008, "highest": 0.097},
    {"name": "Playlists", "average": 0.016, "highest": 0.034},
    {"name": "Reposts", "average": 0.0003, "highest": 0.002}
]

# Convert to pandas dataframes
top_engagement_df = pd.DataFrame(top_engagement_data)
country_df = pd.DataFrame(country_data)
hidden_gems_df = pd.DataFrame(hidden_gems_data)
top_artists_df = pd.DataFrame(top_artists_data)
benchmark_df = pd.DataFrame(benchmark_data)

# Dashboard title and description
st.title("Music Data Analysis Dashboard")
st.write("UGC Music Upload Analysis (01/2023-01/2025) for songs with 3,000-1,000,000 plays")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Engagement Analysis", 
    "Country Analysis", 
    "Hidden Gems", 
    "Top Artists", 
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
        color_discrete_sequence=["#8884d8"]
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
        value_vars=["favoriteRatio", "playlistRatio"],
        var_name="Metric",
        value_name="Value"
    )
    
    metrics_df2["Metric"] = metrics_df2["Metric"].map({
        "favoriteRatio": "Favorite Ratio",
        "playlistRatio": "Playlist Ratio"
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
    sorted_artists = top_artists_df.sort_values(by="songCount", ascending=False)
    
    fig8 = px.bar(
        sorted_artists,
        x="artist",
        y="songCount",
        title="Top Artists by Song Count",
        color_discrete_sequence=["#8884d8"]
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    # Create the artist engagement comparison
    st.header("Artist Engagement Comparison")
    
    fig9 = px.bar(
        sorted_artists,
        x="artist",
        y="avgEngagement",
        title="Average Engagement Score by Artist",
        color_discrete_sequence=["#FF8042"]
    )
    fig9.update_layout(yaxis_title="Average Engagement Score")
    st.plotly_chart(fig9, use_container_width=True)

# Tab 5: Benchmarks
with tab5:
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
        }
    )
    fig10.update_layout(xaxis_title="Metric", yaxis_title="Ratio Value")
    st.plotly_chart(fig10, use_container_width=True)

# Key Findings section
st.header("Key Findings")
st.markdown("""
- **Top Success Indicator:** Download-to-play ratio is the strongest predictor of engagement (avg: 0.202)
- **Country Insights:** Ghana has the highest download rate (0.315), US has highest favorite rate (0.013)
- **Hidden Gem:** "Have Mercy" by Shane Eli shows exceptional engagement (10.689) with moderate plays
- **Artist Insights:** Future, Juice WRLD, and Zinoleesky have the most songs in the dataset
- **Geographic Trend:** Nigeria has the highest content volume (452M plays, 17.6K songs), followed by Ghana and US
""")