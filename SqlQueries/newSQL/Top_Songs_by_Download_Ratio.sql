-- ===============================================================
-- QUERY 10: Top Songs by Download Ratio
-- ===============================================================
-- GOAL: Identify songs with exceptional download-to-play ratios
--       which indicates strong intent for repeat/offline listening.
-- ===============================================================

SELECT
    -- Track identification columns
    music_id,
    song_name,
    artist_name,
    
    -- Total play count to understand popularity scale
    SUM(total_play30s) AS total_plays,
    
    -- Total download count for raw volume understanding
    SUM(total_downloads) AS total_downloads,
    
    -- Calculate download-to-play ratio
    -- This normalized metric enables fair comparison between songs
    -- regardless of their absolute popularity level
    SUM(total_downloads) / SUM(total_play30s) AS download_play_ratio
FROM music_data
-- Group by track identifiers to aggregate metrics per unique song
GROUP BY music_id, song_name, artist_name
-- Filter to include only songs with meaningful play counts
-- This ensures statistical reliability by excluding very low-volume tracks
HAVING SUM(total_play30s) > 3000
-- Order by download ratio to surface songs with highest offline intent
ORDER BY download_play_ratio DESC
-- Limit to top 10 for focused analysis and visualization
LIMIT 10;