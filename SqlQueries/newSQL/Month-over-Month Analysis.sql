# Month-over-Month Analysis
SELECT
    DATE_FORMAT(month, '%Y-%m') AS month_str,
    COUNT(DISTINCT music_id) AS unique_songs,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) / SUM(total_play30s) AS download_rate,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_rate
FROM music_data
GROUP BY month_str
ORDER BY month_str;
