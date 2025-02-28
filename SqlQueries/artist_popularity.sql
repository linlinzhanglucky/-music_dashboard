-- Artist Popularity Analysis
-- Identifies artists with multiple successful songs

SELECT 
    artist_name,
    COUNT(DISTINCT music_id) AS song_count,
    SUM(total_play30s) AS total_plays,
    AVG(total_play30s) AS avg_plays_per_song,
    SUM(total_downloads) AS total_downloads,
    SUM(total_favorites) AS total_favorites,
    -- Calculate overall artist engagement metrics
    SUM(total_downloads) / SUM(total_play30s) AS overall_download_ratio,
    SUM(total_favorites) / SUM(total_play30s) AS overall_favorite_ratio,
    COUNT(DISTINCT geo_country) AS country_reach
FROM music_data
GROUP BY artist_name
HAVING COUNT(DISTINCT music_id) > 1
ORDER BY total_plays DESC;
