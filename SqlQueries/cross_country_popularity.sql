-- Cross-Country Popularity
-- Identifies songs gaining traction across multiple countries

SELECT 
    music_id,
    song_name,
    artist_name,
    COUNT(DISTINCT geo_country) AS country_count,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) AS total_downloads,
    SUM(total_favorites) AS total_favorites,
    -- Calculate the average engagement per country
    SUM(total_downloads) / COUNT(DISTINCT geo_country) AS avg_downloads_per_country,
    SUM(total_favorites) / COUNT(DISTINCT geo_country) AS avg_favorites_per_country
FROM music_data
GROUP BY music_id, song_name, artist_name
HAVING COUNT(DISTINCT geo_country) > 1
ORDER BY country_count DESC, total_plays DESC
LIMIT 10;
