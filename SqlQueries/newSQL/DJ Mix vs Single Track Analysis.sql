# DJ Mix vs. Single Track Analysis
SELECT
    CASE
        WHEN LOWER(song_name) LIKE '%mix%' OR LOWER(song_name) LIKE '%dj%' THEN 'DJ Mix'
        ELSE 'Single Track'
        END AS content_type,
    COUNT(DISTINCT music_id) AS track_count,
    AVG(total_downloads / total_play30s) AS avg_download_ratio,
    AVG(total_favorites / total_play30s) AS avg_favorite_ratio,
    AVG(total_playlist_adds / total_play30s) AS avg_playlist_ratio
FROM music_data
WHERE total_play30s > 3000
GROUP BY content_type;
