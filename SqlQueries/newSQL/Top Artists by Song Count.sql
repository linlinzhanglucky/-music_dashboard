# Top Artists by Song Count
SELECT
    artist_name,
    COUNT(DISTINCT music_id) AS song_count,
    SUM(total_play30s) AS total_plays,
    AVG(total_play30s) AS avg_plays_per_song
FROM music_data
GROUP BY artist_name
HAVING COUNT(DISTINCT music_id) > 5
ORDER BY song_count DESC
LIMIT 10;
