USE streamflix;

SELECT 'subscribers' AS table_name, COUNT(*) AS total_rows FROM subscribers
UNION ALL
SELECT 'titles', COUNT(*) FROM titles
UNION ALL
SELECT 'watch_history', COUNT(*) FROM watch_history
UNION ALL
SELECT 'ratings', COUNT(*) FROM ratings
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'watchlist', COUNT(*) FROM watchlist;

-- Q1. Top genres by total watch hours
SELECT t.primary_genre,
       ROUND(SUM(w.watch_duration_min) / 60.0, 1) AS watch_hours,
       COUNT(*) AS plays
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.primary_genre
ORDER BY watch_hours DESC;

-- Q2. Top origin countries by watch hours, plus efficiency (hours per title)
SELECT t.country,
       ROUND(SUM(w.watch_duration_min) / 60.0, 1)              AS watch_hours,
       COUNT(DISTINCT t.title_id)                              AS titles,
       ROUND(SUM(w.watch_duration_min) / 60.0
             / COUNT(DISTINCT t.title_id), 1)                  AS hours_per_title
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.country
ORDER BY watch_hours DESC;

-- Q3. Engagement by release year (hours per title)
SELECT t.release_year,
       COUNT(DISTINCT t.title_id)                              AS titles,
       ROUND(SUM(w.watch_duration_min) / 60.0, 1)             AS watch_hours,
       ROUND(SUM(w.watch_duration_min) / 60.0
             / COUNT(DISTINCT t.title_id), 1)                  AS hours_per_title
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.release_year
ORDER BY t.release_year;

-- Q4. Movies vs TV Shows: share of hours and completion
SELECT t.type,
       ROUND(SUM(w.watch_duration_min) / 60.0, 1)             AS watch_hours,
       COUNT(*)                                                AS plays,
       ROUND(AVG(w.completion_pct), 1)                         AS avg_completion_pct
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.type
ORDER BY watch_hours DESC;

-- Q5. Watch hours by language (rank markets)
SELECT t.language,
       ROUND(SUM(w.watch_duration_min) / 60.0, 1)             AS watch_hours,
       COUNT(*)                                                AS plays
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.language
ORDER BY watch_hours DESC;

-- Q6. Completion rate by genre
SELECT t.primary_genre,
       ROUND(AVG(w.completion_pct), 1)                         AS avg_completion_pct,
       SUM(CASE WHEN w.completed THEN 1 ELSE 0 END)            AS completed_sessions,
       COUNT(*)                                                AS total_sessions
FROM watch_history w
JOIN titles t ON t.title_id = w.title_id
GROUP BY t.primary_genre
ORDER BY avg_completion_pct DESC;

-- Q7. Most engaged subscriber segments (by plan)
SELECT s.plan_type,
       COUNT(DISTINCT s.subscriber_id)                         AS subscribers,
       ROUND(SUM(w.watch_duration_min) / 60.0
             / COUNT(DISTINCT s.subscriber_id), 1)             AS avg_hours_per_subscriber
FROM watch_history w
JOIN subscribers s ON s.subscriber_id = w.subscriber_id
GROUP BY s.plan_type
ORDER BY avg_hours_per_subscriber DESC;

-- Q8. Device usage share
SELECT w.device,
       COUNT(*)                                                AS sessions,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM watch_history), 1) AS pct_of_sessions
FROM watch_history w
GROUP BY w.device
ORDER BY sessions DESC;

-- Q9. Churn rate and active rate
SELECT COUNT(*)                                                   AS total_subscribers,
       SUM(CASE WHEN is_active THEN 1 ELSE 0 END)                 AS active,
       ROUND(100.0 * SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
             / COUNT(*), 1)                                       AS active_rate_pct,
       ROUND(100.0 * SUM(CASE WHEN NOT is_active THEN 1 ELSE 0 END)
             / COUNT(*), 1)                                       AS churn_rate_pct
FROM subscribers;

-- Q10. Monthly Recurring Revenue (MRR) and ARPU from active subscribers
SELECT ROUND(SUM(monthly_price_usd), 2)                          AS mrr_usd,
       COUNT(*)                                                  AS active_subscribers,
       ROUND(SUM(monthly_price_usd) / COUNT(*), 2)              AS arpu_usd
FROM subscribers
WHERE is_active = TRUE;

-- Q11. Watchlist conversion rate (saved -> watched)
SELECT COUNT(*)                                                   AS watchlist_entries,
       SUM(CASE WHEN watched THEN 1 ELSE 0 END)                  AS converted,
       ROUND(100.0 * SUM(CASE WHEN watched THEN 1 ELSE 0 END)
             / COUNT(*), 1)                                       AS conversion_rate_pct
FROM watchlist;

-- Q12. Content investment efficiency: watch hours per $1,000 of licence cost, by genre
SELECT t.primary_genre,
       ROUND(SUM(t.license_cost_usd) / 1000.0, 0)              AS spend_thousands_usd,
       ROUND(SUM(t.total_watch_hours), 0)                      AS watch_hours,
       ROUND(SUM(t.total_watch_hours)
             / (SUM(t.license_cost_usd) / 1000.0), 3)          AS hours_per_1k_usd
FROM titles t
GROUP BY t.primary_genre
ORDER BY hours_per_1k_usd DESC;

SELECT CURRENT_USER(), DATABASE();
