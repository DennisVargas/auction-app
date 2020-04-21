-- 11. No auction may have a bid before its start time or after its end time.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS valid_bid_time;

CREATE TRIGGER valid_bid_time
BEFORE INSERT ON Bids
  FOR EACH ROW
  WHEN ((SELECT Time FROM Bids) < (SELECT Start_Time FROM (SELECT Start_Time, Item_ID FROM Items AS i WHERE (SELECT Item_ID FROM Bids) = i.Item_ID)) OR
        (SELECT Time FROM Bids) > (SELECT End_Time FROM (SELECT End_Time, Item_ID FROM Items AS i WHERE (SELECT Item_ID FROM Bids) = i.Item_ID)))
  BEGIN
    SELECT RAISE(ABORT, 'Bid time must be between auction start and end times.');
  END;
