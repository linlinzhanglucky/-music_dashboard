# Top Songs by Download Ratio
SELECT
    music_id,
    song_name,
    artist_name,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) AS total_downloads,
    SUM(total_downloads) / SUM(total_play30s) AS download_play_ratio
FROM music_data
GROUP BY music_id, song_name, artist_name
HAVING SUM(total_play30s) > 3000
ORDER BY download_play_ratio DESC
LIMIT 10;
