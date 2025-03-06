# Artist Engagement Comparison
SELECT
    artist_name,
    COUNT(DISTINCT music_id) AS song_count,
    AVG((SUM(total_downloads) / SUM(total_play30s) * 0.3) +
        (SUM(total_favorites) / SUM(total_play30s) * 0.3) +
        (SUM(total_playlist_adds) / SUM(total_play30s) * 0.3) +
        (SUM(total_reposts) / SUM(total_play30s) * 0.1)) OVER (PARTITION BY artist_name) AS avg_engagement_score
FROM music_data
GROUP BY artist_name
HAVING COUNT(DISTINCT music_id) > 5
ORDER BY avg_engagement_score DESC
LIMIT 10;
