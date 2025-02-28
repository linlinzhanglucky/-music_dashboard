-- Trending Songs Month-over-Month
-- Identifies trending songs based on growth between months

WITH monthly_metrics AS (
    SELECT 
        music_id,
        song_name,
        artist_name,
        DATE_TRUNC('month', month) AS month_date,
        SUM(total_play30s) AS monthly_plays
    FROM music_data
    GROUP BY music_id, song_name, artist_name, DATE_TRUNC('month', month)
),
growth_metrics AS (
    SELECT 
        curr.music_id,
        curr.song_name,
        curr.artist_name,
        curr.month_date AS current_month,
        prev.month_date AS previous_month,
        curr.monthly_plays AS current_plays,
        prev.monthly_plays AS previous_plays,
        (curr.monthly_plays - prev.monthly_plays) / prev.monthly_plays AS growth_rate
    FROM monthly_metrics curr
    JOIN monthly_metrics prev 
      ON curr.music_id = prev.music_id 
      AND curr.month_date = prev.month_date + INTERVAL '1 month'
    WHERE prev.monthly_plays > 1000
)
SELECT * FROM growth_metrics
ORDER BY growth_rate DESC
LIMIT 10;
