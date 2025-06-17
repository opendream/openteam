SELECT
    c.id AS campaign_id,
    SUM(p.amount_thb) AS total_thb,
    ROUND(1.0 * SUM(p.amount_thb) / c.target_thb, 4) AS pct_of_target
FROM campaign c
JOIN pledge p ON c.id = p.campaign_id
GROUP BY c.id
ORDER BY pct_of_target DESC;
