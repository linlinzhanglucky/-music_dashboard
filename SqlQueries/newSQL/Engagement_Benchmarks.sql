-- ===============================================================
-- QUERY 5: Engagement Benchmarks
-- ===============================================================
-- GOAL: Establish platform-wide baseline metrics for different engagement types
--       to enable comparative analysis and anomaly detection.
-- ===============================================================

-- First subquery: Calculate download ratio benchmarks
SELECT
    'Downloads' AS metric,
    -- Calculate platform-wide average download ratio
    AVG(total_downloads / total_play30s) AS average_ratio,
    -- Identify maximum download ratio to understand upper bounds
    MAX(total_downloads / total_play30s) AS highest_ratio
FROM music_data
-- Filter to include only songs with meaningful play counts
WHERE total_play30s > 1000

UNION ALL

-- Second subquery: Calculate favorite ratio benchmarks
SELECT
    'Favorites' AS metric,
    -- Calculate platform-wide average favorite ratio
    AVG(total_favorites / total_play30s) AS average_ratio,
    -- Identify maximum favorite ratio to understand upper bounds
    MAX(total_favorites / total_play30s) AS highest_ratio
FROM music_data
-- Filter to include only songs with meaningful play counts
WHERE total_play30s > 1000

UNION ALL

-- Third subquery: Calculate playlist ratio benchmarks
SELECT
    'Playlists' AS metric,
    -- Calculate platform-wide average playlist ratio
    AVG(total_playlist_adds / total_play30s) AS average_ratio,
    -- Identify maximum playlist ratio to understand upper bounds
    MAX(total_playlist_adds / total_play30s) AS highest_ratio
FROM music_data
-- Filter to include only songs with meaningful play counts
WHERE total_play30s > 1000

UNION ALL

-- Fourth subquery: Calculate repost ratio benchmarks
SELECT
    'Reposts' AS metric,
    -- Calculate platform-wide average repost ratio
    AVG(total_reposts / total_play30s) AS average_ratio,
    -- Identify maximum repost ratio to understand upper bounds
    MAX(total_reposts / total_play30s) AS highest_ratio
FROM music_data
-- Filter to include only songs with meaningful play counts
WHERE total_play30s > 1000;