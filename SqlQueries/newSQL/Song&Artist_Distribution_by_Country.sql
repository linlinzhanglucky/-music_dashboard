-- ===============================================================
-- QUERY 8: Song & Artist Distribution by Country
-- ===============================================================
-- GOAL: Analyze content diversity across geographic markets
--       to identify content gaps and growth opportunities.
-- ===============================================================

SELECT
    geo_country,
    -- Calculate content volume metrics per country
    COUNT(DISTINCT music_id) AS song_count,
    COUNT(DISTINCT artist_name) AS artist_count
FROM music_data
-- Group by country for regional analysis
GROUP BY geo_country
-- Order by song count to see markets with most diverse content first
ORDER BY song_count DESC;