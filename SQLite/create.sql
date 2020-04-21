DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Time;

CREATE TABLE Items(
  Item_ID INTEGER,
  Name TEXT,
  High_Bid REAL,
  Buy_Price REAL,
  Min_Bid REAL,
  Start_Time TEXT,
  End_Time TEXT,
  Seller_ID TEXT,
  Item_Description TEXT,
  Bid_Count INTEGER,
  PRIMARY KEY (Item_ID), -- Satisfies constraint 3
  FOREIGN KEY (Seller_ID) REFERENCES Users (User_ID), -- Satisfies constraint 2 (part 1)
  CONSTRAINT CHK_Valid_Times CHECK (Start_Time < End_Time) -- Satisfies constraint 7
);

CREATE TABLE Categories(
  Item_ID INTEGER REFERENCES Items (Item_ID) DEFERRABLE INITIALLY DEFERRED, -- Satisfies constraint 5
  Category TEXT,
  PRIMARY KEY (Item_ID, Category) -- Satisfies constraint 6
);

CREATE TABLE Bids(
  Item_ID INTEGER REFERENCES Items (Item_ID) DEFERRABLE INITIALLY DEFERRED, -- Satisfies constraint 4
  Bidder_ID TEXT,
  Time TEXT,
  Amount REAL,
  PRIMARY KEY (Item_ID, Time),
  UNIQUE (Bidder_ID, Item_ID, Amount), -- Satisfies constraint 12
  FOREIGN KEY (Bidder_ID) REFERENCES Users (User_ID) -- Satisfies constraint 2 (part 2)
);

CREATE TABLE Users(
  User_ID TEXT PRIMARY KEY, -- Satisfies constraint 1
  Rating INTEGER,
  Location TEXT,
  Country TEXT
);

CREATE TABLE Time (
  Sys_Time TEXT,
  PRIMARY KEY (Sys_Time)
);

INSERT INTO Time VALUES ('2001-12-20 00:00:01');

SELECT Sys_Time
FROM Time;