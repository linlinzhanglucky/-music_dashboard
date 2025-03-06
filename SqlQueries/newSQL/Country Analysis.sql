# Country Analysis
SELECT
    geo_country,
    COUNT(DISTINCT music_id) AS unique_songs,
    COUNT(DISTINCT artist_name) AS unique_artists,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) / SUM(total_play30s) AS download_rate,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_rate,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_rate,
    SUM(total_reposts) / SUM(total_play30s) AS repost_rate
FROM music_data
GROUP BY geo_country
ORDER BY total_plays DESC;
