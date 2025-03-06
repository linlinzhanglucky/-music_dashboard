# Music Data Analysis: Summary Report
*Analysis of UGC Music Uploads (04/2023-12/2024)*

*Author: Linlin Zhang (lz2981@columbia.edu)*

## 1. Early Indicators of Success

This analysis identifies **download-to-play ratio** as the most reliable predictor of long-term song success. With a platform-wide average of 0.199, songs exhibiting ratios above 0.3 demonstrate exceptional user commitment and significantly higher retention. The strongest predictors of success are:

1. **Download-to-play ratio** (R² = 0.78 correlation with future growth)
2. **Playlist-to-play ratio** (R² = 0.51 correlation with cross-country expansion)
3. **Favorites-to-play ratio** (R² = 0.43 correlation with artist account follows)

The most successful tracks demonstrate balanced engagement metrics with particularly strong download ratios:
* **"Have Mercy" by Shane Eli** (34.67 download ratio, 207,866 plays)
* **"Pluto" by Shallipopi** (10.61 download ratio, 3,990 plays)
* **"Joy is coming" by Fido** (6.01 download ratio, 5,976 plays)

The extraordinary performance of "Have Mercy" (with downloads 34.7x plays) warrants further investigation as a potential viral phenomenon or platform anomaly. This extreme outlier significantly exceeds typical engagement patterns and might represent a unique growth case study.

## 2. Trends & Patterns

**Geographic engagement variations** reveal distinct market behaviors:

* **Nigeria (NG)**: Dominates in volume (4.92B plays, 43,692 songs, 16,867 artists) with moderate engagement (0.194 download rate, 0.005 favorite rate), suggesting a mature, mainstream market.
* **Ghana (GH)**: Shows highest commitment (0.314 download rate) with substantial volume (1.10B plays), indicating a dedicated listener base prioritizing offline access.
* **United States (US)**: Exhibits distinctive platform behavior with highest favoriting rate (0.013) and strong playlist adds (0.019), suggesting a streaming-first market focus.

**Artist clustering analysis** revealed that top-performing artists like Juice WRLD (538 songs), KIRAT (359), and DJ Wizkel (344) show significantly different engagement patterns across markets, with Nigerian artists commanding higher download rates while US artists dominate playlisting metrics.

**Content format impact**: DJ mixes and compilations consistently outperform single tracks by approximately 58.7% in download metrics (0.299 vs 0.189), with Nigerian and Ghanaian markets showing particularly strong preference for extended mixes.

## 3. Hidden Gems

The algorithm identified these high-potential tracks that demonstrate exceptional engagement despite moderate play counts:

1. **"juju" by Big smur lee** (32,581 plays, 1.25 engagement score)
   * Strong download ratio of 4.08
   * Balanced engagement metrics (favorites: 0.049, playlists: 0.044)
   * Showing 6.8x higher favorite ratio than platform average

2. **"Medicine after death" by Mohbad** (4,019 plays, 1.24 engagement score)
   * Strong download ratio of 4.06
   * Balanced metrics across all engagement types
   * Artist with consistent quality (236 songs in dataset)

3. **"Twe Twe (remix)" by Kizz Daniel** (8,614 plays, 1.23 engagement score)
   * Above-average metrics across all engagement types
   * Download ratio of 4.03, 20x platform average
   * Demonstrates consistent performance in both Nigerian and Ghanaian markets

4. **"Area Boys prayers" by Seyi vibez** (4,425 plays, 1.13 engagement score)
   * Strong, balanced metrics across all engagement types
   * Notable for having both high download rate (3.70) and playlist adds (0.028)
   * Significant momentum in Nigerian market with emerging presence in Ghana

5. **"Gbona" by Zinoleesky** (7,899 plays, 1.05 engagement score)
   * Above-average metrics across all engagement types (download ratio: 3.41)
   * Strong artist performance history
   * Demonstrates consistent growth trajectory across multiple metrics

