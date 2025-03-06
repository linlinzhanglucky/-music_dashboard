-- ===============================================================
-- QUERY 2: Country Analysis
-- ===============================================================
-- GOAL: Identify geographic differences in content volume and user behavior
--       to inform regional content strategies and market prioritization.
-- ===============================================================

SELECT
    geo_country,
    -- Calculate content diversity metrics per country
    COUNT(DISTINCT music_id) AS unique_songs,
    COUNT(DISTINCT artist_name) AS unique_artists,
    
    -- Calculate total play volume to understand market size
    SUM(total_play30s) AS total_plays,
    
    -- Calculate engagement ratios for each interaction type
    -- These normalized metrics allow fair comparison between countries
    -- regardless of their absolute play volume
    SUM(total_downloads) / SUM(total_play30s) AS download_rate,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_rate,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_rate,
    SUM(total_reposts) / SUM(total_play30s) AS repost_rate
FROM music_data
-- Group by country to analyze regional patterns
GROUP BY geo_country
-- Order by total plays to see largest markets first
ORDER BY total_plays DESC;