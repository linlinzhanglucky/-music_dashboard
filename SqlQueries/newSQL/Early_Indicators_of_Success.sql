-- ===============================================================
-- QUERY 4: Early Indicators of Success
-- ===============================================================
-- GOAL: Identify engagement metrics that best predict long-term success
--       by calculating normalized interaction ratios and a composite score.
-- ===============================================================

SELECT
    -- Track identification columns
    music_id,
    song_name,
    artist_name,
    
    -- Absolute volume metrics to understand scale
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) AS total_downloads,
    SUM(total_favorites) AS total_favorites,
    SUM(total_playlist_adds) AS total_playlist_adds,
    SUM(total_reposts) AS total_reposts,
    
    -- Geographic reach metric to identify cross-market appeal
    COUNT(DISTINCT geo_country) AS country_count,
    
    -- Calculate engagement ratios normalized by play count
    -- These relative metrics enable fair comparison between songs
    -- regardless of their absolute popularity level
    SUM(total_downloads) / SUM(total_play30s) AS download_play_ratio,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_play_ratio,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_play_ratio,
    SUM(total_reposts) / SUM(total_play30s) AS repost_play_ratio,
    
    -- Calculate weighted composite engagement score
    -- Weights are assigned based on the relative importance of each interaction type:
    -- * Downloads (30%): Indicates intent for repeat/offline listening
    -- * Favorites (30%): Shows explicit user preference and collection
    -- * Playlist adds (30%): Demonstrates integration into user listening routines
    -- * Reposts (10%): Reflects social sharing/viral potential but less common
    (SUM(total_downloads) / SUM(total_play30s) * 0.3) +
    (SUM(total_favorites) / SUM(total_play30s) * 0.3) +
    (SUM(total_playlist_adds) / SUM(total_play30s) * 0.3) +
    (SUM(total_reposts) / SUM(total_play30s) * 0.1) AS engagement_score
FROM music_data
-- Group by track identifiers to aggregate metrics per unique song
GROUP BY music_id, song_name, artist_name
-- Filter to include only songs with meaningful play counts
-- This ensures statistical reliability by excluding very low-volume tracks
HAVING SUM(total_play30s) > 3000
-- Order by the composite engagement score to surface highest engaging songs first
ORDER BY engagement_score DESC
-- Limit to top 20 for focused analysis and visualization
LIMIT 20;