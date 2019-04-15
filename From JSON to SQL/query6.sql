SELECT COUNT(*)
FROM USERS
WHERE UserID in
  (
    SELECT SellerID
    FROM AUCTIONS
  ) AND UserID in
  (
    SELECT BidderID
    FROM BIDS
  );