DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS AUCTIONS;
DROP TABLE IF EXISTS BIDS;
DROP TABLE IF EXISTS CATEGORY;
CREATE TABLE USERS(
  UserID varchar,
  Rating int,
  Location varchar,
  Country varchar,
  PRIMARY KEY (UserID)
);
CREATE TABLE AUCTIONS(
  SellerID varchar,
  ItemID varchar,
  Name varchar,
  StartTime varchar,
  EndTime varchar,
  FirstBid double,
  BuyPrice double,
  NumOfBids int,
  Currently double,
  Description varchar(100000),
  PRIMARY KEY (ItemID),
  FOREIGN KEY (SellerID) REFERENCES USERS(UserID)
);
CREATE TABLE BIDS(
  ItemID varchar,
  BidderID varchar,
  Time varchar,
  Amount double,
  PRIMARY KEY (ItemID,BidderID,Time),
  FOREIGN KEY (ItemID) REFERENCES AUCTIONS(ItemID),
  FOREIGN KEY (BidderID) REFERENCES USERS(UserID)
);
CREATE TABLE CATEGORY(
  ItemID varchar,
  Category varchar,
  PRIMARY KEY (ItemID,Category),
  FOREIGN KEY (ItemID) REFERENCES AUCTIONS(ItemID)
);