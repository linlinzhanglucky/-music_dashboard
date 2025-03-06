# Early Indicators of Success
SELECT
    music_id,
    song_name,
    artist_name,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) AS total_downloads,
    SUM(total_favorites) AS total_favorites,
    SUM(total_playlist_adds) AS total_playlist_adds,
    SUM(total_reposts) AS total_reposts,
    COUNT(DISTINCT geo_country) AS country_count,
    -- Calculate engagement ratios
    SUM(total_downloads) / SUM(total_play30s) AS download_play_ratio,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_play_ratio,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_play_ratio,
    SUM(total_reposts) / SUM(total_play30s) AS repost_play_ratio,
    -- Weighted engagement score
    (SUM(total_downloads) / SUM(total_play30s) * 0.3) +
    (SUM(total_favorites) / SUM(total_play30s) * 0.3) +
    (SUM(total_playlist_adds) / SUM(total_play30s) * 0.3) +
    (SUM(total_reposts) / SUM(total_play30s) * 0.1) AS engagement_score
FROM music_data
GROUP BY music_id, song_name, artist_name
HAVING SUM(total_play30s) > 3000
ORDER BY engagement_score DESC
LIMIT 20;
