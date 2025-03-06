-- ===============================================================
-- QUERY 1: Artist Engagement Comparison
-- ===============================================================
-- GOAL: Identify artists with consistently high engagement metrics across their catalog
--       rather than just looking at play counts or total song volume.
-- ===============================================================

SELECT
    artist_name,
    -- Count the number of unique songs per artist (using music_id for uniqueness)
    COUNT(DISTINCT music_id) AS song_count,
    
    -- Calculate a weighted engagement score that prioritizes multiple interaction types:
    -- * Downloads (30% weight): Indicates intent to listen offline/repeatedly
    -- * Favorites (30% weight): Shows explicit preference/collection behavior
    -- * Playlist adds (30% weight): Demonstrates integration into user collections
    -- * Reposts (10% weight): Reflects social sharing/viral potential
    -- Using window function with PARTITION BY to calculate the average engagement score
    -- across all songs for each artist, ensuring consistent artist-level metrics
    AVG((SUM(total_downloads) / SUM(total_play30s) * 0.3) +
        (SUM(total_favorites) / SUM(total_play30s) * 0.3) +
        (SUM(total_playlist_adds) / SUM(total_play30s) * 0.3) +
        (SUM(total_reposts) / SUM(total_play30s) * 0.1)) OVER (PARTITION BY artist_name) AS avg_engagement_score
FROM music_data
-- Group by artist to analyze per-artist metrics
GROUP BY artist_name
-- Filter to include only artists with substantial catalog (>5 songs)
-- This ensures statistical significance and focuses on established artists
HAVING COUNT(DISTINCT music_id) > 5
-- Order by engagement score to surface most engaging artists first
ORDER BY avg_engagement_score DESC
-- Limit to top 10 for focused analysis and visualization
LIMIT 10;
