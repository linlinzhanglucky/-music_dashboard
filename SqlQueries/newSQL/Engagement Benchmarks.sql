# Engagement Benchmarks
SELECT
    'Downloads' AS metric,
    AVG(total_downloads / total_play30s) AS average_ratio,
    MAX(total_downloads / total_play30s) AS highest_ratio
FROM music_data
WHERE total_play30s > 1000

UNION ALL

SELECT
    'Favorites' AS metric,
    AVG(total_favorites / total_play30s) AS average_ratio,
    MAX(total_favorites / total_play30s) AS highest_ratio
FROM music_data
WHERE total_play30s > 1000

UNION ALL

SELECT
    'Playlists' AS metric,
    AVG(total_playlist_adds / total_play30s) AS average_ratio,
    MAX(total_playlist_adds / total_play30s) AS highest_ratio
FROM music_data
WHERE total_play30s > 1000

UNION ALL

SELECT
    'Reposts' AS metric,
    AVG(total_reposts / total_play30s) AS average_ratio,
    MAX(total_reposts / total_play30s) AS highest_ratio
FROM music_data
WHERE total_play30s > 1000;
