-- 9. A user may not bid on an item he or she is also selling.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS bidder_not_seller;

CREATE TRIGGER bidder_not_seller
AFTER INSERT ON Bids
  FOR EACH ROW
  WHEN (new.Bidder_ID = (SELECT Seller_ID FROM (SELECT Seller_ID, Item_ID FROM Items AS i WHERE (SELECT Item_ID FROM Bids) = i.Item_ID)))
  BEGIN
    SELECT RAISE(ABORT, 'Seller cannot bid on his/her own auction.');
  END;