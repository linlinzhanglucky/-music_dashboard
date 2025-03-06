-- ===============================================================
-- QUERY 9: Top Artists by Song Count
-- ===============================================================
-- GOAL: Identify prolific artists with substantial catalog presence
--       to understand content volume distribution.
-- ===============================================================

SELECT
    artist_name,
    -- Calculate content volume metrics per artist
    COUNT(DISTINCT music_id) AS song_count,
    
    -- Calculate total and average play metrics
    -- These help differentiate between volume and performance
    SUM(total_play30s) AS total_plays,
    AVG(total_play30s) AS avg_plays_per_song
FROM music_data
-- Group by artist for artist-level analysis
GROUP BY artist_name
-- Filter to include only artists with substantial catalog (>5 songs)
-- This ensures focus on established artists with meaningful presence
HAVING COUNT(DISTINCT music_id) > 5
-- Order by song count to identify most prolific content creators
ORDER BY song_count DESC
-- Limit to top 10 for focused analysis and visualization
LIMIT 10;