These tracks demonstrate engagement ratios 5-6x above platform average, suggesting significant growth potential with targeted promotional support.

## 4. Temporal Analysis

Monthly data analysis from April 2023 through December 2024 reveals significant trends:

* **Overall growth**: Total monthly plays increased from 296.7M in April 2023 to 479.8M in December 2024 (+61.7%)
* **Seasonal patterns**: December consistently shows highest activity (399.6M in 2023, 479.8M in 2024)
* **Download behavior evolution**: Download rates increased significantly from 14.3% (May 2023) to 23.2% (June 2024)
* **Content volume expansion**: Unique songs per month grew from 19,723 to 28,847 (+46.3%)

The platform shows clear annual seasonality with Q4 (October-December) consistently delivering the strongest performance metrics. This pattern is valuable for planning promotional campaigns and content strategy.

## 5. Artist Analysis

Two distinct artist performance patterns emerged:

**Content Volume Leaders**:
* Juice WRLD (538 songs, 72.5M plays, 13,357 avg plays/song)
* KIRAT (359 songs, 11.6M plays, 8,103 avg plays/song) 
* DJ Wizkel (344 songs, 30.5M plays, 14,058 avg plays/song)

**Engagement Quality Leaders**:
* Mama le succès (15 songs, 0.405 avg engagement score)
* Big Smur Lee (8 songs, 0.358 avg engagement score)
* Dj Amass (7 songs, 0.269 avg engagement score)

Notably, none of the top 10 artists by song count appear in the top 10 by engagement score, suggesting quantity and quality represent distinct success paths. Mohbad stands out with 236 songs and the highest average plays per song (35,262), demonstrating balanced success in both metrics.

## 6. Areas for Improvement

I would like to highlight several data limitations impacting predictive accuracy:

* **Temporal granularity**: Monthly aggregation masks weekly growth patterns critical for early detection of viral potential
* **Genre/mood classification**: Absence of content tagging limits discovery algorithm refinement and cross-genre analysis
* **User demographic data**: Limited demographic insights prevent audience alignment analysis and targeted growth strategies
* **Platform feature utilization**: Lack of data on share activity, comments, and profile visits prevents comprehensive funnel analysis
* **Cross-platform tracking**: Missing data on external sharing limits understanding of true reach beyond platform

## 7. Benchmarks & Performance Metrics

Analysis of platform-wide engagement metrics established these benchmarks:

| Metric | Average Ratio | Highest Ratio | Key Insight |
|--------|--------------|--------------|------------|
| Downloads | 0.199 | 84.362 | 422x variation between average and maximum |
| Favorites | 0.007 | 2.677 | US market shows 81% higher favorite rate than average |
| Playlists | 0.017 | 3.185 | Ghana leads playlist engagement at 0.025 (47% above average) |
| Reposts | 0.0003 | 0.349 | Least common engagement type, but vital for virality |

The extraordinary gap between average and highest ratios indicates substantial opportunity for optimization in content promotion and feature design.

## Recommendations

For **platform optimization**:
* Implement algorithmic emphasis on download-to-play ratio in recommendation engines
* Create dedicated "Hidden Gems" discovery section featuring highly engaged but moderately played content
* Develop market-specific algorithms that account for regional engagement preferences (downloads in Ghana, favorites in US)
* Target cross-country content promotion specifically for Ghana→US content flow

For **content strategy**:
* Increase promotion of DJ mixes, particularly in African markets where they outperform single tracks by nearly 60%
* Spotlight emerging artists with high engagement ratios but moderate plays like Mama le succès and Big Smur Lee
* Develop curated playlists featuring content with balanced engagement metrics
* Implement specialized features for offline listening to capitalize on strong download behavior

For **talent acquisition and development**:
* Prioritize artists showing exceptional engagement metrics across multiple songs
* Create growth pathways for artists demonstrating strong cross-country appeal
* Implement engagement-based contract incentives rather than purely play-count-based models
* Develop artist education around optimizing for engagement rather than raw play counts
