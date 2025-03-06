-- ===============================================================
-- QUERY 6: Hidden Gems (High Engagement, Moderate Plays)
-- ===============================================================
-- GOAL: Identify songs that show strong engagement signals despite
--       moderate play counts, suggesting growth potential and future success.
-- ===============================================================

SELECT
    -- Track identification columns
    music_id,
    song_name,
    artist_name,
    
    -- Total play count to understand current popularity level
    SUM(total_play30s) AS total_plays,
    
    -- Calculate engagement ratios normalized by play count
    -- These relative metrics enable fair comparison between songs
    -- regardless of their absolute popularity level
    SUM(total_downloads) / SUM(total_play30s) AS download_ratio,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_ratio,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_ratio,
    
    -- Geographic reach metric to identify cross-market appeal
    COUNT(DISTINCT geo_country) AS country_reach,
    
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
-- Multiple filters for "hidden gem" identification:
-- 1. Play count between 3,000-20,000: Focus on moderate popularity
-- 2. Either download ratio OR favorite ratio significantly above average
--    (at least 50% higher than platform average)
-- This approach targets songs with moderate plays but exceptional engagement
HAVING SUM(total_play30s) BETWEEN 3000 AND 20000
   AND ((SUM(total_downloads) / SUM(total_play30s)) >
        (SELECT AVG(total_downloads) / AVG(total_play30s) FROM music_data) * 1.5
    OR
        (SUM(total_favorites) / SUM(total_play30s)) >
        (SELECT AVG(total_favorites) / AVG(total_play30s) FROM music_data) * 1.5)
-- Order by the composite engagement score to surface highest potential tracks first
ORDER BY engagement_score DESC
-- Limit to top 15 for focused analysis and visualization
LIMIT 15;