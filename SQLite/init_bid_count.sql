INSERT INTO Items(Name, High_Bid, Buy_Price, Min_Bid,
                  Start_Time, End_Time, Seller_ID, Item_Description, Bid_Count)
SELECT DISTINCT i1.Name, i1.High_Bid, i1.Buy_Price, i1.Min_Bid,
  i1.Start_Time, i1.End_Time, i1.Seller_ID, i1.Item_Description, t1.cnt1
FROM Items AS i1,(
  SELECT DISTINCT b1.Item_ID, count(Item_ID) AS cnt1
  FROM Bids AS b1
  GROUP BY Item_ID
  ORDER BY cnt1) AS t1
  WHERE i1.Item_ID = t1.Item_ID
  GROUP BY i1.Item_ID