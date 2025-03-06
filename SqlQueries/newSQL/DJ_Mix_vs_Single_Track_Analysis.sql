-- ===============================================================
-- QUERY 3: DJ Mix vs. Single Track Analysis
-- ===============================================================
-- GOAL: Compare engagement metrics between different content types
--       to understand format preferences and optimize content strategy.
-- ===============================================================

SELECT
    -- Create content type categorization based on track title patterns
    -- Simple heuristic approach using keyword matching in song titles
    -- LOWER() ensures case-insensitive matching
    CASE
        WHEN LOWER(song_name) LIKE '%mix%' OR LOWER(song_name) LIKE '%dj%' THEN 'DJ Mix'
        ELSE 'Single Track'
        END AS content_type,
    
    -- Calculate volume metrics for each content type
    COUNT(DISTINCT music_id) AS track_count,
    
    -- Calculate average engagement ratios per content type
    -- This allows fair comparison between formats regardless of total volume
    AVG(total_downloads / total_play30s) AS avg_download_ratio,
    AVG(total_favorites / total_play30s) AS avg_favorite_ratio,
    AVG(total_playlist_adds / total_play30s) AS avg_playlist_ratio
FROM music_data
-- Filter to include only songs with meaningful play counts
-- This ensures statistical reliability by excluding very low-volume tracks
WHERE total_play30s > 3000
-- Group by content type for comparative analysis
GROUP BY content_type;
