-- 16.  The current time of your AuctionBase system can only advance forward in time, not backward in time.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS time_advance;

CREATE TRIGGER time_advance
BEFORE UPDATE ON Time
  FOR EACH ROW
  WHEN new.Sys_Time < old.Sys_Time
  BEGIN
    SELECT RAISE(ABORT, 'Cannot go back in time.');
  END;