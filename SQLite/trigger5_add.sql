-- 13. In every auction, the Number_of_Bids attribute corresponds to the actual number of bids for that particular item.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS update_bid_count;

CREATE TRIGGER update_bid_count
AFTER INSERT ON Bids
  FOR EACH ROW
  BEGIN
    UPDATE Items
    SET Bid_Count = Bid_Count + 1;
  END;
