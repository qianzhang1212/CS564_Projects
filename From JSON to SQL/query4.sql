SELECT a1.ItemID
FROM AUCTIONS a1
WHERE a1.Currently =
      (
        SELECT MAX(a2.Currently)
        FROM AUCTIONS a2
      );