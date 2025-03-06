# Song & Artist Distribution by Country
SELECT
    geo_country,
    COUNT(DISTINCT music_id) AS song_count,
    COUNT(DISTINCT artist_name) AS artist_count
FROM music_data
GROUP BY geo_country
ORDER BY song_count DESC;
