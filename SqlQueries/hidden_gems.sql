-- Hidden Gems
-- Identifies songs with high engagement but moderate play counts

SELECT 
    music_id,
    song_name,
    artist_name,
    SUM(total_play30s) AS total_plays,
    SUM(total_downloads) / SUM(total_play30s) AS download_ratio,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_ratio,
    SUM(total_playlist_adds) / SUM(total_play30s) AS playlist_ratio,
    COUNT(DISTINCT geo_country) AS country_reach,
    -- Calculate overall engagement score
    (SUM(total_downloads) / SUM(total_play30s) * 0.3) + 
    (SUM(total_favorites) / SUM(total_play30s) * 0.3) + 
    (SUM(total_playlist_adds) / SUM(total_play30s) * 0.3) + 
    (SUM(total_reposts) / SUM(total_play30s) * 0.1) AS engagement_score
FROM music_data
GROUP BY music_id, song_name, artist_name
HAVING SUM(total_play30s) BETWEEN 3000 AND 20000  
   AND (SUM(total_favorites) / SUM(total_play30s)) > 
       (SELECT AVG(total_favorites) / AVG(total_play30s) FROM music_data)
ORDER BY engagement_score DESC
LIMIT 10;
