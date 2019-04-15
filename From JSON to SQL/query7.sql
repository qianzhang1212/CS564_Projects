SELECT COUNT(DISTINCT c.Category)
FROM CATEGORY c
WHERE
  (
    SELECT COUNT(*)
    FROM BIDS b
    WHERE b.ItemID = c.ItemID AND b.Amount>100
  )>0;