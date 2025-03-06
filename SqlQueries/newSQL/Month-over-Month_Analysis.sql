-- ===============================================================
-- QUERY 7: Month-over-Month Analysis
-- ===============================================================
-- GOAL: Analyze temporal trends in content volume and engagement patterns
--       to identify seasonality and platform growth patterns.
-- ===============================================================

SELECT
    -- Format date into YYYY-MM format for consistent monthly grouping
    -- DATE_FORMAT ensures standardized representation of months
    DATE_FORMAT(month, '%Y-%m') AS month_str,
    
    -- Calculate content diversity metrics per month
    COUNT(DISTINCT music_id) AS unique_songs,
    
    -- Calculate total play volume to understand platform growth
    SUM(total_play30s) AS total_plays,
    
    -- Calculate key engagement ratios to track behavior changes over time
    SUM(total_downloads) / SUM(total_play30s) AS download_rate,
    SUM(total_favorites) / SUM(total_play30s) AS favorite_rate
FROM music_data
-- Group by month for temporal analysis
GROUP BY month_str
-- Order chronologically to see trends over time
ORDER BY month_str;
